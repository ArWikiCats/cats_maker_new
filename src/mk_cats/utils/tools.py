#!/usr/bin/python3

import json
import re
import time
import urllib
import urllib.parse

from ...helps import logger


def loads_json(sparql):
    if not sparql or sparql.strip() == "":
        logger.output('API/tools.py loads_json sparql == "" ')
        return {}
    # ---
    if "java.util.concurrent" in str(sparql):
        logger.output("API/tools.py loads_json java.util.concurrent ")
        return {}
    # ---
    try:
        return json.loads(sparql)
    except json.decoder.JSONDecodeError:
        logger.warning("", text="API/tools.py json.decoder.JSONDecodeError ")
    except Exception as e:
        logger.warning(e, text="API/tools.py loads_json json.loads(sparql) is False ")
        # strip sparql
        if sparql.find("<!DOCTYPE html>") == -1:
            if len(sparql) > 1000:
                sparql = sparql[:1000]
            logger.output(sparql)
        logger.output("API/tools.py loads_json json.loads(sparql) is False ")
        return {}
    return {}


def quoteurl(fao):
    endash = False
    # ---
    # url2 = urllib.parse.quote_plus(url)
    # ---
    if fao.find("–") != -1:
        endash = True
        fao = fao.replace("–", "ioioioioio")
    # ---
    try:
        fao = urllib.parse.quote(fao)
    except Exception as e:
        logger.warning(e, text=None)
    # ---
    if endash:
        fao = fao.replace("ioioioioio", "%E2%80%93")
    # ---
    return fao


def new_split_dict_or_list(cat_m2, numb=100):
    # ---
    List = {}
    # ---
    start = time.time()
    final = time.time()
    # ---
    for i in range(0, len(cat_m2), numb):
        # ---
        if isinstance(cat_m2, dict):
            group = dict(list(cat_m2.items())[i : i + numb])
        else:
            group = cat_m2[i : i + numb]
        # ---
        List[i] = group
    # ---
    final = time.time()
    delta = int(final - start)
    # ---
    logger.output(f"new_split_dict_or_list, split {len(List)} list in {delta} seconds")
    # ---
    return List


def makejson(property, numeric):
    # ---
    if numeric:
        numeric = re.sub(r"Q", "", numeric)
        Q = f"Q{numeric}"
        return {
            "mainsnak": {
                "snaktype": "value",
                "property": property,
                "datavalue": {
                    "value": {
                        "entity-type": "item",
                        "numeric-id": numeric,
                        "id": Q,
                    },
                    "type": "wikibase-entityid",
                },
                "datatype": "wikibase-item",
            },
            "type": "statement",
            "rank": "normal",
        }
