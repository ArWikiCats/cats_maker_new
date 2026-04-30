"""
Unit tests for src/core/new_c18/io/json_store.py module.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.new_c18.io.json_store import JsonStore, _load_json, _save_json


class TestLoadJson:
    def test_loads_list(self, tmp_path):
        path = tmp_path / "test.json"
        path.write_text(json.dumps(["a", "b"]), encoding="utf-8")
        result = _load_json(path)
        assert result == ["a", "b"]

    def test_loads_dict(self, tmp_path):
        path = tmp_path / "test.json"
        path.write_text(json.dumps({"key": "val"}), encoding="utf-8")
        result = _load_json(path, empty_data="dict")
        assert result == {"key": "val"}

    def test_creates_missing_file_as_list(self, tmp_path):
        path = tmp_path / "missing.json"
        result = _load_json(path)
        assert result == []

    def test_creates_missing_file_as_dict(self, tmp_path):
        path = tmp_path / "missing.json"
        result = _load_json(path, empty_data="dict")
        assert result == {}

    def test_handles_invalid_json(self, tmp_path):
        path = tmp_path / "bad.json"
        path.write_text("not json", encoding="utf-8")
        result = _load_json(path)
        assert result == []


class TestSaveJson:
    def test_saves_list(self, tmp_path):
        path = tmp_path / "test.json"
        _save_json(["a", "b"], path)
        with open(path, encoding="utf-8") as f:
            assert json.load(f) == ["a", "b"]

    def test_saves_dict(self, tmp_path):
        path = tmp_path / "test.json"
        _save_json({"key": "val"}, path)
        with open(path, encoding="utf-8") as f:
            assert json.load(f) == {"key": "val"}


class TestJsonStore:
    def test_load(self, tmp_path):
        path = tmp_path / "store.json"
        path.write_text(json.dumps([1, 2]), encoding="utf-8")
        store = JsonStore(path)
        assert store.load() == [1, 2]

    def test_save(self, tmp_path):
        path = tmp_path / "store.json"
        store = JsonStore(path)
        store.save([3, 4])
        with open(path, encoding="utf-8") as f:
            assert json.load(f) == [3, 4]

    def test_is_stale_true_for_missing(self, tmp_path):
        path = tmp_path / "missing.json"
        store = JsonStore(path)
        assert store.is_stale() is True

    def test_is_stale_true_for_old_file(self, tmp_path):
        path = tmp_path / "old.json"
        path.write_text("[]", encoding="utf-8")
        old_time = datetime.now() - timedelta(days=2)
        os.utime(path, (old_time.timestamp(), old_time.timestamp()))
        store = JsonStore(path)
        assert store.is_stale(days=1) is True

    def test_is_stale_false_for_fresh_file(self, tmp_path):
        path = tmp_path / "fresh.json"
        path.write_text("[]", encoding="utf-8")
        store = JsonStore(path)
        assert store.is_stale(days=1) is False
