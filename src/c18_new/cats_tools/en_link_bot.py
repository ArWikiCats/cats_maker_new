#!/usr/bin/python3
"""

from ..cats_tools.en_link_bot import english_page_link, en_title_for_arpage_cache

"""
import re

from ...b18_new.LCN_new import find_LCN, get_cache_L_C_N, set_cache_L_C_N
from ...wd_bots.wd_api_bot import Get_Sitelinks_from_qid, Get_Sitelinks_From_wikidata
from ..log import logger

En_title_for_ar_page = {}


def en_title_for_arpage_cache(key):
    return En_title_for_ar_page.get(key)


def english_page_link(link, firstsite_code, second_site_code, text=""):
    """
    This function is used to find the English page link for a given page on a Wikipedia-like site.

    Args:
        link (str): The title of the page to find the English link for.
        firstsite_code (str): The language code of the site that the page is on.
        second_site_code (str): The language code of the site to find the link for.
        text (str, optional): The text of the page. Defaults to "".

    Returns:
        str: The title of the English page that corresponds to the given page, or False if no such page exists.
    """
    tubb = (link, firstsite_code, second_site_code, "en_links")
    # ---
    if link in En_title_for_ar_page:
        logger.debug(f" En_title_for_ar_page ({link}).")
        return En_title_for_ar_page[link]
    # ---
    cac = get_cache_L_C_N(tubb)
    # ---
    if cac:
        logger.debug(f'>> _cache LCN tubb: "{link}":  = {second_site_code}:{cac}')
        return cac
    # ---
    # logger.debug(f'>> english_page_link type: "{str(type(link))}" {firstsite_code}:{link}'  )
    logger.debug(f">> english_page_link {firstsite_code}:{link}")
    link = link.replace("[[", "").replace("]]", "").replace("en:", "").replace("ar:", "")
    # ---
    link1 = link.replace("_", " ")
    # ---
    if text:
        logger.debug(">>sssss text: ")
        qid = ""
        # ttt = re.match( linr, text )
        # if ttt :
        # qid = ttt.group(1)
        # ---
        foos = re.compile(r"\{\{قيمة ويكي بيانات\/قالب تحقق\s*\|\s*(Q\d+)\s*\}\}").findall(text)
        foos2 = re.compile(r"\{\{قيمة ويكي بيانات\/قالب تحقق\s*\|\s*id\s*\=\s*(Q\d+)\s*\}\}").findall(text)
        match3 = re.search(r"\{\{سباق الدراجات\/صندوق معلومات\s*\|\s*(Q\d+)\s*\}\}", text)
        match4 = re.search(r"\{\{Cycling race\/infobox\s*\|\s*(Q\d+)\s*\}\}", text)
        # ---
        if foos:
            qid = foos[0]
        elif foos2:
            qid = foos2[0]
        elif match3:
            qid = match3.group(1)
        elif match4:
            qid = match4.group(1)

        # ---
        # ---
        if qid.startswith("Q"):
            logger.debug(f">> get qid from text: {qid} ")
            logger.debug(f">> qid {qid} ")
            Sitelinks = Get_Sitelinks_from_qid(ssite="", ids=qid)
            # ---
            if Sitelinks and "sitelinks" in Sitelinks:
                # ---
                Sitelinks = Sitelinks["sitelinks"]
                logger.debug(">> Sitelinks ")
                logger.debug(Sitelinks)
                # ---
                table = {}
                for x in Sitelinks:
                    x2 = re.sub(r"wiki$", "", x)
                    table[x2] = Sitelinks[x]
                # ---
                # sitewiki = second_site_code + "wiki"
                # logger.debug('>> sitewiki ' + sitewiki   )
                logger.debug(table)
                # ---
                if second_site_code in table:
                    result = table[second_site_code]
                    logger.debug(">> table: result : " + result)
                    if result.find("#") != -1:
                        set_cache_L_C_N(tubb, False)
                        return False
                    oppsite_tubb = (result, second_site_code, firstsite_code, "en_links")
                    set_cache_L_C_N(oppsite_tubb, link)
                    # ---
                    set_cache_L_C_N(tubb, result)
                    # logger.debug( f" table ({enn})." )
                    return result
            # ---
            logger.debug(">> Sitelinks ")
            logger.debug(Sitelinks)
    # ---
    # link = link.replace(' ', '_')
    sasa = find_LCN(link, prop="categories|langlinks", first_site_code=firstsite_code)
    # sasa = {}
    logger.debug(sasa)
    results = ""
    # ---
    if sasa and link1 in sasa:
        if "langlinks" in sasa[link1]:
            results = sasa[link1]["langlinks"].get(second_site_code, "")
            ar_to_match = sasa[link1]["langlinks"].get(firstsite_code, "")
            # if second_site_code in sasa[link1]['langlinks']:
            # result = sasa[link1]['langlinks'][second_site_code]
            # ---
            if ar_to_match and ar_to_match != link1:
                logger.output(f">> ar_to_match:({ar_to_match}) != ar:({link1}).")
                return False
        # ---
    if text and results == "":
        match = re.search(r"\[\[en:(Category\:.+?)\]\]", text)
        if match:
            logger.output(f"FindEngInArwiki: {match.group(1)}.")
            results = match.group(1)
    # ---
    Sitelinks2 = {}
    # ---
    if results:
        # ---
        tavr = Get_Sitelinks_From_wikidata("enwiki", results)
        # ---
        if tavr and "sitelinks" in tavr:
            # ---
            Sitelinks2 = tavr["sitelinks"]
    else:
        # ---
        tavr = Get_Sitelinks_From_wikidata(firstsite_code + "wiki", link)
        # ---
        if tavr and "sitelinks" in tavr:
            # ---
            Sitelinks2 = tavr["sitelinks"]
            logger.output("sitelinks 2020.")
    # ---
    if Sitelinks2 != {}:
        table = {}
        for x in Sitelinks2:
            x2 = re.sub(r"wiki$", "", x)
            table[x2] = Sitelinks2[x]
        # ---
        if firstsite_code in table:
            link1_other = table[firstsite_code]
            if link1 != link1_other:
                logger.output(f"link1 ({link1}) != link1_other ({link1_other}).")
                set_cache_L_C_N(tubb, False)
                return False
        # ---
        oppsite_tubb = (results, second_site_code, firstsite_code, "en_links")
        set_cache_L_C_N(oppsite_tubb, link)
        set_cache_L_C_N(tubb, results)
        logger.output(f" ({results}).")
        return results
    # ---
    set_cache_L_C_N(tubb, False)
    # ---
    return False
