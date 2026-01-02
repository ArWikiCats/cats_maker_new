"""
Tests for src/wd_bots/utils/out_json.py

This module tests JSON output handling functions.
"""

import pytest

from src.wd_bots.utils.out_json import (
    outbot_json_bot,
    outbot_json,
)


class TestOutbotJsonBot:
    """Tests for outbot_json_bot function"""

    def test_handles_origin_not_empty_error(self):
        """Test handling of origin-not-empty error"""
        err = {
            "code": "origin-not-empty",
            "info": "Can't create redirect on non empty item Q123",
            "messages": [{"html": {"*": "Can't create redirect"}}],
        }

        result = outbot_json_bot(err)

        assert result == "origin-not-empty"

    def test_handles_missingparam_error(self):
        """Test handling of missingparam error"""
        err = {"code": "missingparam", "info": 'The "token" parameter must be set.'}

        result = outbot_json_bot(err)

        assert result == "warn"

    def test_handles_modification_failed_error(self):
        """Test handling of modification-failed error"""
        err = {
            "code": "modification-failed",
            "info": "Modification failed",
            "messages": [{"name": "wikibase-api-failed-modify", "html": {"*": "Failed"}}],
            "extradata": ["Conflicting sitelinks"],
        }

        result = outbot_json_bot(err)

        assert result == "wikibase-api-failed-modify"

    def test_handles_label_equals_description(self):
        """Test handling of label equals description error"""
        err = {
            "code": "modification-failed",
            "messages": [
                {
                    "name": "wikibase-validator-label-equals-description",
                    "parameters": ["ar"],
                    "html": {"*": "Label equals description"},
                }
            ],
        }

        result = outbot_json_bot(err)

        assert result == "wikibase-validator-label-equals-description"

    def test_handles_label_with_description_conflict(self):
        """Test handling of label with description conflict"""
        err = {
            "code": "modification-failed",
            "messages": [
                {
                    "name": "wikibase-validator-label-with-description-conflict",
                    "parameters": ["Test", "ar", "[[Q123|Q123]]"],
                    "html": {"*": "Conflict"},
                }
            ],
        }

        result = outbot_json_bot(err)

        assert result == "same description"

    def test_handles_unresolved_redirect(self):
        """Test handling of unresolved-redirect error"""
        err = {"code": "unresolved-redirect", "info": "Entity refers to redirect"}

        result = outbot_json_bot(err)

        assert result == "unresolved-redirect"

    def test_handles_failed_save_with_throttle(self, mocker):
        """Test handling of failed-save with throttle"""
        mock_sleep = mocker.patch("src.wd_bots.utils.out_json.time.sleep")

        # Use the exact error text that the code checks for
        err_wait = "احترازًا من الإساء، يُحظر إجراء هذا الفعل مرات كثيرة في فترةٍ زمنية قصيرة، ولقد تجاوزت هذا الحد"
        err = {"code": "failed-save", "info": err_wait, "messages": [{"html": {"*": err_wait}}]}

        result = outbot_json_bot(err)

        assert result == "reagain"
        mock_sleep.assert_called_with(5)

    def test_handles_no_external_page(self):
        """Test handling of no-external-page error"""
        err = {"code": "no-external-page", "info": "No external page found"}

        result = outbot_json_bot(err)

        assert result is False

    def test_handles_invalid_json(self):
        """Test handling of invalid JSON error"""
        err = {"code": "other", "info": "wikibase-api-invalid-json error"}

        result = outbot_json_bot(err)

        assert result == "wikibase-api-invalid-json"


class TestOutbotJson:
    """Tests for outbot_json function"""

    def test_returns_true_on_success(self):
        """Test that True is returned on success"""
        js_text = {"success": 1}

        result = outbot_json(js_text)

        assert result is True

    def test_returns_warn_on_no_error(self):
        """Test that 'warn' is returned when no error"""
        js_text = {"success": 0}

        result = outbot_json(js_text)

        assert result == "warn"

    def test_delegates_to_outbot_json_bot(self):
        """Test that error handling is delegated"""
        js_text = {"success": 0, "error": {"code": "origin-not-empty", "info": "Test error"}}

        result = outbot_json(js_text)

        assert result == "origin-not-empty"

    def test_handles_entity_response(self):
        """Test handling of entity response"""
        js_text = {"success": 1, "entity": {"id": "Q123", "sitelinks": {}}}

        result = outbot_json(js_text)

        assert result is True
