#!/usr/bin/python3
"""
"""
import sys

from ..log import logger

# ---
AAr_site = {1: False, "family": "wikipedia", "code": "ar"}
EEn_site = {1: False, "family": "wikipedia", "code": "en"}

FR_site = {"use": False}
FR_site["family"] = ""
FR_site["code"] = "fr"
# ---
Use_Labels = {1: False}
use_sqldb = {1: True}
Make_New_Cat = {1: True}

To = {1: 10000}
Depth = {1: 0}
offseet = {1: 0}

# ---
for arg in sys.argv:
    arg, _, value = arg.partition(":")
    # ---
    if arg == "-offset" or arg == "-off":
        offseet[1] = int(value)
    # ---
    if arg == "depth":
        Depth[1] = int(value)
    # ---
    if arg == "to" or arg == "-to":
        To[1] = int(value)
    # ---
    if arg == "-commons" or arg == "commons":
        EEn_site["family"] = "commons"
        EEn_site["code"] = "commons"
        # ---
        logger.info(f"<<lightred>> EEn_site[family] = {EEn_site['family']}.")
    # ---
    # python3 core8/pwb.py c18/cat -family:wikiquote -newpages:20
    if arg == "-family" or arg == "family":
        if value == "wikiquote" or value == "wikisource":
            # ---
            EEn_site["family"] = "wikiquote"
            EEn_site["code"] = "en"
            # ---

            AAr_site["family"] = "wikiquote"
            AAr_site["code"] = "ar"
            # ---
            logger.info(f'<<lightred>> EEn_site["family"] = {EEn_site["family"]}.')
            logger.info(f'<<lightred>> AAr_site["family"] = {AAr_site["family"]}.')
            Use_Labels[1] = True
            logger.info("<<lightred>> -------------------------------")
            logger.info("<<lightred>> Use_Labels.")
    # ---
    if arg == "-uselang" or arg == "uselang":
        # ---
        EEn_site["family"] = "wikipedia"
        EEn_site["code"] = value
        # ---
        logger.info("<<lightred>> uselang[2] = {}:{}.".format(value, EEn_site["family"]))
        Make_New_Cat[1] = False
    # ---
    # python3 core8/pwb.py c18/cat -page:شوليه_باي_دي_لا_لورا_2018 -slang:fr
    # python3 core8/pwb.py c18/cat -ref:قالب:بيانات_قالب_من_ويكي_بيانات -ns:10 -slang:fr

    if arg == "-slang" or arg == "slang":
        FR_site["use"] = True
        # ---
        FR_site["family"] = "wikipedia"
        FR_site["code"] = value
        # ---
        logger.info("<<lightred>> uselang[2] = {}:{}.".format(value, EEn_site["family"]))
        logger.info('<<lightred>> FR_site["family"] = {}:{}.'.format(value, FR_site["family"]))
        Make_New_Cat[1] = False
    # ---
    if arg == "usesql":
        use_sqldb[1] = True
        logger.info("<<lightred>> use My SQl .")
    # ---
    if arg == "-nosql":
        use_sqldb[1] = False
        logger.info("<<lightred>> dont_use_sqldb .")
    # ---
    if arg == "-dontMakeNewCat" or arg == "-dontmakenewcat":
        Make_New_Cat[1] = False
        logger.info("<<lightred>> -------------------------------")
        logger.info("<<lightred>> dont New Categories.")
    # ---
    if arg == "-uselabels":
        Use_Labels[1] = True
        logger.info("<<lightred>> -------------------------------")
        logger.info("<<lightred>> Use_Labels.")

if To[1] != 0:
    To[1] = To[1] + offseet[1]
# ---
