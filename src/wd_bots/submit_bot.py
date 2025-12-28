# -*- coding: utf-8 -*-
"""

from .wd_bots.submit_bot import submitAPI

"""
from urllib.parse import urlencode

import requests

from ..helps import logger

Session_t = {1: requests.Session()}


def submitAPI(params):
    # ---
    # global Session_t
    # ---
    Code = "www"
    family = "wikidata"
    # ---
    params["formatversion"] = 1
    params["utf8"] = 1
    params["format"] = "json"
    # ---
    if params.get("titles"):
        titles = params["titles"]
        if isinstance(titles, list):
            params["titles"] = "|".join(titles)
    # ---
    # himo API
    if family == "commons":
        family = "wikimedia"
    # ---
    mainurl = f"https://{Code}.{family}.org/w/api.php"
    # ---
    encode_params = urlencode(params)
    url = f"https://{Code}.{family}.org/w/api.php?{encode_params}"
    url2 = url.replace("&format=json", "").replace("?format=json", "?")
    # ---
    r22 = False
    # ---
    headers = {"User-Agent": "Himo bot/1.0 (https://himo.toolforge.org/; tools.himo@toolforge.org)"}
    # ---
    try:
        r22 = Session_t[1].post(mainurl, data=params, timeout=10, headers=headers)

    except requests.exceptions.ReadTimeout:
        logger.info(f"ReadTimeout: {mainurl}")

    except Exception as e:
        logger.exception(e)
        _known_exceptions = [
            "('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))",
            """('Connection aborted.', OSError("(104, "ECONNRESET")"))""",
            """""",
        ]

    # ---
    json1 = {}
    # ---
    if r22:
        try:
            json1 = r22.json()
        except Exception as e:
            logger.exception(e, text=url2)
            json1 = {}
    # ---
    return json1
