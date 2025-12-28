#!/usr/bin/python3
"""
"""
import datetime
import functools
import json
import re
import sys
from datetime import datetime as datetime2
from datetime import timedelta
from urllib.parse import urlencode

import requests

from ..helps import logger
from ..wd_api_bot import Get_Sitelinks_From_wikidata

# ---
menet = datetime2.now().strftime("%Y-%b-%d  %H:%M:%S")
Get_Redirect = {1: True} if "getred" in sys.argv else {1: False}
# ---
redirects_table = {}
# ---
Session = requests.Session()


def load_SPARQL_New(sparql):
    try:
        return json.loads(sparql)
    except Exception as e:
        logger.warning(f"load_SPARQL_New error: {e}")
        return {}


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
        json1 = r22.json()

    except requests.exceptions.ReadTimeout:
        logger.debug(f"ReadTimeout: {mainurl}")

    except Exception as e:
        logger.warning(e)
        json1 = {}
    # ---
    return json1


@functools.lru_cache(maxsize=1000)
def Get_template_pages(title, namespace="*", limit="max", sitecode=""):
    # ---
    logger.debug(f'Get_template_pages for template:"{title}", limit:"{limit}",namespace:"{namespace}"')
    # ---
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    # ---
    params = {
        "action": "query",
        "format": "json",
        "prop": "info",
        "titles": title,
        "generator": "transcludedin",
        "gtinamespace": namespace,
        "gtilimit": limit,
    }
    # ---
    Main_table = []
    gticontinue = "x"
    # ---
    while gticontinue != "":
        # ---
        if gticontinue != "x":
            params["gticontinue"] = gticontinue
        # ---
        Pr = gticontinue == "x"
        # ---
        json1 = submitAPI(params, sitecode, "wikipedia", printurl=Pr)
        # ---
        if not json1:
            break
        # ---
        gticontinue = json1.get("continue", {}).get("gticontinue", "")
        # ---
        pages = json1.get("query", {}).get("pages", {})
        # ---
        Main_table.extend(tab["title"] for _, tab in pages.items())
        # ---
        logger.debug(f"len of Main_table:{len(Main_table)}.")
    # ---
    logger.debug(f"mdwiki_api.py Get_template_pages : find {len(Main_table)} pages.")
    # ---
    return Main_table


# @functools.lru_cache(maxsize=1000)
def Find_pages_exists_or_not(liste, sitecode="ar", family="wikipedia", return_json=False):
    # ---
    params = {
        "action": "query",
        "titles": "|".join(liste),
        # "redirects": 0,
        # "normalize": 1,
    }
    # ---
    table = {}
    # ---
    json1 = submitAPI(params, sitecode, family)
    # ---
    if not json1:
        return table
    # ---
    if return_json:
        return json1
    # ---
    query = json1.get("query", {})
    normalz = query.get("normalized", {})
    normalized = {red["to"]: red["from"] for red in normalz}
    # ---
    query_pages = query.get("pages", {})
    for _, kk in query_pages.items():
        tit = kk.get("title", "")
        if tit:
            tit = normalized.get(tit, tit)
            # ---
            table[tit] = True
            # ---
            if "missing" in kk:
                table[tit] = False
        # ---
    return table


@functools.lru_cache(maxsize=1000)
def get_redirects(title, sitecode, family):
    # ---
    _result = {
        "batchcomplete": "",
        "query": {
            "pages": {
                "1369": {"pageid": 1369, "ns": 0, "title": "اليمن", "redirects": [{"ns": 0, "title": "جمهورية يمنية"}]}
            }
        },
        "limits": {"redirects": 500},
    }
    # ---
    if isinstance(title, list):
        title = "|".join(title)
    # ---
    params = {"action": "query", "prop": "redirects", "titles": title, "rdprop": "pageid|title", "rdlimit": "max"}
    # ---
    json1 = submitAPI(params, sitecode, family)
    # ---
    pages = json1.get("query", {}).get("pages", {})
    # ---
    liste = []
    # ---
    for _, x in pages.items():
        title = x.get("title", "")
        redirects = x.get("redirects", [])
        if x["title"] == title:
            liste.extend(io["title"] for io in redirects)
    # ---
    return liste


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
def wordcount(title, ns="", sitecode=""):
    # ---
    if not sitecode:
        sitecode = "ar"
    # ---
    # logger.debug(' wordcount %s:' % title )
    srlimit = "30"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": title,
        "srlimit": srlimit,
        # "token": SS["r3_token"]
    }
    # ---
    if not ns:
        ns = 0
    params["srnamespace"] = ns
    # ---
    json1 = submitAPI(params, "ar", "wikipedia")
    # ---
    if not json1:
        return 0
    # ---
    search = json1.get("query", {}).get("search", [])
    # ---
    for pag in search:
        tit = pag["title"]
        if tit == title:
            return pag["wordcount"]
    # ---
    return 0


