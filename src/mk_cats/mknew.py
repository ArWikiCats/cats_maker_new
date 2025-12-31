"""
python3 core8/pwb.py mk_cats/mknew
"""
import sys

from ..b18_new import MakeLitApiWay
from ..b18_new import get_listenpageTitle
from ..b18_new import add_SubSub, get_SubSub_keys, get_SubSub_value

from ..wiki_api import find_Page_Cat_without_hidden

from ..b18_new import get_ar_list_from_en, make_ar_list_newcat2

from ..c18_new.bots.cat_tools_argv import use_sqldb
from .add_bot import add_to_final_list
from ..wd_bots.wd_api_bot import Get_Sitelinks_From_wikidata
from ..wiki_api import himoBOT2
from ..wd_bots import to_wd
from ..helps import logger
from .utils import filter_en
from .create_category_page import new_category
from .utils.check_en import check_en_temps

try:
    from ArWikiCats import resolve_arabic_category_label, logger as cat_logger  # type: ignore
    cat_logger.setLevel("ERROR")
except ImportError:
    resolve_arabic_category_label = None


def configure_parameters():
    DONE_D = []
    NewCat_Done = {}
    Already_Created = []
    Range = {1: 5}
    We_Try = {1: True}

    wiki_site_ar = {"family": "wikipedia", "code": "ar"}
    wiki_site_en = {"family": "wikipedia", "code": "en"}

    for arg in sys.argv:
        arg, _, value = arg.partition(":")

        if arg == "-We_Try":
            We_Try[1] = True
            logger.debug("<<lightred>> We_Try.")

        if arg == "-nowetry":
            We_Try[1] = False
            logger.debug("<<lightred>> NO We_Try.")

        if arg == "-range":
            Range[1] = int(value)
            logger.debug("<<lightred>> Range : %d ." % Range[1])
    return DONE_D, NewCat_Done, Already_Created, Range, We_Try, wiki_site_ar, wiki_site_en


DONE_D, NewCat_Done, Already_Created, Range, We_Try, wiki_site_ar, wiki_site_en = configure_parameters()


def ar_make_lab(title, **Kwargs):
    okay = filter_en.filter_cat(title)

    if not okay:
        return ""

    if resolve_arabic_category_label:
        label = resolve_arabic_category_label(title)
        logger.warning(f'<<lightgreen>> Resolved label for "{title}": "{label}"')
        return label

    return ""


def scan_ar_title(title):
    if title in Already_Created:
        logger.debug(f'<<lightpurple>> title "{title}". in Already_Created')
        return False

    cat3 = str(title)
    if cat3 in NewCat_Done.keys():
        NewCat_Done[cat3] += 1
        if We_Try[1] and cat3 in get_SubSub_keys():
            logger.debug(f'<<lightred>>2070:<<lightpurple>>new trying with cat: "{title}"')
            NewCat_Done[cat3] += 1
            return True
        else:
            logger.debug(f'<<lightblue>> We tried {NewCat_Done[cat3]} times to/created title:<<lightred>>"{cat3}".')
            return False
    else:
        if cat3 in NewCat_Done.keys():
            logger.debug(f'<<lightred>>2070:<<lightpurple>>new trying with cat: "{title}"')
            NewCat_Done[cat3] += 1
        else:
            NewCat_Done[cat3] = 1
    return True


def check_if_artitle_exists(en_title_1, test_title):
    if not test_title.startswith("تصنيف:"):
        test_title = f"تصنيف:{test_title}"

    test_page = himoBOT2.get_page_info_from_wikipedia(wiki_site_ar["code"], test_title, Workredirects=False)

    if test_page and test_page["exists"]:
        logger.debug(f"<<lightred>>* category:{test_title} already exists in arwiki.")

        return False

    return True


