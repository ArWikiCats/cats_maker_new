"""
Unit tests for src/core/new_api/super_login.py module.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.core.new_api.super_login import Login, _load_session


class TestLoadSession:
    def test_returns_session(self):
        session = _load_session()
        assert session is not None

    def test_is_cached(self):
        s1 = _load_session("en", "wikipedia", "bot")
        s2 = _load_session("en", "wikipedia", "bot")
        assert s1 is s2


class TestLoginInit:
    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_sets_attributes(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        assert login.lang == "en"
        assert login.family == "wikipedia"
        assert login.endpoint == "https://en.wikipedia.org/w/api.php"


class TestFilterParams:
    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_adds_format_and_utf8(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        result = login.filter_params({"action": "query"})
        assert result["format"] == "json"
        assert result["utf8"] == 1

    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_strips_bot_from_query(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        result = login.filter_params({"action": "query", "bot": 1, "summary": "test"})
        assert "bot" not in result
        assert "summary" not in result

    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_keeps_bot_for_edit(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        result = login.filter_params({"action": "edit", "bot": 1})
        assert result["bot"] == 1


class TestParamsW:
    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_injects_bot_flag(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_settings.bot.no_login = False
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        login.username = "MyBot"
        result = login.params_w({"action": "edit"})
        assert result["bot"] == 1

    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_injects_assertuser_for_write(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_settings.bot.no_login = False
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        login.username = "MyBot"
        result = login.params_w({"action": "edit"})
        assert result["assertuser"] == "MyBot"

    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_no_assertuser_for_query(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_settings.bot.no_login = False
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        login.username = "MyBot"
        result = login.params_w({"action": "query"})
        assert "assertuser" not in result


class TestParseData:
    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_parses_json_response(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        mock_response = MagicMock()
        mock_response.json.return_value = {"query": {}}
        result = login.parse_data(mock_response)
        assert "query" in result

    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_handles_dict_input(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        result = login.parse_data({"query": {}})
        assert "query" in result

    @patch("src.core.new_api.super_login.get_file_name")
    @patch("src.core.new_api.super_login.settings")
    def test_returns_empty_on_error(self, mock_settings, mock_get_file):
        mock_settings.wikipedia.user_agent = "test"
        mock_get_file.return_value = MagicMock()
        login = Login("en", "wikipedia")
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("bad json")
        mock_response.text = "not json"
        result = login.parse_data(mock_response)
        assert result == {}
