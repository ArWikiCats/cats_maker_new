"""
Tests for src/wiki_api/check_redirects.py

This module tests Wikipedia API helper functions.
"""

import pytest

from src.wiki_api.check_redirects import (
    _load_new_api,
    load_non_redirects,
    remove_redirect_pages,
)


class TestLoadNewApi:
    """Tests for _load_new_api helper function"""

    def test_returns_api_instance(self, mocker):
        """Test that _load_new_api returns a NEW_API instance"""
        mock_new_api = mocker.MagicMock()
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_new_api)

        result = _load_new_api("en")

        assert result == mock_new_api

    def test_calls_new_api_with_correct_params(self, mocker):
        """Test that _load_new_api calls NEW_API with correct parameters"""
        mock_new_api_class = mocker.patch("src.wiki_api.check_redirects.NEW_API")

        _load_new_api("ar")

        mock_new_api_class.assert_called_once_with("ar", family="wikipedia")

    def test_supports_different_languages(self, mocker):
        """Test that _load_new_api works with different language codes"""
        mock_new_api_class = mocker.patch("src.wiki_api.check_redirects.NEW_API")

        for lang in ["en", "ar", "fr", "de"]:
            _load_new_api(lang)

        assert mock_new_api_class.call_count == 4


class TestLoadNonRedirects:
    """Tests for load_non_redirects helper function"""

    def test_returns_non_redirect_pages(self, mocker):
        """Test that load_non_redirects returns only non-redirect pages"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {
            "Page1": True,
            "Page2": True,
            "redirect": False,
        }
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)

        result = load_non_redirects("en", ["Page1", "Page2", "Page3"])

        assert result == ["Page1", "Page2"]
        mock_api.Find_pages_exists_or_not.assert_called_once_with(
            ["Page1", "Page2", "Page3"], get_redirect=True
        )

    def test_filters_out_redirect_key(self, mocker):
        """Test that 'redirect' key is filtered out from results"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {
            "Page1": True,
            "redirect": "redirect",
        }
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)

        result = load_non_redirects("en", ["Page1"])

        assert "redirect" not in result
        assert result == ["Page1"]

    def test_filters_out_false_values(self, mocker):
        """Test that pages with False values are filtered out"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {
            "Page1": True,
            "Page2": False,
            "Page3": True,
        }
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)

        result = load_non_redirects("en", ["Page1", "Page2", "Page3"])

        assert result == ["Page1", "Page3"]

    def test_handles_empty_input(self, mocker):
        """Test that load_non_redirects handles empty input list"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {}
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)

        result = load_non_redirects("en", [])

        assert result == []
        mock_api.Find_pages_exists_or_not.assert_called_once_with([], get_redirect=True)

    def test_handles_all_redirects(self, mocker):
        """Test that load_non_redirects returns empty list when all pages are redirects"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {
            "Page1": False,
            "Page2": False,
            "redirect": True,
        }
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)

        result = load_non_redirects("en", ["Page1", "Page2"])

        assert result == ["redirect"]

    def test_uses_correct_language(self, mocker):
        """Test that load_non_redirects uses the correct language code"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {}
        mock_new_api_class = mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)

        load_non_redirects("ar", ["Page1"])

        mock_new_api_class.assert_called_once_with("ar", family="wikipedia")


class TestRemoveRedirectPages:
    """Tests for remove_redirect_pages function"""

    def test_returns_non_redirect_pages(self, mocker):
        """Test that remove_redirect_pages returns only non-redirect pages"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {
            "Science": True,
            "Mathematics": True,
            "redirect": False,
        }
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)
        mocker.patch("src.wiki_api.check_redirects.logger")

        result = remove_redirect_pages("en", ["Science", "Mathematics", "Physics"])

        assert result == ["Science", "Mathematics"]

    def test_logs_zero_removals(self, mocker):
        """Test that remove_redirect_pages logs correctly when no redirects are removed"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {
            "Page1": True,
            "Page2": True,
        }
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)
        mock_logger = mocker.patch("src.wiki_api.check_redirects.logger")

        result = remove_redirect_pages("en", ["Page1", "Page2"])

        # 2 input pages - 2 non-redirects = 0 removed
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "0" in call_args

    def test_handles_empty_input(self, mocker):
        """Test that remove_redirect_pages handles empty input list"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {}
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)
        mock_logger = mocker.patch("src.wiki_api.check_redirects.logger")

        result = remove_redirect_pages("en", [])

        assert result == []
        mock_logger.info.assert_called_once()

    def test_handles_all_redirects(self, mocker):
        """Test that remove_redirect_pages handles case where all pages are redirects"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {
            "Page1": False,
            "Page2": False,
            "Page3": False,
            "redirect": True,
        }
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)
        mock_logger = mocker.patch("src.wiki_api.check_redirects.logger")

        result = remove_redirect_pages("en", ["Page1", "Page2", "Page3"])

        assert result == ["redirect"]
        # 3 input pages - 0 non-redirects = 2 removed
        call_args = mock_logger.info.call_args[0][0]
        assert "2" in call_args

    def test_preserves_order(self, mocker):
        """Test that remove_redirect_pages preserves the order of non-redirect pages"""
        mock_api = mocker.MagicMock()
        # Dictionary order is preserved in Python 3.7+
        mock_api.Find_pages_exists_or_not.return_value = {
            "Page1": True,
            "Page2": False,
            "Page3": True,
            "Page4": True,
            "redirect": False,
        }
        mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)
        mocker.patch("src.wiki_api.check_redirects.logger")

        result = remove_redirect_pages("en", ["Page1", "Page2", "Page3", "Page4"])

        assert result == ["Page1", "Page3", "Page4"]

    def test_works_with_different_languages(self, mocker):
        """Test that remove_redirect_pages works with different language codes"""
        mock_api = mocker.MagicMock()
        mock_api.Find_pages_exists_or_not.return_value = {
            "صفحة": True,
        }
        mock_new_api_class = mocker.patch("src.wiki_api.check_redirects.NEW_API", return_value=mock_api)
        mocker.patch("src.wiki_api.check_redirects.logger")

        result = remove_redirect_pages("ar", ["صفحة"])

        assert result == ["صفحة"]
        mock_new_api_class.assert_called_once_with("ar", family="wikipedia")

    def test_calls_load_non_redirects(self, mocker):
        """Test that remove_redirect_pages uses load_non_redirects internally"""
        mock_load_non_redirects = mocker.patch(
            "src.wiki_api.check_redirects.load_non_redirects",
            return_value=["Page1", "Page2"]
        )
        mocker.patch("src.wiki_api.check_redirects.logger")

        result = remove_redirect_pages("en", ["Page1", "Page2", "Page3"])

        mock_load_non_redirects.assert_called_once_with("en", ["Page1", "Page2", "Page3"])
        assert result == ["Page1", "Page2"]
