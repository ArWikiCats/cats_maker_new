#!/usr/bin/python3
"""
"""
# ---
from ..helps import logger
from ..new_api.page import MainPage


def Add_To_Head(prependtext, summary, title, Ask, minor="", basetimestamp=""):
    # ---
    if not title.strip():
        logger.info('** Add_To_Head ..  title == ""')
        return False
    # ---
    if not prependtext.strip():
        logger.info('** Add_To_Head ..  prependtext == ""')
        return False
    # ---
    logger.info(f" Add_To_Head for Page {title}:")
    # ---
    page = MainPage(title, "ar")
    text = page.get_text()
    # ---
    if not text:
        logger.info(' text = "" ')
        return
    # ---
    if not page.exists():
        return
    # ---
    page_edit = page.can_edit(script="cat")
    # ---
    if not page_edit:
        return
    # ---
    newtext = prependtext + "\n" + text
    # ---
    save = page.save(newtext=newtext, summary=summary)
    # ---
    return save


def Add_To_Bottom(appendtext, summary, title, Ask, family="", minor="", basetimestamp=""):
    # ---
    if not title.strip():
        logger.info('** Add_To_Bottom ..  title == ""')
        return False
    # ---
    if not appendtext.strip():
        logger.info('** Add_To_Bottom ..  appendtext == ""')
        return False
    # ---
    logger.info(f" Add_To_Bottom for Page {title}:")
    # ---
    page = MainPage(title, "ar")
    text = page.get_text()
    # ---
    if not text:
        logger.info(' text = "" ')
        return
    # ---
    if not page.exists():
        return
    # ---
    page_edit = page.can_edit(script="cat")
    # ---
    if not page_edit:
        return
    # ---
    newtext = text + "\n" + appendtext
    # ---
    save = page.save(newtext=newtext, summary=summary)
    # ---
    return save
