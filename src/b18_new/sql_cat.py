#!/usr/bin/python3
"""

"""
import sys

from pymysql.converters import escape_string
from ..api_sql import GET_SQL, sql_new_title_ns, sql_new
from ..c18_new.cats_tools.ar_from_en2 import get_en_title
from ..helps import logger
from ..utils.skip_cats import global_False_entemps
from ..wiki_api import himoBOT2
from .cat_tools_enlist2 import get_ar_list_from_cat

JustAdd = {1: False}
USE_SQLL = {1: False}
# ---
NO_Templates_ar = [
    "تصنيف ويكيبيديا",
    "تحويل تصنيف",
    "تصنيف تتبع",
    "تصنيف تهذيب شهري",
    "تصنيف مخفي",
    "تصنيف بذرة",
    "تصنيف حاوية",
]
# ---
NO_Templates_lower = [x.lower() for x in global_False_entemps]
# ---
if "-stubs" in sys.argv or "stubs" in sys.argv:
    NO_Templates_ar.remove("تصنيف بذرة")
    NO_Templates_ar.remove("تصنيف مخفي")


def get_ar_list(arcat, us_sql=True):
    """Retrieve a list of Arabic pages from a specified category.

    This function generates a SQL query to fetch page titles and namespaces
    from the specified Arabic category. It can either execute the query
    against a SQL database or retrieve the list using an alternative method
    based on the `us_sql` flag. If SQL execution is enabled and the SQL
    connection is available, it will use that method; otherwise, it will
    fall back to a different retrieval approach.

    Args:
        arcat (str): The category name from which to retrieve the Arabic pages.
        us_sql (bool): A flag indicating whether to use SQL for retrieval.
            Defaults to True.

    Returns:
        list: A list of page titles from the specified Arabic category.
    """

    # ---
    ar_cat2 = arcat.replace(" ", "_").replace("تصنيف:", "")
    ar_cat2 = escape_string(ar_cat2)
    # ---
    qia_ar = f"""select page_title, page_namespace
        from page, categorylinks
        where cl_from = page_id
        and cl_to = "{ar_cat2}"
    """
    # ---
    ar_list = []
    # ---
    if us_sql is True and GET_SQL():
        # ---
        ar_list = sql_new_title_ns(qia_ar, wiki="arwiki", t1="page_title", t2="page_namespace")
    else:
        ar_list = get_ar_list_from_cat(arcat, code="ar", typee="", return_list=True)
    # ---
    logger.info(f"<<lightgreen>> lenth ar_list:{len(ar_list)}")
    # ---
    return ar_list


def get_ar_list_from_en(encat, us_sql=True, wiki="en"):
    # ---
    encat2 = encat.replace(" ", "_").replace("Category:", "").replace("category:", "")
    encat2 = escape_string(encat2)
    # ---
    nss = "0, 10, 14"
    # ---
    if "nons10" in sys.argv:
        nss = "0, 14"
    # ---
    if "ns:14" in sys.argv:
        nss = "14"
    # ---
    en_qua = f"""
        select DISTINCT ll_title
            from page p1,categorylinks cla, langlinks
            where p1.page_id = ll_from
            and p1.page_namespace in ({nss})
            and cla.cl_to = "{encat2}"
            and ll_lang = 'ar'
            and cla.cl_from = p1.page_id
    """
    # ---
    if us_sql is True and GET_SQL():
        en_list_table = sql_new(en_qua, wiki=f"{wiki}wiki")
        en_list = [x.get("ll_title") for x in en_list_table if x.get("ll_title")]
    else:
        en_list = get_en_title(encat, wiki=wiki)
    # ---
    en_list = [x.replace("_", " ") for x in en_list]
    # ---
    return en_list


def do_sql(encat, arcat, us_sql=True, wiki="en"):
    # ---
    ar_list = get_ar_list(arcat, us_sql=us_sql)
    # ---
    en_list = get_ar_list_from_en(encat, us_sql=us_sql, wiki=wiki)
    # ---
    arlist_from_en = [x for x in en_list if x not in ar_list]
    # ---
    logger.info(f"<<lightgreen>> lenth arlist_from_en:{len(arlist_from_en)}")
    # ---
    return arlist_from_en


