#!/usr/bin/python3
"""

"""
import os
import sys
from datetime import datetime
from pathlib import Path

from ...api_sql.wiki_sql import GET_SQL, sql_new_title_ns
from ...helps import logger
from .funcs import load_json, log_to_file

# ---
Dir = Path(__file__).parent.parent.parent
# ---
filename_json = Dir / "textfiles/Dont_add_to_pages.json"
# ---
Dont_add_to_pages = load_json(filename_json)


def from_sql():
    queries = """select page_title, page_namespace
        from page, templatelinks, linktarget
        where page_id = tl_from
        and page_namespace in (0, 10)
        and tl_target_id = lt_id
        and lt_namespace = 10
        and lt_title = "لا_للتصنيف_المعادل"
        ;"""
    # ---
    cats = []
    # ---
    if GET_SQL():
        cats = sql_new_title_ns(queries, wiki="ar", t1="page_title", t2="page_namespace")
    # ---
    return cats


def get_pages_nocat():
    global Dont_add_to_pages
    # ---
    if "nodontadd" in sys.argv or "test" in sys.argv:
        return Dont_add_to_pages
    # ---
    if "testadd" not in sys.argv:
        if str(Dir).find("/data/project/") == -1 and str(Dir).find("/mnt/") == -1:
            logger.output("dont get dontadd list in local server")
            return Dont_add_to_pages
    # ---
    # logger.output("makenew to Dont_add_to_pages...")
    # ---
    encats = from_sql()
    # ---
    Dont_add_to_pages = encats
    # ---
    if not Dont_add_to_pages:
        logger.output("Dont_add_to_pages is empty")
        return Dont_add_to_pages
    # ---
    logger.output(f"len Dont_add_to_pages : {len(Dont_add_to_pages)}")
    # ---
    log_to_file(Dont_add_to_pages, filename_json)
    # ---
    return Dont_add_to_pages


def Dont_add_to_pages_def():
    global Dont_add_to_pages

    # Get the time of last modification
    last_modified_time = os.path.getmtime(filename_json)
    # ---
    date = datetime.fromtimestamp(last_modified_time).strftime("%Y-%m-%d")
    # ---
    today = datetime.today().strftime("%Y-%m-%d")
    # ---
    if date != today or not Dont_add_to_pages:
        logger.output(f"<<purple>> last modified: {date} , today: {today}, len: {len(Dont_add_to_pages)} ")
        Dont_add_to_pages = get_pages_nocat()
    # ---
    return Dont_add_to_pages


if __name__ == "__main__":
    u = Dont_add_to_pages_def()
    logger.output(f"len Dont_add_to_pages : {len(u)}")
