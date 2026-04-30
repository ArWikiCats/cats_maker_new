"""
Unit tests for src/core/wiki_client/client_1.py module.
"""

from unittest.mock import MagicMock, patch

import mwclient.errors
import pytest

from src.core.wiki_client.client_1 import WikiLoginClient
from src.core.wiki_client.exceptions import LoginError, WikiClientError


def _make_client():
    """Helper to create a WikiLoginClient with all external deps mocked."""
    with patch("src.core.wiki_client.client_1.wrap_session"), \
         patch("src.core.wiki_client.client_1.load_into_session"), \
         patch("src.core.wiki_client.client_1.mwclient.Site") as mock_site, \
         patch("src.core.wiki_client.client_1.get_cookie_path"):
        mock_site.return_value.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("en", "wikipedia", "bot", "pass")
    return client, mock_site


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


# ── New tests for missing coverage ──────────────────────────────────────────


class TestSiteProperty:
    """Covers line 95: the `site` property."""

    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_site_property_returns_internal_site(self, mock_path, mock_site_cls, mock_load, mock_wrap):
        mock_site_cls.return_value.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("en", "wikipedia", "bot", "pass")
        # The site property should return the same object stored in _site
        assert client.site is client._site
        assert client.site is mock_site_cls.return_value


class TestLoginMethod:
    """Covers lines 106-107: the `login()` method delegates to `_do_login`."""

    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_login_calls_do_login(self, mock_path, mock_site_cls, mock_load, mock_wrap):
        mock_site_cls.return_value.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("en", "wikipedia", "bot", "pass")
        with patch.object(client, "_do_login") as mock_do_login:
            client.login()
            mock_do_login.assert_called_once()


class TestSaveCookies:
    """Covers lines 116-117: the `save_cookies()` method."""

    @patch("src.core.wiki_client.client_1.save_from_session")
    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_save_cookies_delegates_to_save_from_session(
        self, mock_path, mock_site_cls, mock_load, mock_wrap, mock_save
    ):
        mock_site_cls.return_value.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("en", "wikipedia", "bot", "pass")
        # Reset mock to clear calls from __init__ (though save_from_session
        # is not called in __init__ unless login happens)
        mock_save.reset_mock()

        client.save_cookies()

        mock_save.assert_called_once_with(client._site.connection, client._cookie_path)


class TestClientRequestPaths:
    """Covers lines 214, 220, and 230-231 of client_request."""

    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_client_request_get(self, mock_path, mock_site_cls, mock_load, mock_wrap):
        """GET path: session.request called with method 'GET' and params."""
        site_instance = mock_site_cls.return_value
        site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}
        site_instance.connection = MagicMock()
        site_instance.api_url = "http://example.com/api"

        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = {"batchcomplete": ""}
        site_instance.connection.request.return_value = response

        client = WikiLoginClient("en", "wikipedia", "bot", "pass")
        result = client.client_request({"action": "query", "titles": "Python"}, method="get")

        expected_params = {"format": "json", "action": "query", "titles": "Python"}
        site_instance.connection.request.assert_called_once_with(
            "GET", "http://example.com/api", params=expected_params
        )
        assert result == {"batchcomplete": ""}

    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_client_request_post_no_files(self, mock_path, mock_site_cls, mock_load, mock_wrap):
        """POST without files: session.request called with 'POST' and data."""
        site_instance = mock_site_cls.return_value
        site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}
        site_instance.connection = MagicMock()
        site_instance.api_url = "http://example.com/api"

        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = {"edit": {"result": "Success"}}
        site_instance.connection.request.return_value = response

        client = WikiLoginClient("en", "wikipedia", "bot", "pass")
        params = {"action": "edit", "title": "Sandbox", "text": "hello"}
        result = client.client_request(params, method="post")

        expected_params = {"format": "json", "action": "edit", "title": "Sandbox", "text": "hello"}
        site_instance.connection.request.assert_called_once_with(
            "POST", "http://example.com/api", data=expected_params
        )
        assert result == {"edit": {"result": "Success"}}

    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_client_request_api_error_raises_wiki_client_error(
        self, mock_path, mock_site_cls, mock_load, mock_wrap
    ):
        """API error in response body raises WikiClientError (lines 230-231)."""
        site_instance = mock_site_cls.return_value
        site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}
        site_instance.connection = MagicMock()
        site_instance.api_url = "http://example.com/api"

        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = {"error": {"code": "unknownaction", "info": "Unrecognized value for parameter 'action'"}}
        site_instance.connection.request.return_value = response

        client = WikiLoginClient("en", "wikipedia", "bot", "pass")
        with pytest.raises(WikiClientError, match="API error unknownaction"):
            client.client_request({"action": "badaction"})


