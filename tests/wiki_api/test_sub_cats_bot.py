"""
Tests for src/wiki_api/sub_cats_bot.py
"""

import pytest


class TestSubCatsQuery:
    """Tests for sub_cats_query function"""

    def test_returns_false_for_empty_enlink(self):
        """Test that empty enlink returns False"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        result = sub_cats_query("", "en")
        assert result is False

    def test_returns_false_for_none_enlink(self):
        """Test that None enlink returns False"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        result = sub_cats_query(None, "en")
        assert result is False

    def test_uses_cache_when_available(self, mocker):
        """Test that cached results are returned"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        cached_data = {"categorymembers": {"Page1": {"ns": 0}}}

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=cached_data)
        mock_submit = mocker.patch("src.wiki_api.sub_cats_bot.submitAPI")

        result = sub_cats_query("Category:Science", "en")

        assert result == cached_data
        # Should not call API if cached
        mock_submit.assert_not_called()

    def test_increments_api_call_counter(self, mocker):
        """Test that API call counter is incremented"""
        from src.wiki_api.sub_cats_bot import sub_cats_query, API_n_CALLS

        initial_count = API_n_CALLS[1]

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value={"query": {"pages": {}}})
        mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        sub_cats_query("Category:Test", "en")

        assert API_n_CALLS[1] == initial_count + 1

    def test_api_params_for_subcat_type(self, mocker):
        """Test API parameters when ctype is 'subcat'"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mock_submit = mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value={"query": {"pages": {}}})
        mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        sub_cats_query("Category:Test", "en", ctype="subcat")

        call_args = mock_submit.call_args[0][0]
        assert call_args["gcmtype"] == "subcat"

    def test_api_params_for_page_type(self, mocker):
        """Test API parameters when ctype is 'page'"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mock_submit = mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value={"query": {"pages": {}}})
        mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        sub_cats_query("Category:Test", "en", ctype="page")

        call_args = mock_submit.call_args[0][0]
        assert call_args["gcmtype"] == "page"

    def test_api_params_for_default_type(self, mocker):
        """Test API parameters with default ctype (both pages and subcats)"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mock_submit = mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value={"query": {"pages": {}}})
        mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        sub_cats_query("Category:Test", "en")

        call_args = mock_submit.call_args[0][0]
        assert call_args["gcmtype"] == "page|subcat"

    def test_extracts_category_members(self, mocker):
        """Test extraction of category members from API response"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        api_response = {
            "query": {
                "pages": {
                    "123": {
                        "title": "Science",
                        "ns": 14,
                        "langlinks": [{"lang": "ar", "*": "علوم"}]
                    },
                    "456": {
                        "title": "Physics",
                        "ns": 0,
                        "langlinks": [{"lang": "ar", "*": "فيزياء"}]
                    }
                }
            }
        }

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value=api_response)
        mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        result = sub_cats_query("Category:Test", "en")

        assert "categorymembers" in result
        assert "Science" in result["categorymembers"]
        assert "Physics" in result["categorymembers"]
        assert result["categorymembers"]["Science"]["ar"] == "علوم"
        assert result["categorymembers"]["Physics"]["ar"] == "فيزياء"

    def test_stores_namespace_info(self, mocker):
        """Test that namespace info is stored for each page"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        api_response = {
            "query": {
                "pages": {
                    "123": {
                        "title": "Category:Science",
                        "ns": 14,
                    }
                }
            }
        }

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value=api_response)
        mock_set_cache = mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        result = sub_cats_query("Category:Test", "en")

        assert result["categorymembers"]["Category:Science"]["ns"] == 14
        # Verify namespace was cached
        assert any(call[0][0] == ("Category:Science", "en", "ns") for call in mock_set_cache.call_args_list)

    def test_caches_result(self, mocker):
        """Test that result is cached after API call"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        api_response = {"query": {"pages": {"123": {"title": "Test", "ns": 0}}}}

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value=api_response)
        mock_set_cache = mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        result = sub_cats_query("Category:Test", "en")

        # Verify the final result was cached
        cache_calls = [call[0] for call in mock_set_cache.call_args_list]
        assert any(
            call[0] == ("Category:Test", "en", "sub_cats_query")
            for call in cache_calls
        )

    def test_handles_ar_sitecode(self, mocker):
        """Test langcode is set to 'ar' when sitecode is not 'en'"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mock_submit = mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value={"query": {"pages": {}}})
        mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        sub_cats_query("Category:Test", "ar")

        call_args = mock_submit.call_args[0][0]
        # When sitecode is "en", langcode should be "ar"
        # When sitecode is not "en", langcode should be from EEn_site['code']

    def test_handles_empty_api_response(self, mocker):
        """Test handling of empty API response"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value={})
        mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        result = sub_cats_query("Category:Test", "en")

        assert result == {"categorymembers": {}}

    def test_handles_none_api_response(self, mocker):
        """Test handling when submitAPI returns None"""
        from src.wiki_api.sub_cats_bot import sub_cats_query

        mocker.patch("src.wiki_api.sub_cats_bot.get_cache_L_C_N", return_value=None)
        mocker.patch("src.wiki_api.sub_cats_bot.submitAPI", return_value=None)
        mocker.patch("src.wiki_api.sub_cats_bot.set_cache_L_C_N")

        result = sub_cats_query("Category:Test", "en")

        assert result == {"categorymembers": {}}
