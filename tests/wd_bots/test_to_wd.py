"""
Tests for src/wd_bots/to_wd.py

This module tests Wikidata write functions.
"""

import pytest

from src.wd_bots.to_wd import (
    add_label,
    makejson,
    Make_New_item,
    Log_to_wikidata,
    get_wd_api_bot,
    wikimedia_category_descraptions,
)


class TestWikimediaCategoryDescriptions:
    """Tests for wikimedia_category_descraptions dictionary"""

    def test_is_dict(self):
        """Test that wikimedia_category_descraptions is a dictionary"""
        assert isinstance(wikimedia_category_descraptions, dict)

    def test_contains_arabic(self):
        """Test that Arabic description is present"""
        assert "ar" in wikimedia_category_descraptions
        assert wikimedia_category_descraptions["ar"] == "تصنيف ويكيميديا"

    def test_contains_english(self):
        """Test that English description is present"""
        assert "en" in wikimedia_category_descraptions
        assert wikimedia_category_descraptions["en"] == "Wikimedia category"

    def test_contains_multiple_languages(self):
        """Test that multiple languages are present"""
        assert len(wikimedia_category_descraptions) > 10

    def test_all_values_are_strings(self):
        """Test that all values are strings"""
        for lang, desc in wikimedia_category_descraptions.items():
            assert isinstance(desc, str)


class TestMakejson:
    """Tests for makejson function"""

    def test_creates_valid_claim_structure(self):
        """Test that valid claim structure is created"""
        result = makejson("P31", "Q4167836")

        assert "mainsnak" in result
        assert result["mainsnak"]["property"] == "P31"
        assert result["type"] == "statement"
        assert result["rank"] == "normal"

    def test_handles_q_prefix(self):
        """Test that Q prefix in numeric is handled"""
        result = makejson("P31", "Q123")

        value = result["mainsnak"]["datavalue"]["value"]
        assert value["numeric-id"] == "123"
        assert value["id"] == "Q123"

    def test_returns_none_for_empty_numeric(self):
        """Test that None is returned for empty numeric"""
        result = makejson("P31", "")
        assert result is None

    def test_returns_none_for_none_numeric(self):
        """Test that None is returned for None numeric"""
        result = makejson("P31", None)
        assert result is None

    def test_datavalue_structure(self):
        """Test the datavalue structure"""
        result = makejson("P31", "Q5")

        datavalue = result["mainsnak"]["datavalue"]
        assert datavalue["type"] == "wikibase-entityid"
        assert datavalue["value"]["entity-type"] == "item"


class TestGetWdApiBot:
    """Tests for get_wd_api_bot function"""

    def test_returns_api_bot_instance(self, mocker):
        """Test that function returns API bot instance"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.to_wd.NewHimoAPIBot", return_value=mock_bot)

        # Clear cache
        get_wd_api_bot.cache_clear()

        result = get_wd_api_bot()

        assert result is not None

    def test_caches_result(self, mocker):
        """Test that result is cached"""
        mock_bot = mocker.MagicMock()
        mock_class = mocker.patch("src.wd_bots.to_wd.NewHimoAPIBot", return_value=mock_bot)

        get_wd_api_bot.cache_clear()

        get_wd_api_bot()
        get_wd_api_bot()

        # Should only be called once due to caching
        assert mock_class.call_count == 1


class TestAddLabel:
    """Tests for add_label function"""

    def test_calls_labels_api(self, mocker):
        """Test that Labels_API is called"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.to_wd.get_wd_api_bot", return_value=mock_bot)

        add_label("Q123", "تسمية عربية")

        mock_bot.Labels_API.assert_called_once()

    def test_passes_correct_parameters(self, mocker):
        """Test that correct parameters are passed"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.to_wd.get_wd_api_bot", return_value=mock_bot)

        add_label("Q123", "تسمية")

        mock_bot.Labels_API.assert_called_with("Q123", "تسمية", "ar", True, nowait=True, tage="catelabels")


class TestMakeNewItem:
    """Tests for Make_New_item function"""

    def test_creates_item_with_sitelinks(self, mocker):
        """Test that item is created with sitelinks"""
        mock_bot = mocker.MagicMock()
        mock_bot.New_API.return_value = "Q999"
        mocker.patch("src.wd_bots.to_wd.get_wd_api_bot", return_value=mock_bot)
        mocker.patch("src.wd_bots.to_wd.wwdesc")

        Make_New_item("تصنيف:علوم", "Category:Science")

        mock_bot.New_API.assert_called_once()
        call_args = mock_bot.New_API.call_args[0][0]
        assert "sitelinks" in call_args

    def test_creates_item_with_labels(self, mocker):
        """Test that item is created with labels"""
        mock_bot = mocker.MagicMock()
        mock_bot.New_API.return_value = "Q999"
        mocker.patch("src.wd_bots.to_wd.get_wd_api_bot", return_value=mock_bot)
        mocker.patch("src.wd_bots.to_wd.wwdesc")

        Make_New_item("تصنيف:علوم", "Category:Science")

        call_args = mock_bot.New_API.call_args[0][0]
        assert "labels" in call_args
        assert "ar" in call_args["labels"]
        assert "en" in call_args["labels"]

    def test_adds_p31_claim(self, mocker):
        """Test that P31 claim is added"""
        mock_bot = mocker.MagicMock()
        mock_bot.New_API.return_value = "Q999"
        mocker.patch("src.wd_bots.to_wd.get_wd_api_bot", return_value=mock_bot)
        mocker.patch("src.wd_bots.to_wd.wwdesc")

        Make_New_item("تصنيف:علوم", "Category:Science")

        call_args = mock_bot.New_API.call_args[0][0]
        assert "claims" in call_args
        assert "P31" in call_args["claims"]


class TestLogToWikidata:
    """Tests for Log_to_wikidata function"""

    def test_adds_sitelink_when_qid_provided(self, mocker):
        """Test that sitelink is added when QID is provided"""
        mock_bot = mocker.MagicMock()
        mocker.patch("src.wd_bots.to_wd.get_wd_api_bot", return_value=mock_bot)

        Log_to_wikidata("تصنيف:علوم", "Category:Science", "Q123")

        mock_bot.Sitelink_API.assert_called()
        mock_bot.Labels_API.assert_called()

    def test_creates_new_item_when_no_qid(self, mocker):
        """Test that new item is created when no QID"""
        mock_bot = mocker.MagicMock()
        mock_bot.Sitelink_API.return_value = False  # Not True, so create new
        mocker.patch("src.wd_bots.to_wd.get_wd_api_bot", return_value=mock_bot)
        mock_make_new = mocker.patch("src.wd_bots.to_wd.Make_New_item")

        Log_to_wikidata("تصنيف:علوم", "Category:Science", "")

        # Should try to create new item
        mock_bot.Sitelink_API.assert_called()
