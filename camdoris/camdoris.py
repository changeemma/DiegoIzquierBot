#!/usr/bin/env python3
#

import logging

import time
import requests
from telnetlib import Telnet

from camdoris_cfg import *
from bot.cabilbot import sendMessageToAdmin


class Camdoris(object):
    def __init__(self, host, user, password, port, timeout, check_interval):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.timeout = timeout
        self.check_interval = check_interval
        self.site_down_alarm_triggered = False

    def sendTelnetCommand(conn, cmd, prompt):
        conn.write(f"{cmd}\n".encode("ascii"))
        match, _, data = conn.expect([prompt.encode("ascii")], timeout=self.timeout)
        if match == -1:
            logging.error(
                f"Reached timeout expecting prompt ('{prompt}'). Received from server: '{data.decode()}'"
            )
            raise TimeoutError()
        return data

    def fetchConfig(self):
        output = b""

        with Telnet(host=self.host, port=self.port, timeout=self.timeout) as conn:
            conn.read_until("Username> ".encode("ascii"))
            output += self.sendTelnetCommand(conn, "login", CAMDORIS_PROMPT_REGEX)
            output += self.sendTelnetCommand(conn, "show ftp", CAMDORIS_PROMPT_REGEX)
            output += self.sendTelnetCommand(
                conn, "show image mask", CAMDORIS_PROMPT_REGEX
            )

        splitted = output.decode().split("\r\n")
        _ = splitted.pop(0)
        _ = splitted.pop(-1)
        return "\n".join(splitted)

    def isSiteUp(self):
        try:
            sc = requests.head(
                f"http://{self.host}/appletvid.html", timeout=self.timeout
            ).status_code
            return True if sc == 200 else False
        except:
            return False

    def isCompliant(self):
        try:
            current_config = self.fetchConfig()
        except:
            logging.warning("could not check compliance. aborting...")
            return False

        return all([c in current_config for c in CAMDORIS_COMPLIANT_CONFIG_LIST])

    def configure(self):
        with Telnet(host=self.host, port=self.port, timeout=self.timeout) as conn:

            def send_cmd(cmd, prompt):
                conn.write((cmd + "\n").encode("ascii"))
                match, _, data = conn.expect(
                    [prompt.encode("ascii")], timeout=self.timeout
                )
                if match == -1:
                    logging.error(
                        f"Reached timeout expecting prompt ('{prompt}'). Received from server: '{data.decode()}'"
                    )
                    raise TimeoutError()

            conn.read_until("Username> ")
            self.sendTelnetCommand(conn, self.user, CAMDORIS_PROMPT_REGEX)
            self.sendTelnetCommand(conn, "set privilege over", "Password> ")
            self.sendTelnetCommand(conn, self.password, CAMDORIS_PROMPT_REGEX)

            for cmd in CAMDORIS_CONFIGURATION_CMD_LIST:
                self.sendTelnetCommand(conn, cmd, CAMDORIS_PROMPT_REGEX)

            self.sendTelnetCommand(
                conn, CAMDORIS_TEST_TRIGGER_CMD, CAMDORIS_PROMPT_REGEX
            )

    def monitor(self):
        while True:
            logging.info("checking site...")
            if not self.isSiteUp():
                if not self.site_down_alarm_triggered:
                    # se debe informar la caida del sitio
                    logging.warning("site is down - alerting admins...")
                    try:
                        sendMessageToAdmin("camdoris: hey! site is down.")
                        self.site_down_alarm_triggered = True
                    except:
                        logging.warning("could not send msg.")
                    logging.info("done.")
                else:
                    # el sitio ya estaba abajo y fue alertado
                    logging.warning("site is down - already alerted.")
            else:
                # se debe informar vuelta a la normalidad
                if self.site_down_alarm_triggered:
                    logging.info("site is up - alerting admins...")
                    try:
                        sendMessageToAdmin("camdoris: site is back online.")
                        self.site_down_alarm_triggered = False
                    except:
                        logging.warning("could not send msg.")
                    logging.info("done.")
                else:
                    logging.info("site is up.")

                logging.info("checking compliance...")
                if not self.isCompliant():
                    logging.info("camera is not compliant - configuring now...")
                    try:
                        self.configure()
                        continue
                    except:
                        pass
                else:
                    logging.info("camera is compliant.")

            time.sleep(self.check_interval)
