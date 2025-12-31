#!/usr/bin/python3
"""

"""
import time

from ..c18_new.bots.text_to_temp_bot import add_text_to_template
from ..c18_new.dontadd import Dont_add_to_pages_def
from ..c18_new.tools_bots.sort_bot import sort_categories
from ..helps import logger
from ..new_api.page import MainPage

Dont_add_to_pages = Dont_add_to_pages_def()


def add_to_page(page_title, arcat, callback=None):
    # ---
    start = time.perf_counter()
    # ---
    logger.info(f"add_to_page page_title:{page_title} , cat:{arcat}")
    # ---
    if page_title in Dont_add_to_pages:
        logger.info(f"<<lightred>> page_title:{page_title} in [[تصنيف:صفحات لا تقبل التصنيف المعادل]]")
        return False
    # ---
    arcat = arcat.replace("_", " ")
    final_categories = f"\n[[{arcat}]]"
    # ---
    # susu = " بوت: أضاف 1 تصنيف"
    # ---
    susu = f"بوت [[مستخدم:Mr.Ibrahembot/التصانیف المعادلة|التصانيف المعادلة]]: +([[{arcat}]])"
    # ---
    page = MainPage(page_title, "ar")
    text = page.get_text()
    ns = page.namespace()
    # ---
    if not text:
        logger.info(' text = "" ')
        return False
    # ---
    if page.isRedirect():
        return False
    # ---
    if page.isDisambiguation():
        return False
    # ---
    if not page.exists():
        return False
    # ---
    page_edit = page.can_edit(script="cat")
    # ---
    if not page_edit:
        return False
    # ---
    categories = page.get_categories(with_hidden=False)
    # ---
    if text.find(f"[[{arcat}]]") != -1 or text.find(f"[[{arcat}|") != -1:
        logger.info(" text.find( final_categories.strip() ) != -1 ")
        return False
    # ---
    newtext = text
    # ---
    # إضافة التصانيف إلى القوالب
    if ns == 10:
        newtext = add_text_to_template(newtext, final_categories, page_title)
    # ---
    # إضافة التصانيف إلى المقالات
    else:
        if newtext.find("[[تصنيف:") != -1:
            num = newtext.find("[[تصنيف:")
            newtext = f"{(newtext[:num] + final_categories)}\n{newtext[num:]}"
            # ---
            if newtext.find(final_categories.strip()) == -1:
                newtext = newtext + final_categories
    # ---
    if newtext == text:
        return False
    # ---
    # newtext = cosmetic_change_bot.do_cos_meticchanges(newtext, False, title=page_title, page_ns=ns)
    # ---
    newtext = sort_categories(newtext, page_title)
    # ---
    save = page.save(newtext=newtext, summary=susu)
    # ---
    if not save:
        logger.error(f"<<lightred>> page.save() failed for {page_title=}, {arcat=}")
        return False
    # ---
    if callback:
        try:
            callback(page_title)
        except Exception as e:
            logger.info(f"<<lightred>> Error in callback: {e}")
    # ---
    delta = time.perf_counter() - start
    logger.info(f"add_bot.py done in {delta:.2f} seconds")
    # ---
    return True


def add_to_final_list(final_list, title, callback=None):
    # ---
    title = title.replace("_", " ")
    # ---
    if not title.startswith("تصنيف:"):
        title = f"تصنيف:{title}"
    # ---
    if final_list:
        for n, page in enumerate(final_list, start=1):
            logger.info(f"<<yellow>> add_to_final_list cat:{title} page:{page} n:{n}/{len(final_list)}")
            add_to_page(page, title, callback=callback)
