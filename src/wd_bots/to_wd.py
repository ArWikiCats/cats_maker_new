#!/usr/bin/python3
"""
Wikidata functions for cats_maker_new bot
"""
import functools
import json
import logging
import re

from .utils import bad_lag, outbot_json
from .wd_bots_main import WD_API, log_in_wikidata

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1024)
def get_session_post(Mr_or_bot="bot", www="www") -> WD_API:
    login_bot = log_in_wikidata(www=www)
    return WD_API(login_bot, Mr_or_bot=Mr_or_bot)


def add_labels(
    qid,
    label,
    lang,
):

    if bad_lag(True):
        return ""

    if not qid:
        logger.debug(" Qid == '' ")
        return False

    if label == "":
        logger.debug(" label == '' and remove = False ")
        return False

    # save the edit
    out = f'{qid} label:"{lang}"@{label}.'
    wd_api = get_session_post()
    r4 = wd_api.post_to_newapi(
        params={
            "action": "wbsetlabel",
            "id": qid,
            "language": lang,
            "value": label,
        },
    )

    if not r4:
        logger.debug(" r4 == {} ")
        return False

    text = str(r4)
    if ("using the same description text" in text) and ("associated with language code" in text):
        item2 = re.search(r"(Q\d+)", str(r4["error"]["info"])).group(1)
        logger.debug(f"<<lightred>>API: same label item: {item2}")

    success = r4.get("success", 0)
    if success == 1:
        logger.warning(f"<<lightgreen>> ** true.")
        return True

    d = outbot_json(r4, fi=out)

    if d == "warn":
        logger.warning(str(r4))


def add_sitelinks_to_wikidata(
    qid,
    title,
    wiki,
    enlink="",
    ensite="",
    nowait=False,
    returnid=False,
    return_text=False,
):

    if bad_lag(nowait):
        return ""

    if not wiki.endswith("wiki") and wiki.find("wiki") == -1 and wiki.find("wiktionary") == -1:
        wiki = f"{wiki}wiki"

    if enlink:
        logger.debug(f' **: enlink:"{ensite}:{enlink}" {wiki}:{title}')
    else:
        logger.debug(f' **: Qid:"{qid}" {wiki}:{title}')

    # save the edit

    if qid.strip() == "" and enlink == "":
        logger.debug(f'<<lightred>> **: False: Qid == "" {wiki}:{title}.')
        return False

    paramse = {
        "action": "wbsetsitelink",
        "linktitle": title,
        "linksite": wiki,
    }

    out = f'Added link to "{qid}" [{wiki}]:"{title}"'

    if qid:
        paramse["id"] = qid
    else:
        out = f'Added link to "{ensite}:{enlink}" [{wiki}]:"{title}"'
        paramse["title"] = enlink
        paramse["site"] = ensite

    wd_api = get_session_post()
    r4 = wd_api.post_to_newapi(params=paramse)

    if not r4:
        return False

    success = r4.get("success", 0)
    if success == 1:
        logger.warning(f"<<lightgreen>> true {out}")
        if enlink and returnid:
            ido = re.match(r".*\"id\"\:\"(Q\d+)\".*", str(r4))
            if ido:
                return ido.group(1)
        else:
            return True

    d = outbot_json(r4, fi=out)

    if return_text:
        return str(r4)

    if d == "warn":
        logger.warning(str(r4))

    return d


def create_new_item(
    data2,
    summary,
    RRE=0,
    returnid=False,
    nowait=False,
):
    """
    Create a new item in the API with the provided data and summary.
    """

    if bad_lag(nowait):
        return ""

    data = json.JSONEncoder().encode(data2)

    wd_api = get_session_post()
    r4 = wd_api.post_to_newapi(
        params={
            "action": "wbeditentity",
            "new": "item",
            "summary": summary,
            "data": data,
        },
    )

    if not r4:
        return False

    success = r4.get("success", 0)

    if success == 1:
        logger.warning(f"<<lightgreen>> ** true.")
        if returnid:
            Qid = False
            if cf is True:
                if "entity" in r4 and "id" in r4["entity"]:
                    Qid = r4["entity"]["id"]
                    logger.debug(f'<<lightgreen>> bot.py : returnid:"{Qid}" ')
            return Qid
        return str(r4)

    cf = outbot_json(r4, fi=summary)

    if cf == "reagain" and RRE == 0:
        return create_new_item(
            data2,
            summary,
            RRE=1,
            returnid=returnid,
            nowait=nowait,
        )

    if cf == "warn":
        logger.warning(str(r4))

    return str(r4)


def makejson(property, numeric):

    if numeric:
        numeric = numeric.replace("Q", "")
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


def Make_New_item(artitle, entitle, family=""):
    logger.debug(f'<<lightgreen>>* :ar:"{artitle}", english:"{entitle}".')

    enwiki = "enwiki"
    arwiki = "arwiki"

    if family and family != "wikipedia":
        enwiki = f"en{family}"
        arwiki = f"ar{family}"

    data = {
        "sitelinks": {enwiki: {"site": enwiki, "title": entitle}, arwiki: {"site": arwiki, "title": artitle}},
        "labels": {"ar": {"language": "ar", "value": artitle}, "en": {"language": "en", "value": entitle}},
        "claims": {"P31": [makejson("P31", "Q4167836")]},
    }

    summary = f"Bot: New item from [[w:en:{entitle}|{enwiki}]]/[[w:ar:{artitle}|{arwiki}]]."

    new_item_id = create_new_item(data, summary, returnid=True, nowait=True)

    if new_item_id and new_item_id.startswith("Q"):
        return True
    return False


def Log_to_wikidata(ar, enca, qid) -> None:
    if qid:
        add_sitelinks_to_wikidata(qid, ar, "arwiki", nowait=True)
        add_labels(qid, ar, "ar")
        return

    cd = add_sitelinks_to_wikidata("", ar, "arwiki", enlink=enca, ensite="enwiki", nowait=True)
    if cd is not True:
        Make_New_item(ar, enca, family="wikipedia")
