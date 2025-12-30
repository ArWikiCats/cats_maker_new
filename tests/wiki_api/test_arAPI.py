"""
Tests for src/wiki_api/arAPI.py

This module tests Wikipedia page manipulation functions.
"""

import pytest

from src.wiki_api.arAPI import (
    Add_To_Bottom,
    Add_To_Head,
    create_Page,
    page_put,
)


class TestAddToHead:
    """Tests for Add_To_Head function"""

    def test_returns_false_for_empty_title(self, mocker):
        """Test that Add_To_Head returns False for empty title"""
        result = Add_To_Head("text", "summary", "", False)
        assert result is False

    def test_returns_false_for_whitespace_title(self, mocker):
        """Test that Add_To_Head returns False for whitespace-only title"""
        result = Add_To_Head("text", "summary", "   ", False)
        assert result is False

    def test_returns_false_for_empty_prependtext(self, mocker):
        """Test that Add_To_Head returns False for empty prepend text"""
        result = Add_To_Head("", "summary", "Test Page", False)
        assert result is False

    def test_returns_false_for_whitespace_prependtext(self, mocker):
        """Test that Add_To_Head returns False for whitespace-only prepend text"""
        result = Add_To_Head("   ", "summary", "Test Page", False)
        assert result is False


class TestAddToBottom:
    """Tests for Add_To_Bottom function"""

    def test_returns_false_for_empty_title(self, mocker):
        """Test that Add_To_Bottom returns False for empty title"""
        result = Add_To_Bottom("text", "summary", "", False)
        assert result is False

    def test_returns_false_for_whitespace_title(self, mocker):
        """Test that Add_To_Bottom returns False for whitespace-only title"""
        result = Add_To_Bottom("text", "summary", "   ", False)
        assert result is False

    def test_returns_false_for_empty_appendtext(self, mocker):
        """Test that Add_To_Bottom returns False for empty append text"""
        result = Add_To_Bottom("", "summary", "Test Page", False)
        assert result is False

    def test_returns_false_for_whitespace_appendtext(self, mocker):
        """Test that Add_To_Bottom returns False for whitespace-only append text"""
        result = Add_To_Bottom("   ", "summary", "Test Page", False)
        assert result is False


class TestCreatePage:
    """Tests for create_Page function"""

    def test_returns_false_for_empty_text(self, mocker):
        """Test that create_Page returns False for empty text"""
        mocker.patch("src.wiki_api.arAPI.MainPage")
        result = create_Page("", "summary", "Test Page", False)
        assert result is False

    def test_returns_false_for_talk_sandbox_pages(self, mocker):
        """Test that create_Page returns False for talk namespace sandbox pages"""
        result = create_Page("text", "summary", "نقاش القالب:Test/ملعب", False)
        assert result is False


class TestPagePut:
    """Tests for page_put function"""

    def test_accepts_required_parameters(self):
        """Test that page_put accepts its parameters"""
        # This test verifies the function signature
        import inspect

        sig = inspect.signature(page_put)
        params = sig.parameters

        assert "oldtext" in params
        assert "newtext" in params
        assert "summary" in params
        assert "title" in params

    def test_accepts_optional_parameters(self):
        """Test that page_put accepts optional parameters"""
        import inspect

        sig = inspect.signature(page_put)
        params = sig.parameters

        assert "minor" in params
        assert "nocreate" in params
        assert "tags" in params
        assert "nodiff" in params


class TestFunctionSignatures:
    """Tests for function signatures and parameters"""

    def test_add_to_head_signature(self):
        """Test Add_To_Head function signature"""
        import inspect

        sig = inspect.signature(Add_To_Head)
        params = list(sig.parameters.keys())

        assert "prependtext" in params
        assert "summary" in params
        assert "title" in params

    def test_add_to_bottom_signature(self):
        """Test Add_To_Bottom function signature"""
        import inspect

        sig = inspect.signature(Add_To_Bottom)
        params = list(sig.parameters.keys())

        assert "appendtext" in params
        assert "summary" in params
        assert "title" in params

    def test_create_page_signature(self):
        """Test create_Page function signature"""
        import inspect

        sig = inspect.signature(create_Page)
        params = list(sig.parameters.keys())

        assert "text" in params
        assert "summary" in params
        assert "title" in params
        assert "ask" in params
