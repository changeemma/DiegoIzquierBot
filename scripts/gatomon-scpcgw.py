#!/usr/bin/env python3
#

from gatoway.gatoway import Gatoway
from scripts.gatomon_cfg import *

import logging


def main():

    logging.info("")
    logging.info("/*********************** GATOMON ***********************/")
    logging.info("")
    logging.info(f" Interval: {GATOMON_SCPCGW_CHECK_INTERVAL}s")
    logging.info("")

    gw = Gatoway(
        gateway=GATOMON_SCPCGW_GATEWAY,
        alarm_threshold=GATOMON_SCPCGW_ALARM_THRESHOLD,
        dismiss_threshold=GATOMON_SCPCGW_DISMISS_THRESHOLD,
        check_interval=GATOMON_SCPCGW_CHECK_INTERVAL,
    )

    logging.info(f" Gateway: {gw.gateway}")
    logging.info(f" Fetching status...")
    logging.info(f"{gw.printStatus()}")
    logging.info("")

    logging.info("")
    logging.info("/*********************************************************/")
    logging.info("")

    # checking loop
    logging.info("")
    logging.info(" BEGINING GATOMON MONITOR...")
    logging.info("")
    try:
        gw.monitor()
    finally:
        logging.info("")
        logging.info(" EXITING GATOMON MONITOR...")
        logging.info("")


if __name__ == "__main__":
    logging.basicConfig(
        filename=GATOMON_SCPCGW_LOGFILE,
        level=logging.INFO,
        filemode="a",
        format="[%(asctime)s] [%(levelname)s] [gatomon-scpcgw] %(message)s",
    )
    main()
