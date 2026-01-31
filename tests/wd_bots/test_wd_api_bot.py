"""
Tests for src/wd_bots/wd_api_bot.py

This module tests the Wikidata API bot imports/re-exports.
"""

from src.wd_bots.wd_api_bot import (
    Get_infos_wikidata,
    Get_P373_API,
    Get_Sitelinks_from_qid,
    Get_Sitelinks_From_wikidata,
)


class TestWdApiImports:
    """Tests for wd_api_bot imports"""

    def test_get_sitelinks_from_wikidata_imported(self):
        """Test that Get_Sitelinks_From_wikidata is imported"""
        assert Get_Sitelinks_From_wikidata is not None
        assert callable(Get_Sitelinks_From_wikidata)

    def test_get_p373_api_imported(self):
        """Test that Get_P373_API is imported"""
        assert Get_P373_API is not None
        assert callable(Get_P373_API)

    def test_get_infos_wikidata_imported(self):
        """Test that Get_infos_wikidata is imported"""
        assert Get_infos_wikidata is not None
        assert callable(Get_infos_wikidata)

    def test_get_sitelinks_from_qid_imported(self):
        """Test that Get_Sitelinks_from_qid is imported"""
        assert Get_Sitelinks_from_qid is not None
        assert callable(Get_Sitelinks_from_qid)
