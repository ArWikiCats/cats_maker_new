"""
Tests for src/wd_bots/wd_api_bot.py

This module tests the Wikidata API bot imports/re-exports.
"""

import pytest

from src.wd_bots.wd_api_bot import (
    wd_sparql_generator_url,
    sparql_generator_url,
    sparql_generator_big_results,
    Get_item_descriptions_or_labels,
    Get_Sitelinks_From_wikidata,
    Get_P373_API,
    Get_infos_wikidata,
    Get_Sitelinks_from_qid,
    Get_Item_API_From_Qid,
    Get_Claim_API,
    Get_Property_API,
    Get_Items_API_From_Qids,
)


class TestWdApiImports:
    """Tests for wd_api_bot imports"""

    def test_wd_sparql_generator_url_imported(self):
        """Test that wd_sparql_generator_url is imported"""
        assert wd_sparql_generator_url is not None
        assert callable(wd_sparql_generator_url)

    def test_sparql_generator_url_imported(self):
        """Test that sparql_generator_url is imported"""
        assert sparql_generator_url is not None
        assert callable(sparql_generator_url)

    def test_sparql_generator_big_results_imported(self):
        """Test that sparql_generator_big_results is imported"""
        assert sparql_generator_big_results is not None
        assert callable(sparql_generator_big_results)

    def test_get_item_descriptions_or_labels_imported(self):
        """Test that Get_item_descriptions_or_labels is imported"""
        assert Get_item_descriptions_or_labels is not None
        assert callable(Get_item_descriptions_or_labels)

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

    def test_get_item_api_from_qid_imported(self):
        """Test that Get_Item_API_From_Qid is imported"""
        assert Get_Item_API_From_Qid is not None
        assert callable(Get_Item_API_From_Qid)

    def test_get_claim_api_imported(self):
        """Test that Get_Claim_API is imported"""
        assert Get_Claim_API is not None
        assert callable(Get_Claim_API)

    def test_get_property_api_imported(self):
        """Test that Get_Property_API is imported"""
        assert Get_Property_API is not None
        assert callable(Get_Property_API)

    def test_get_items_api_from_qids_imported(self):
        """Test that Get_Items_API_From_Qids is imported"""
        assert Get_Items_API_From_Qids is not None
        assert callable(Get_Items_API_From_Qids)
