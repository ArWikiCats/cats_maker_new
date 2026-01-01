#!/usr/bin/python3
"""
"""
from ...config import settings
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

# Initialize from settings
offseet[1] = settings.query.offset
Depth[1] = settings.query.depth
To[1] = settings.query.to_limit
use_sqldb[1] = settings.database.use_sql
Make_New_Cat[1] = settings.category.make_new_cat
Use_Labels[1] = settings.category.use_labels

# Handle commons site
if settings.site.use_commons:
    EEn_site["family"] = "commons"
    EEn_site["code"] = "commons"
    logger.info(f"<<lightred>> EEn_site[family] = {EEn_site['family']}.")

# Handle custom family (wikiquote, wikisource)
if settings.site.custom_family:
    EEn_site["family"] = settings.site.custom_family
    EEn_site["code"] = "en"
    AAr_site["family"] = settings.site.custom_family
    AAr_site["code"] = "ar"
    logger.info(f'<<lightred>> EEn_site["family"] = {EEn_site["family"]}.')
    logger.info(f'<<lightred>> AAr_site["family"] = {AAr_site["family"]}.')
    Use_Labels[1] = True
    logger.info("<<lightred>> -------------------------------")
    logger.info("<<lightred>> Use_Labels.")

# Handle custom language
if settings.site.custom_lang:
    EEn_site["family"] = "wikipedia"
    EEn_site["code"] = settings.site.custom_lang
    logger.info("<<lightred>> uselang[2] = {}:{}.".format(settings.site.custom_lang, EEn_site["family"]))
    Make_New_Cat[1] = False

# Handle secondary language (slang)
if settings.site.use_secondary:
    FR_site["use"] = True
    FR_site["family"] = settings.site.secondary_family
    FR_site["code"] = settings.site.secondary_lang
    logger.info("<<lightred>> uselang[2] = {}:{}.".format(settings.site.secondary_lang, EEn_site["family"]))
    logger.info('<<lightred>> FR_site["family"] = {}:{}.'.format(settings.site.secondary_lang, FR_site["family"]))
    Make_New_Cat[1] = False

# Log SQL usage if disabled
if not settings.database.use_sql:
    logger.info("<<lightred>> dont_use_sqldb .")

# Log make new cat if disabled
if not settings.category.make_new_cat:
    logger.info("<<lightred>> -------------------------------")
    logger.info("<<lightred>> dont New Categories.")

# Log use labels if enabled
if settings.category.use_labels and not settings.site.custom_family:
    logger.info("<<lightred>> -------------------------------")
    logger.info("<<lightred>> Use_Labels.")
# ---
