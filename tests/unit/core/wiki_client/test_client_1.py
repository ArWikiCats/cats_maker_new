"""
Unit tests for src/core/wiki_client/client_1.py module.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.core.wiki_client.client_1 import WikiLoginClient
from src.core.wiki_client.exceptions import WikiClientError


class TestClient1Init:
    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_sets_attributes(self, mock_path, mock_site, mock_load, mock_wrap):
        mock_site.return_value.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("en", "wikipedia", "MyBot", "pass")
        assert client.lang == "en"
        assert client.family == "wikipedia"
        assert client.username == "MyBot"


class TestClient1Request:
    def test_invalid_method_raises(self):
        with patch("src.core.wiki_client.client_1.wrap_session"), \
             patch("src.core.wiki_client.client_1.load_into_session"), \
             patch("src.core.wiki_client.client_1.mwclient.Site") as mock_site, \
             patch("src.core.wiki_client.client_1.get_cookie_path"):
            mock_site.return_value.api.return_value = {"query": {"userinfo": {"id": 1}}}
            client = WikiLoginClient("en", "wikipedia", "bot", "pass")
            with pytest.raises(ValueError, match="method must be"):
                client.client_request({"action": "query"}, method="delete")

    def test_files_forces_post(self):
        with patch("src.core.wiki_client.client_1.wrap_session"), \
             patch("src.core.wiki_client.client_1.load_into_session"), \
             patch("src.core.wiki_client.client_1.mwclient.Site") as mock_site, \
             patch("src.core.wiki_client.client_1.get_cookie_path"):
            site_instance = mock_site.return_value
            site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}
            site_instance.connection = MagicMock()
            site_instance.api_url = "http://example.com/api"

            response = MagicMock()
            response.raise_for_status = MagicMock()
            response.json.return_value = {"query": {}}
            site_instance.connection.request.return_value = response

            client = WikiLoginClient("en", "wikipedia", "bot", "pass")
            client.client_request({"action": "upload"}, files={"file": MagicMock()})
            # Should call with POST
            site_instance.connection.request.assert_called()


class TestClient1Repr:
    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_repr(self, mock_path, mock_site, mock_load, mock_wrap):
        mock_site.return_value.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("ar", "wiktionary", "bot", "pass")
        r = repr(client)
        assert "WikiLoginClient" in r
        assert "ar" in r
        assert "bot" in r
