#!/usr/bin/python3
"""
POST bot - Items functionality

This module provides functions for working with items in Wikidata.
"""

import json
import re

from .. import qs_bot
from ..utils import lag_bot, logger
from ..utils.out_json import outbot_json


class WD_Items:
    def __init__(self, wdapi_new):
        self.wdapi_new = wdapi_new
        self.post_continue_wrap = self.wdapi_new.post_continue
        self.session_post = self.wdapi_new.post_to_newapi
        # pass

    def New_API(self, data2, summary, RRE=0, returnid=False, nowait=False, tage=""):
        """Create a new item in the API with the provided data and summary.

        This function sends a request to create a new item in the API using the
        provided data and summary. It first checks for any lag issues and then
        processes the input data. If the request is successful, it handles the
        response accordingly. If the response indicates a need to retry, it
        calls another API function. The function can also return the ID of the
        newly created item if requested.

        Args:
            data2 (any): The data to be sent to the API for creating a new item.
            summary (str): A summary or description of the new item.
            RRE (int?): A retry counter for handling specific response cases. Defaults to 0.
            returnid (bool?): If True, returns the ID of the created item. Defaults to False.
            nowait (bool?): If True, indicates that the function should not wait for a response.
                Defaults to False.
            tage (str?): An optional tag for the request. Defaults to an empty string.

        Returns:
            str or bool: The response from the API as a string if successful,
                False if the request failed, or the ID of the created item if returnid
                is True.
        """
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        data = json.JSONEncoder().encode(data2)
        # ---
        r4 = self.session_post(
            params={
                "action": "wbeditentity",
                "new": "item",
                "summary": summary,
                "data": data,
            },
            tage=tage,
        )
        # ---
        if not r4:
            return False
        # ---
        cf = outbot_json(r4, fi=summary, NoWait=nowait)
        if cf == "reagain" and RRE == 0:
            return qs_bot.QS_New_API(data2)
        # ---
        if cf == "warn":
            logger.warning(str(r4))
        # ---
        if returnid:
            Qid = False
            if cf is True:
                if "entity" in r4 and "id" in r4["entity"]:
                    Qid = r4["entity"]["id"]
                    logger.debug(f'<<lightgreen>> bot.py New_API: returnid:"{Qid}" ')
            return Qid
        # ---
        return str(r4)

    def clearitem(self, q, summary, nowait=False):
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        logger.debug("bot.New_Mult_Des: ")
        # ---
        r4 = self.session_post(
            params={
                "action": "wbeditentity",
                "errorformat": "wikitext",
                "id": q,
                "summary": summary,
                "clear": 1,
                "data": "{}",
            }
        )
        # ---
        if not r4:
            return False
        # ---
        d = outbot_json(r4, fi=summary, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning(str(r4))
        # ---
        return d

    def Mergehistory(self, q1, q2, nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        q11 = re.sub(r"Q", "", q1)
        q22 = re.sub(r"Q", "", q2)
        # ---
        if int(q11) > int(q22):
            From = q1
            To = q2
        else:
            From = q2
            To = q1
        # ---
        out = f"Mergehistory from {From} to {To} "
        logger.debug(out)
        # ---
        r4 = self.session_post(
            params={
                "action": "mergehistory",
                "from": From,
                "to": To,
                "reason": "duplicated",
            }
        )
        # ---
        if not r4:
            return False
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d is True:
            logger.warning(f"<<lightgreen>> {out} true.")
            return True
        # ---
        if d == "warn":
            logger.warning(str(r4))
        # ---
        return False
