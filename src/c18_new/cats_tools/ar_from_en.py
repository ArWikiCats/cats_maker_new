#!/usr/bin/python3
"""

"""
from ...b18_new.cat_tools_enlist import get_ar_list_from_cat
from ...b18_new.LCN_new import find_LCN, get_arpage_inside_encat
from ..bots.cat_tools_argv import EEn_site, use_sqldb
from ..cat_tools2 import Categorized_Page_Generator
from ..log import logger
from ..tools_bots.sql_bot import find_sql
from .en_link_bot import en_title_for_arpage_cache


def make_ar_list_from_en_cat(encat):
    """Generate a list of categorized pages from an English category string.

    This function takes an English category string, processes it to remove
    unnecessary prefixes and suffixes, and attempts to generate a list of
    categorized pages associated with that category. If the input category
    is empty, it returns False. The function also checks if the category can
    be found in a SQL database and falls back to generating the list using
    other methods if necessary.

    Args:
        encat (str): The English category string to process.

    Returns:
        list: A list of unique categorized page titles derived from the input
        category. If the input category is empty, it returns False.
    """

    # ---
    if not encat:
        logger.output("<<lightblue>> No encat")
        return False
    # ---
    logger.output(f'<<lightgreen>>* make_ar_list_from_en_cat: cat:"{encat}" ')
    # count = 0
    encat = (
        encat.replace("[[", "")
        .replace("]]", "")
        .replace("Category:", "")
        .replace("category:", "")
        .replace("category talk:", "")
        .strip()
    )
    encat = encat.replace("Catégorie:", "")
    # ---
    enpageTitle = encat
    logger.debug("cat: " + encat)
    # ---
    listenpageTitle2 = []
    # ---
    if use_sqldb[1]:
        listenpageTitle2 = find_sql(enpageTitle)
    # ---
    if not listenpageTitle2:
        # ---
        gent_faso_list = Categorized_Page_Generator(enpageTitle, "all")
        # ---
        UUX = get_arpage_inside_encat("Category:" + enpageTitle)
        # ---
        if UUX:
            logger.output("arpage inside_encat: " + (",a: ".join(UUX)))
            for x in UUX:
                gent_faso_list.append(x.replace("_", " "))
        # ---
        if not gent_faso_list:
            gent_faso_list = get_ar_list_from_cat(encat, code="en", typee="all")
        # ---
        logger.output(f" make_ar_list_from_en_cat lenth : {len(gent_faso_list)}")
        # ---
        new_ll = Get_ar_list_from_en_list(gent_faso_list)
        # ---
        for cc in new_ll:
            listenpageTitle2.append(cc)
    # ---
    listenpageTitle = []
    for cdv in listenpageTitle2:
        if cdv not in listenpageTitle:
            listenpageTitle.append(cdv)
    # ---
    if len(listenpageTitle) == 0:
        logger.output("<<lightblue>>make_ar_list_from_en_cat No cats listenpageTitle = [] ")
    # ---
    logger.output(f"<<lightblue>> end of make_ar_list_from_en_cat, lenth:{len(listenpageTitle)}")
    return listenpageTitle


def Get_ar_list_from_en_list(enlist):
    # ---
    new_ar_list = []
    en_done = []
    # ---
    for i in range(0, len(enlist), 50):
        liste = enlist[i : i + 50]
        part_list = "|".join(liste)
        if part_list:
            if part_list.startswith("|"):
                part_list = part_list[len("|") :]
            # ---
            new_list = find_LCN(part_list, prop="langlinks", lllang="ar", first_site_code=EEn_site["code"])
            # logger.debug(f'gent_sasa {gent_sasa} ' )
            # ---
            if new_list:
                for p_w in new_list:
                    # ---
                    # logger.debug(f'p_w {p_w} ' )
                    # logger.debug(f'new_list[p_w] {new_list[p_w]} ' )
                    # ---
                    fapagetitle = ""
                    if "langlinks" in new_list[p_w] and "ar" in new_list[p_w]["langlinks"]:
                        fapagetitle = new_list[p_w]["langlinks"]["ar"]
                    # ---
                    if fapagetitle:
                        # ---
                        logger.debug(f"<<lightblue>>Adding {fapagetitle} to ar lists {p_w}<<default>>")
                        # ---
                        new_ar_list.append(fapagetitle)
                        en_done.append(p_w.replace("_", " "))
        # ---
        for xen in liste:
            # ---
            en = xen.replace("_", " ")
            # ar_title = ''
            # ---
            if en not in en_done and en_title_for_arpage_cache(en):
                tat = en_title_for_arpage_cache(en)
                logger.debug(f"<<lightblue>>Adding {tat} from En_title_for_ar page {xen}<<default>>")
                new_ar_list.append(tat)
    # ---
    logger.output(f"<<lightyellow>> Get_ar_list_from_en_list, <<lightblue>>lenth of new_ar_list:{len(new_ar_list)}")
    # ---
    new_ar_list = list(set(new_ar_list))
    # ---
    return new_ar_list
