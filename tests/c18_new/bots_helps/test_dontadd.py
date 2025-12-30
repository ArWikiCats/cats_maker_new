"""
Tests for src/c18_new/dontadd.py

This module tests the "don't add" list functionality for categories.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
import json

from src.c18_new.dontadd import (
    load_json,
    log_to_file,
    filename_json,
)


class TestFilenameJson:
    """Tests for filename_json path"""

    def test_is_path_object(self):
        """Test that filename_json is a Path object"""
        assert isinstance(filename_json, Path)

    def test_filename_ends_with_json(self):
        """Test that filename ends with .json"""
        assert str(filename_json).endswith(".json")

    def test_filename_contains_dont_add(self):
        """Test that filename contains 'Dont_add'"""
        assert "Dont_add" in str(filename_json)


class TestLoadJson:
    """Tests for load_json function"""

    def test_returns_list_by_default(self, tmp_path):
        """Test that load_json returns empty list by default"""
        # Test with non-existent file
        result = load_json(tmp_path / "nonexistent.json", empty_data="list")
        assert isinstance(result, list)

    def test_returns_dict_when_specified(self, tmp_path):
        """Test that load_json returns empty dict when specified"""
        result = load_json(tmp_path / "nonexistent_dict.json", empty_data="dict")
        assert isinstance(result, dict)

    def test_loads_existing_json_file(self, tmp_path):
        """Test that load_json loads existing JSON file"""
        test_file = tmp_path / "test.json"
        test_data = ["item1", "item2", "item3"]
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        result = load_json(test_file)
        assert result == test_data

    def test_loads_dict_from_file(self, tmp_path):
        """Test that load_json loads dict from existing file"""
        test_file = tmp_path / "test_dict.json"
        test_data = {"key1": "value1", "key2": "value2"}
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        result = load_json(test_file, empty_data="dict")
        assert result == test_data


class TestLogToFile:
    """Tests for log_to_file function"""

    def test_writes_list_to_file(self, tmp_path):
        """Test that log_to_file writes list to file"""
        test_file = tmp_path / "output.json"
        test_data = ["item1", "item2"]

        log_to_file(test_data, test_file)

        with open(test_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded == test_data

    def test_writes_dict_to_file(self, tmp_path):
        """Test that log_to_file writes dict to file"""
        test_file = tmp_path / "output_dict.json"
        test_data = {"key": "value"}

        log_to_file(test_data, test_file)

        with open(test_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded == test_data

    def test_writes_arabic_text_correctly(self, tmp_path):
        """Test that log_to_file handles Arabic text"""
        test_file = tmp_path / "arabic.json"
        test_data = ["تصنيف:علوم", "تصنيف:تاريخ"]

        log_to_file(test_data, test_file)

        with open(test_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded == test_data
        assert "تصنيف:علوم" in loaded


class TestIntegration:
    """Integration tests for dontadd module"""

    def test_round_trip_json(self, tmp_path):
        """Test that data can be saved and loaded correctly"""
        test_file = tmp_path / "roundtrip.json"
        original_data = ["page1", "قالب:اختبار", "Page 3"]

        log_to_file(original_data, test_file)
        loaded_data = load_json(test_file)

        assert loaded_data == original_data

    def test_empty_list_roundtrip(self, tmp_path):
        """Test that empty list can be saved and loaded"""
        test_file = tmp_path / "empty.json"

        log_to_file([], test_file)
        loaded = load_json(test_file)

        assert loaded == []
