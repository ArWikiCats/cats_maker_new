#!/usr/bin/python3
"""

"""
from ..temp import main_make_temp_no_title
from ..wd_bots.wd_api_bot import Get_P373_API
from ..wiki_api import himoBOT2
from .utils import portal_en_to_ar_lower
from .categorytext_data import category_mapping, LocalLanguageLinks


def fetch_commons_category(entitle, Qid):
    template = ""
    P373 = Get_P373_API(q=Qid, titles=entitle, sites="enwiki")

    if P373:
        template = "{{تصنيف كومنز|%s}}" % P373

    return template


def generate_portal_content(title, enca, return_list=False):
    lilo = []
    en_links = himoBOT2.GetPagelinks(enca, sitecode="en")

    for x in en_links:
        if en_links[x].get("ns") == 100 or en_links[x].get("ns") == "100":
            cc = x.replace("Portal:", "")
            if cc.lower() in portal_en_to_ar_lower:
                lilo.append(portal_en_to_ar_lower[cc.lower()])

    # lilo = [ portal_en_to_ar_lower[x.lower()] for x in en_params if x.lower() in portal_en_to_ar_lower ]

    # lilo = []
    for cd in category_mapping:
        portal = category_mapping[cd]
        if title.find(cd) != -1 and portal not in lilo:
            lilo.append(portal)

    for xc in LocalLanguageLinks:
        if xc not in lilo:
            if title.find(" %s " % xc) != -1 or title.startswith("تصنيف:%s " % xc) or title.endswith(" %s" % xc):
                lilo.append(xc)

    litp = ""

    if len(lilo) != 0:
        litp = "|".join(lilo)

        litp = "{{بوابة|%s}}\n" % litp

    if return_list:
        return litp, lilo

    return litp


def generate_category_text(enca, title, Qid):
    ff = main_make_temp_no_title(enca, title)
    # ---
    text = ""
    text += generate_portal_content(title, enca)
    text += "{{نسخ:#لوموجود:{{نسخ:اسم_الصفحة}}|{{مقالة تصنيف}}|}}\n"
    text += fetch_commons_category(enca, Qid)

    if ff:
        text += "\n%s" % ff

    return text
