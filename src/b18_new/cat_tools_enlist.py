#!/usr/bin/python3
"""

"""
import sys
from ..c18_new.bots.cat_tools_argv import EEn_site, FR_site, use_sqldb
from ..c18_new.cats_tools.en_link_bot import english_page_link
from ..c18_new.tools_bots.sql_bot import MySQLdb_finder_New
from . import sql_cat
from ..api_sql import sql

from ..helps import logger

pages_in_arcat_toMake = {}


def get_listenpageTitle(artitle, enpageTitle1):
    listenpageTitle = []
    # ---
    enpageTitle = enpageTitle1.strip()
    # ---
    listenpageTitle = sql_cat.make_ar_list_newcat2(artitle, enpageTitle1, us_sql=True) or []
    # ---
    if "getfr" in sys.argv:
        frcat = english_page_link(enpageTitle1, EEn_site["code"], FR_site["code"])
        listenpage2 = sql_cat.make_ar_list_newcat2(artitle, frcat, us_sql=True, wiki="fr") or []
        for xfr in listenpage2:
            if xfr not in listenpageTitle:
                listenpageTitle.append(xfr)
    else:
        listenpage2 = sql_cat.make_ar_list_newcat2(artitle, enpageTitle1, us_sql=True, wiki="en") or []
        for xfr in listenpage2:
            if xfr not in listenpageTitle:
                listenpageTitle.append(xfr)
    # ---
    if not listenpageTitle:
        # xsfg = False
        fapages = []
        # ---
        if sql.GET_SQL() and use_sqldb[1]:
            cat2 = enpageTitle.replace("Category:", "").replace("category:", "").strip()
            # ---
            try:
                fapages = MySQLdb_finder_New(cat2, "")
            except Exception as e:
                logger.exception(e)
            # ---
            if fapages and fapages != []:
                # Work_API = False
                logger.output(f"<<lightgreen>>Adding {len(fapages)} pages to fapage lists<<default>>")
                for pages in fapages:
                    # logger.output( '<<lightgreen>>Adding ' + pages + ' to fapage lists<<default>>')
                    if pages not in listenpageTitle:
                        listenpageTitle.append(pages)
    # ---
    if enpageTitle in pages_in_arcat_toMake:
        logger.output(f'<<lightgreen>> pages_in_arcat_toMake Adding for cats: "{enpageTitle}" : ')
        for cai in pages_in_arcat_toMake[enpageTitle]:
            if cai not in listenpageTitle:
                listenpageTitle.append(cai)
    # ---
    listenpageTitle = list(set(listenpageTitle))
    listenpageTitle = [x for x in listenpageTitle if isinstance(x, str) and x != ""]
    # ---
    return listenpageTitle
