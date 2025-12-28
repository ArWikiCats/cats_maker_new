#!/usr/bin/python3
"""


"""
import sys
import time as tttime
from datetime import datetime

# ---
from ..helps import logger
from . import sql_qu

# ---
can_use_sql_db = sql_qu.can_use_sql_db
db_username = sql_qu.db_username
# ---
ns_text_tab_1 = {
    "1": "نقاش",
    "2": "مستخدم",
    "3": "نقاش المستخدم",
    "4": "ويكيبيديا",
    "5": "نقاش ويكيبيديا",
    "6": "ملف",
    "7": "نقاش الملف",
    "10": "قالب",
    "11": "نقاش القالب",
    "12": "مساعدة",
    "13": "نقاش المساعدة",
    "14": "تصنيف",
    "15": "نقاش التصنيف",
    "100": "بوابة",
    "101": "نقاش البوابة",
    "828": "وحدة",
    "829": "نقاش الوحدة",
    "2600": "موضوع",
    "1728": "فعالية",
    "1729": "نقاش الفعالية",
}
ns_text_tab = {}
# ---
for ns, title in ns_text_tab_1.items():
    ns_text_tab[int(ns)] = title
    ns_text_tab[str(ns)] = title


def GET_SQL():
    if "nosql" in sys.argv:
        return False
    # ---
    logger.debug(f"GET_SQL() == {can_use_sql_db[1]}")
    # ---
    return can_use_sql_db[1]


def Decode_bytes(x):
    if isinstance(x, bytes):
        x = x.decode("utf-8")
    return x


def make_labsdb_dbs_p(wiki):  # host, dbs_p = make_labsdb_dbs_p('ar')
    # ---
    if wiki.endswith("wiki"):
        wiki = wiki[:-4]
    # ---
    wiki = wiki.replace("-", "_")
    # ---
    databases = {
        "be-x-old": "be_x_old",
        "be_tarask": "be_x_old",
        "be-tarask": "be_x_old",
    }
    # ---
    wiki = databases.get(wiki, wiki)
    # ---
    wiki = f"{wiki}wiki"
    # ---
    dbs = wiki
    # ---
    host = f"{wiki}.analytics.db.svc.wikimedia.cloud"
    # ---
    dbs_p = f"{dbs}_p"
    # ---
    return host, dbs_p


def make_sql_connect(query, db="", host="", update=False, Return=False, return_dict=False):
    # ---
    rows = sql_qu.make_sql_connect(query, db=db, host=host, update=update, Return=Return, return_dict=return_dict)
    # ---
    return rows


def Make_sql_many_rows(queries, wiki="", printqua=False):
    rows = []
    # ---
    if not wiki:
        wiki = "enwiki"
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    logger.debug(f"API/sql_py Make_sql_many_rows wiki '{dbs_p}'")
    # ---
    if not GET_SQL():
        return rows
    # ---
    if printqua:
        logger.output(queries)
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    logger.debug(f'<<yellow>> API/sql_py Make_sql_many_rows 2 db:"{dbs_p}". {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, Return={})
    # ---
    final = tttime.time()
    # ---
    for raw in en_results:
        # if type(raw) == bytes:
        # raw = raw.decode("utf-8")
        raw2 = raw
        # if type(raw2) == list or type(raw2) == tuple :
        if isinstance(raw2, list):
            raw = [Decode_bytes(x) for x in raw2]
        rows.append(raw)
    # ---
    delta = int(final - start)
    logger.output(f'API/sql_py Make_sql_many_rows len(encats) = "{len(rows)}", in {delta} seconds')
    # ---
    return rows


def Make_sql_2_rows(queries, wiki="", printqua=False):
    """Retrieve and format SQL query results into a dictionary.

    This function connects to a specified database and executes the provided
    SQL queries. It processes the results by decoding the bytes and storing
    them in a dictionary, where the first column of the result set is used
    as the key and the second column as the value. The function also logs
    the execution time and can print the queries if specified.

    Args:
        queries (list): A list of SQL query strings to be executed.
        wiki (str?): The wiki database to connect to. Defaults to "enwiki".
        printqua (bool?): If True, prints the queries being executed. Defaults to False.

    Returns:
        dict: A dictionary containing the results of the SQL queries,
            with keys and values derived from the first and second columns of the
            result set, respectively.
    """

    # ---
    encats = {}
    if not wiki:
        wiki = "enwiki"
    # ---
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    logger.debug(f"API/sql_py Make_sql_many_rows wiki '{dbs_p}'")
    # ---
    if printqua:
        logger.output(queries)
    # ---
    if not GET_SQL():
        return encats
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    logger.debug(f'<<yellow>> API/sql_py Make_sql_2_rows 3 db:"{dbs_p}". {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, Return={})
    # ---
    final = tttime.time()
    # ---
    for raw in en_results:
        key = Decode_bytes(raw[0])
        value = Decode_bytes(raw[1])
        # ---
        encats[key] = value
    # ---
    delta = int(final - start)
    logger.output(f'API/sql_py Make_sql_2_rows len(results) = "{len(encats)}", in {delta} seconds')
    # ---
    return encats


def Make_sql_1_rows(queries, wiki="", printqua=False):
    encats = []
    # ---
    if not wiki:
        wiki = "enwiki"
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    logger.debug(f"API/sql_py Make_sql_many_rows wiki '{dbs_p}'")
    # ---
    if printqua:
        logger.output(queries)
    # ---
    if not GET_SQL():
        return encats
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    logger.debug(f'<<yellow>> API/sql_py Make_sql_1_rows 4 db:"{dbs_p}". {TTime}')
    # ---
    en_results = make_sql_connect(queries, host=host, db=dbs_p, Return=[])
    # ---
    final = tttime.time()
    # ---
    for raw in en_results:
        en = Decode_bytes(raw[0])
        encats.append(en)
    # ---
    delta = int(final - start)
    logger.output(f'API/sql_py Make_sql_2_rows len(results) = "{len(encats)}", in {delta} seconds')
    # ---
    return encats


def Make_sql_1_row(queries, wiki="", printqua=False):
    return Make_sql_1_rows(queries, wiki=wiki, printqua=printqua)


if __name__ == "__main__":
    # ---
    arqueries = """
        select CONCAT("تصنيف:",page_title), ll_title
        from page, templatelinks, langlinks
        where page_id = tl_from
        AND page_namespace = 14
        AND ll_lang = "en"
        AND ll_from = page_id
        AND tl_target_id = (SELECT lt_id FROM linktarget WHERE lt_namespace = 10 AND lt_title = "أشخاص_حسب_المهنة")
        """
    # ---
    ss = Make_sql_2_rows(arqueries, wiki="arwiki")
    logger.output(f"sql py test:: Make_sql_2_rows lenth:{len(ss)}")
