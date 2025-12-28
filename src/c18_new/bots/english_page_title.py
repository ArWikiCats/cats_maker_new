"""
Usage:
from ..bots.english_page_title import get_english_page_title
"""

import sys

from ...wiki_api import himoBOT2
from ..cats_tools.en_link_bot import english_page_link
from ..log import logger

# ---


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
            en = himoBOT2.get_en_link_from_ar_text(text_new, pagetitle, ar_site, en_site)
    # ---
    if not en:
        en = english_page_link(pagetitle, en_site, en_site, text=text_new)
    # ---
    if (not en or en == "") and "workfr" in sys.argv:
        fr_page_title = False
        logger.output("<<lightred>>c18/scat/cat.py no en")
        logger.output(ar_page_langlinks)
        fr2 = ar_page_langlinks.get(fr_site, "")
        if fr2:
            fr_page_title = fr2
        else:
            fr_page_title = english_page_link(pagetitle, en_site, fr_site, text=text_new)
        # ---
        if not fr_page_title:
            logger.output("<<lightred>> no fr_page_title")
            return "", ""
        en = fr_page_title
        new_site = fr_site
        logger.output("<<lightred>> find cat from frwiki.....")
    # ---
    pageblacklist = ["Sandbox"]
    # ---
    if en:
        for item in pageblacklist:
            if en.find(item.lower()) != -1:
                logger.output(f"<<lightred>> en {en} in blacklist")
                return "", ""
    # ---
    return en, new_site