def make_ar_list_newcat2(arcat, encat, us_sql=False, wiki="en", arcat_created=False, arpage=False, enpage=False):
    # ---
    encat = encat.replace("Category:Category:", "Category:")
    # ---
    encat = encat.replace("category:", "").replace("Category:", "").replace("Catégorie:", "")
    encat2 = f"Category:{encat.replace('_', ' ')}"
    # ---
    arcat = arcat.replace("تصنيف:تصنيف:", "").replace("تصنيف:", "")
    arcat2 = f"تصنيف:{arcat.replace('_', ' ')}"
    # ---
    no_wrk = ""
    keepwork = True
    # ---
    # فحص التصنيف الانجليزي
    ioio_en = enpage or himoBOT2.get_page_info_from_wikipedia(wiki, encat2)
    if ioio_en:
        # en_temp = ioio_en.get(encat2) or ioio_en
        # ---
        if not ioio_en:
            logger.info(f"<<lightred>> not ioio_en:({encat2})")
            return False
        # ---
        elif ioio_en:
            if not ioio_en["exists"]:
                logger.info(f"<<lightred>> ioio_en:({encat2}) not exists")
                return False
            elif ioio_en["isRedirectPage"]:
                logger.info(f"<<lightred>> ioio_en:({encat2}) isRedirectPage")
                return False
        # ---
        # logger.info(ioio_en)
        # ---
        ar_link = ioio_en.get("langlinks", {}).get("ar", "")
        if ar_link and ar_link != arcat2:
            logger.info(f"<<lightred>> find ar in encat. ({ar_link}) != ({arcat2}) ")
            return False
            # keepwork = False
        # ---
        en_temp = ioio_en.get("templates", {})
        # if encat2 in ioio_en and 'templates' in ioio_en[encat2]:
        # logger.info(f"<<lightred>> en_temp:{','.join(en_temp)}" )
        for TargetTemp in en_temp:
            Target_Temp2 = TargetTemp.replace("Template:", "")
            if Target_Temp2.lower() in NO_Templates_lower and "keep" not in sys.argv:
                no_wrk = Target_Temp2
                logger.info(f"<<lightred>> encat:{encat2} has temp:{no_wrk} ")
                return False
                # break
    # ---
    # if not no_wrk:
    if keepwork:
        # ---
        # فحص التصنيف العربي
        ioio_ar = arpage or himoBOT2.get_page_info_from_wikipedia("ar", arcat2)
        # ---
        if not ioio_ar:
            logger.info(f"<<lightred>> not ioio_ar:({arcat2})")
            return False  # return []
        # ---
        elif ioio_ar:
            # if not ioio_ar['exists'] and not arcat_created :
            if not ioio_ar["exists"]:
                logger.info(f"<<lightred>> ioio_ar:({arcat2}) not exists")
                if not arcat_created:
                    return False  # return []
            elif ioio_ar["isRedirectPage"]:
                logger.info(f"<<lightred>> ioio_ar:({arcat2}) isRedirectPage")
                return False  # return []
        # ---
        if ioio_ar:
            # for x in ioio_ar:
            # ar_temp = ioio_ar.get(arcat2) or ioio_ar
            # ---
            # logger.info(ioio_ar)
            # ---
            en_link = ioio_ar.get("langlinks", {}).get("en", "")
            if en_link and en_link != encat2:
                logger.info(f"<<lightred>> find en in ioio_ar. ({en_link}) != ({encat2}) ")
                keepwork = False
                return False
            # ---
            ar_temp = ioio_ar.get("templates", {})
            # logger.info(f"<<lightred>> ar_temp:{','.join(ar_temp)}" )
            # if arcat2 in ioio_ar and 'templates' in ioio_ar[arcat2]:
            for TargetTemp in ar_temp:
                TargetTemp2 = TargetTemp.replace("قالب:", "")
                if TargetTemp2 in NO_Templates_ar and "keep" not in sys.argv:
                    no_wrk = TargetTemp2
                    logger.info(f"<<lightred>> arcat2:{arcat2} has temp:{no_wrk} ")
                    keepwork = False
                    # break
                    return False
    # ---
    if keepwork is False:
        return []
    # ---
    result = do_sql(encat, arcat, us_sql=us_sql, wiki=wiki)
    # ---
    return result