@functools.lru_cache(maxsize=1000)
def Get_iwlinks(sitecode, title):
    # ---
    logger.debug(f'himoBOT2.Get_iwlinks for "{sitecode}:{title}"')
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    # ---
    _sitewiki = f"{sitecode}wiki"
    # ---
    table = {}
    # ---
    params = {
        "action": "query",
        "titles": title,
        "lllimit": "max",
        "prop": "iwlinks",
    }
    # ---
    json1 = submitAPI(params, sitecode, "wikipedia")
    if not json1:
        return table
    # ---
    pages = json1.get("query", {}).get("pages", {})
    for _pageid, tat in pages.items():
        table = {x["prefix"]: x["*"] for x in tat.get("iwlinks", [])}
        break
    # ---
    logger.debug(table)
    # ---
    logger.debug(f'himoBOT2.Get_iwlinks find "{len(table)}" in table')
    # ---
    return table


@functools.lru_cache(maxsize=1000)
def Get_langlinks(sitecode, title, targtsitecode="", Workredirects=False):
    # ---
    logger.debug(f'himoBOT2.Get_langlinks for "{sitecode}:{title}"')
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    # ---
    _sitewiki = f"{sitecode}wiki"
    # ---
    table = {}
    # ---
    """tabes = {
        "batchcomplete": "",
        "query": {
            "normalized": [{
                "from": "Category:Sportspeople_by_nationality",
                "to": "Category:Sportspeople by nationality"
            }],
            "pages": {
                "1755616": {
                    "pageid": 1755616,
                    "ns": 14,
                    "title": "Category:Sportspeople by nationality",
                    "langlinks": [{
                        "lang": "ar",
                        "*": "تصنيف:رياضيون ورياضيات حسب الجنسية"
                    }]
                }
            }
        }
    }"""
    # ---
    params = {
        "action": "query",
        "titles": title,
        "lllimit": "max",
        "prop": "langlinks",
        # "normalize": 1,
    }
    # ---
    if targtsitecode.endswith("wiki"):
        targtsitecode = targtsitecode[:-4]
    if targtsitecode:
        params["lllang"] = targtsitecode
    if Workredirects or Get_Redirect[1]:
        params["redirects"] = 1
    # ---
    json1 = submitAPI(params, sitecode, "wikipedia")
    if not json1:
        return table
    # ---
    query_pages = json1.get("query", {}).get("pages", {})
    for page in query_pages:
        kk = query_pages[page]
        # ---
        table = {x["lang"]: x["*"] for x in kk.get("langlinks", [])}
    # ---
    logger.debug(table)
    # ---
    return table


@functools.lru_cache(maxsize=1000)
def Get_langlinks_for_list(sitecode, title, targtsitecode="", numbes=50):
    # ---
    logger.debug(f'himoBOT2.Get_langlinks_for_list for "{sitecode}:{len(title)} pages"')
    # ---
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    # ---
    if targtsitecode.endswith("wiki"):
        targtsitecode = targtsitecode[:-4]
    # ---
    _sitewiki = f"{sitecode}wiki"
    # ---
    # new_ar_list = []
    # DDone = []
    # ---
    if not isinstance(title, list):
        title = [title]
    # ---
    if sitecode != "ar":
        numbes = 200
    # ---
    find_targtsitecode = 0
    normalized = {}
    table = {}
    # ---
    for i in range(0, len(title), numbes):
        titles_1 = title[i : i + numbes]
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "langlinks",
            "titles": "|".join(titles_1),
            # "redirects":1,
            "lllimit": "max",
            "utf8": 1,
            # "normalize": 1
        }
        # ---
        if targtsitecode:
            params["lllang"] = targtsitecode
            logger.debug(f'params["lllang"] = {targtsitecode}')
        # ---
        json1 = submitAPI(params, sitecode, "wikipedia")
        # ---
        if not json1:
            continue
        # ---
        logger.debug(json1)
        # ---
        norma = json1.get("query", {}).get("normalized", {})
        for red in norma:
            normalized[red["to"]] = red["from"]
        # ---
        query_pages = json1.get("query", {}).get("pages", {})
        for _page, kk in query_pages.items():
            if "title" in kk:
                titlle = kk.get("title", "")
                titlle = normalized.get(titlle, titlle)
                # ---
                table[titlle] = {}
                # ---
                for lang in kk.get("langlinks", []):
                    table[titlle][lang["lang"]] = lang["*"]
                    # ---
                    if lang["lang"] == targtsitecode:
                        find_targtsitecode += 1
    # ---
    logger.debug(table)
    # ---
    logger.debug(
        f'himoBOT2.Get_langlinks_for_list find "{len(table)}" in table,find_targtsitecode:{targtsitecode}:{find_targtsitecode}'
    )
    # ---
    return table