class TestEnsureLoggedIn:
    """Covers lines 247-249 (exception path) and 261-267 (anonymous session)."""

    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_ensure_logged_in_valid_session_skips_login(self, mock_path, mock_site_cls, mock_load, mock_wrap):
        """When user_id != 0, _do_login should NOT be called (lines 251-259)."""
        site_instance = mock_site_cls.return_value
        site_instance.api.return_value = {"query": {"userinfo": {"id": 42}}}
        client = WikiLoginClient("en", "wikipedia", "bot", "pass")
        # _ensure_logged_in was already called during __init__.
        # Calling it again explicitly to verify the valid-session path.
        with patch.object(client, "_do_login") as mock_do_login:
            client._ensure_logged_in()
            mock_do_login.assert_not_called()

    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_ensure_logged_in_api_exception_calls_login(self, mock_path, mock_site_cls, mock_load, mock_wrap):
        """When site.api raises, _do_login should be called (lines 247-249)."""
        site_instance = mock_site_cls.return_value
        # First call in __init__ succeeds, so client can be constructed.
        site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("en", "wikipedia", "bot", "pass")

        # Now make api raise for the explicit _ensure_logged_in call.
        site_instance.api.side_effect = RuntimeError("network error")
        with patch.object(client, "_do_login") as mock_do_login:
            client._ensure_logged_in()
            mock_do_login.assert_called_once()

    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_ensure_logged_in_anonymous_session_calls_login(self, mock_path, mock_site_cls, mock_load, mock_wrap):
        """When user_id == 0, _do_login should be called (lines 261-267)."""
        site_instance = mock_site_cls.return_value
        site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("en", "wikipedia", "bot", "pass")

        # Now return anonymous user.
        site_instance.api.return_value = {"query": {"userinfo": {"id": 0}}}
        site_instance.api.side_effect = None
        with patch.object(client, "_do_login") as mock_do_login:
            client._ensure_logged_in()
            mock_do_login.assert_called_once()


class TestDoLogin:
    """Covers lines 276-287 (success) and 278-279 (LoginError)."""

    @patch("src.core.wiki_client.client_1.save_from_session")
    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_do_login_success(self, mock_path, mock_site_cls, mock_load, mock_wrap, mock_save):
        """Successful login calls site.login and save_from_session (lines 276-287)."""
        site_instance = mock_site_cls.return_value
        site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}
        client = WikiLoginClient("en", "wikipedia", "bot", "pass")

        # Reset save mock to isolate _do_login call.
        mock_save.reset_mock()

        client._do_login()

        site_instance.login.assert_called_with("bot", "pass")
        mock_save.assert_called_once_with(site_instance.connection, client._cookie_path)

    @patch("src.core.wiki_client.client_1.save_from_session")
    @patch("src.core.wiki_client.client_1.wrap_session")
    @patch("src.core.wiki_client.client_1.load_into_session")
    @patch("src.core.wiki_client.client_1.mwclient.Site")
    @patch("src.core.wiki_client.client_1.get_cookie_path")
    def test_do_login_login_error(self, mock_path, mock_site_cls, mock_load, mock_wrap, mock_save):
        """When site.login raises LoginError, our LoginError is raised (lines 278-279)."""
        site_instance = mock_site_cls.return_value
        site_instance.api.return_value = {"query": {"userinfo": {"id": 1}}}
        site_instance.login.side_effect = mwclient.errors.LoginError(site_instance, "IncorrectPassword", "wrong password")
        client = WikiLoginClient("en", "wikipedia", "bot", "pass")

        with pytest.raises(LoginError, match="Login failed for bot"):
            client._do_login()
