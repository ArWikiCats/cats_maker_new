#!/usr/bin/python3
"""Category filter — refactored from filter_cat.py."""

from __future__ import annotations

import logging
import re

from ....config import settings
from ...wiki_api import get_deleted_pages
from ..constants import FALSE_TEMPLATES, FALSE_TEMPLATES_WITHOUT_STUBS, SKIPPED_CATEGORIES
from ..io.json_store import get_dont_add_pages
from ..tools.template_query import get_templates
from ..utils.text import clean_category_input

logger = logging.getLogger(__name__)


def _get_false_templates() -> frozenset[str]:
    if settings.category.stubs:
        return FALSE_TEMPLATES_WITHOUT_STUBS
    return FALSE_TEMPLATES


def _is_template_category(cat: str, ns: int) -> bool:
    if ns not in (10, 14):
        return cat.startswith("تصنيف:قوالب") or cat.startswith("تصنيف:صناديق تصفح")
    return False


def _is_deleted_category(cat: str, deleted: set[str]) -> bool:
    return cat in deleted


def _has_false_template(cat: str, false_templates: frozenset[str]) -> bool:
    return any(ft in cat for ft in false_templates)


def _is_already_in_text(cat: str, text: str) -> bool:
    return f"{cat}]]" in text or f"{cat}|" in text


def _is_blacklisted(cat: str) -> bool:
    return cat in SKIPPED_CATEGORIES


def _has_blacklisted_template(templates: list[str] | None) -> bool:
    if not templates:
        return False
    blacklist = {"قالب:تحويل تصنيف", "قالب:delete", "قالب:حذف"}
    return any(t in blacklist for t in templates)


def _is_hidden_category(templates: list[str] | None) -> bool:
    if not templates or settings.category.stubs:
        return False
    return "قالب:تصنيف مخفي" in templates


def _is_tracking_category(templates: list[str] | None) -> bool:
    if not templates:
        return False
    return "قالب:تصنيف تتبع" in templates


def _should_exclude(
    cat: str,
    ns: int,
    text: str,
    deleted: set[str],
    false_templates: frozenset[str],
    templates_map: dict[str, list[str]],
) -> bool:
    if _is_template_category(cat, ns):
        logger.info(f"remove templates cat {cat}.")
        return True

    if not cat.startswith("تصنيف:"):
        logger.debug(f"item {cat} not startswith تصنيف:")
        return True

    if _is_blacklisted(cat):
        logger.info(f"<<lightred>>Category {cat} in SKIPPED_CATEGORIES")
        return True

    if _is_deleted_category(cat, deleted):
        logger.info(f"<<lightred>>Category {cat} had in get_deleted_pages()")
        return True

    textremove = re.sub(r"\s*\|\s*", "|", text)

    if "{{لا للتصنيف الميلادي}}" in textremove:
        if "(الميلادي)" in cat or "(قبل الميلاد)" in cat:
            return True

    if "تصنيف:متوفون" in textremove:
        if "أشخاص أحياء" in cat or "أشخاص_أحياء" in cat:
            return True

    if _has_false_template(cat, false_templates):
        logger.info(f"Remove cat:{cat} it has false template")
        return True

    if _is_already_in_text(cat, textremove):
        return True

    cat_templates = templates_map.get(cat, [])

    if _has_blacklisted_template(cat_templates):
        logger.info(
            f"<<lightred>>Category {cat} had {{تحويل تصنيف}} or {{delete}} so it is skipped! please edit en.wiki interwiki"
        )
        return True

    if _is_hidden_category(cat_templates):
        logger.info(f"<<lightred>>Category {cat} had {{تصنيف مخفي}} so it is skipped!")
        return True

    if _is_tracking_category(cat_templates):
        logger.info(f"<<lightred>>Category {cat} had {{تصنيف تتبع}} so it is skipped!")
        return True

    return False


def filter_category_text(
    cats: list[str],
    ns: int,
    text: str,
    *,
    deleted: set[str] | None = None,
) -> list[str]:
    """Pure function — returns a new list, never mutates input.

    Args:
        cats: List of category strings to filter.
        ns: Namespace ID of the page being processed.
        text: Full wikitext of the page.
        deleted: Optional set of deleted page titles. Defaults to dont-add list.
    """
    if deleted is None:
        deleted = set(get_dont_add_pages())

    false_temps = _get_false_templates()
    templates_map = get_templates(cats, "ar") or {}

    len_first = len(cats)

    filtered = [
        cat
        for cat in cats
        if not _should_exclude(cat, ns, text, deleted, false_temps, templates_map)
    ]

    removed = len_first - len(filtered)
    logger.info(f"len removed items: {removed}")

    return filtered
