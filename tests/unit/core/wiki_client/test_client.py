"""
Unit tests for src/core/wiki_client/client.py module.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.core.wiki_client.client import WikiLoginClient, _get_shared_session
from src.core.wiki_client.exceptions import LoginError, WikiClientError


class TestEnrichParams:
    @patch("src.core.wiki_client.client.wrap_session")
    @patch("src.core.wiki_client.client.load_into_session")
    @patch("src.core.wiki_client.client.mwclient.Site")
    @patch("src.core.wiki_client.client._get_shared_session")
    @patch("src.core.wiki_client.client.get_cookie_path")
    def test_query_action_strips_bot_and_summary(self, mock_path, mock_session, mock_site, mock_load, mock_wrap):
        mock_path.return_value = MagicMock()
        mock_session.return_value = MagicMock()
        mock_site.return_value = MagicMock()
        site_instance = mock_site.return_value
        site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}

        client = WikiLoginClient("en", "wikipedia", "bot", "pass")
        params = {"action": "query", "bot": 1, "summary": "test", "titles": "Python"}
        result = client._enrich_params(params)
        assert "bot" not in result
        assert "summary" not in result
        assert result["titles"] == "Python"

    @patch("src.core.wiki_client.client.wrap_session")
    @patch("src.core.wiki_client.client.load_into_session")
    @patch("src.core.wiki_client.client.mwclient.Site")
    @patch("src.core.wiki_client.client._get_shared_session")
    @patch("src.core.wiki_client.client.get_cookie_path")
    def test_write_action_injects_bot_and_assertuser(self, mock_path, mock_session, mock_site, mock_load, mock_wrap):
        mock_path.return_value = MagicMock()
        mock_session.return_value = MagicMock()
        mock_site.return_value = MagicMock()
        site_instance = mock_site.return_value
        site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}

        client = WikiLoginClient("en", "wikipedia", "MyBot", "pass")
        params = {"action": "edit", "title": "Test"}
        result = client._enrich_params(params)
        assert result["bot"] == 1
        assert result["assertuser"] == "MyBot"


class TestClientRequest:
    def test_invalid_method_raises(self):
        with patch("src.core.wiki_client.client.wrap_session"), \
             patch("src.core.wiki_client.client.load_into_session"), \
             patch("src.core.wiki_client.client.mwclient.Site") as mock_site, \
             patch("src.core.wiki_client.client._get_shared_session"), \
             patch("src.core.wiki_client.client.get_cookie_path"):
            mock_site.return_value.api.return_value = {"query": {"userinfo": {"id": 1}}}
            client = WikiLoginClient("en", "wikipedia", "bot", "pass")
            with pytest.raises(ValueError, match="method must be"):
                client.client_request({"action": "query"}, method="delete")

    def test_api_error_raises_wiki_client_error(self):
        with patch("src.core.wiki_client.client.wrap_session"), \
             patch("src.core.wiki_client.client.load_into_session"), \
             patch("src.core.wiki_client.client.mwclient.Site") as mock_site, \
             patch("src.core.wiki_client.client._get_shared_session"), \
             patch("src.core.wiki_client.client.get_cookie_path"):
            site_instance = mock_site.return_value
            site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}
            site_instance.connection = MagicMock()
            site_instance.api_url = "http://example.com/api"

            response = MagicMock()
            response.raise_for_status = MagicMock()
            response.json.return_value = {"error": {"code": "badtoken", "info": "Invalid token"}}
            site_instance.connection.request.return_value = response

            client = WikiLoginClient("en", "wikipedia", "bot", "pass")
            # The wrapped request may handle CSRF, so we test the unwrapped path
            with pytest.raises(WikiClientError):
                client.client_request({"action": "edit"})


class TestRepr:
    @patch("src.core.wiki_client.client.wrap_session")
    @patch("src.core.wiki_client.client.load_into_session")
    @patch("src.core.wiki_client.client.mwclient.Site")
    @patch("src.core.wiki_client.client._get_shared_session")
    @patch("src.core.wiki_client.client.get_cookie_path")
    def test_repr(self, mock_path, mock_session, mock_site, mock_load, mock_wrap):
        mock_site.return_value.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("en", "wikipedia", "MyBot", "pass")
        assert "WikiLoginClient" in repr(client)
        assert "en" in repr(client)
        assert "MyBot" in repr(client)
