"""
Tests for src/wd_bots/utils/handle_wd_errors.py
"""

import pytest


class TestWDErrorsHandler:
    """Tests for WD_ERRORS_HANDLER class"""

    def test_init_logs_creation(self, mocker):
        """Test that __init__ logs class creation"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mock_logger = mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()

        mock_logger.debug.assert_called_with("class WD_ERRORS_HANDLER:")

    def test_abusefilter_disallowed_with_bot_delay(self, mocker):
        """Test handling of abusefilter-disallowed with bot delay"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "abusefilter-disallowed",
            "info": "This action has been automatically identified as harmful",
            "abusefilter": {
                "id": "169",
                "description": "تأخير البوتات 3 ساعات",
                "actions": ["disallow"],
            },
        }

        result = handler.handle_err_wd(error, "test_function")
        assert result is False

    def test_abusefilter_disallowed_with_custom_description(self, mocker):
        """Test abusefilter-disallowed with non-bot-delay description"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "abusefilter-disallowed",
            "info": "This action has been automatically identified as harmful",
            "abusefilter": {
                "id": "123",
                "description": "Custom filter description",
                "actions": ["disallow"],
            },
        }

        result = handler.handle_err_wd(error, "test_function")
        assert result == "Custom filter description"

    def test_no_such_entity_error(self, mocker):
        """Test handling of no-such-entity error"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "no-such-entity",
            "info": "The specified entity does not exist",
        }

        result = handler.handle_err_wd(error, "test_function")
        assert result is False

    def test_protectedpage_error(self, mocker):
        """Test handling of protectedpage error"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "protectedpage",
            "info": "This page is protected",
        }

        result = handler.handle_err_wd(error, "test_function")
        assert result is False

    def test_articleexists_error(self, mocker):
        """Test handling of articleexists error"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "articleexists",
            "info": "The article you tried to create has been created already",
        }

        result = handler.handle_err_wd(error, "test_function")
        assert result == "articleexists"

    def test_maxlag_error(self, mocker):
        """Test handling of maxlag error"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "maxlag",
            "info": "Maximum lag exceeded",
            "lag": 10,
        }

        result = handler.handle_err_wd(error, "test_function")
        assert result is False

    def test_modifies_params_data_for_unknown_error(self, mocker):
        """Test that params['data'] is set to {} for unknown errors"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "unknown-error",
            "info": "An unknown error occurred",
        }
        params = {"data": "original_data"}

        handler.handle_err_wd(error, "test_function", params)
        assert params["data"] == {}

    def test_raises_exception_when_raise_in_argv(self, mocker):
        """Test that exception is raised when 'raise' in sys.argv"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")
        mocker.patch("src.wd_bots.utils.handle_wd_errors.sys.argv", ["script.py", "raise"])

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "unknown-error",
            "info": "An unknown error occurred",
        }
        params = {"data": {}}

        with pytest.raises(Exception) as exc_info:
            handler.handle_err_wd(error, "test_function", params)

        assert exc_info.value.args[0] == error

    def test_logs_error_code_and_function(self, mocker):
        """Test that error code and function name are logged"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mock_logger = mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "test-error",
            "info": "Test error info",
        }
        params = {"data": {}}

        handler.handle_err_wd(error, "my_function", params)

        # Verify function name and error code were logged
        debug_calls = [str(call) for call in mock_logger.debug.call_args_list]
        assert any("my_function" in call and "test-error" in call for call in debug_calls)

    def test_handles_missing_abusefilter_key(self, mocker):
        """Test handling when abusefilter key is missing"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "abusefilter-disallowed",
            "info": "This action has been automatically identified as harmful",
        }
        params = {"data": {}}

        # Should not raise an exception
        result = handler.handle_err_wd(error, "test_function", params)
        # Should return empty string since description.get() returns ""
        assert result == ""

    def test_handles_none_params(self, mocker):
        """Test handling when params is None"""
        from src.wd_bots.utils.handle_wd_errors import WD_ERRORS_HANDLER

        mocker.patch("src.wd_bots.utils.handle_wd_errors.logger")
        mocker.patch("src.wd_bots.utils.handle_wd_errors.sys.argv", [])

        handler = WD_ERRORS_HANDLER()
        error = {
            "code": "unknown-error",
            "info": "An unknown error occurred",
        }

        # Should raise AttributeError when trying to set params["data"]
        with pytest.raises(TypeError):
            handler.handle_err_wd(error, "test_function", None)
