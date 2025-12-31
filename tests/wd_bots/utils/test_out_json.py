"""
Tests for src/wd_bots/utils/out_json.py
"""

import pytest

from src.wd_bots.utils.out_json import (
    outbot_json_bot,
    outbot_json,
)


class TestOutbotJsonBot:
    """Tests for outbot_json_bot function"""

    def test_origin_not_empty_error(self, mocker):
        """Test handling of origin-not-empty error"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "origin-not-empty",
            "info": "Can't create redirect on non empty item Q65686922",
            "messages": [
                {
                    "name": "wikibase-api-origin-not-empty",
                    "parameters": ["Can't create redirect on non empty item Q65686922"],
                    "html": {"*": "Can't create redirect on non empty item Q65686922"},
                }
            ],
        }

        result = outbot_json_bot(err)
        assert result == "origin-not-empty"

    def test_missingparam_error(self, mocker):
        """Test handling of missingparam error"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "missingparam",
            "info": 'The "token" parameter must be set.',
        }

        result = outbot_json_bot(err)
        assert result == "warn"

    def test_modification_failed_with_failed_modify(self, mocker):
        """Test modification-failed with wikibase-api-failed-modify message"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "failed-modify",
            "info": "Attempted modification of the Item failed.",
            "extradata": ["Conflicting sitelinks for arwiki"],
            "messages": [
                {
                    "name": "wikibase-api-failed-modify",
                    "parameters": [],
                    "html": {"*": "Attempted modification of the Item failed."},
                }
            ],
        }

        result = outbot_json_bot(err)
        assert result == "wikibase-api-failed-modify"

    def test_modification_failed_with_label_equals_description(self, mocker):
        """Test modification-failed with label equals description error"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "modification-failed",
            "info": "Label and description for language code ar can not have the same value.",
            "messages": [
                {
                    "name": "wikibase-validator-label-equals-description",
                    "parameters": ["ar"],
                    "html": {"*": "لا يمكن أن تكون للتسمية والوصف لرمز اللغة ar نفس القيمة."},
                }
            ],
        }

        result = outbot_json_bot(err)
        assert result == "wikibase-validator-label-equals-description"

    def test_modification_failed_with_label_description_conflict(self, mocker):
        """Test modification-failed with label-description conflict"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "modification-failed",
            "info": 'Item [[Q116681602|Q116681602]] already has label "منحوتة1" associated with language code ar',
            "messages": [
                {
                    "name": "wikibase-validator-label-with-description-conflict",
                    "parameters": ["منحوتة1", "ar", "[[Q116681602|Q116681602]]"],
                    "html": {"*": "Item has label"},
                }
            ],
        }

        result = outbot_json_bot(err)
        assert result == "same description"

    def test_unresolved_redirect_error(self, mocker):
        """Test handling of unresolved-redirect error"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "unresolved-redirect",
            "info": "The given entity ID refers to a redirect, which is not supported in this context.",
        }

        result = outbot_json_bot(err)
        assert result == "unresolved-redirect"

    def test_failed_save_with_throttle(self, mocker):
        """Test failed-save error with throttle message"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")
        mock_sleep = mocker.patch("src.wd_bots.utils.out_json.time.sleep")

        err = {
            "code": "failed-save",
            "info": "The save has failed.",
            "messages": [
                {
                    "name": "actionthrottledtext",
                    "html": {"*": "احترازًا من الإساء، يُحظر إجراء هذا الفعل مرات كثيرة في فترةٍ زمنية قصيرة، ولقد تجاوزت هذا الحد"},
                }
            ],
        }

        result = outbot_json_bot(err)
        assert result == "reagain"
        mock_sleep.assert_called_once_with(5)

    def test_failed_save_without_throttle(self, mocker):
        """Test failed-save error without throttle message"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "failed-save",
            "info": "The save has failed.",
        }

        result = outbot_json_bot(err)
        assert result is False

    def test_no_external_page_error(self, mocker):
        """Test handling of no-external-page error"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "no-external-page",
            "info": 'The external client site "enwiki" did not provide page information',
        }

        result = outbot_json_bot(err)
        assert result is False

    def test_invalid_json_error(self, mocker):
        """Test handling of wikibase-api-invalid-json error"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {"code": "some-error", "messages": [{"name": "wikibase-api-invalid-json"}]}

        # Convert to string since function checks string representation
        import json
        err_str = json.dumps(err)

        # Create a dict-like object that has the string "wikibase-api-invalid-json" when converted to str
        class ErrorDict(dict):
            def __str__(self):
                return err_str

        result = outbot_json_bot(ErrorDict(err))
        assert result == "wikibase-api-invalid-json"

    def test_no_item_with_sitelink_error(self, mocker):
        """Test handling of 'Could not find an Item' error"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "some-error",
            "info": "Could not find an Item containing a sitelink to the provided site and page name",
        }

        # Convert to errordict with proper string representation
        class ErrorDict(dict):
            def __str__(self):
                return "Could not find an Item containing a sitelink to the provided site and page name"

        result = outbot_json_bot(ErrorDict(err))
        assert result == "Could not find an Item containing a sitelink to the provided site and page name"

    def test_unknown_error_code(self, mocker):
        """Test handling of unknown error code"""
        from src.wd_bots.utils.out_json import outbot_json_bot

        mocker.patch("src.wd_bots.utils.out_json.logger")

        err = {
            "code": "unknown-error",
            "info": "Some unknown error occurred",
        }

        result = outbot_json_bot(err)
        assert result == "unknown-error"


class TestOutbotJson:
    """Tests for outbot_json function"""

    def test_success_response(self, mocker):
        """Test handling of successful response"""
        from src.wd_bots.utils.out_json import outbot_json

        mocker.patch("src.wd_bots.utils.out_json.logger")

        js_text = {
            "success": 1,
            "entity": {"id": "Q12345", "type": "item"},
        }

        result = outbot_json(js_text)
        assert result is True

    def test_no_error_key(self, mocker):
        """Test handling when no error key is present"""
        from src.wd_bots.utils.out_json import outbot_json

        mocker.patch("src.wd_bots.utils.out_json.logger")

        js_text = {"success": 0}

        result = outbot_json(js_text)
        assert result == "warn"

    def test_delegates_to_outbot_json_bot(self, mocker):
        """Test that errors are delegated to outbot_json_bot"""
        from src.wd_bots.utils.out_json import outbot_json

        mocker.patch("src.wd_bots.utils.out_json.logger")
        mock_outbot_json_bot = mocker.patch(
            "src.wd_bots.utils.out_json.outbot_json_bot",
            return_value="test-error-code"
        )

        js_text = {
            "success": 0,
            "error": {"code": "test-error", "info": "Test error"},
        }

        result = outbot_json(js_text)

        assert result == "test-error-code"
        mock_outbot_json_bot.assert_called_once_with({"code": "test-error", "info": "Test error"})

    def test_logs_file_info(self, mocker):
        """Test that file info is logged when provided"""
        from src.wd_bots.utils.out_json import outbot_json

        mock_logger = mocker.patch("src.wd_bots.utils.out_json.logger")
        mocker.patch("src.wd_bots.utils.out_json.outbot_json_bot", return_value="error")

        js_text = {"error": {"code": "test", "info": "info"}}

        outbot_json(js_text, fi="test_file.py")

        # Verify logger.debug was called with file info
        assert any("test_file.py" in str(call) for call in mock_logger.debug.call_args_list)

    def test_logs_line_info(self, mocker):
        """Test that line info is logged when provided"""
        from src.wd_bots.utils.out_json import outbot_json

        mock_logger = mocker.patch("src.wd_bots.utils.out_json.logger")
        mocker.patch("src.wd_bots.utils.out_json.outbot_json_bot", return_value="error")

        js_text = {"error": {"code": "test", "info": "info"}}

        outbot_json(js_text, line="123")

        # Verify logger.debug was called with line info
        assert any("123" in str(call) for call in mock_logger.debug.call_args_list)
