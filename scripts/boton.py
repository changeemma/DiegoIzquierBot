#!/usr/bin/env python3
#

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from izquierbot.izquierbot import IzquierBot 
from scripts.boton_cfg import *

import logging

def main():
    logging.info("")
    logging.info("/*********************** BOTON ***********************/")
    logging.info("")
    logging.info(f"BotOn - Logfile: {BOTON_LOGFILE}")
    logging.info("")
    logging.info("Initializing IzquierBot...")
    izquierbot = IzquierBot()
    izquierbot.add_handlers()
    logging.info("IzquierBot initialized.")
    logging.info("")
    logging.info("/********************************************************/")
    logging.info("")
    logging.info("Starting IzquierBot polling...")
    logging.info("")

    izquierbot.start_polling()



if __name__ == "__main__":
    logging.basicConfig(
        filename=BOTON_LOGFILE,
        level=logging.DEBUG,
        filemode="a",
        format="[%(asctime)s] [%(levelname)s] [boton] %(message)s",
    )
    main()
