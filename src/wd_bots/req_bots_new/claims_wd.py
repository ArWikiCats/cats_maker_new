#!/usr/bin/python3
"""
POST bot - Claims functionality

This module provides functions for working with claims in Wikidata.
"""

import json
import re

from ..qs_bot import QS_line
from ..utils import lag_bot, logger
from ..utils.out_json import outbot_json


class WD_Claims:
    def __init__(self, wdapi_new):
        self.wdapi_new = wdapi_new
        self.post_continue_wrap = self.wdapi_new.post_continue
        self.session_post = self.wdapi_new.post_to_newapi
        # pass

    def add_quall(self, Claimid, quall_prop, valueline, hashx="", nowait=False):
        """Add a qualifier to a claim.

        This function adds a specified qualifier to a given claim identified by
        the Claimid. It first checks for any lag conditions and then prepares
        the necessary parameters for the action. If the numeric ID in the
        valueline matches the ID extracted from the Claimid, it will not proceed
        with adding the qualifier. The function also handles optional parameters
        such as hash and nowait to modify its behavior.

        Args:
            Claimid (str): The identifier of the claim to which the qualifier is added.
            quall_prop (str): The property name of the qualifier being added.
            valueline (dict): A dictionary containing the value details for the qualifier.
            hash (str?): An optional hash value for the qualifier. Defaults to an empty string.
            nowait (bool?): A flag indicating whether to wait for a response. Defaults to False.

        Returns:
            dict or bool: Returns a dictionary with the result of the operation if
                successful,
                or False if the operation fails.
        """

        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        valueline2 = json.JSONEncoder().encode(valueline)
        logger.debug(f'add_quall Claimid: "{Claimid}" ,{valueline2}: ')
        # ---
        id2 = Claimid.split("$")[0].replace("Q", "")
        numeric = valueline.get("numeric-id", False)
        if numeric and numeric == id2:
            logger.debug(f"<<lightred>> add_quall {quall_prop}: q:Q{id2} == numeric:Q{numeric}.")
            return ""
        # ---
        papams = {
            "action": "wbsetqualifier",
            "claim": Claimid,
            "snaktype": "value",
            "property": quall_prop,
            "value": valueline2,
        }
        # ---
        if hashx:
            papams["snakhash"] = hashx
        # ---
        nhh = numeric or valueline.get("time", valueline.get("amount", ""))
        out = f'Add qualifier "{quall_prop}":"{nhh}" to Claimid {Claimid}. '
        # ---
        if hashx:
            out = f'change qualifier "{quall_prop}":"{nhh}" in Claimid {Claimid}. '
        # ---
        r6 = self.session_post(params=papams)
        # ---
        if not r6:
            return False
        # ---
        d = outbot_json(r6, fi=out, line=valueline2, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning("", text=r6)
        # ---
        return d

    def _Set_Quall(self, js, quall_prop, quall_id, nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        out = f'Add qualifier "{quall_prop}":"{quall_id}" to Claimid: '
        # logger.debug(out)
        # ---
        Claimid = ""
        # ---
        entitytype = "item"
        qua_id = re.sub(r"Q", "", quall_id)
        if quall_id != re.sub(r"P", "", quall_id):
            entitytype = "property"
            qua_id = re.sub(r"P", "", quall_id)
        value = '{"entity-type":"' + entitytype + '","numeric-id":' + qua_id + "}"
        # ---
        Claimid = js.get("claim", {}).get("id", "")
        # ---
        if not Claimid:
            logger.debug('Claimid == ""')
            return False
        # ---
        logger.debug(f'Claimid: "{Claimid}"')
        # ---
        r6 = self.session_post(
            params={
                "action": "wbsetqualifier",
                "claim": Claimid,
                "snaktype": "value",
                "property": quall_prop,
                "value": value,
            }
        )
        # ---
        if not r6:
            return False
        # ---
        d = outbot_json(r6, fi=out, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning("", text=r6)
        # ---
        return Claimid

    def _Set_Quall2(self, js, qualifiers, nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        Claimid = js.get("claim", {}).get("id", "")
        # ---
        if not Claimid:
            logger.debug(f'cant find Claimid in: "{str(js)}"')
        # ---
        logger.debug(f'<<lightyellow>> _Set_Quall2: Claimid: "{Claimid}"')
        # ---
        for qua in qualifiers:
            quall_prop = qua["property"]
            value = qua["value"]
            ty_pe = qua["type"]
            valueline = {}
            if ty_pe == "time":  # , 'time': '+2003-04-27T00:00:00Z'
                if value.get("time"):
                    valueline = value
                else:
                    valueline = {
                        "after": 0,
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727",
                        "time": "",
                        "timezone": 0,
                        "before": 0,
                        "precision": 11,
                    }
                    valueline["time"] = value  # '+2003-04-27T00:00:00Z'
            elif ty_pe == "quantity":
                # valueline["property"] = quall_prop
                # valueline["type"] = "quantity"
                # valueline["value"] = {}
                # valueline = value
                # if type(value) != dict:
                valueline = {"amount": "+" + str(value), "unit": "1"}
                # else:
                #  valueline["value"] = value
            else:
                entitytype = "item"
                quat = ""
                if value.get("numeric-id", False):
                    valueline = value
                    quat = value.get("numeric-id", "")
                else:
                    quat = value
                    qua_id = re.sub(r"Q", "", quat)
                    if quat != re.sub(r"P", "", quat):
                        entitytype = "property"
                        qua_id = re.sub(r"P", "", quat)
                    valueline = {"entity-type": entitytype, "numeric-id": qua_id}
            # ---
            self.add_quall(Claimid, quall_prop, valueline)

    def Claim_API2(self, uid, proprty, numeric, qualifiers=[], nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        try:
            numeric = re.sub(r"Q", "", numeric)
        except Exception as e:
            logger.warning(e, text=numeric)
        out = f"Claim_API2: {uid}: {proprty}:Q{numeric}."
        # logger.debug(out)
        # ---
        if uid == "" or proprty == "" or numeric == "":
            logger.debug(f"one of (id '{uid}' proprty '{proprty}' numeric '{numeric}') == '' ")
            return False
        # ---
        if not numeric:
            logger.debug(f'numeric is "{numeric}"')
            return ""
        # ---
        qq = re.sub(r"Q", "", uid)
        if qq == numeric:
            logger.debug(out)
            logger.debug(f"<<lightred>> Claim_API2 {proprty}:  id:Q{uid} == numeric:Q{numeric}.")
            return ""
        # ---
        r4 = self.session_post(
            params={
                "action": "wbcreateclaim",
                "entity": uid,
                "snaktype": "value",
                "property": proprty,
                "value": '{"entity-type":"item","numeric-id":' + numeric + "}",
            }
        )
        # ---
        if not r4:
            return False
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning("", text=r4)
        # ---
        if qualifiers != []:
            self._Set_Quall2(r4, qualifiers)

    def Claim_API_time(self, q, proprty, precision=9, year="", strtime="", nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        out = f"{q}: {proprty}:{year}."
        # logger.debug(out)
        if precision == 9 and strtime == "":
            strtime = f"+{year}-00-00T00:00:00Z"
        time = {
            "after": 0,
            "before": 0,
            "calendarmodel": "http://www.wikidata.org/entity/Q1985727",
            "precision": precision,
            "time": strtime,
            "timezone": 0,
        }
        # ---
        if not strtime:
            logger.debug(f'strtime is "{strtime}"')
        # ---

        r4 = self.session_post(
            params={
                "action": "wbcreateclaim",
                "entity": q,
                "snaktype": "value",
                "property": proprty,
                "value": json.JSONEncoder().encode(time),
            }
        )
        # ---
        if not r4:
            return False
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning("", text=r4)

    def Claim_API_quantity(self, q, proprty, quantity, nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        out = f"{q}: {proprty}:{quantity}."
        if not quantity:
            return ""
        # ---
        valueline2 = json.JSONEncoder().encode({"amount": "+" + str(quantity), "unit": "1"})

        r4 = self.session_post(
            params={
                "action": "wbcreateclaim",
                "entity": q,
                "snaktype": "value",
                "property": proprty,
                "value": valueline2,
            }
        )
        # ---
        if not r4:
            return False
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning("", text=r4)

    def Claim_API_string(self, q, proprty, string, Make=0, nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        out = f"{q}: {proprty}:{string}."
        logger.debug(f"<<lightred>>Claim_API_string: {out}")
        # ---
        if not string:
            logger.debug(f'Claim_API_string: string is "{string}"')
        # ---
        # if string:

        r4 = self.session_post(
            params={
                "action": "wbcreateclaim",
                "entity": q,
                "snaktype": "value",
                "property": proprty,
                # "value": "\"%s\"" % json.JSONEncoder().encode(string) ,
                # "value": string ,
                "value": json.JSONEncoder().encode(string),
            }
        )
        # ---
        if not r4:
            return False
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning("", text=r4)
        # ---
        if d == "reagain":
            qsline = f'{q}|{proprty}|"{string}"'
            QS_line(qsline, user="Mr. Ibrahem")

    def Claim_API_With_Quall(self, q, proprty, numeric, quall_prop, quall_id, returnClaimid=False, nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        Claimid = ""
        # ---
        if not quall_prop or not quall_id:
            logger.debug("<<lightred>> Claim_API_With_Quall Can' find quall_prop or quall_id.")
            return False
        # ---
        numeric = re.sub(r"Q", "", numeric)
        quall_numeric = re.sub(r"Q", "", quall_id)
        # ---
        out = f"{q}: {proprty}:Q{numeric}."
        logger.debug(out)
        # ---
        # js = {}
        qq = re.sub(r"Q", "", q)
        if qq == numeric:
            logger.debug(f"<<lightred>> Claim_API_With_Quall {proprty}:  q:Q{qq} == numeric:Q{numeric}.")
            return False
        elif qq == quall_numeric:
            logger.debug(f"<<lightred>> Claim_API_With_Quall {proprty}:  q:Q{qq} == quall_numeric:Q{quall_numeric}.")
            return False
        # ---
        r4 = self.session_post(
            params={
                "action": "wbcreateclaim",
                "entity": q,
                "snaktype": "value",
                "property": proprty,
                "value": '{"entity-type":"item","numeric-id":' + numeric + "}",
            }
        )
        # ---
        if not r4:
            return False
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d is True:
            logger.debug("<<lightgreen>> ** true.")
            if quall_prop and quall_id:
                return self._Set_Quall(r4, quall_prop, quall_id)
            else:
                logger.debug(f'<<lightred>> ** cant find quall_prop:"{quall_prop}" or quall_id:"{quall_id}" .')
            # ---
            if returnClaimid:
                # ---
                Claimid = r4.get("claim", {}).get("id", "")
                # ---
                return Claimid
                # ---
            else:
                return True
            # ---
        else:
            if d == "warn":
                logger.warning("", text=r4)

    def Remove_Claim(self, claimid, nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        if not claimid:
            return False
        # ---
        out = f"Remove_Claim with id {claimid}."
        r4 = self.session_post(
            params={
                "action": "wbremoveclaims",
                "claim": claimid,  # "Q42$D8404CDA-25E4-4334-AF13-A3290BCD9C0N",
            }
        )
        # ---
        if not r4:
            return False
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning("", text=r4)
