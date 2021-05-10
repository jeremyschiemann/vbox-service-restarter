"""Main Module."""
import asyncio

from app import service_restarter
import os
import logging
import sys
from app.constants import MINUTE

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

username = os.environ.get("VBOX_USERNAME")
password = os.environ.get("VBOX_PASSWORD")
baseurl = os.environ.get("VBOX_IP")
sleeptime = os.environ.get("SLEEPTIME", 10*MINUTE)


if __name__ == "__main__":

    error_list = []

    if not username:
        error_list.append("VBOX_USERNAME")

    if not password:
        error_list.append("VBOX_PASSWORD")

    if not baseurl:
        error_list.append("VBOX_IP")
    else:
        baseurl = "http://" + baseurl

    try:
        sleeptime = int(sleeptime)
    except ValueError:
        log.warning("Please make sure sleeptime is an integer! Falling back to default value.")
        sleeptime = 10*MINUTE

    if error_list:
        log.error(f"Please set {', '.join(error_list)}")
        sys.exit(1)

    log.info("Starting service...")

    loop = asyncio.get_event_loop()
    loop.create_task(service_restarter.runner(username, password, baseurl, sleeptime))
    loop.run_forever()