@functools.lru_cache(maxsize=1000)
def Get_page_Categories(sitecode, title, Workredirects=False, with_hidden=True):
    # ---
    logger.debug(f'himoBOT2.Get_page_Categories for "{sitecode}:{title}"')
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    langcode = sitecode if sitecode else "ar"
    # ---
    params = {
        "action": "query",
        "titles": title,
        # "redirects":1,
        "prop": "categories",
        "clprop": "sortkey|hidden",
        # "clshow": "!hidden",
        # "normalize": 1,
        "cllimit": "max",
    }
    # ---
    if not with_hidden:
        params["clshow"] = "!hidden"
    # ---
    if Workredirects or Get_Redirect[1]:
        params["redirects"] = 1
    # ---
    json1 = submitAPI(params, langcode, "wikipedia")
    # ---
    if not json1:
        return {}
    # ---
    Tables = {}
    # ---
    pages = json1.get("query", {}).get("pages", {})
    # ---
    for _xo, tayo in pages.items():
        # ---
        titley = ""
        # ---
        if "title" in tayo:
            titley = tayo["title"]
        # ---
        Tables[titley] = tayo
        # ---
        Tables[titley]["categories"] = [x["title"] for x in tayo.get("categories", [])]
        # ---
        if "missing" in tayo:
            logger.debug(f"<<lightred>> page:{titley} is missing")
            Tables[titley] = {"missing": True}
    # ---
    if len(Tables) == 1:
        for value in Tables.values():
            return value
    # ---
    return Tables


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


def Search(title, lang="", family="", ns="", offset="", srlimit="max", RETURN_dict=False, addparams={}):
    # ---
    nsvalue = ns
    # ---
    if not nsvalue:
        for arg in sys.argv:
            arg, _, value = arg.partition(":")
            # ---
            if arg == "-ns":
                nsvalue = value
    # ---
    if not lang:
        lang = "www"
        family = "wikidata"
    # ---
    srlimit = "max"
    # ---
    params = {
        "action": "query",
        "list": "search",
        "srsearch": title,
        "srnamespace": 0,
        "srlimit": srlimit,
        # "token": SS["r3_token"]
    }
    # ---
    for x, d in addparams.items():
        params[x] = d
    # ---
    if nsvalue:
        params["srnamespace"] = nsvalue
    if offset:
        params["sroffset"] = offset
    # ---
    json1 = submitAPI(params, lang, family)
    # ---
    Lidy = []
    # ---
    if not json1:
        return Lidy
    # ---
    search = json1.get("query", {}).get("search", [])
    for pag in search:
        if RETURN_dict:
            Lidy.append(pag)
        else:
            Lidy.append(pag["title"])
    # ---
    return Lidy


@functools.lru_cache(maxsize=1000)
def Get_section_numbers_table(title, sitecode):
    # ---
    logger.debug(f"**Get_section_numbers_table: for {sitecode}:{title} ")
    # ---
    params = {
        "action": "parse",
        "page": title,
        "prop": "sections",
        # "section": level,
        "utf8": 1,
    }
    langcode = sitecode if sitecode else "ar"
    # ---
    json1 = submitAPI(params, langcode, "wikipedia")
    # ---
    levels = {}
    # ---
    if not json1:
        return levels
    # ---
    sections = json1.get("parse", {}).get("sections", {})
    for x in sections:
        # levels[x["line"]] = x["index"]
        lline = x["line"].strip().lower()
        levels[lline] = x
    # ---
    return levels


