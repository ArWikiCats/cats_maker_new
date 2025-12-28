#!/usr/bin/python3
"""

"""
import json
import sys
import time

import requests

from .log import logger


class classgetURL:
    def __init__(self, url):
        self.start = time.time()
        self.url = url
        self.html = ""
        self.session = requests.session()
        self.session.headers.update(
            {"User-Agent": "Himo bot/1.0 (https://himo.toolforge.org/; tools.himo@toolforge.org)"}
        )

    def open_it(self):
        if not self.url:
            logger.output('open_url.py: self.url == ""')
            return ""
        if "printurl" in sys.argv:
            logger.output(f"getURL: {self.url}")

        try:
            req = self.session.get(self.url, timeout=10)
            # ---
            if 500 <= req.status_code < 600:
                logger.output(f"received {req.status_code} status from {req.url}")
                self.html = ""
            else:
                # ---
                self.html = req.text

        except requests.exceptions.ReadTimeout:
            logger.output(f"ReadTimeout: {self.url}")

        except Exception as e:
            logger.exception(e)
            _except_ions_ = [
                "Too long GET request",
                "HTTPSConnectionPool(host='en.wikipedia.org', port=443): Read timed out. (read timeout=45)",
                "('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))",
                """('Connection aborted.', OSError("(104, 'ECONNRESET')"))""",
                """HTTP Error 414: URI Too Long""",
                "HTTP Error 500: Internal Server Error",
            ]
        # ---
        return self.html


def getURL(url, maxsleeps=0):
    bot = classgetURL(url)
    return bot.open_it()


def open_the_url(url, maxsleeps=0):
    bot = classgetURL(url)
    return bot.open_it()


def open_json_url(url, maxsleeps=0, **kwargs):
    bot = classgetURL(url)
    js_text = bot.open_it()
    try:
        return json.loads(js_text)
    except json.decoder.JSONDecodeError:
        logger.output(f"open_url.open_json_url json.decoder.JSONDecodeError url {url}")
        return {}
