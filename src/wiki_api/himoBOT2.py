#!/usr/bin/python3
"""
"""
import functools
import re
import sys
from datetime import datetime as datetime2
from urllib.parse import urlencode

import requests

from ..helps import logger
from ..wd_bots.wd_api_bot import Get_Sitelinks_From_wikidata

Get_Redirect = {1: True} if "getred" in sys.argv else {1: False}

redirects_table = {}

Session = requests.Session()
# Session.headers.update(
#     {"User-Agent": "Himo bot/1.0 (https://himo.toolforge.org/; tools.himo@toolforge.org)"}
# )


def submitAPI(params, Code, family, printurl=False, type="get"):
    # ---
    if Code.endswith("wiki"):
        Code = Code[:-4]
    # ---
    sparql = ""
    # ---
    params["formatversion"] = 1
    params["utf8"] = 1
    params["format"] = "json"
    # ---
    if params.get("titles"):
        titles = params["titles"]
        if isinstance(titles, list):
            params["titles"] = "|".join(titles)
    # ---
    # himo API
    if family == "commons":
        family = "wikimedia"
    # ---
    mainurl = f"https://{Code}.{family}.org/w/api.php?"
    # ---
    encode_params = urlencode(params)
    # ---
    url = f"https://{Code}.{family}.org/w/api.php?{encode_params}"
    # ---
    if printurl or "printboturl" in sys.argv:
        url2 = url.replace("&format=json", "").replace("?format=json", "?")
        logger.debug(f"printboturl: {url2}")
    # ---
    json1 = {}
    try:
        r22 = Session.post(mainurl, data=params, timeout=10)

    except requests.exceptions.ReadTimeout:
        logger.debug(f"ReadTimeout: {mainurl}")

    except Exception as e:
        logger.warning(f"<<red>> Error submitting to API: {e}")

    try:
        json1 = r22.json()
    except Exception as e:
        logger.warning(f"<<red>> Error parsing API response: {e}")

    return json1


@functools.lru_cache(maxsize=1000)
def Get_Newpages(sitecode, family, limit="max", namespace="0", rcstart=""):
    # ---
    params = {
        "action": "query",
        "list": "recentchanges",
        # "rcdir": "newer",
        "rcnamespace": namespace,
        "rclimit": limit,
        "rctype": "new",
    }
    # ---
    if rcstart:
        params["rcstart"] = rcstart
    # ---
    json1 = submitAPI(params, sitecode, family)
    # ---
    Main_table = []
    # ---
    if not json1:
        return []
    # ---
    newp = json1.get("query", {}).get("recentchanges", {})
    Main_table = [x["title"] for x in newp]
    # ---
    _ccc = {
        "type": "new",
        "ns": 0,
        "title": "تشارلز مسيون ريمي",
        "pageid": 7004776,
        "revid": 41370093,
        "old_revid": 0,
        "rcid": 215347464,
        "timestamp": "2019-12-15T13:14:34Z",
    }
    # ---
    return Main_table


@functools.lru_cache(maxsize=1000)
def Get_page_info_from_wikipedia_new(
    sitecode,
    title,
    findtemp="",
    Workredirects=False,
    findiwlinks=False,
    getcach=False,
    Print=True,
    return_all_table=False,
    nohidden=False,
):
    # Note: getcach parameter is deprecated and ignored - caching is handled by @lru_cache decorator
    if Print:
        logger.debug(f'himoBOT2.Get_page_info_from_wikipedia_new for "{sitecode}:{title}"')
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
    if return_all_table:
        return table
    # ---
    if title in table:
        result = table[title]
    elif title2 in table:
        result = table[title2]
    # ---
    return result


@functools.lru_cache(maxsize=1000)
def Get_page_info_from_wikipedia(
    sitecode, title, findtemp="", Workredirects=False, findiwlinks=False, getcach=False, Print=False, nohidden=False
):
    return Get_page_info_from_wikipedia_new(
        sitecode,
        title,
        findtemp=findtemp,
        Workredirects=Workredirects,
        findiwlinks=findiwlinks,
        getcach=getcach,
        Print=Print,
        nohidden=nohidden,
    )


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


@functools.lru_cache(maxsize=1000)
def get_en_link_from_ar_text(text, title, site, sitetarget, getqid=False):
    # ---
    matches = [
        r"\{\{قيمة ويكي بيانات\/قالب تحقق\s*\|\s*(Q\d+)\s*\}\}",
        r"\{\{قيمة ويكي بيانات\/قالب تحقق\s*\|\s*id\s*\=\s*(Q\d+)\s*\}\}",
        r"\{\{سباق الدراجات\/صندوق [\s\w]+\s*\|\s*(Q\d+)\s*\}\}",
        r"\{\{Cycling race\/infobox\s*\|\s*(Q\d+)\s*\}\}",
        r"\{\{نتيجة سباق الدراجات\/بداية\s*\|\s*id\s*\=\s*(Q\d+)\s*\}\}",
    ]
    # ---
    qid = ""
    # ---
    if text:
        for ma in matches:
            if match := re.search(ma, text):
                qid = match.group(1)
                break
        # ---
        if getqid and qid:
            return qid
    # ---
    enpage = Get_Sitelinks_From_wikidata(site, title, return_main_table=True)
    # {"sitelinks": {"arwiki": "كريس فروم","enwiki": "Chris Froome","fiwiki": "Chris Froome"},"q": "Q319591"}
    # ---
    # logger.debug( json.dumps(enpage, indent=1, ensure_ascii=False) )
    # ---
    if not enpage:
        return ""
    # ---
    EngInterwiki = ""
    # ---
    qid = enpage.get("q", "")
    if getqid:
        return qid
    elif sitetarget:
        sitetarget2 = sitetarget
        if not sitetarget.endswith("wiki"):
            sitetarget2 += "wiki"
        # ---
        sitelinks = enpage.get("sitelinks", {})
        EngInterwiki = sitelinks.get(sitetarget) or sitelinks.get(sitetarget2) or ""
    # ---
    if EngInterwiki:
        logger.debug(f"<<lightblue>> himoBOT2.py, get_en_link_from_ar_text {EngInterwiki}")
    # ---
    return EngInterwiki