@functools.lru_cache(maxsize=1000)
def Get_section(title, sitecode, level):
    section_name = ""
    section_text = ""
    # ---
    level = str(level)
    # ---
    params = {"action": "parse", "page": title, "prop": "sections|wikitext", "section": level, "utf8": 1}
    langcode = sitecode if sitecode else "ar"
    # ---
    json1 = submitAPI(params, langcode, "wikipedia")
    # ---
    if not json1:
        return section_name, section_text
    # ---
    parse = json1.get("parse", {})
    sections = parse.get("sections", [])
    if level != "0" and len(sections) == 1:
        section_name = sections[0]["line"]
    # ---
    section_text = parse.get("wikitext", {}).get("*", "")
    # ---
    return section_name, section_text


@functools.lru_cache(maxsize=1000)
def Get_section_by_sectname_or_level(title, sitecode, section_name, level=""):
    # section_name = ""
    section_text = ""
    # ---
    if section_name:
        section_name = section_name.lower().strip()
    # ---
    section_level = ""
    # ---
    if level:
        section_level = level
    else:
        levelss = Get_section_numbers_table(title, sitecode)
        if section_name and section_name in levelss:
            section_level = levelss[section_name]["index"]
        else:
            logger.debug(f"Get_section_by_sectname_or_level: no section with name {section_name}")
            logger.debug(json.dumps(levelss, indent=2, ensure_ascii=False))
    # ---
    _sec_name, section_text = Get_section(title, sitecode, section_level)
    # ---
    return section_text


@functools.lru_cache(maxsize=1000)
def Getpageassessments(title, site, find_redirects=False, pasubprojects=0):
    logger.debug(f'himoBOT2.Getpageassessments for "{site}:{title}"')
    # ---
    stub_title = "قالب:صندوق_رسالة_بذرة"  # "قالب:بذرة"
    # ---
    params = {
        "action": "query",
        "prop": "pageassessments|templates",
        "redirects": 1,
        "titles": title,
        "palimit": "max",
        "tlnamespace": "10",
        "tllimit": "max",
        "tltemplates": stub_title,
    }  # للتأكد إذا كانت المقالة تستخدم قالب بذرة
    if pasubprojects == 1:
        params["pasubprojects"] = 1
    langcode = site if site else "ar"
    # ---
    json1 = submitAPI(params, langcode, "wikipedia")
    # ---
    Tables = {
        # "stub" : False,
    }
    # ---
    if not json1:
        return Tables
    # ---
    query = json1.get("query", {})
    pages = query.get("pages", {})
    # ---
    Tables[title] = {}
    # ---
    for _page_id, tayo in pages.items():
        # ---
        titley = tayo.get("title", "")
        # ---
        Tables[titley] = tayo
        # ---
        if "missing" in tayo:
            logger.debug(f"<<lightred>> page:{titley} is missing")
            Tables[titley]["missing"] = True
        # ---
        # "templates": [{"ns": 10,"title": "قالب:شريط بوابات"}]
        templates = tayo.get("templates", {})
        for temp in templates:
            # ---
            temptitle = temp.get("title", "").replace("_", " ")
            # ---
            if temptitle in ["قالب:بذرة", "قالب:صندوق رسالة بذرة"]:
                Tables[titley]["stub"] = True
                break
        # ---
        if find_redirects and query.get("redirects"):
            for red in query.get("redirects"):
                if title == red["from"]:
                    if title not in Tables:
                        Tables[title] = {}
                    Tables[title]["is_redirect"] = True
    # ---
    return Tables


@functools.lru_cache(maxsize=1000)
def Parse_Text(line, title, sitecode):
    # ---
    textnew = ""
    # ---
    params = {
        "action": "parse",
        "prop": "wikitext",
        "text": line,
        "title": title,
        "pst": 1,
        "contentmodel": "wikitext",
        "utf8": 1,
    }
    json1 = submitAPI(params, sitecode, "wikipedia")
    # ---
    if not json1:
        return ""
    # ---
    textnew = json1.get("parse", {}).get("psttext", {}).get("*", "")
    # ---
    if not textnew:
        logger.debug('Parse_Text: textnew == ""')
    # ---
    return textnew


