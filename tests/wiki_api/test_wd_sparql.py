"""
Tests for src/wiki_api/wd_sparql.py

This module tests SPARQL query functions for Wikidata.
"""

import pytest

from src.wiki_api.wd_sparql import (
    get_query_data,
    get_query_result,
)


class TestGetQueryData:
    """Tests for get_query_data function"""

    def test_returns_empty_dict_on_exception(self, mocker):
        """Test that empty dict is returned on exception"""
        mock_sparql = mocker.MagicMock()
        mock_sparql.query.side_effect = Exception("Network error")
        mocker.patch("src.wiki_api.wd_sparql.SPARQLWrapper", return_value=mock_sparql)

        result = get_query_data("SELECT * WHERE { ?s ?p ?o }")
        assert result == {}

    def test_returns_query_result(self, mocker):
        """Test that query result is returned"""
        mock_result = mocker.MagicMock()
        mock_result.convert.return_value = {"results": {"bindings": [{"item": {"value": "Q123"}}]}}
        mock_sparql = mocker.MagicMock()
        mock_sparql.query.return_value = mock_result
        mocker.patch("src.wiki_api.wd_sparql.SPARQLWrapper", return_value=mock_sparql)

        result = get_query_data("SELECT * WHERE { ?s ?p ?o }")
        assert "results" in result

    def test_sets_json_return_format(self, mocker):
        """Test that JSON return format is set"""
        mock_sparql = mocker.MagicMock()
        mock_result = mocker.MagicMock()
        mock_result.convert.return_value = {}
        mock_sparql.query.return_value = mock_result
        mocker.patch("src.wiki_api.wd_sparql.SPARQLWrapper", return_value=mock_sparql)

        get_query_data("SELECT * WHERE { ?s ?p ?o }")

        mock_sparql.setReturnFormat.assert_called()

    def test_uses_wikidata_endpoint(self, mocker):
        """Test that Wikidata endpoint is used"""
        mock_sparql_class = mocker.patch("src.wiki_api.wd_sparql.SPARQLWrapper")
        mock_sparql = mocker.MagicMock()
        mock_result = mocker.MagicMock()
        mock_result.convert.return_value = {}
        mock_sparql.query.return_value = mock_result
        mock_sparql_class.return_value = mock_sparql

        get_query_data("SELECT * WHERE { ?s ?p ?o }")

        call_args = mock_sparql_class.call_args[0]
        assert "wikidata.org" in call_args[0]


class TestGetQueryResult:
    """Tests for get_query_result function"""

    def test_returns_list_of_bindings(self, mocker):
        """Test that list of bindings is returned"""
        mocker.patch(
            "src.wiki_api.wd_sparql.get_query_data",
            return_value={"results": {"bindings": [{"item": {"value": "Q123"}}, {"item": {"value": "Q456"}}]}},
        )

        result = get_query_result("SELECT * WHERE { ?s ?p ?o }")

        assert isinstance(result, list)
        assert len(result) == 2

    def test_returns_empty_list_on_no_results(self, mocker):
        """Test that empty list is returned when no results"""
        mocker.patch("src.wiki_api.wd_sparql.get_query_data", return_value={})

        result = get_query_result("SELECT * WHERE { ?s ?p ?o }")

        assert result == []

    def test_returns_empty_list_on_empty_bindings(self, mocker):
        """Test that empty list is returned when bindings are empty"""
        mocker.patch("src.wiki_api.wd_sparql.get_query_data", return_value={"results": {"bindings": []}})

        result = get_query_result("SELECT * WHERE { ?s ?p ?o }")

        assert result == []

    def test_preserves_binding_structure(self, mocker):
        """Test that binding structure is preserved"""
        mocker.patch(
            "src.wiki_api.wd_sparql.get_query_data",
            return_value={
                "results": {
                    "bindings": [
                        {"item": {"value": "Q123", "type": "uri"}, "label": {"value": "Test", "type": "literal"}}
                    ]
                }
            },
        )

        result = get_query_result("SELECT * WHERE { ?s ?p ?o }")

        assert result[0]["item"]["value"] == "Q123"
        assert result[0]["label"]["value"] == "Test"