def make_ar(en_page_title, ar_title, callback=None):  # -> list:
    if not ar_title.strip():
        logger.debug("<<lightred>> ar_title is empty.")
        return []

    if not scan_ar_title(ar_title):
        logger.debug("<<lightred>> scan_ar_title failed.")
        return []

    en_page_title = en_page_title.replace("[[", "").replace("]]", "").strip()
    en_page_title = en_page_title.replace("_", " ")

    if not check_if_artitle_exists(en_page_title, ar_title):
        logger.debug("<<lightred>> artitle already exists.")
        return []

    members = []
    ar_site_wiki = "arwiki"
    en_site_lang = wiki_site_en["code"]  # "en"

    if wiki_site_en["family"] != "wikipedia" and wiki_site_en["code"] != "commons":
        ar_site_wiki = f"ar{wiki_site_ar['family']}"
        en_site_lang = wiki_site_en["code"] + wiki_site_en["family"]

    # check sitelinks
    ar_info = Get_Sitelinks_From_wikidata(en_site_lang, en_page_title) or {}

    if ar_info and ("sitelinks" in ar_info) and (ar_site_wiki in ar_info["sitelinks"]):
        ar_page = ar_info["sitelinks"][ar_site_wiki]

        logger.debug(f'found "{ar_site_wiki}" link "{ar_page}" for en cat. ')

        return []
    else:
        logger.debug(f'No "{ar_site_wiki}" link for en cat "{en_page_title}", ar_title:"{ar_title}"')

    qid = ar_info.get("q", "")

    cates = find_Page_Cat_without_hidden(
        en_page_title,
        prop="langlinks",
        site_code=wiki_site_en["code"],
        family=wiki_site_en["family"],
    )

    en_cats_of_new_cat = []
    cats_of_new_cat = []

    if cates:
        for cato in cates:
            if "ar" in cates[cato]:
                cats_of_new_cat.append(cates[cato]["ar"])
            else:
                en_cats_of_new_cat.append(cato)

        if en_cats_of_new_cat:
            logger.debug(f"en_cats_of_new_cat : {','.join(en_cats_of_new_cat)}")
        if cats_of_new_cat:
            logger.debug(f"cats_of_new_cat : {','.join(cats_of_new_cat)}")

    Already_Created.append(en_page_title)

    # add cat to final list
    members = get_listenpageTitle(ar_title, en_page_title)

    if use_sqldb[1] is False or members == []:
        liste = MakeLitApiWay(en_page_title, Type="all")
        if liste:
            for ccat in liste:
                if ccat not in members:
                    members.append(ccat)
    # ---
    sub_category_values = get_SubSub_value(en_page_title.strip())

    if sub_category_values:
        logger.debug('<<lightgreen>> New Adding for cats: "%s" : ' % en_page_title)
        for cai in sub_category_values:
            logger.debug('<<lightgreen>> New Adding "%s" to fapage list.............' % cai)
            if cai not in members:
                members.append(cai)

    members = list(set(members))
    members = [m for m in members if m and isinstance(m, str)]

    if len(members) == 0:
        logger.debug(" get_listenpageTitle == [] ")
        return []

    opuo = ""

    if members and len(members) < 30:
        opuo = ",".join(members)

    logger.debug(f"Add to {len(members)} pages: {opuo}")

    # إنشاء التصنيف وإضافته للصفحات

    hhh = new_category(en_page_title, ar_title, cats_of_new_cat, qid, family=wiki_site_ar["family"])

    if hhh:
        add_to_final_list(members, ar_title, callback=callback)

        add_SubSub(en_cats_of_new_cat, hhh)

        listen = make_ar_list_newcat2(ar_title, en_page_title, us_sql=True, arcat_created=True) or []

        if listen != []:
            add_to_final_list(listen, ar_title, callback=callback)

        to_wd.Log_to_wikidata(ar_title, en_page_title, qid)
    else:
        to_wd.add_label(qid, ar_title)
    return en_cats_of_new_cat


def process_catagories(cat, arlab, num, lenth, callback=None):
    logger.debug(f"*process_catagories: <<lightred>> {num}/{lenth} cat: {cat}, arlab: {arlab}")

    ma_table = make_ar(cat, arlab, callback=callback)

    for i in range(0, Range[1]):
        if not ma_table:
            break

        logger.debug("===========================")
        logger.debug(f"**process_catagories: range: {i} of {Range[1]}: for {len(ma_table)} cats.")
        logger.debug("===========================")

        enriched_titles = []
        number = 0

        for title in ma_table:
            logger.debug(r"<<lightred>>\/\/\/ +++++++++ \/\/\/")
            logger.debug(f'work:{number} <<lightpurple>>"{title}"')
            number += 1

            labe = ar_make_lab(title)

            logger.debug(f"*<<lightred>> arlab: {labe}")

            if not labe:
                continue

            en_list = get_ar_list_from_en(title, us_sql=True, wiki="en")

            if not en_list:
                continue

            enriched_article_list = make_ar(title, labe, callback=callback)

            enriched_titles.extend(enriched_article_list)

        ma_table = list(set(enriched_titles))

    logger.debug("<<lightred>> tago done........... ")


def one_cat(en_title, num, lenth, sugust="", uselabs=False, callback=None):
    logger.debug("_________________________________________________________")

    logger.debug(f"{num}/{lenth} {en_title=}, {sugust=}")

    if not en_title.strip():
        logger.warning("<<lightred>> en_title is empty. return")
        return False

    if en_title in DONE_D:
        logger.warning(f'en_title:"{en_title}" in DONE_D ')
        return False

    DONE_D.append(en_title)
    labb = ar_make_lab(en_title)

    logger.debug(f"{num}/{lenth} {en_title=}, {sugust=}, {labb=}")

    labb = labb or sugust

    if not labb:
        logger.warning("<<lightred>> labb is empty.")
        return False

    if not check_en_temps(en_title):
        logger.warning("<<lightred>> check_en_temps failed.")
        return False

    en_list = get_ar_list_from_en(en_title, us_sql=True, wiki="en")

    if not en_list:
        logger.warning("<<lightred>> en_list is empty. return")
        return False

    return process_catagories(en_title, labb, num, lenth, callback=callback)


def create_categories_from_list(liste, uselabs=False, callback=None):
    lenth = len(liste)

    for num, en_title in enumerate(liste, 1):
        one_cat(en_title, num, lenth, uselabs=uselabs, callback=callback)


# Legacy name
ToMakeNewCat2222 = create_categories_from_list
no_work = process_catagories
