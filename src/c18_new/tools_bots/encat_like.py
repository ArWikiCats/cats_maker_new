"""

"""
import re
import sys

from pymysql.converters import escape_string

from ...api_sql import wiki_sql
from ...utils.skip_cats import False_entemps_line_to_sql
from ..log import logger


def get_en_categories_like(mo, mo2="", limit="600", off=0):
    # ---
    logger.info(f"<<lightred>> sql . get_en_categories_like {mo}")
    # ---
    if not mo.strip():
        return False
    # ---
    mo = re.sub(r" ", "_", mo)
    # ---
    mo = escape_string(mo)
    # ---
    popo = f'p.page_title like "%{mo}%" OR p.page_title like "%{mo}"'
    # ---
    if mo2:
        popo = f'p.page_title like "%{mo}%" OR p.page_title like "%{mo2}%"'
    # ---
    if "only" in sys.argv:
        popo = f'p.page_title like "{mo}"'
    # ---
    off_line = ""
    # ---
    if off > 0:
        off_line = f"offset {off}"
    # ---
    only_with_ar = """
        AND p.page_title IN (
            SELECT DISTINCT cla.cl_to
            FROM page p1
            JOIN categorylinks cla ON cla.cl_from = p1.page_id
            JOIN langlinks ON p1.page_id = ll_from
            WHERE p1.page_namespace IN (0, 10, 14)
                AND ll_lang = 'ar'
                AND cla.cl_to = p.page_title
        )
    """
    # ---
    only_with_ar = only_with_ar if "test" not in sys.argv else ""
    # ---
    Queris = f"""
        SELECT CONCAT("Category:", p.page_title) AS category_title
        FROM page p
        WHERE p.page_namespace = 14
        AND ({popo})
        AND p.page_title not like "CS1_%"
        AND p.page_id NOT IN (
            SELECT ll_from
            FROM langlinks
            WHERE ll_lang = "ar"
        )
        AND p.page_id NOT IN (
            SELECT tl_from
            FROM templatelinks
            JOIN linktarget ON lt_id = tl_target_id
            WHERE lt_namespace = 10
                AND lt_title IN ({False_entemps_line_to_sql})
        )
        {only_with_ar}

        GROUP BY p.page_title
        limit {limit}
        {off_line}
    """
    # ---
    logger.info(Queris)
    # ---
    result = wiki_sql.sql_new(Queris, wiki="enwiki", printqua=False)
    # ---
    result = [x["category_title"].replace("_", " ") for x in result]
    # ---
    return result
