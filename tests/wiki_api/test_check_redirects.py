"""
Tests for src/wiki_api/check_redirects.py

This module tests Wikipedia API helper functions.
"""

import pytest

from src.wiki_api.check_redirects import (
    remove_redirect_pages,
)


@pytest.mark.network
class TestRemoveRedirectPagesReal:
    """Tests for remove_redirect_pages function"""

    def test_removes_redirects_english(self):
        """Test that redirect pages are removed from the list"""
        page_titles = ["Python (programming language)", "USA", "Nonexistent Page 12345"]
        non_redirects = remove_redirect_pages("en", page_titles)
        assert "Python (programming language)" in non_redirects
        assert "USA" in non_redirects
        assert "Nonexistent Page 12345" not in non_redirects

    def test_removes_redirects_arabic(self):
        """Test that redirect pages are removed from the list"""
        page_titles = ["يمن", "اليمن"]
        non_redirects = remove_redirect_pages("en", page_titles)
        assert "يمن" not in non_redirects
        assert "اليمن" in non_redirects
