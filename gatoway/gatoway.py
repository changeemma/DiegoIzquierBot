from pefesens.pefesens import *
from bot.cabilbot import sendMessageToAdmin

import logging
import time


class Gatoway(object):
    def __init__(self, gateway, alarm_threshold, dismiss_threshold, check_interval):
        self.gateway = gateway
        self.alarm_threshold = alarm_threshold
        self.dismiss_threshold = dismiss_threshold
        self.check_interval = check_interval
        self.alarm_triggered = False
        self.fetchStatus()

    def fetchStatus(self):
        logging.debug(f"[gatoway] {self.gateway} - fetching status...")
        self.status = gatewayStatus(self.gateway)

    def printStatus(self):
        return f"[gatoway] {self.gateway} - rtt: {self.status['rtt']:.2f}ms rttsd: {self.status['rttsd']:.2f}ms loss: {self.status['loss']:3}%"

    def notifyStatus(self):
        logging.debug(f"[gatoway] {self.gateway} - notifying status...")
        sendMessageToAdmin(
            f"[gatoway]: {self.gateway}\nrtt: {self.status['rtt']:.2f}ms\nrttsd: {self.status['rttsd']:.2f}ms\nloss: {self.status['loss']:3}%"
        )

    def toggleAlarm(self):
        self.alarm_triggered = not self.alarm_triggered

    def monitor(self):
        while True:
            self.fetchStatus()
            alarm = any(self.status[k] > self.alarm_threshold[k] for k in self.status)
            dismiss = all(
                self.status[k] < self.dismiss_threshold[k] for k in self.status
            )

            if self.alarm_triggered and dismiss:
                logging.info(self.printStatus())
            elif alarm:
                logging.warning(self.printStatus())
            else:
                logging.debug(self.printStatus())

            if (not self.alarm_triggered and alarm) or (
                self.alarm_triggered and dismiss
            ):
                try:
                    self.notifyStatus()
                    self.toggleAlarm()
                except:
                    pass
            time.sleep(self.check_interval)
