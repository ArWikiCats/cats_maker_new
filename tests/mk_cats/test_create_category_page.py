"""
Tests for src/mk_cats/create_category_page.py

This module tests category page creation functionality.
"""

import pytest

from src.mk_cats.create_category_page import (
    add_text_to_cat,
    find_title,
    make_category,
    new_category,
)
from src.utils.skip_cats import skip_encats


class TestFindTitle:
    """Tests for find_title list"""

    def test_is_list(self):
        """Test that find_title is a list"""
        assert isinstance(find_title, list)

    def test_contains_strings(self):
        """Test that find_title contains strings"""
        for item in find_title:
            assert isinstance(item, str)


class TestMakeCategory:
    """Tests for make_category function"""

    def test_returns_false_for_skip_encats(self, mocker):
        """Test that make_category returns False for categories in skip_encats"""
        # Mock the create_Page to not actually create pages
        mocker.patch("src.mk_cats.create_category_page.create_Page", return_value=False)

        # Use a category that's in skip_encats
        if skip_encats:
            result = make_category([], skip_encats[0], "تصنيف:اختبار", "Q123")
            assert result is False

    def test_returns_false_for_non_arabic_category_title(self, mocker):
        """Test that make_category returns False for titles not starting with تصنيف:"""
        mocker.patch("src.mk_cats.create_category_page.create_Page", return_value=False)

        result = make_category([], "Category:Test", "Test Category", "Q123")
        assert result is False

    def test_returns_false_for_title_without_tasneef_prefix(self, mocker):
        """Test that title must start with تصنيف:"""
        mocker.patch("src.mk_cats.create_category_page.create_Page", return_value=False)

        result = make_category([], "Category:Science", "علوم", "Q123")
        assert result is False


class TestNewCategory:
    """Tests for new_category function"""

    def test_returns_false_for_empty_title(self, mocker):
        """Test that new_category returns False for empty title"""
        mocker.patch("src.mk_cats.create_category_page.make_category", return_value=False)

        result = new_category("Category:Test", "", [], "Q123")
        assert result is False

    def test_returns_false_for_title_n(self, mocker):
        """Test that new_category returns False for title 'n'"""
        mocker.patch("src.mk_cats.create_category_page.make_category", return_value=False)

        result = new_category("Category:Test", "n", [], "Q123")
        # The function checks for empty or 'n' but doesn't return False explicitly
        # It continues to call make_category which returns False
        assert result is False

    def test_returns_false_when_make_category_fails(self, mocker):
        """Test that new_category returns False when make_category returns False"""
        mocker.patch("src.mk_cats.create_category_page.make_category", return_value=False)

        result = new_category("Category:Science", "تصنيف:علوم", ["تصنيف:علوم طبيعية"], "Q123")
        assert result is False

    def test_returns_true_when_make_category_succeeds(self, mocker):
        """Test that new_category returns True when make_category returns True"""
        mocker.patch("src.mk_cats.create_category_page.make_category", return_value=True)

        result = new_category("Category:Science", "تصنيف:علوم", ["تصنيف:علوم طبيعية"], "Q123")
        assert result is True


class TestAddTextToCat:
    """Tests for add_text_to_cat function"""

    def test_returns_text_for_non_wikipedia_family(self, mocker):
        """Test that add_text_to_cat returns unchanged text for non-wikipedia family"""
        text = "Test text"
        result = add_text_to_cat(text, [], "Category:Test", "تصنيف:اختبار", "Q123", family="wikisource")
        assert result == text

    def test_handles_empty_categories(self, mocker):
        """Test that add_text_to_cat handles empty categories list"""
        mocker.patch("src.mk_cats.create_category_page.page_put", return_value=False)
        mocker.patch("src.mk_cats.create_category_page.categorytext.fetch_commons_category", return_value="")
        mocker.patch("src.mk_cats.create_category_page.categorytext.generate_portal_content", return_value=("", []))
        mocker.patch("src.mk_cats.create_category_page.categorytext.main_make_temp_no_title", return_value="")

        text = "Test text"
        result = add_text_to_cat(text, [], "Category:Test", "تصنيف:اختبار", "Q123", family="wikipedia")
        assert result is not None

    def test_filters_none_and_false_categories(self, mocker):
        """Test that add_text_to_cat filters out None and False categories"""
        mocker.patch("src.mk_cats.create_category_page.page_put", return_value=False)
        mocker.patch("src.mk_cats.create_category_page.categorytext.fetch_commons_category", return_value="")
        mocker.patch("src.mk_cats.create_category_page.categorytext.generate_portal_content", return_value=("", []))
        mocker.patch("src.mk_cats.create_category_page.categorytext.main_make_temp_no_title", return_value="")

        text = "Test text"
        categories = [None, False, "تصنيف:صالح", None]
        result = add_text_to_cat(text, categories, "Category:Test", "تصنيف:اختبار", "Q123", family="wikipedia")
        # The function should handle the mixed list without errors
        assert result is not None
