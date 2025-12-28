#!/usr/bin/python3
"""
Add_To_Head
page_put
create_Page
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


def create_Page(text, summary, title, ask, sleep=0, family="", duplicate4="", minor=""):
    logger.info(f" create Page {title}:")
    # ---
    if title.startswith("نقاش القالب:") and title.endswith("/ملعب"):
        logger.info(" skip make talk to sandboxes..")
        return False
    # ---
    if not text:
        logger.info(' text != "" ')
        return False
    # ---
    page = MainPage(title, "ar")
    page_text = page.get_text()
    # ---
    if page_text:
        logger.info(' text != "" ')
        return False
    # ---
    if page.exists():
        return False
    # ---
    page_edit = page.can_edit(script="cat")
    # ---
    if not page_edit:
        return False
    # ---
    save = page.Create(text=text, summary=summary)
    # ---
    return save


def page_put(
    oldtext="",
    newtext="",
    summary="",
    title="",
    time_sleep="",
    family="",
    lang="",
    minor="",
    nocreate=1,
    tags="",
    basetimestamp="",
    returntrue=False,
    return_newtimestamp=False,
    nodiff=False,
    **kwargs,
):
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
    save = page.save(newtext=newtext, summary=summary, nocreate=nocreate, tags=tags, minor=minor, nodiff=nodiff)
    # ---
    return save
