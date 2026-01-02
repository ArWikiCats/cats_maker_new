"""
Tests for src/b18_new/cat_tools.py

اختبارات لملف cat_tools.py - أدوات التصنيفات

This module tests:
- get_SubSub_keys() - Get SubSub dictionary keys
- get_SubSub_value() - Get SubSub value by key
- add_SubSub() - Add items to SubSub dictionary
- work_in_one_cat() - Process a single category
- templateblacklist - Template blacklist
- nameblcklist - Name blacklist
"""

from unittest.mock import MagicMock, patch

import pytest

from src.b18_new import cat_tools


class TestSubSubFunctions:
    """Tests for SubSub dictionary operations."""

    def test_get_subsub_keys_empty(self):
        """Test get_SubSub_keys returns empty list when SubSub is empty."""

        # Clear SubSub
        cat_tools.SubSub.clear()

        result = cat_tools.get_SubSub_keys()

        assert result == []

    def test_get_subsub_keys_with_data(self):
        """Test get_SubSub_keys returns list of keys."""

        # Clear and populate SubSub
        cat_tools.SubSub.clear()
        cat_tools.SubSub["key1"] = ["value1"]
        cat_tools.SubSub["key2"] = ["value2"]

        result = cat_tools.get_SubSub_keys()

        assert "key1" in result
        assert "key2" in result
        assert len(result) == 2

        # Cleanup
        cat_tools.SubSub.clear()

    def test_get_subsub_value_existing_key(self):
        """Test get_SubSub_value returns value for existing key."""

        # Clear and populate SubSub
        cat_tools.SubSub.clear()
        cat_tools.SubSub["test_key"] = ["test_value"]

        result = cat_tools.get_SubSub_value("test_key")

        assert result == ["test_value"]

        # Cleanup
        cat_tools.SubSub.clear()

    def test_get_subsub_value_missing_key(self):
        """Test get_SubSub_value returns None for missing key."""

        # Clear SubSub
        cat_tools.SubSub.clear()

        result = cat_tools.get_SubSub_value("nonexistent_key")

        assert result is None

    def test_add_subsub_new_key(self):
        """Test add_SubSub creates new key with value."""

        # Clear SubSub
        cat_tools.SubSub.clear()

        cat_tools.add_SubSub(["new_cat"], "page_title")

        assert "new_cat" in cat_tools.SubSub
        assert "page_title" in cat_tools.SubSub["new_cat"]

        # Cleanup
        cat_tools.SubSub.clear()

    def test_add_subsub_existing_key(self):
        """Test add_SubSub appends to existing key."""

        # Clear and populate SubSub
        cat_tools.SubSub.clear()
        cat_tools.SubSub["existing_cat"] = ["existing_value"]

        cat_tools.add_SubSub(["existing_cat"], "new_page")

        assert len(cat_tools.SubSub["existing_cat"]) == 2
        assert "existing_value" in cat_tools.SubSub["existing_cat"]
        assert "new_page" in cat_tools.SubSub["existing_cat"]

        # Cleanup
        cat_tools.SubSub.clear()

    def test_add_subsub_multiple_categories(self):
        """Test add_SubSub handles multiple categories."""

        # Clear SubSub
        cat_tools.SubSub.clear()

        cat_tools.add_SubSub(["cat1", "cat2", "cat3"], "page_title")

        assert "cat1" in cat_tools.SubSub
        assert "cat2" in cat_tools.SubSub
        assert "cat3" in cat_tools.SubSub

        # Cleanup
        cat_tools.SubSub.clear()

    def test_add_subsub_empty_list(self):
        """Test add_SubSub handles empty list."""

        # Clear SubSub
        cat_tools.SubSub.clear()

        cat_tools.add_SubSub([], "page_title")

        assert len(cat_tools.SubSub) == 0


class TestBlacklists:
    """Tests for template and name blacklists."""

    def test_templateblacklist_exists(self):
        """Test that templateblacklist is defined."""
        from src.b18_new.cat_tools import templateblacklist

        assert templateblacklist is not None
        assert isinstance(templateblacklist, (list, tuple))

    def test_nameblcklist_exists(self):
        """Test that nameblcklist is defined."""
        from src.b18_new.cat_tools import nameblcklist

        assert nameblcklist is not None
        assert isinstance(nameblcklist, list)

    def test_nameblcklist_contains_expected_items(self):
        """Test that nameblcklist contains expected items."""
        from src.b18_new.cat_tools import nameblcklist

        expected_items = [
            "Current events",
            "Articles with",
            "Tracking",
            "Surnames",
            "Given names",
        ]

        for item in expected_items:
            assert item in nameblcklist

    def test_nameblcklist_contains_stubs(self):
        """Test that nameblcklist contains 'stubs'."""
        from src.b18_new.cat_tools import nameblcklist

        # stubs should be in the list by default
        assert "stubs" in nameblcklist


