#!/usr/bin/python3
"""



"""
from ..wd_bots import NewHimoAPIBot
from ..wiki_api import arAPI
from . import categorytext
from ..helps import logger
from .mk_bots import no1help
from ..utils.skip_cats import skip_encats

import functools


@functools.lru_cache(maxsize=1)
def get_wd_api_bot():
    return NewHimoAPIBot(Mr_or_bot="bot", www="www")


find_title = [
    "إسرائيل",
    "إرهاب",
]
Cate_Created = {}
dump = {}
dump["new"] = []
done_list = []


def add_text_to_cat(text, categories, enca, title, qid, family=""):
    if family != "wikipedia" and family:
        return text

    new_text = text

    if len(categories) > 0:
        # اضافة التصنيفات المعادلة

        caca = "\n".join([f"[[{str(cai)}]]" for cai in categories if cai is not None and cai is not False])

        numadd = str(len(categories))

        suu = "، ".join([f"[[{s}]]" for s in categories if s is not None and s is not False])
        suu = f"({suu})"

        if len(categories) > 6:
            suu = "تصنيف"

        msg = f"بوت: [[مستخدم:Mr.Ibrahembot/التصانیف المعادلة|التصانيف المعادلة]]:+ {numadd} {suu}"

        new_text += f"\n{caca}"

        ux = arAPI.page_put(oldtext=text, newtext=new_text, summary=msg, title=title)

        if ux:
            text = new_text

    p373 = categorytext.getP373(enca, qid)

    if p373:
        # اضافة قالب كومنز
        susa = f"بوت: أضاف {p373}"

        new_text += f"\n{p373}"

        ux0 = arAPI.page_put(oldtext=text, newtext=new_text, summary=susa, title=title)

        if ux0:
            text = new_text

    portalse, portals_list = categorytext.Make_Portal(title, enca, return_list=True)

    if portalse and portals_list != []:
        # اضافة قالب بوابة
        asds = ",".join([f"بوابة:{dd}" for dd in portals_list])

        sus2 = f"بوت:إضافة بوابة ({asds})"

        new_text = f"{portalse}\n{new_text}"

        ux1 = arAPI.page_put(oldtext=text, newtext=new_text, summary=sus2, title=title)

        if ux1:
            text = new_text

    temp = categorytext.Make_temp(enca, title)

    if temp:
        new_text += f"\n{temp}"

        ux2 = arAPI.page_put(oldtext=text, newtext=new_text, summary="بوت: إضافة قالب تصفح", title=title)

        if ux2:
            text = new_text

    return new_text


def make_category(categories, enca, title, qid, family=""):
    if enca in skip_encats:
        logger.debug(f"<<lightred>> enca: {enca} in skip_encats")
        return False

    if not title.startswith("تصنيف:"):
        logger.debug(f'<<lightreed>> title: {title} not start with "تصنيف:"')
        return False

    caia = ""

    for cai in categories:
        if cai is not None and cai is not False:
            caia = f"\n[[{str(cai)}]]"
            break

    text = "{{نسخ:#لوموجود:{{نسخ:اسم_الصفحة}}|{{مقالة تصنيف}}|}}\n"

    text = text + caia
    text += f"\n\n[[en:{enca}]]"

    New_Cat = arAPI.create_Page(text, "بوت:إنشاء تصنيف.", title, False, sleep=0, family=family, minor=1)

    if New_Cat is not False:
        text = add_text_to_cat(text, categories, enca, title, qid, family="")

        # ass4.work_ar_title_page(title, "", 14, enlink=enca, askk=False, newwa=True)

    logger.warning(f"<<lightgreen>> New_Cat: {New_Cat}")

    return New_Cat


def Log_to_wikidata(ar, enca, qid):
    if qid:
        get_wd_api_bot().Sitelink_API(qid, ar, "arwiki", nowait=True)
        get_wd_api_bot().Labels_API(qid, ar, "ar", False, nowait=True, tage="catelabels")

    else:
        cd = get_wd_api_bot().Sitelink_API("", ar, "arwiki", enlink=enca, ensite="enwiki", nowait=True)
        if cd is not True:
            no1help.Make_New_item(ar, enca, family="wikipedia")


def new_category(enca, title, categories, qid, family=""):
    logger.debug(f'<<lightgreen>>* make ar cat:"{title}", for english:"{enca}". ')

    if not title or title == "n":
        logger.debug('<<lightred>> not title or title != "n"')

    New_Cat = make_category(categories, enca, title, qid, family=family)

    susu = f"بوت: [[مستخدم:Mr.Ibrahembot/التصانیف المعادلة|التصانيف المعادلة]]:+ 1 ([[{title}]])"

    if New_Cat is False or New_Cat is not True:
        logger.debug("no1: New_Cat is False")
        get_wd_api_bot().Labels_API(qid, title, "ar", True, nowait=True, tage="catelabels")
        logger.debug("return False")
        return False

    Cate_Created[enca] = title

    return True
