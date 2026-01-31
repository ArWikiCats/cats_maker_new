"""
Tests for src/wd_bots/bot_wd.py

This module tests the WD_Functions class.
"""

from src.wd_bots.bot_wd import (
    WD_Functions,
)


class TestWDFunctions:
    """Tests for WD_Functions class"""

    def test_instantiation(self):
        """Test that WD_Functions can be instantiated"""
        wd = WD_Functions()
        assert wd is not None

    def test_format_labels_descriptions(self):
        """Test format_labels_descriptions method"""
        wd = WD_Functions()
        labels = {"en": {"language": "en", "value": "Science"}, "ar": {"language": "ar", "value": "علوم"}}

        result = wd.format_labels_descriptions(labels)

        assert result["en"] == "Science"
        assert result["ar"] == "علوم"

    def test_format_labels_descriptions_empty(self):
        """Test format_labels_descriptions with empty input"""
        wd = WD_Functions()
        result = wd.format_labels_descriptions({})
        assert result == {}

    def test_pages_with_prop(self, mocker):
        """Test _pages_with_prop method"""
        wd = WD_Functions()

        mock_post_continue = mocker.MagicMock(
            return_value=[{"title": "Page1", "value": "Q123"}, {"title": "Page2", "value": "Q456"}]
        )

        result = wd._pages_with_prop(mock_post_continue)

        mock_post_continue.assert_called_once()
        assert len(result) == 2

    def test_pages_with_prop_custom_propname(self, mocker):
        """Test _pages_with_prop with custom property name"""
        wd = WD_Functions()

        mock_post_continue = mocker.MagicMock(return_value=[])

        wd._pages_with_prop(mock_post_continue, pwppropname="custom_prop")

        call_args = mock_post_continue.call_args[0][0]
        assert call_args["pwppropname"] == "custom_prop"
