#!/usr/bin/python3
"""Core logic for new_c18."""

from .category_filter import filter_category_text
from .category_generator import fetch_category_members, translate_titles_to_ar
from .category_resolver import CategoryResolver
from .category_validator import validate_categories_for_new_cat
from .cross_wiki_linker import get_english_page_title, get_page_link
from .member_lister import MemberLister

__all__ = [
    "CategoryResolver",
    "fetch_category_members",
    "filter_category_text",
    "get_english_page_title",
    "get_page_link",
    "MemberLister",
    "translate_titles_to_ar",
    "validate_categories_for_new_cat",
]
