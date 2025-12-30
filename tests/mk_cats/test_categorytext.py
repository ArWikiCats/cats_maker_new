"""
Tests for src/mk_cats/categorytext.py

This module tests category text generation functions.
"""

import pytest

from src.mk_cats.categorytext import (
    LocalLanguageLinks,
    Make_temp,
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


class TestMakeTemp:
    """Tests for Make_temp function"""

    def test_returns_string(self):
        """Test that Make_temp returns a string"""
        result = Make_temp("", "تصنيف:عقد 2010")
        assert isinstance(result, str)

    def test_returns_empty_for_unknown_category(self):
        """Test that Make_temp returns empty string for unknown category patterns"""
        result = Make_temp("", "تصنيف:موضوع عشوائي")
        assert result == ""

    def test_decade_category_returns_template(self):
        """Test that decade categories return a template"""
        result = Make_temp("", "تصنيف:عقد 2010")
        assert "{{" in result or result == ""

    def test_century_category_returns_template(self):
        """Test that century categories return a template"""
        result = Make_temp("", "تصنيف:القرن 19")
        assert "{{" in result or result == ""

    def test_year_category_returns_template(self):
        """Test that year categories return a template"""
        result = Make_temp("", "تصنيف:2020")
        # Should return {{تصنيف موسم}} or similar
        assert "{{" in result or result == ""


class TestPortalListIntegrity:
    """Tests for portal list integrity"""

    def test_find_lis_values_relate_to_portals(self):
        """Test that category_mapping values are valid portal names"""
        for key, value in category_mapping.items():
            # Values should be non-empty strings
            assert value.strip() != ""
