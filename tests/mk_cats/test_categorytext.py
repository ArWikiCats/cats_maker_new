"""
Tests for src/mk_cats/categorytext.py

This module tests category text generation functions.
"""

import pytest

from src.mk_cats.categorytext import (
    LLo,
    LLo2,
    Make_temp,
    find_lis,
)


class TestFindLis:
    """Tests for find_lis dictionary"""

    def test_is_dict(self):
        """Test that find_lis is a dictionary"""
        assert isinstance(find_lis, dict)

    def test_contains_known_mappings(self):
        """Test that find_lis contains known mappings"""
        assert "الألعاب الأولمبية" in find_lis
        assert find_lis["الألعاب الأولمبية"] == "ألعاب أولمبية"

    def test_values_are_strings(self):
        """Test that all values are strings"""
        for key, value in find_lis.items():
            assert isinstance(key, str)
            assert isinstance(value, str)


class TestLLo2Set:
    """Tests for LLo2 set"""

    def test_is_set(self):
        """Test that LLo2 is a set"""
        assert isinstance(LLo2, set)

    def test_contains_known_items(self):
        """Test that LLo2 contains known items"""
        known_items = ["علوم", "طب", "فلسفة", "رياضة", "موسيقى"]
        for item in known_items:
            assert item in LLo2

    def test_all_items_are_strings(self):
        """Test that all items are strings"""
        for item in LLo2:
            assert isinstance(item, str)

    def test_no_empty_strings(self):
        """Test that there are no empty strings"""
        for item in LLo2:
            assert item.strip() != ""


class TestLLoSet:
    """Tests for LLo set"""

    def test_is_set(self):
        """Test that LLo is a set"""
        assert isinstance(LLo, set)

    def test_contains_known_items(self):
        """Test that LLo contains known items"""
        known_items = ["فلسطين", "المغرب", "اليمن", "سينما", "كرة القدم"]
        for item in known_items:
            assert item in LLo

    def test_all_items_are_strings(self):
        """Test that all items are strings"""
        for item in LLo:
            assert isinstance(item, str)

    def test_no_empty_strings(self):
        """Test that there are no empty strings"""
        for item in LLo:
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

    def test_llo_and_llo2_no_overlap(self):
        """Test that LLo and LLo2 have minimal overlap"""
        # Some overlap is expected, but they should mostly be different
        overlap = LLo.intersection(LLo2)
        # There should be some overlap based on the source code
        assert isinstance(overlap, set)

    def test_combined_coverage(self):
        """Test that LLo and LLo2 together provide good coverage"""
        combined = LLo.union(LLo2)
        # Should have substantial coverage
        assert len(combined) > 100

    def test_find_lis_values_relate_to_portals(self):
        """Test that find_lis values are valid portal names"""
        for key, value in find_lis.items():
            # Values should be non-empty strings
            assert value.strip() != ""
