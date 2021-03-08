#!/usr/bin/env python3
#

from camdoris.camdoris import Camdoris
from scripts.dorimon_cfg import *

import logging


def main():
    logging.info("")
    logging.info("/*********************** DORIMON ***********************/")
    logging.info("")
    cam = Camdoris(
        host=DORIMON_HOST,
        port=DORIMON_PORT,
        user=DORIMON_USER,
        password=DORIMON_PASSWORD,
        timeout=DORIMON_TIMEOUT,
        check_interval=DORIMON_CHECK_INTERVAL,
    )
    logging.info(f"Compliance check - Camera IP: {cam.host}")
    logging.debug("Current configuration...")
    try:
        logging.info(f"\n{cam.getConfig()}")
    except:
        logging.warning("Could not retrieve config.")
    logging.info(f"Compliance check - Interval: {cam.check_interval}s")
    logging.info(f"Compliance check - Logfile: {DORIMON_LOGFILE}")
    logging.info("")
    logging.info("/********************************************************/")
    logging.info("")

    # checking loop
    logging.info("")
    logging.info("BEGINING CAMDORIS MONITOR...")
    logging.info("")
    try:
        cam.monitor()
    finally:
        logging.info("")
        logging.info("EXITING CAMDORIS MONITOR...")
        logging.info("")


if __name__ == "__main__":
    logging.basicConfig(
        filename=DORIMON_LOGFILE,
        level=logging.INFO,
        filemode="a",
        format="[%(asctime)s] [%(levelname)s] [dorimon] %(message)s",
    )
    main()
