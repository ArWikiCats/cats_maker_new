#!/usr/bin/python3
"""
!
"""
import re
from ..utils import lag_bot, logger
from ..mk_cats.wd_login_wrap import log_in_wikidata
from .wd_newapi_bot import WD_API
from .req_bots_new import descriptions_wd, items_wd, sitelinks_wd
from .utils.out_json import outbot_json, outbot_json_bot


class NewHimoAPIBot:
    def __init__(self, Mr_or_bot="bot", www="www"):
        # ---
        self.login_bot = log_in_wikidata(Mr_or_bot=Mr_or_bot, www=www)
        # ---
        self.wdapi_new = WD_API(self.login_bot, Mr_or_bot=Mr_or_bot)
        # ---
        self.get_rest_result = self.wdapi_new.get_rest_result
        # ---
        self.outbot_json_bot = outbot_json_bot
        self.outbot_json = outbot_json
        self.session_post = self.wdapi_new.post_to_newapi

        # =======================
        items_wd_bot = items_wd.WD_Items(self.wdapi_new)
        descriptions_wd_bot = descriptions_wd.WD_Descriptions(self.wdapi_new)
        sitelinks_wd_bot = sitelinks_wd.WD_Sitelinks(self.wdapi_new)
        # ---
        self.New_API = items_wd_bot.New_API
        self.New_Mult_Des_2 = descriptions_wd_bot.New_Mult_Des_2
        self.Des_API = descriptions_wd_bot.Des_API
        self.Sitelink_API = sitelinks_wd_bot.Sitelink_API

    def Labels_API(
        self, Qid, label, lang, ret, Or_Alii=False, change_des=False, number=0, nowait=False, tage="", remove=False
    ):
        # ---
        if lag_bot.bad_lag(nowait):
            return ""
        # ---
        if not Qid:
            logger.debug("Labels_API Qid == '' ")
            return False
        # ---
        if label == "" and not remove:
            logger.debug("Labels_API label == '' and remove = False ")
            return False
        # ---
        # save the edit
        out = f'{Qid} label:"{lang}"@{label}.'
        if number:
            out = f'{number} {Qid} label:"{lang}"@{label}.'
        r4 = self.session_post(
            params={
                "action": "wbsetlabel",
                "id": Qid,
                "language": lang,
                "value": label,
            },
            tage=tage,
        )
        # ---
        if not r4:
            logger.debug("Labels_API r4 == {} ")
            return False
        # ---
        text = str(r4)
        if ("using the same description text" in text) and ("associated with language code" in text):
            item2 = re.search(r"(Q\d+)", str(r4["error"]["info"])).group(1)
            logger.debug(f"<<lightred>>API: same label item: {item2}")
            if change_des is True:
                self.find_des_and_replace(Qid, label, lang)
            elif Or_Alii is True:
                self.Alias_API(Qid, [label], lang, ret)
        if ret:
            return text
        # ---
        d = outbot_json(r4, fi=out, NoWait=nowait)
        # ---
        if d == "warn":
            logger.warning(str(r4))


__all__ = [
    "NewHimoAPIBot",
]