@functools.lru_cache(maxsize=1000)
def get_text_html(title, sitecode):
    # ---
    textnew = ""
    # ---
    params = {
        "action": "parse",
        "format": "json",
        "page": title,
        "prop": "text",
        # "pst": 1,
        "utf8": 1,
        "formatversion": "1",
    }
    # ---
    json1 = submitAPI(params, sitecode, "wikipedia")
    # ---
    if not json1:
        return ""
    # ---
    textnew = json1.get("parse", {}).get("text", {}).get("*", "")
    # ---
    if not textnew:
        logger.debug('Parse_Text: textnew == ""')
    # ---
    return textnew


@functools.lru_cache(maxsize=1000)
def GetarPageText(title, sitecode="", redirects=False, family="wikipedia"):
    # ---
    params = {
        "action": "parse",
        "prop": "wikitext|sections",
        "page": title,
        # "normalize": 1,
    }
    # ---
    if redirects:
        params["redirects"] = 1
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    langcode = sitecode if sitecode else "ar"
    # ---
    json1 = submitAPI(params, langcode, family)
    # ---
    text = ""
    if not json1:
        return text
    # ---
    text = json1.get("parse", {}).get("wikitext", {}).get("*", "")
    # ---
    if not text:
        logger.debug(f'page {sitecode}:{title} text == "".')
    # ---
    return text


@functools.lru_cache(maxsize=1000)
def Get_PageText_with_timestamp(title, sitecode="", redirects=False, family="wikipedia", get_user=False):
    # ---
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "timestamp|content|user",
        "rvslots": "*",
    }
    # ---
    if redirects:
        params["redirects"] = 1
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    langcode = sitecode if sitecode else "ar"
    # ---
    timestamp = ""
    text = ""
    user = ""
    # ---
    json1 = submitAPI(params, langcode, family)
    # ---
    if not json1:
        return (timestamp, text, user) if get_user else (timestamp, text)
    # ---
    pages = json1.get("query", {}).get("pages", {})
    # ---
    for x in pages:
        content = pages[x].get("revisions", [])
        for o in content:
            user = o.get("user", "")
            timestamp = o.get("timestamp", "")
            text = o.get("slots", {}).get("main", {}).get("*", "")
            break
    # ---
    if not text:
        logger.debug(f'page {sitecode}:{title} text == "".')
    # ---
    return (timestamp, text, user) if get_user else (timestamp, text)


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


@functools.lru_cache(maxsize=1000)
def Get_Newpages_arwiki(limit="max", namespace="0", listonly=False):
    """
    # ---
    newpages = 'max'
    # ---
    for arg in sys.argv:
        arg, sep, value=arg.partition(':')
        # ---
        if arg == "-newpages2" :
            newpages = value
            generator = Get_Newpages_arwiki( limit = newpages, namespace="0" )
    # ---"""
    # Rcstart = "2020-01-14T1:52:58.000Z"
    # Rcstart = "2020-01-13T22:52:58.000Z"
    x = datetime.datetime.utcnow()
    print(f"utcnow:{x.strftime('%Y-%m-%dT%H:%M:%S:00.000Z')}")
    # ---
    # hour = int( x.strftime("%H") ) - 3
    # day = int( x.strftime("%d") )
    # ---
    # if hour < 0 :
    # hour = hour + 24
    # day = day - 1
    # ---
    # hour = str(hour)
    # if len(hour) == 1 :
    # hour = "0" + hour
    # ---
    # Rcstart = "%s-%s-%sT%s:%s:%s:00.000Z" % ( x.strftime("%Y"), x.strftime("%m"), str(day), hour, x.strftime("%M"), x.strftime("%S") )
    # print("before:%s" % Rcstart )
    # ---
    dd = datetime.datetime.utcnow() - timedelta(hours=3)
    # Rcstart = dd.strftime('%Y-%m-%dT%H:%M:%S:00.000Z')
    Rcstart = dd.strftime("%Y-%m-%dT%H:%M:00.000Z")
    print(f"Rcstart:{Rcstart}")
    # ---
    # Rcstart = "%sT%s:%s:00.000Z" % ( x.strftime("%Y-%m-%d"), hour, x.strftime("%M") )
    # print(Rcstart)
    # ---
    nnn = Get_Newpages("ar", "wikipedia", limit=limit, namespace=namespace, rcstart=Rcstart)
    # ---
    return nnn
