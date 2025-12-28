#!/usr/bin/python3
"""
!
"""

import json
import re
import sys
import time

from ..utils import lag_bot, logger
from ..utils.out_json import outbot_json


def ask_put(s):
    yes_answer = ["y", "a", "", "Y", "A", "all", "aaa"]
    sa = input(s)
    if sa not in yes_answer:
        print(" bot: wrong answer")
        return False
    if sa == "a" or sa == "A":
        return "a"
    return True


class WD_Sitelinks:
    def __init__(self, wdapi_new):
        self.wdapi_new = wdapi_new
        self.session_post = self.wdapi_new.post_to_newapi

    def Merge(self, q1, q2, nowait=False):
        """Merge two items in a knowledge base.

        This function merges two items identified by their IDs (q1 and q2). It
        first checks for any lag issues and then determines which item should be
        the source and which should be the target based on their numeric values.
        The merge operation is performed via a session post request, and the
        function handles potential redirection and errors that may arise during
        the process.

        Args:
            q1 (str): The ID of the first item to merge.
            q2 (str): The ID of the second item to merge.
            nowait (bool): A flag indicating whether to wait for the operation to complete.

        Returns:
            bool: True if the merge was successful, False otherwise.
        """

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
        out = f"Merge from {From} to {To} "
        # ---
        logger.debug(out)
        # ---
        r4 = self.session_post(
            params={
                "action": "wbmergeitems",
                "fromid": From,
                "toid": To,
                "ignoreconflicts": "description",
                "summary": "",
                # "summary": "duplicated",
            }
        )
        # ---
        if not r4:
            return False
        # ---
        if r4.get("success", 0) == 1:
            _e_ = {
                "success": 1,
                "redirected": 0,
                "from": {"id": "Q65687062", "type": "item", "lastrevid": 1849114386},
                "to": {"id": "Q8278540", "type": "item", "lastrevid": 1849114387},
            }
            # ---
            redirected = r4.get("redirected", 0)
            # ---
            if redirected == 1:
                logger.debug("<<lightgreen>> ** true .. redirected.")
                time.sleep(lag_bot.newsleep[1])
            else:
                logger.debug("<<lightgreen>> ** true, no redirected.")
                ioi = self.wbcreateredirect(From, To, nowait=False)
            return True
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning("", text=r4)
        # ---
        _err_ = {
            "error": {
                "code": "failed-modify",
                "info": "Attempted modification of the Item failed.",
                "extradata": ["Conflicting sitelinks for arwiki"],
                "messages": [
                    {
                        "name": "wikibase-api-failed-modify",
                        "parameters": [],
                        "html": {"*": "Attempted modification of the Item failed."},
                    }
                ],
                "*": ".",
            },
            "servedby": "mw2404",
        }
        # ---
        return False

    def wbcreateredirect(self, From, To, nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        if From.strip() == To.strip():
            logger.debug("<<lightgreen>> **False: From == To.")
            return False
        # ---
        out = f"wbcreateredirect from {From} to {To} "
        # ---
        r4 = self.session_post(
            params={
                "action": "wbcreateredirect",
                "from": From,
                "to": To,
                "ignoreconflicts": "description",
            }
        )
        # ---
        if not r4:
            return False
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d is True:
            logger.debug("<<lightgreen>> **createredirect true.")
            time.sleep(lag_bot.newsleep[1])
            return True
        # ---
        if d == "warn":
            logger.warning("", text=r4)

    def Find_page_qids(self, sitecode, titles):
        _false = True
        if sitecode.endswith("wiki"):
            sitecode = sitecode[:-4]
        # ---
        params = {
            "action": "query",
            "titles": titles,
            "redirects": 1,
            "prop": "pageprops",
            "ppprop": "wikibase_item",
            # "normalize": 1,
        }
        # ---
        _sitewiki = f"{sitecode}wiki"
        # ---
        json1 = self.session_post(params)
        # ---
        if not json1:
            return {}
        # ---
        Main_table = {}
        js = json1.get("query", {})
        # ---
        for red in js.get("redirects", []):
            Main_table[red["from"]] = {
                "isRedirectPage": True,
                "missing": True,
                "from": red["from"],
                "to": red["to"],
                "title": red["from"],
                "ns": "",
                "q": "",
            }
        # ---
        for _id, kk in js.get("pages", {}).items():
            if "title" in kk:
                title = kk["title"]
                Main_table[title] = {}
                if "missing" in kk:
                    Main_table[title]["missing"] = True
                Main_table[title]["ns"] = kk.get("ns", "")
                Main_table[title]["pageid"] = kk.get("pageid", "")
                Main_table[title]["q"] = kk.get("pageprops", {}).get("wikibase_item", "")
        # ---
        return Main_table

    def Sitelink_API_or_Merge(
        self, Qid, title, wiki, enlink="", ensite="", nowait=False, returnid=False, return_text=False
    ):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        daf = self.Sitelink_API(Qid, title, wiki, enlink=enlink, ensite=ensite, return_text=True)
        # ---
        if not isinstance(daf, str):
            return False
        # ---
        # {"error":{"code":"failed-save","info":"The save has failed.","messages":[{"name":"wikibase-api-failed-save","parameters":[]},{"name":"wikibase-validator-sitelink-conflict"}]}}
        # ---
        daf = json.loads(daf)
        err = daf.get("error", {}).get("messages", [])
        # ---
        for x in err:
            if x["name"] == "wikibase-validator-sitelink-conflict":
                qid_en = self.Find_page_qids("enwiki", enlink).get(enlink, {}).get("q", "")
                qid_ar = self.Find_page_qids("arwiki", title).get(title, {}).get("q", "")
                # ---
                logger.debug(f"<<lightyellow>> *Sitelink_API_or_Merge: False: qid_en[{qid_en}], qid_ar[{qid_ar}].")
                # ---
                if qid_en and qid_ar:
                    self.Merge(qid_en, qid_ar)
                # ---
                break

    def Sitelink_API(self, Qid, title, wiki, enlink="", ensite="", nowait=False, returnid=False, return_text=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        if not wiki.endswith("wiki") and wiki.find("wiki") == -1 and wiki.find("wiktionary") == -1:
            wiki = f"{wiki}wiki"
        # ---
        if enlink:
            logger.debug(f' **Sitelink_API: enlink:"{ensite}:{enlink}" {wiki}:{title}')
        else:
            logger.debug(f' **Sitelink_API: Qid:"{Qid}" {wiki}:{title}')
        # ---
        # save the edit
        # ---
        if Qid.strip() == "" and enlink == "":
            logger.debug(f'<<lightred>> **Sitelink_API: False: Qid == "" {wiki}:{title}.')
            return False
        # ---
        paramse = {
            "action": "wbsetsitelink",
            "linktitle": title,
            "linksite": wiki,
        }
        # ---
        out = f'Added link to "{Qid}" [{wiki}]:"{title}"'
        # ---
        if Qid:
            paramse["id"] = Qid
        else:
            out = f'Added link to "{ensite}:{enlink}" [{wiki}]:"{title}"'
            paramse["title"] = enlink
            paramse["site"] = ensite
        # ---
        r4 = self.session_post(params=paramse, tage="setsitelink")
        # ---
        if not r4:
            return False
        # ---
        if "printtext" in sys.argv:
            logger.debug(r4)
            # {"entity":{"sitelinks":{"arwiki":{"site":"arwiki","title":"قالب:Db-attack-deleted","badges":[],"url":"https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D9%84%D8%A8:Db-attack-deleted"}},"id":"Q97928551","type":"item","lastrevid":1242627521,"nochange":""},"success":1}
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d is True:
            logger.warning(f"<<lightgreen>> true {out}")
            if enlink and returnid:
                ido = re.match(r".*\"id\"\:\"(Q\d+)\".*", str(r4))
                if ido:
                    return ido.group(1)
            else:
                return True
        # ---
        if return_text:
            return str(r4)
        # ---
        if d == "warn":
            logger.warning("", text=r4)
        # ---
        return d

    def Remove_Sitelink(self, Qid, wiki, nowait=False):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        if wiki.endswith("wiki"):
            wiki = wiki[:-4]
        # ---
        wiki = f"{wiki}wiki"
        # ---
        # save the edit
        out = f'remove "{wiki}" link from "{Qid}"'
        # ---
        r4 = self.session_post(
            params={
                "action": "wbsetsitelink",
                "id": Qid,
                # "linktitle": title,
                "linksite": wiki,
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
        if d is True:
            return True
        # ---
        return False
