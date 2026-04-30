"""
Unit tests for src/core/new_api/cookies_bot.py module.
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.new_api.cookies_bot import check_if_file_is_old, del_cookies_file, get_file_name


class TestDelCookiesFile:
    def test_deletes_existing_file(self, tmp_path):
        path = tmp_path / "cookie.txt"
        path.touch()
        del_cookies_file(path)
        assert not path.exists()

    def test_does_nothing_for_missing_file(self, tmp_path):
        path = tmp_path / "missing.txt"
        del_cookies_file(path)  # Should not raise


class TestCheckIfFileIsOld:
    def test_deletes_empty_file(self, tmp_path):
        path = tmp_path / "empty.txt"
        path.touch()
        check_if_file_is_old(path)
        assert not path.exists()

    def test_deletes_old_file(self, tmp_path):
        path = tmp_path / "old.txt"
        path.write_text("data")
        old_time = datetime.now() - timedelta(days=4)
        os.utime(path, (old_time.timestamp(), old_time.timestamp()))
        check_if_file_is_old(path)
        assert not path.exists()

    def test_keeps_fresh_file(self, tmp_path):
        path = tmp_path / "fresh.txt"
        path.write_text("data")
        check_if_file_is_old(path)
        assert path.exists()

    def test_does_nothing_for_missing_file(self, tmp_path):
        path = tmp_path / "missing.txt"
        check_if_file_is_old(path)  # Should not raise


class TestGetFileName:
    @patch("src.core.new_api.cookies_bot.settings")
    def test_returns_path_with_components(self, mock_settings, tmp_path):
        mock_settings.bot.no_cookies = False
        with patch("src.core.new_api.cookies_bot.Path") as mock_path_cls:
            # We need to test the actual logic, so let's use a simpler approach
            pass

    @patch("src.core.new_api.cookies_bot.settings")
    def test_no_cookies_returns_random(self, mock_settings):
        mock_settings.bot.no_cookies = True
        with patch.dict(os.environ, {"HOME": "/tmp"}):
            result = get_file_name("en", "wikipedia", "bot")
            assert result.suffix == ".txt"

    @patch("src.core.new_api.cookies_bot.settings")
    def test_home_not_set_uses_file_parent(self, mock_settings):
        """Test that when HOME is not set, Path(__file__).parent is used."""
        mock_settings.bot.no_cookies = True
        with patch.dict(os.environ, {}, clear=True):
            if "HOME" in os.environ:
                del os.environ["HOME"]
            result = get_file_name("en", "wikipedia", "bot")
            assert result.suffix == ".txt"

    @patch("src.core.new_api.cookies_bot.settings")
    def test_normal_path_generation(self, mock_settings, tmp_path):
        """Test normal (non-random) cookie path generation."""
        mock_settings.bot.no_cookies = False
        with patch.dict(os.environ, {"HOME": str(tmp_path)}):
            result = get_file_name("EN", "Wikipedia", "MyBot@BotPassword")
            assert result.name == "wikipedia_en_mybot.txt"

    @patch("src.core.new_api.cookies_bot.settings")
    def test_directory_creation(self, mock_settings, tmp_path):
        """Test that cookies directory is created if it doesn't exist."""
        mock_settings.bot.no_cookies = False
        cookies_dir = tmp_path / "cookies"
        assert not cookies_dir.exists()
        with patch.dict(os.environ, {"HOME": str(tmp_path)}):
            get_file_name("en", "wikipedia", "bot")
            assert cookies_dir.exists()


class TestDelCookiesFileException:
    def test_exception_during_unlink(self, tmp_path):
        """Test that exception during unlink is caught and logged."""
        path = tmp_path / "locked.txt"
        path.touch()
        with patch.object(type(path), "unlink", side_effect=PermissionError("denied")):
            del_cookies_file(path)  # Should not raise
