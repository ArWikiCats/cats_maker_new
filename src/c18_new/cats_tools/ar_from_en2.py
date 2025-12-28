#!/usr/bin/python3
"""

"""
from ...b18_new.LCN_new import find_LCN
from ..bots.cat_tools_argv import EEn_site, FR_site
from ..log import logger
from .en_link_bot import en_title_for_arpage_cache
from ...new_api.page import CatDepth


def Get_ar_list_title_from_en_list(enlist, wiki="en"):
    # ---
    new_ar_list = []
    # ---
    en_done = []
    # ---
    for i in range(0, len(enlist), 50):
        liste = enlist[i : i + 50]
        part_list = "|".join(liste)
        if part_list:
            if part_list.startswith("|"):
                part_list = part_list[len("|") :]
            # ---
            sito_code = EEn_site["code"]
            # ---
            if wiki == "fr":
                sito_code = FR_site["code"]
            # ---
            new_list = find_LCN(part_list, prop="langlinks", lllang="ar", first_site_code=sito_code)
            # logger.debug(f'gent_sasa {gent_sasa} ' )
            # ---
            if new_list:
                for p_w in new_list:
                    # ---
                    # logger.debug(f'p_w {p_w} ' )
                    # logger.debug(f'new_list[p_w] {new_list[p_w]} ' )
                    # ---
                    if "langlinks" in new_list[p_w] and "ar" in new_list[p_w]["langlinks"]:
                        fapagetitle = new_list[p_w]["langlinks"]["ar"]
                        # ---
                        logger.debug(f"<<lightblue>>Adding {fapagetitle} to ar lists {p_w}<<default>>")
                        new_ar_list.append(fapagetitle)
                        en_done.append(fapagetitle.replace("_", " "))
        # ---
        for xen in liste:
            # ---
            en = xen.replace("_", " ")
            # ar_title = ''
            # ---
            if en not in en_done and en_title_for_arpage_cache(en):
                tat = en_title_for_arpage_cache(en)
                logger.debug("<<lightblue>>Adding " + tat + " from En_title_for_ar page " + xen + "<<default>>")

                new_ar_list.append(tat)
    # ---
    logger.info(
        f"<<lightyellow>> Get_ar_list_title_from_en_list, <<lightblue>>lenth of new_ar_list:{len(new_ar_list)}"
    )
    # ---
    return new_ar_list


def get_en_title(enpageTitle, wiki="en"):
    # ---
    logger.info(f"<<lightyellow>> get_en_title from category: {enpageTitle} <<default>>")
    # ---
    nss = [0, 14, 100]
    # ---
    cat_member = CatDepth(
        enpageTitle, sitecode=wiki, family="wikipedia", depth=0, ns="all", without_lang="", with_lang="ar", tempyes=[]
    )
    # ---
    en_titles = []
    # ---
    for title in cat_member:
        if int(cat_member[title]["ns"]) in nss:
            en_titles.append(title)
    # ---
    listenpageTitle = []
    # ---
    new_ll = Get_ar_list_title_from_en_list(en_titles, wiki=wiki)
    # ---
    for cc in new_ll:
        listenpageTitle.append(cc)
    # ---
    return listenpageTitle
