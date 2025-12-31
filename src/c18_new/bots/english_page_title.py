"""
Usage:
from ..bots.english_page_title import get_english_page_title
"""

import sys
from ..cats_tools.en_link_bot import english_page_link
from ..log import logger
from ...wd_bots.wd_api_bot import Get_Sitelinks_From_wikidata


def get_en_link_from_ar_text(title, site, sitetarget):
    # ---
    enpage = Get_Sitelinks_From_wikidata(site, title, return_main_table=True)
    # ---
    if not enpage:
        return ""
    # ---
    EngInterwiki = ""
    # ---
    if sitetarget:
        sitetarget2 = sitetarget
        if not sitetarget.endswith("wiki"):
            sitetarget2 += "wiki"
        # ---
        sitelinks = enpage.get("sitelinks", {})
        EngInterwiki = sitelinks.get(sitetarget) or sitelinks.get(sitetarget2) or ""
    # ---
    if EngInterwiki:
        logger.debug(f"<<lightblue>> himoBOT2.py, get_en_link_from_ar_text {EngInterwiki}")
    # ---
    return EngInterwiki


def get_english_page_title(englishlink, pagetitle, text_new, ar_page_langlinks):
    # ---
    en = ""
    # ---
    if englishlink:
        en = englishlink
    # ---
    ar_site = "ar"
    en_site = "en"
    fr_site = "fr"
    # ---
    new_site = en_site
    # ---
    if not en:
        en2 = ar_page_langlinks.get(en_site, "")
        if en2:
            en = en2
        else:
            en = get_en_link_from_ar_text(pagetitle, ar_site, en_site)
    # ---
    if not en:
        en = english_page_link(pagetitle, en_site, en_site, text=text_new)
    # ---
    if (not en or en == "") and "workfr" in sys.argv:
        fr_page_title = False
        logger.info("<<lightred>>c18/scat/cat.py no en")
        logger.info(ar_page_langlinks)
        fr2 = ar_page_langlinks.get(fr_site, "")
        if fr2:
            fr_page_title = fr2
        else:
            fr_page_title = english_page_link(pagetitle, en_site, fr_site, text=text_new)
        # ---
        if not fr_page_title:
            logger.info("<<lightred>> no fr_page_title")
            return "", ""
        en = fr_page_title
        new_site = fr_site
        logger.info("<<lightred>> find cat from frwiki.....")
    # ---
    pageblacklist = ["Sandbox"]
    # ---
    if en:
        for item in pageblacklist:
            if en.find(item.lower()) != -1:
                logger.info(f"<<lightred>> en {en} in blacklist")
                return "", ""
    # ---
    return en, new_site
