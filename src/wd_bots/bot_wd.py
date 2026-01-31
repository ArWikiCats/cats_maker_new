"""
Wikidata functions

This module provides Wikidata-specific functionality.

"""

import logging

logger = logging.getLogger(__name__)


class WD_Functions:
    def __init__(self):
        # self.post_continue = post_continue
        # super().__init__()
        pass

    def _pages_with_prop(self, post_continue, pwppropname="unlinkedwikibase_id", pwplimit=None, Max=None):
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "pageswithprop",
            "utf8": 1,
            "formatversion": "2",
            "pwplimit": "max",
            "pwppropname": "unlinkedwikibase_id",
            "pwpprop": "title|value",
        }
        # ---
        if pwplimit and pwplimit.isdigit():
            params["pwplimit"] = pwplimit
        # ---
        if pwppropname != "":
            params["pwppropname"] = pwppropname
        # ---
        results = post_continue(params, "query", _p_="pageswithprop", p_empty=[], Max=Max)
        # ---
        logger.debug(f"pageswithprop len(results) = {len(results)}")
        # ---
        return results

    def format_labels_descriptions(self, labels):
        return {x["language"]: x["value"] for _, x in labels.items()}
