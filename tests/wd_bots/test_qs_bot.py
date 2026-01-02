"""
Tests for src/wd_bots/qs_bot.py

This module tests QuickStatements API wrapper functions.
"""

import pytest

from src.wd_bots.qs_bot import (
    QS_line,
    QS_New_API,
    _load_session,
)


class TestLoadSession:
    """Tests for _load_session function"""

    def test_returns_session(self):
        """Test that function returns a requests Session"""
        import requests

        # Clear cache first
        _load_session.cache_clear()

        result = _load_session()

        assert isinstance(result, requests.Session)

    def test_session_has_user_agent(self):
        """Test that session has User-Agent header"""
        _load_session.cache_clear()

        session = _load_session()

        assert "User-Agent" in session.headers

    def test_caches_session(self):
        """Test that session is cached"""
        _load_session.cache_clear()

        session1 = _load_session()
        session2 = _load_session()

        assert session1 is session2


class TestQSNewAPI:
    """Tests for QS_New_API function"""

    def test_creates_correct_format(self, mocker):
        """Test that correct QuickStatements format is created"""
        mock_session = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_session.post.return_value = mock_response
        mocker.patch("src.wd_bots.qs_bot._load_session", return_value=mock_session)

        data = {"sitelinks": {"enwiki": {"site": "enwiki", "title": "Test"}}, "claims": {}}

        QS_New_API(data)

        mock_session.post.assert_called_once()

    def test_includes_sitelinks(self, mocker):
        """Test that sitelinks are included"""
        mock_session = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_session.post.return_value = mock_response
        mocker.patch("src.wd_bots.qs_bot._load_session", return_value=mock_session)

        data = {
            "sitelinks": {
                "enwiki": {"site": "enwiki", "title": "Science"},
                "arwiki": {"site": "arwiki", "title": "علوم"},
            },
            "claims": {},
        }

        QS_New_API(data)

        call_args = mock_session.post.call_args
        post_data = call_args[1]["data"]["data"]
        assert "Science" in post_data or "Senwiki" in post_data

    def test_includes_claims(self, mocker):
        """Test that claims are included"""
        mock_session = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_session.post.return_value = mock_response
        mocker.patch("src.wd_bots.qs_bot._load_session", return_value=mock_session)

        data = {
            "sitelinks": {},
            "claims": {"P31": [{"mainsnak": {"property": "P31", "datavalue": {"value": {"id": "Q5"}}}}]},
        }

        QS_New_API(data)

        call_args = mock_session.post.call_args
        post_data = call_args[1]["data"]["data"]
        assert "P31" in post_data

    def test_returns_false_on_no_response(self, mocker):
        """Test that False is returned when no response"""
        mock_session = mocker.MagicMock()
        mock_session.post.return_value = None
        mocker.patch("src.wd_bots.qs_bot._load_session", return_value=mock_session)

        result = QS_New_API({"sitelinks": {}, "claims": {}})

        assert result is False


class TestQSLine:
    """Tests for QS_line function"""

    def test_sends_post_request(self, mocker):
        """Test that POST request is sent"""
        mock_session = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_session.post.return_value = mock_response
        mocker.patch("src.wd_bots.qs_bot._load_session", return_value=mock_session)
        mocker.patch("src.wd_bots.qs_bot.time.sleep")

        QS_line('Q123|Lar|"Test"')

        mock_session.post.assert_called_once()

    def test_uses_correct_endpoint(self, mocker):
        """Test that correct QuickStatements endpoint is used"""
        mock_session = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_session.post.return_value = mock_response
        mocker.patch("src.wd_bots.qs_bot._load_session", return_value=mock_session)
        mocker.patch("src.wd_bots.qs_bot.time.sleep")

        QS_line('Q123|Lar|"Test"')

        call_args = mock_session.post.call_args[0][0]
        assert "quickstatements.toolforge.org" in call_args

    def test_returns_false_on_no_response(self, mocker):
        """Test that False is returned when no response"""
        mock_session = mocker.MagicMock()
        mock_session.post.return_value = None
        mocker.patch("src.wd_bots.qs_bot._load_session", return_value=mock_session)
        mocker.patch("src.wd_bots.qs_bot.time.sleep")

        result = QS_line('Q123|Lar|"Test"')

        assert result is False

    def test_sleeps_after_request(self, mocker):
        """Test that function sleeps after request"""
        mock_session = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_session.post.return_value = mock_response
        mocker.patch("src.wd_bots.qs_bot._load_session", return_value=mock_session)
        mock_sleep = mocker.patch("src.wd_bots.qs_bot.time.sleep")

        QS_line('Q123|Lar|"Test"')

        mock_sleep.assert_called_with(2)

    def test_supports_different_users(self, mocker):
        """Test that different users can be specified"""
        mock_session = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_session.post.return_value = mock_response
        mocker.patch("src.wd_bots.qs_bot._load_session", return_value=mock_session)
        mocker.patch("src.wd_bots.qs_bot.time.sleep")

        QS_line('Q123|Lar|"Test"', user="Mr.Ibrahembot")

        call_args = mock_session.post.call_args[1]["data"]
        assert call_args["username"] == "Mr.Ibrahembot"
