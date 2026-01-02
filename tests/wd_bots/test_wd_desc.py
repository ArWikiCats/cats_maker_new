"""
Tests for src/wd_bots/wd_desc.py

This module tests Wikidata description functions.
"""

import pytest

from src.wd_bots.wd_desc import (
    del_keys,
    get_wd_api_bot,
    work_api_desc,
    wwdesc,
)


class TestDelKeys:
    """Tests for del_keys function"""

    def test_removes_en_gb(self):
        """Test that en-gb is removed"""
        translation_map = {"en": "test", "en-gb": "test", "ar": "اختبار"}
        result = del_keys(translation_map)

        assert "en-gb" not in result
        assert "en" in result

    def test_removes_en_ca(self):
        """Test that en-ca is removed"""
        translation_map = {"en": "test", "en-ca": "test"}
        result = del_keys(translation_map)

        assert "en-ca" not in result

    def test_removes_de_variants(self):
        """Test that de-at and de-ch are removed"""
        translation_map = {"de": "test", "de-at": "test", "de-ch": "test"}
        result = del_keys(translation_map)

        assert "de-at" not in result
        assert "de-ch" not in result
        assert "de" in result

    def test_removes_zh_variants(self):
        """Test that zh variants are removed"""
        translation_map = {
            "zh": "test",
            "zh-cn": "test",
            "zh-sg": "test",
            "zh-my": "test",
            "zh-hk": "test",
            "zh-mo": "test",
            "zh-tw": "test",
        }
        result = del_keys(translation_map)

        assert "zh-cn" not in result
        assert "zh-sg" not in result
        assert "zh" in result

    def test_returns_dict(self):
        """Test that function returns a dict"""
        result = del_keys({"en": "test"})
        assert isinstance(result, dict)

    def test_handles_empty_dict(self):
        """Test handling of empty dict"""
        result = del_keys({})
        assert result == {}


class TestGetWdApiBot:
    """Tests for get_wd_api_bot function"""

    def test_returns_api_bot(self, mocker):
        """Test that API bot is returned"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.wd_desc.NewHimoAPIBot", return_value=mock_bot)

        get_wd_api_bot.cache_clear()

        result = get_wd_api_bot()

        assert result is not None

    def test_caches_result(self, mocker):
        """Test that result is cached"""
        mock_bot = mocker.MagicMock()
        mock_class = mocker.patch("src.wd_bots.wd_desc.NewHimoAPIBot", return_value=mock_bot)

        get_wd_api_bot.cache_clear()

        get_wd_api_bot()
        get_wd_api_bot()

        assert mock_class.call_count == 1


class TestWwdesc:
    """Tests for wwdesc function"""

    def test_removes_language_variants(self, mocker):
        """Test that language variants are removed"""
        mock_bot = mocker.MagicMock()
        mock_bot.New_Mult_Des_2.return_value = '{"success": 1}'
        mocker.patch("src.wd_bots.wd_desc.get_wd_api_bot", return_value=mock_bot)

        NewDesc = {
            "en": {"language": "en", "value": "test"},
            "en-gb": {"language": "en-gb", "value": "test"},
        }

        wwdesc(NewDesc, "Q123", 1, [])

        # Should process without en-gb

    def test_skips_only_en_variants(self, mocker):
        """Test that function skips when only en-gb and en-ca"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.wd_desc.get_wd_api_bot", return_value=mock_bot)

        NewDesc = {
            "en-gb": {"language": "en-gb", "value": "test"},
            "en-ca": {"language": "en-ca", "value": "test"},
        }

        result = wwdesc(NewDesc, "Q123", 1, [])

        # Should skip and return None
        mock_bot.New_Mult_Des_2.assert_not_called()

    def test_returns_none_for_empty_queries(self, mocker):
        """Test that None is returned for empty queries"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.wd_desc.get_wd_api_bot", return_value=mock_bot)

        result = wwdesc({}, "Q123", 1, [])

        assert result is None


class TestWorkApiDesc:
    """Tests for work_api_desc function"""

    def test_removes_language_variants(self, mocker):
        """Test that language variants are removed"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.wd_desc.get_wd_api_bot", return_value=mock_bot)
        mocker.patch("src.wd_bots.wd_desc.wwdesc")

        NewDesc = {
            "en": {"language": "en", "value": "test"},
            "en-gb": {"language": "en-gb", "value": "test"},
        }

        work_api_desc(NewDesc, "Q123")

        # Should process

    def test_handles_single_language(self, mocker):
        """Test handling of single language"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.wd_desc.get_wd_api_bot", return_value=mock_bot)

        NewDesc = {"ar": {"language": "ar", "value": "اختبار"}}

        work_api_desc(NewDesc, "Q123")

        mock_bot.Des_API.assert_called_with("Q123", "اختبار", "ar")

    def test_skips_tg_latn_single_language(self, mocker):
        """Test that tg-latn is skipped when only language"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.wd_desc.get_wd_api_bot", return_value=mock_bot)

        NewDesc = {"tg-latn": {"language": "tg-latn", "value": "test"}}

        work_api_desc(NewDesc, "Q123")

        mock_bot.Des_API.assert_not_called()

    def test_calls_wwdesc_for_multiple_languages(self, mocker):
        """Test that wwdesc is called for multiple languages"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.wd_desc.get_wd_api_bot", return_value=mock_bot)
        mock_wwdesc = mocker.patch("src.wd_bots.wd_desc.wwdesc")

        NewDesc = {
            "en": {"language": "en", "value": "test"},
            "ar": {"language": "ar", "value": "اختبار"},
            "de": {"language": "de", "value": "Test"},
        }

        work_api_desc(NewDesc, "Q123")

        mock_wwdesc.assert_called_once()
