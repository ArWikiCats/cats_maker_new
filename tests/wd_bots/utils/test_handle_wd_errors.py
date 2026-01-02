"""
Tests for src/wd_bots/utils/handle_wd_errors.py

This module tests Wikidata error handling functions.
"""

import pytest

from src.wd_bots.utils.handle_wd_errors import (
    WD_ERRORS_HANDLER,
)


class TestWDErrorsHandler:
    """Tests for WD_ERRORS_HANDLER class"""

    def test_instantiation(self):
        """Test that class can be instantiated"""
        handler = WD_ERRORS_HANDLER()
        assert handler is not None

    def test_handle_abusefilter_error(self):
        """Test handling of abusefilter-disallowed error"""
        handler = WD_ERRORS_HANDLER()
        error = {"code": "abusefilter-disallowed", "abusefilter": {"description": "Test filter"}}

        result = handler.handle_err_wd(error)

        assert result == "Test filter"

    def test_handle_bot_delay_filter(self):
        """Test handling of bot delay filter"""
        handler = WD_ERRORS_HANDLER()
        error = {"code": "abusefilter-disallowed", "abusefilter": {"description": "تأخير البوتات 3 ساعات"}}

        result = handler.handle_err_wd(error)

        assert result is False

    def test_handle_no_such_entity_error(self):
        """Test handling of no-such-entity error"""
        handler = WD_ERRORS_HANDLER()
        error = {"code": "no-such-entity"}

        result = handler.handle_err_wd(error)

        assert result is False

    def test_handle_protectedpage_error(self):
        """Test handling of protectedpage error"""
        handler = WD_ERRORS_HANDLER()
        error = {"code": "protectedpage"}

        result = handler.handle_err_wd(error)

        assert result is False

    def test_handle_articleexists_error(self):
        """Test handling of articleexists error"""
        handler = WD_ERRORS_HANDLER()
        error = {"code": "articleexists"}

        result = handler.handle_err_wd(error)

        assert result == "articleexists"

    def test_handle_maxlag_error(self):
        """Test handling of maxlag error"""
        handler = WD_ERRORS_HANDLER()
        error = {"code": "maxlag"}

        result = handler.handle_err_wd(error)

        assert result is False

    def test_handle_unknown_error(self):
        """Test handling of unknown error"""
        handler = WD_ERRORS_HANDLER()
        error = {"code": "unknown_error", "info": "Unknown error occurred"}
        params = {"data": {"test": "data"}}

        result = handler.handle_err_wd(error, params=params)

        # Should clear data in params
        assert params["data"] == {}

    def test_extracts_error_code(self):
        """Test that error code is extracted"""
        handler = WD_ERRORS_HANDLER()
        error = {"code": "test_code", "info": "Test info"}
        params = {"data": {"test": "data"}}

        # Should not raise error - params must be provided
        handler.handle_err_wd(error, function="test_func", params=params)

    def test_extracts_error_info(self):
        """Test that error info is extracted"""
        handler = WD_ERRORS_HANDLER()
        error = {"code": "unknown", "info": "Test error info"}
        params = {"data": {}}

        handler.handle_err_wd(error, params=params)

        # Should process without error
