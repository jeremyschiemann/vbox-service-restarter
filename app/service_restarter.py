"""Module to restart the vbox services."""
import asyncio
from io import StringIO

from lxml import etree
import requests
import logging
from app.constants import URL_PATH

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def _needs_update(states) -> bool:
    return states["STREAMER"] != "STARTED" or states["UPNP_SERVER"] != "STARTED"


def _make_arg_list(states) -> str:
    args = ["OPTION=3",
            "NEXT_STATE=0",
            "NEXT_STATE=0",
            "NEXT_STATE=0",
            f"NEXT_STATE={'1' if states['STREAMER'] != 'STARTED' else '0'}",
            f"NEXT_STATE={'1' if states['UPNP_SERVER'] != 'STARTED' else '0'}",
            "NEXT_STATE=0",
            "NEXT_STATE=0"]
    return "?" + "&".join(args)


async def runner(username: str, password: str, baseurl: str, sleeptime: int) -> None:
    while True:
        try:
            log.info("Checking status of services")
            res = requests.get(baseurl + URL_PATH + "?OPTION=2", auth=(username, password))
            log.info(f"Received code {res.status_code}: {res.reason}")

            if res.status_code != 200:
                raise ValueError("Received non 200 code!")

            tree = etree.parse(StringIO(res.text), etree.HTMLParser())
            tbody = tree.xpath("//form")[0].getchildren()[3].getchildren()[0].getchildren()[1:]

            states = {}
            for tr in tbody:
                key = tr.getchildren()[0].text.strip('\xa0')
                value = tr.getchildren()[1].getchildren()[1].text.strip('\xa0')
                states[key] = value

            log.info("Status: " + ", ".join([f"{key}={val}" for key, val in states.items()]))

            if _needs_update(states):
                log.info("One or more services are not running! Sending restart request!")
                arg_list = _make_arg_list(states)
                upd = requests.get(baseurl + URL_PATH + arg_list, auth=(username, password))
                log.info(f"Received code {upd.status_code}: {upd.reason}")
        except Exception as e:
            print("Error occured!")
            print(str(e))

        await asyncio.sleep(sleeptime)
