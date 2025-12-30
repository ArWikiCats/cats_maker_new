#!/usr/bin/python3
"""

"""
from ..c18_new.bots.cat_tools_argv import use_sqldb
from . import sql_cat
from ..api_sql import GET_SQL, MySQLdb_finder_New

from ..helps import logger

pages_in_arcat_toMake = {}


def extract_fan_page_titles(enpageTitle):
    if GET_SQL() and use_sqldb[1]:
        cat2 = enpageTitle.replace("Category:", "").replace("category:", "").strip()
        # ---
        try:
            fapages = MySQLdb_finder_New(cat2, "")
        except Exception as e:
            logger.exception(e)
        # ---
    logger.info(f"<<lightgreen>>Adding {len(fapages)} pages to fapage lists<<default>>")
    return fapages


def get_listenpageTitle(artitle, enpageTitle1):
    # ---
    enpageTitle = enpageTitle1.strip()
    # ---
    listenpageTitle = sql_cat.make_ar_list_newcat2(artitle, enpageTitle1, us_sql=True) or []
    # ---
    listenpage2 = sql_cat.make_ar_list_newcat2(artitle, enpageTitle1, us_sql=True, wiki="en") or []
    # ---
    listenpageTitle.extend(listenpage2)
    # ---
    if not listenpageTitle:
        fapages = extract_fan_page_titles(enpageTitle)
        listenpageTitle.extend(fapages)
    # ---
    if enpageTitle in pages_in_arcat_toMake:
        logger.info(f'<<lightgreen>> pages_in_arcat_toMake Adding for cats: "{enpageTitle}" : ')
        listenpageTitle.extend(pages_in_arcat_toMake[enpageTitle])
    # ---
    listenpageTitle = list(set(listenpageTitle))
    listenpageTitle = [x for x in listenpageTitle if isinstance(x, str) and x != ""]
    # ---
    return listenpageTitle
