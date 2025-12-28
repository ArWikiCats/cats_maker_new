#!/usr/bin/python3
"""
!
"""
from ..mk_cats.wd_login_wrap import log_in_wikidata
from .h_wd_newapi.wd_newapi_bot import WD_API
from .req_bots_new import descriptions_wd, items_wd, labels_wd, sitelinks_wd
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
        labels_wd_bot = labels_wd.WD_Labels(self.wdapi_new, descriptions_wd_bot.Des_API)
        sitelinks_wd_bot = sitelinks_wd.WD_Sitelinks(self.wdapi_new)
        # ---
        self.New_API = items_wd_bot.New_API
        self.New_Mult_Des_2 = descriptions_wd_bot.New_Mult_Des_2
        self.Des_API = descriptions_wd_bot.Des_API
        self.Labels_API = labels_wd_bot.Labels_API
        self.Sitelink_API = sitelinks_wd_bot.Sitelink_API


__all__ = [
    "NewHimoAPIBot",
]
