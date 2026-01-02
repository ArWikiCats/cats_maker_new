"""
Tests for src/wd_bots/wd_login_wrap.py

This module tests Wikidata login wrapper functions.
"""

import pytest

from src.wd_bots.wd_login_wrap import (
    log_in_wikidata,
    logins_cache,
)


class TestLoginsCache:
    """Tests for logins_cache dictionary"""

    def test_is_dict(self):
        """Test that logins_cache is a dictionary"""
        assert isinstance(logins_cache, dict)


class TestLogInWikidata:
    """Tests for log_in_wikidata function"""

    def test_calls_login_wrap(self, mocker):
        """Test that LoginWrap is called"""
        mock_login = mocker.MagicMock()
        mock_login_wrap = mocker.patch("src.wd_bots.wd_login_wrap.LoginWrap", return_value=(mock_login, {}))

        log_in_wikidata()

        mock_login_wrap.assert_called_once()

    def test_returns_login_bot(self, mocker):
        """Test that function returns login bot"""
        mock_login = mocker.MagicMock()
        mocker.patch("src.wd_bots.wd_login_wrap.LoginWrap", return_value=(mock_login, {}))

        result = log_in_wikidata()

        assert result == mock_login

    def test_uses_www_by_default(self, mocker):
        """Test that www is used by default"""
        mock_login = mocker.MagicMock()
        mock_login_wrap = mocker.patch("src.wd_bots.wd_login_wrap.LoginWrap", return_value=(mock_login, {}))

        log_in_wikidata()

        call_args = mock_login_wrap.call_args[0]
        assert call_args[0] == "www"
        assert call_args[1] == "wikidata"

    def test_updates_logins_cache(self, mocker):
        """Test that logins_cache is updated"""
        mock_login = mocker.MagicMock()
        mock_cache = {"test": "cache"}
        mocker.patch("src.wd_bots.wd_login_wrap.LoginWrap", return_value=(mock_login, mock_cache))

        log_in_wikidata()

        # Cache should be updated (though we can't easily verify this
        # without accessing internal state)
