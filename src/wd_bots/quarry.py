"""
Usage:
from .quarry import get_quarry_results#get_quarry_results(number, get_rows=None)

"""
import json

from ..helps import logger, open_the_url


def get_result(num):
    url = f"https://quarry.wmcloud.org/run/{str(num)}/output/0/json"
    # ---
    result = open_the_url(url)
    # ---
    rows = []
    # ---
    try:
        jsons = json.loads(result)
        rows = jsons["rows"]
    except json.decoder.JSONDecodeError:
        logger.output(f" json.decoder.JSONDecodeError url {url}")
    # ---
    return rows


def get_quarry_results(number, get_rows=None):
    # ---
    results = get_result(number)
    # ---
    if get_rows == 1:
        return [x[0] for x in results]
    # ---
    if get_rows == 2:
        return {x[0]: x[1] for x in results}
    # ---
    return results
