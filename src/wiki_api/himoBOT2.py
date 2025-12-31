#!/usr/bin/python3
"""
"""
import functools
import re
import sys
from ..helps import logger
from .api_requests import submitAPI

Get_Redirect = {1: True} if "getred" in sys.argv else {1: False}
redirects_table = {}


@functools.lru_cache(maxsize=1000)
def get_page_info_from_wikipedia(
    sitecode,
    title,
    findtemp="",
    Workredirects=False,
    findiwlinks=False,
    Print=True,
    nohidden=False,
):
    if Print:
        logger.debug(f'himoBOT2.get_page_info_from_wikipedia for "{sitecode}:{title}"')
    # ---
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    # ---
    title = title.strip()
    # ---
    params = {
        "action": "query",
        "titles": title,
        "redirects": 1,
        "prop": "langlinks|pageprops|templates|linkshere|flagged|categories",
        "ppprop": "wikibase_item",
        # "normalize": 1,
        "tlnamespace": "10",
        "tllimit": "max",
    }
    # ---Template:Category redirect
    if nohidden:
        params["clshow"] = "!hidden"
    if findiwlinks:
        params["prop"] += "|iwlinks"
    if findtemp:
        params["tltemplates"] = findtemp  # للتأكد إذا كانت المقالة تستخدم قالب بذرة
    if Workredirects or Get_Redirect[1]:
        params["redirects"] = 1
    # ---
    # purge_ar(title, sitecode)
    # ---
    tata = {
        "isRedirectPage": False,
        "exists": True,
        "from": "",
        "to": "",
        "title": "",
        "ns": "",
        "pageid": "",
        "countlinkshere": 0,
        "linkshere": {},
        "langlinks": {},
        "templates": {},
        "wikibase_item": "",
        "q": "",
    }
    table = {}
    # ---
    json1 = submitAPI(params, sitecode, "wikipedia")
    # ---
    if not json1:
        return {}
    # ---
    title2 = title
    # ---
    # {'batchcomplete': '', 'query': {'pages': {'361534': {'pageid': 361534, 'ns': 4, 'title': 'ويكيبيديا:ملعب'}}}}
    query = json1.get("query", {})
    if not query:
        return {}
    # ---
    for _ in query.get("normalized", []):
        for xio in query["normalized"]:
            if xio["from"] == title:
                title2 = xio["to"]
    # ---
    for red in query.get("redirects", []):
        if Print:
            logger.debug(f"page is redirects to : \"{red['to']}\"")
        redirects_table[red["from"]] = red["to"]
        # ---
        table2 = dict(tata)
        table2["isRedirectPage"] = True
        table2["exists"] = False
        table2["from"] = red["from"]
        table2["to"] = red["to"]
        table2["title"] = red["from"]
        table[red["from"]] = table2
    # ---
    pages = query.get("pages", {})
    # ---
    numb = 0
    numb = 1
    # ---
    for id2, kk in pages.items():
        # ---
        titlle = kk.get("title", "")
        table[titlle] = dict(tata)
        table[titlle]["title"] = titlle
        # ---
        if id2 == "-1":
            if Print:
                logger.debug(f'a {numb}/{len(pages)} titlle:{sitecode}:{titlle}, id :"{id2}"')
            table[titlle]["exists"] = False
            continue
        # ---
        if titlle in redirects_table:
            table[titlle]["isRedirectPage"] = True
            table[titlle]["from"] = titlle
            table[titlle]["to"] = redirects_table[titlle]
        # ---
        table[titlle]["ns"] = kk.get("ns", "")
        if "missing" in kk:
            table[titlle]["exists"] = False
        # ---
        # table[titlle]["langlinks"] = make_langlinks(kk)
        table[titlle]["langlinks"] = {x["lang"]: x["*"] for x in kk.get("langlinks", [])}
        # ---
        table[titlle]["flagged"] = kk.get("flagged", False) is not False
        # ---
        table[titlle]["pageid"] = kk.get("pageid", "")
        # ---
        q_q = kk.get("pageprops", {}).get("wikibase_item", "")
        table[titlle]["wikibase_item"] = q_q
        table[titlle]["q"] = q_q
        linkshere = {x["title"]: x for x in kk.get("linkshere", []) if x["ns"] in [0, 10]}
        table[titlle]["linkshere"] = linkshere
        table[titlle]["countlinkshere"] = len(linkshere.keys())
        # ---
        table[titlle]["categories"] = [x["title"] for x in kk.get("categories", [])]
        # ---
        table[titlle]["templates"] = [x["title"] for x in kk.get("templates", [])]
        # ---
        table[titlle]["iwlinks"] = {x["prefix"]: x["*"] for x in kk.get("iwlinks", [])}
    # ---
    result = table
    # ---
    if title in table:
        result = table[title]
    elif title2 in table:
        result = table[title2]
    # ---
    return result


@functools.lru_cache(maxsize=1000)
def GetPagelinks(title, sitecode=""):
    langcode = sitecode if sitecode else "ar"
    # ---
    _result = {
        "parse": {
            "title": "وحدة:Wikidata/تتبع",
            "pageid": 3196192,
            "links": [{"ns": 828, "*": "وحدة:Wikidata/تتبع/طباعة"}, {"ns": 828, "exists": "", "*": "وحدة:Wikidata2"}],
        }
    }
    # ---
    params = {
        "action": "parse",
        "prop": "links",
        "page": title,
        # "redirects":1,
        # "normalize": 1,
    }
    json1 = submitAPI(params, langcode, "wikipedia")
    # ---
    tab = {}
    # ---
    if not json1:
        return tab
    # ---
    parse = json1.get("parse", {})
    # title = parse.get("title", "" )
    # ---
    for cx in parse.get("links", []):
        ti = cx["*"]
        # tab[ti] = cx
        tab[ti] = {x: va for x, va in cx.items() if x != "*"}
    # ---
    logger.debug(tab)
    # ---
    return tab
