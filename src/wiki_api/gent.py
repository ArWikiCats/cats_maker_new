#!/usr/bin/python3
"""
"""
import sys

from ..helps import logger
from . import himoBOT2

try:
    import pywikibot
    from pywikibot import pagegenerators
except BaseException:
    pywikibot = False
    logger.exception("gent.py import pywikibot error")


def Get_Newpages(sitecode, family, limit="max", namespace="0", user="", listonly=False):
    # ---
    if namespace.find(",") != -1:
        namespace = namespace.split(",")
    # ---
    logger.output(f"gent.py Get_Newpages namespace: {str(namespace)}")
    # ---
    params = {
        "action": "query",
        "format": "json",
        "list": "recentchanges",
        # "rcdir": "newer",
        "rcnamespace": namespace,
        "rclimit": limit,
        "utf8": 1,
        "rctype": "new",
        "rcuser": user,
    }
    # ---
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    # ---
    if family == "commons":
        family = "wikimedia"
    # ---
    # mainurl = f"https://{sitecode}.{family}.org/w/api.php?"
    # ---
    json1 = {}
    # ---
    site = pywikibot.Site(sitecode, family)
    # ---
    try:
        json1 = pywikibot.data.api.Request(site=site, parameters=params).submit()
    except Exception as e:
        logger.exception(e)
        return []
    # ---
    # Main_table = []
    # ---
    if json1:
        newp = json1.get("query", {}).get("recentchanges", {})
        # Main_table = [ x[ "title" ] for x in newp ]
        for x in newp:
            if listonly:
                yield x["title"]
            else:
                yield pywikibot.Page(site, x["title"])
    # ---
    # logger.output("gent.py lenth of Main_table: %d" % len(Main_table))
    # ---
    # return Main_table


def getusernewpages(listonly):
    # python3 core8/pwb.py gent -mynewpages:10 -ns:0
    usernewpages = ""
    ns = ""
    limit = 100
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg.startswith("-"):
            arg = arg[1:]
        if arg == "usernewpages":
            usernewpages = value
        if arg == "mynewpages":
            usernewpages = "Mr. Ibrahem"
            # ns = "0"
            if value:
                limit = int(value)
        if arg == "limit":
            limit = int(value)
        elif arg == "ns":
            ns = value
    # ---
    if usernewpages and ns == "":
        ns = "0"
    # ---
    lista = []
    # ---
    if usernewpages:
        family = "wikipedia"
        lang = "ar"
        lista = Get_Newpages(lang, family, limit=limit, namespace=ns, user=usernewpages, listonly=listonly)
        # generator = site.recentchanges(namespaces=ns, user=usernewpages, patrolled=False, total=limit, changetype = "edit")
        # for page in generator:
        # print(page['title'])
        # yield page
    # ---
    return lista


def do_title(generator):
    # [page.title(as_link=False) for page in generator]
    for page in generator:
        yield page.title(as_link=False)


def get_gent(listonly=False, *args):
    # ---
    options = {}
    # ---
    # print(sys.argv)
    # ---
    genFactory = pagegenerators.GeneratorFactory()
    # ---
    for arge in pywikibot.handle_args(args):
        arg, sep, value = arge.partition(":")
        # ---
        option = arg[1:]
        # ---
        if option in ("summary", "text"):
            if not value:
                pywikibot.input(f"Please enter a value for {arg}")
            options[option] = value
        else:
            options[option] = True
            # ---
            genFactory.handle_arg(arge)
    # ---
    generator = genFactory.getCombinedGenerator()
    # ---
    if generator and listonly:
        # return [page.title(as_link=False) for page in generator]
        return do_title(generator)
    # ---
    if not generator:
        # ---
        for arg in sys.argv:
            arg, _, value = arg.partition(":")
            # ---
            if arg == "-newpages2":
                generator = himoBOT2.Get_Newpages_arwiki(limit=value, namespace="0", listonly=listonly)
    # ---
    if not generator:
        logger.output("<<lightred>> No pages to work on")
        generator = getusernewpages(listonly)
    # ---
    return generator


if __name__ == "__main__":
    # ---
    generator = get_gent(listonly=True)
    # ---
    for numb, title in enumerate(generator, start=1):
        logger.output(f"<<lightgreen>> {numb} <<lightblue>> {title}")
    # ---
    logger.output("<<lightred>> Done")
    # ---
