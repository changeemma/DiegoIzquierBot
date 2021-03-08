#!/usr/bin/env python3
#
from izquierbot.izquierbot_cfg import *

from pefesens.pefesens import pfctlKill, gatewayStatus

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import subprocess
import requests
import time

import logging



def sendMessage(message, chat_id):
    url = f"https://api.telegram.org/bot{IZQUIERBOT_TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}"
    requests.get(url)


def sendMessageToAdmin(message):
    for chat_id in IZQUIERBOT_ADMIN_CHAT_ID_LIST:
        sendMessage(message, chat_id)


class IzquierBot():

    def __init__(self):
        self.updater = Updater(token=IZQUIERBOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def add_handlers(self):
        logging.info("Instantiating Handlers...")
        start_cmd_handler = CommandHandler("start", startHandler)
        punish_cmd_handler = CommandHandler("punish", punishHandler)
        gateway_cmd_handler = CommandHandler("gateway", gatewayHandler)
        logging.info("Done")
        logging.info("Adding Handlers to Dispatcher...")
        self.dispatcher.add_handler(start_cmd_handler)
        self.dispatcher.add_handler(punish_cmd_handler)
        self.dispatcher.add_handler(gateway_cmd_handler)
        logging.info("Done")

    def start_polling(self):
        self.updater.start_polling()



def startHandler(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def punishHandler(update, context):
    logging.info(
        f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}): {update.message.text}"
    )
    args = update.message.text.split()[1:]

    # permisos
    if not update.message.chat.id in IZQUIERBOT_ADMIN_CHAT_ID_LIST:
        logging.info(update)
        logging.info(
            f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}) - tried to punish: {args}"
        )
        response = f"you must be an admin to punish someone. eeerrga."
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        return

    # validaciones #
    # es mandatorio indicar el target
    if len(args) == 0:
        logging.info(
            f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}) - punish missing arguments"
        )
        response = f"usage: /punish hostname [count [interval]]\ndefault values: count=1, interval=1"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        return

    # el primer argumento adicional corresponde a la cantidad de cortes
    if len(args) > 1 and not args[1].isdigit():
        response = f"invalid count {args[1]}"
        logging.info(
            f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}) -punish invalid count '{args[1]}' ('{update.message.text}')."
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        return

    # el segundo argumento adicional corresponde al intervalo entre cortes
    if len(args) > 2 and not args[2].isdigit():
        response = f"invalid interval {args[2]}"
        logging.info(
            f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}) - punish invalid interval '{args[2]}' ('{update.message.text}')."
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        return

    target = args[0]

    if target[0].isnumeric() or any(c in target for c in [";", "|", ">", "<"]):
        logging.info(
            f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}) tried to punish: {target}"
        )
        response = f"no te hagas el vivo."
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        return

    if any(admin.lower() in target.lower() for admin in IZQUIERBOT_ADMIN_DEVICE_LIST):
        logging.info(
            f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}) tried to punish: {target}"
        )
        response = f"you can't punish an admin. eeerrga."
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        return

    count = int(args[1]) if len(args) > 1 else 1
    interval = int(args[2]) if len(args) > 2 else 1

    for i in range(1, count + 1):
        response = f"{target} punish count {i}:\n" if count > 1 else ""
        response += pfctlKill(target)
        response += (
            "" if interval == 1 or i == count else f"\nwaiting {interval} seconds..."
        )
        logging.info(
            f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}): {response}"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        t_sleep(interval)
    return


def gatewayHandler(update, context):
    logging.info(
        f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}): {update.message.text}"
    )
    gateways = update.message.text.split()[1:]
    gateways = gateways if gateways else ["WANGW", "SCPCGW"]
    for gw in gateways:
        st = gatewayStatus(gw)
        r = f"{gw}\nrtt: {st['rtt']}ms\nrttsd: {st['rttsd']}ms\nloss: {st['loss']}%"
        logging.info(
            f"{update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}): {r}"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=r)