class TestWorkInOneCat:
    """Tests for work_in_one_cat function."""

    def test_returns_list(self, mocker):
        """Test that work_in_one_cat returns a list."""
        from src.b18_new.cat_tools import work_in_one_cat

        tabcat = {}
        en_cate_list = []

        result = work_in_one_cat("TestCat", tabcat, "en", "TestPage", en_cate_list)

        assert isinstance(result, list)

    def test_adds_to_subsub_when_no_ar_cat(self, mocker):
        """Test that work_in_one_cat adds to SubSub when no Arabic category."""

        # Clear SubSub
        cat_tools.SubSub.clear()

        # Mock get_cache_L_C_N to return None
        mocker.patch("src.b18_new.cat_tools.get_cache_L_C_N", return_value=None)

        tabcat = {}
        en_cate_list = []

        cat_tools.work_in_one_cat("MissingCat", tabcat, "en", "TestPage", en_cate_list)

        assert "MissingCat" in cat_tools.SubSub
        assert "TestPage" in cat_tools.SubSub["MissingCat"]

        # Cleanup
        cat_tools.SubSub.clear()

    def test_adds_ar_cat_to_list_when_found(self, mocker):
        """Test that work_in_one_cat adds Arabic category to list when found."""
        from src.b18_new.cat_tools import work_in_one_cat

        tabcat = {"ar": "تصنيف:علوم"}
        en_cate_list = []

        result = work_in_one_cat("Science", tabcat, "en", "TestPage", en_cate_list)

        assert "تصنيف:علوم" in result

    def test_uses_cache_when_no_ar_in_tabcat(self, mocker):
        """Test that work_in_one_cat uses cache when no ar in tabcat."""
        mocker.patch("src.b18_new.cat_tools.get_cache_L_C_N", return_value="تصنيف:من_الكاش")

        from src.b18_new.cat_tools import work_in_one_cat

        tabcat = {}
        en_cate_list = []

        result = work_in_one_cat("TestCat", tabcat, "en", "TestPage", en_cate_list)

        assert "تصنيف:من_الكاش" in result

    def test_filters_blacklisted_names(self, mocker):
        """Test that work_in_one_cat filters blacklisted names."""
        from src.b18_new.cat_tools import work_in_one_cat

        tabcat = {"ar": "تصنيف:أسماء"}
        en_cate_list = []

        # Category with "Surnames" in name should be filtered
        result = work_in_one_cat("Surnames from England", tabcat, "en", "TestPage", en_cate_list)

        # Should not add to list because "Surnames" is in blacklist
        assert "تصنيف:أسماء" not in result

    def test_filters_blacklisted_templates(self, mocker):
        """Test that work_in_one_cat filters blacklisted templates."""
        from src.b18_new.cat_tools import templateblacklist, work_in_one_cat

        # Skip if templateblacklist is empty
        if not templateblacklist:
            pytest.skip("templateblacklist is empty")

        blacklisted_template = templateblacklist[0]
        tabcat = {"ar": "تصنيف:اختبار", "templates": [blacklisted_template]}
        en_cate_list = []

        result = work_in_one_cat("TestCat", tabcat, "en", "TestPage", en_cate_list)

        # Should not add to list because of blacklisted template
        assert "تصنيف:اختبار" not in result

    def test_handles_empty_tabcat(self, mocker):
        """Test that work_in_one_cat handles empty tabcat."""

        # Clear SubSub
        cat_tools.SubSub.clear()

        mocker.patch("src.b18_new.cat_tools.get_cache_L_C_N", return_value=None)

        tabcat = {}
        en_cate_list = []

        result = cat_tools.work_in_one_cat("EmptyCat", tabcat, "en", "TestPage", en_cate_list)

        # Should return original list (which may be empty)
        assert isinstance(result, list)

        # Cleanup
        cat_tools.SubSub.clear()

    def test_case_insensitive_blacklist_matching(self, mocker):
        """Test that blacklist matching is case insensitive."""
        from src.b18_new.cat_tools import work_in_one_cat

        tabcat = {"ar": "تصنيف:اختبار"}
        en_cate_list = []

        # "STUBS" in uppercase should still be filtered (case insensitive)
        result = work_in_one_cat("Category STUBS for testing", tabcat, "en", "TestPage", en_cate_list)

        assert "تصنيف:اختبار" not in result

    def test_preserves_existing_list_items(self, mocker):
        """Test that work_in_one_cat preserves existing list items."""
        from src.b18_new.cat_tools import work_in_one_cat

        tabcat = {"ar": "تصنيف:جديد"}
        en_cate_list = ["تصنيف:موجود"]

        result = work_in_one_cat("NewCat", tabcat, "en", "TestPage", en_cate_list)

        assert "تصنيف:موجود" in result
        assert "تصنيف:جديد" in result
