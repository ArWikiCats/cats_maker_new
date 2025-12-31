"""
Tests for src/wiki_api/himoBOT2.py

This module tests Wikipedia API helper functions.
"""

import pytest

from src.wiki_api.himoBOT2 import (
    get_page_info_from_wikipedia,
    GetPagelinks,
    redirects_table,
)


class TestRedirectsTable:
    """Tests for redirects_table dictionary"""

    def test_is_dict(self):
        """Test that redirects_table is a dictionary"""
        assert isinstance(redirects_table, dict)


class TestGetPageInfoFromWikipediaNew:
    """Tests for get_page_info_from_wikipedia function"""

    def test_returns_dict_for_valid_page(self, mocker):
        """Test that function returns dict for valid page"""
        mock_response = {
            "query": {
                "pages": {
                    "123": {
                        "pageid": 123,
                        "ns": 0,
                        "title": "Test Page",
                        "langlinks": [{"lang": "en", "*": "Test Page"}],
                    }
                }
            }
        }
        mocker.patch("src.wiki_api.himoBOT2.submitAPI", return_value=mock_response)
        get_page_info_from_wikipedia.cache_clear()

        result = get_page_info_from_wikipedia("ar", "Test Page", Print=False)
        assert isinstance(result, dict)

    def test_returns_empty_dict_on_no_response(self, mocker):
        """Test that function returns empty dict when API fails"""
        mocker.patch("src.wiki_api.himoBOT2.submitAPI", return_value=None)
        get_page_info_from_wikipedia.cache_clear()

        result = get_page_info_from_wikipedia("ar", "Nonexistent", Print=False)
        assert result == {}

    def test_handles_missing_page(self, mocker):
        """Test that function handles missing pages correctly"""
        mock_response = {
            "query": {
                "pages": {
                    "-1": {
                        "ns": 0,
                        "title": "Missing Page",
                        "missing": "",
                    }
                }
            }
        }
        mocker.patch("src.wiki_api.himoBOT2.submitAPI", return_value=mock_response)
        get_page_info_from_wikipedia.cache_clear()

        result = get_page_info_from_wikipedia("ar", "Missing Page", Print=False)
        assert isinstance(result, dict)
        if result:
            assert result.get("exists") is False

    def test_strips_wiki_suffix_from_sitecode(self, mocker):
        """Test that function strips 'wiki' suffix from sitecode"""
        mock_response = {"query": {"pages": {"123": {"pageid": 123, "ns": 0, "title": "Test"}}}}
        mock_submit = mocker.patch("src.wiki_api.himoBOT2.submitAPI", return_value=mock_response)
        get_page_info_from_wikipedia.cache_clear()

        get_page_info_from_wikipedia("arwiki", "Test", Print=False)
        # The function should call submitAPI with 'ar' not 'arwiki'
        call_args = mock_submit.call_args
        assert call_args[0][1] == "ar"  # sitecode should be 'ar'


class TestGetPagelinks:
    """Tests for GetPagelinks function"""

    def test_returns_dict(self, mocker):
        """Test that GetPagelinks returns a dictionary"""
        mock_response = {
            "parse": {
                "title": "Test Page",
                "pageid": 123,
                "links": [{"ns": 0, "*": "Link 1"}, {"ns": 0, "*": "Link 2"}],
            }
        }
        mocker.patch("src.wiki_api.himoBOT2.submitAPI", return_value=mock_response)
        GetPagelinks.cache_clear()

        result = GetPagelinks("Test Page", sitecode="ar")
        assert isinstance(result, dict)

    def test_returns_empty_dict_on_no_response(self, mocker):
        """Test that GetPagelinks returns empty dict when API fails"""
        mocker.patch("src.wiki_api.himoBOT2.submitAPI", return_value=None)
        GetPagelinks.cache_clear()

        result = GetPagelinks("Nonexistent", sitecode="ar")
        assert result == {}

    def test_extracts_links_correctly(self, mocker):
        """Test that GetPagelinks extracts links from response"""
        mock_response = {
            "parse": {
                "title": "Test",
                "pageid": 123,
                "links": [
                    {"ns": 0, "*": "Article Link"},
                    {"ns": 100, "*": "Portal:Science"},
                ],
            }
        }
        mocker.patch("src.wiki_api.himoBOT2.submitAPI", return_value=mock_response)
        GetPagelinks.cache_clear()

        result = GetPagelinks("Test", sitecode="en")
        assert "Article Link" in result
        assert "Portal:Science" in result

    def test_default_sitecode_is_ar(self, mocker):
        """Test that default sitecode is 'ar'"""
        mock_response = {"parse": {"title": "Test", "pageid": 123, "links": []}}
        mock_submit = mocker.patch("src.wiki_api.himoBOT2.submitAPI", return_value=mock_response)
        GetPagelinks.cache_clear()

        GetPagelinks("Test")
        call_args = mock_submit.call_args
        assert call_args[0][1] == "ar"
