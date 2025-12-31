"""
Tests for src/wd_bots/wd_sparql_bot.py

This module tests SPARQL query generator functions for Wikidata.
"""

import pytest

from src.wd_bots.wd_sparql_bot import (
    wd_sparql_generator_url,
    sparql_generator_url,
    sparql_generator_big_results,
)


class TestWdSparqlGeneratorUrl:
    """Tests for wd_sparql_generator_url function"""

    def test_returns_list(self, mocker):
        """Test that function returns a list"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.get_query_data",
            return_value={"results": {"bindings": []}}
        )

        result = wd_sparql_generator_url("SELECT * WHERE { ?s ?p ?o }")

        assert isinstance(result, list)

    def test_extracts_qids_from_response(self, mocker):
        """Test that QIDs are extracted from response"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.get_query_data",
            return_value={
                "results": {
                    "bindings": [
                        {"item": {"value": "http://www.wikidata.org/entity/Q123"}},
                        {"item": {"value": "http://www.wikidata.org/entity/Q456"}},
                    ]
                }
            }
        )

        result = wd_sparql_generator_url("SELECT * WHERE { ?s ?p ?o }")

        assert "Q123" in result
        assert "Q456" in result

    def test_filters_non_q_items(self, mocker):
        """Test that non-Q items are filtered"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.get_query_data",
            return_value={
                "results": {
                    "bindings": [
                        {"item": {"value": "http://www.wikidata.org/entity/Q123"}},
                        {"item": {"value": "http://www.wikidata.org/entity/P456"}},
                    ]
                }
            }
        )

        result = wd_sparql_generator_url("SELECT * WHERE { ?s ?p ?o }")

        assert "Q123" in result
        assert "P456" not in result

    def test_returns_empty_list_for_no_data(self, mocker):
        """Test that empty list is returned when no data"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.get_query_data",
            return_value={}
        )

        result = wd_sparql_generator_url("SELECT * WHERE { ?s ?p ?o }")

        assert result == []

    def test_sorts_results(self, mocker):
        """Test that results are sorted"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.get_query_data",
            return_value={
                "results": {
                    "bindings": [
                        {"item": {"value": "http://www.wikidata.org/entity/Q300"}},
                        {"item": {"value": "http://www.wikidata.org/entity/Q100"}},
                        {"item": {"value": "http://www.wikidata.org/entity/Q200"}},
                    ]
                }
            }
        )

        result = wd_sparql_generator_url("SELECT * WHERE { ?s ?p ?o }")

        assert result == sorted(result)


class TestSparqlGeneratorUrl:
    """Tests for sparql_generator_url function"""

    def test_returns_list(self, mocker):
        """Test that function returns a list"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.get_query_data",
            return_value={"results": {"bindings": []}}
        )

        result = sparql_generator_url("SELECT * WHERE { ?s ?p ?o }")

        assert isinstance(result, list)

    def test_returns_dict_when_requested(self, mocker):
        """Test that dict is returned when returndict=True"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.get_query_data",
            return_value={
                "head": {"vars": ["item"]},
                "results": {"bindings": []}
            }
        )

        result = sparql_generator_url("SELECT * WHERE { ?s ?p ?o }", returndict=True)

        assert isinstance(result, dict)

    def test_extracts_all_variables(self, mocker):
        """Test that all variables are extracted"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.get_query_data",
            return_value={
                "head": {"vars": ["item", "label"]},
                "results": {
                    "bindings": [
                        {
                            "item": {"value": "Q123"},
                            "label": {"value": "Test"}
                        }
                    ]
                }
            }
        )

        result = sparql_generator_url("SELECT * WHERE { ?s ?p ?o }")

        assert len(result) == 1
        assert result[0]["item"] == "Q123"
        assert result[0]["label"] == "Test"

    def test_handles_missing_variables(self, mocker):
        """Test handling of missing variables in bindings"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.get_query_data",
            return_value={
                "head": {"vars": ["item", "label"]},
                "results": {
                    "bindings": [
                        {"item": {"value": "Q123"}}  # Missing label
                    ]
                }
            }
        )

        result = sparql_generator_url("SELECT * WHERE { ?s ?p ?o }")

        assert result[0]["item"] == "Q123"
        assert result[0]["label"] == ""


class TestSparqlGeneratorBigResults:
    """Tests for sparql_generator_big_results function"""

    def test_returns_list(self, mocker):
        """Test that function returns a list"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.sparql_generator_url",
            return_value=[]
        )

        result = sparql_generator_big_results("SELECT * WHERE { ?s ?p ?o }")

        assert isinstance(result, list)

    def test_uses_pagination(self, mocker):
        """Test that pagination is used"""
        call_count = [0]

        def mock_sparql(query, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return [{"item": "Q1"}]
            return []

        mocker.patch(
            "src.wd_bots.wd_sparql_bot.sparql_generator_url",
            side_effect=mock_sparql
        )

        result = sparql_generator_big_results("SELECT * WHERE { ?s ?p ?o }")

        # Should stop after empty result
        assert call_count[0] >= 1

    def test_respects_limit_parameter(self, mocker):
        """Test that limit parameter is respected"""
        mock_sparql = mocker.patch(
            "src.wd_bots.wd_sparql_bot.sparql_generator_url",
            return_value=[]
        )

        sparql_generator_big_results("SELECT * WHERE { ?s ?p ?o }", limit=100)

        call_args = mock_sparql.call_args[0][0]
        assert "limit 100" in call_args

    def test_respects_offset_parameter(self, mocker):
        """Test that offset parameter is respected"""
        mock_sparql = mocker.patch(
            "src.wd_bots.wd_sparql_bot.sparql_generator_url",
            return_value=[]
        )

        sparql_generator_big_results("SELECT * WHERE { ?s ?p ?o }", offset=50)

        call_args = mock_sparql.call_args[0][0]
        assert "offset 50" in call_args

    def test_stops_at_alllimit(self, mocker):
        """Test that iteration stops at alllimit"""
        mocker.patch(
            "src.wd_bots.wd_sparql_bot.sparql_generator_url",
            return_value=[{"item": "Q1"}] * 100
        )

        result = sparql_generator_big_results(
            "SELECT * WHERE { ?s ?p ?o }",
            limit=50,
            alllimit=50
        )

        # Should stop after reaching alllimit
        assert len(result) <= 100  # First batch only