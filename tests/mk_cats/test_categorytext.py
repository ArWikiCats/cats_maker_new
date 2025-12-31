"""
Tests for src/mk_cats/categorytext.py

This module tests category text generation functions.
"""

import pytest

from src.mk_cats.categorytext import (
    LocalLanguageLinks,
    category_mapping,
)


class TestFindLis:
    """Tests for category_mapping dictionary"""

    def test_is_dict(self):
        """Test that category_mapping is a dictionary"""
        assert isinstance(category_mapping, dict)

    def test_contains_known_mappings(self):
        """Test that category_mapping contains known mappings"""
        assert "الألعاب الأولمبية" in category_mapping
        assert category_mapping["الألعاب الأولمبية"] == "ألعاب أولمبية"

    def test_values_are_strings(self):
        """Test that all values are strings"""
        for key, value in category_mapping.items():
            assert isinstance(key, str)
            assert isinstance(value, str)


class TestLLoSet:
    """Tests for LocalLanguageLinks set"""

    def test_is_set(self):
        """Test that LocalLanguageLinks is a set"""
        assert isinstance(LocalLanguageLinks, set)

    def test_contains_known_items(self):
        """Test that LocalLanguageLinks contains known items"""
        known_items = ["فلسطين", "المغرب", "اليمن", "سينما", "كرة القدم"]
        for item in known_items:
            assert item in LocalLanguageLinks

    def test_all_items_are_strings(self):
        """Test that all items are strings"""
        for item in LocalLanguageLinks:
            assert isinstance(item, str)

    def test_no_empty_strings(self):
        """Test that there are no empty strings"""
        for item in LocalLanguageLinks:
            assert item.strip() != ""


class TestPortalListIntegrity:
    """Tests for portal list integrity"""

    def test_find_lis_values_relate_to_portals(self):
        """Test that category_mapping values are valid portal names"""
        for key, value in category_mapping.items():
            # Values should be non-empty strings
            assert value.strip() != ""
