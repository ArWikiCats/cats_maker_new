"""
Tests for src/wiki_api/wd_sparql.py
"""

import pytest


class TestGetQueryData:
    """Tests for get_query_data function"""

    def test_successful_query(self, mocker):
        """Test successful SPARQL query execution"""
        from src.wiki_api.wd_sparql import get_query_data

        # Mock SPARQLWrapper
        mock_sparql_instance = mocker.MagicMock()
        mock_sparql_instance.query().convert.return_value = {
            "results": {"bindings": [{"item": {"value": "Q123"}}]}
        }

        mock_sparql_class = mocker.patch("src.wiki_api.wd_sparql.SPARQLWrapper")
        mock_sparql_class.return_value = mock_sparql_instance

        query = "SELECT ?item WHERE { ?item wdt:P31 wd:Q5 }"
        result = get_query_data(query)

        assert result == {"results": {"bindings": [{"item": {"value": "Q123"}}]}}
        mock_sparql_instance.setQuery.assert_called_once_with(query)
        mock_sparql_instance.setReturnFormat.assert_called_once()

    def test_query_with_exception(self, mocker):
        """Test query execution with exception returns empty dict"""
        from src.wiki_api.wd_sparql import get_query_data

        mock_sparql_instance = mocker.MagicMock()
        mock_sparql_instance.query().convert.side_effect = Exception("Network error")

        mock_sparql_class = mocker.patch("src.wiki_api.wd_sparql.SPARQLWrapper")
        mock_sparql_class.return_value = mock_sparql_instance

        # Mock logger to avoid output
        mocker.patch("src.wiki_api.wd_sparql.logger")

        query = "SELECT ?item WHERE { ?item wdt:P31 wd:Q5 }"
        result = get_query_data(query)

        assert result == {}

    def test_user_agent_format(self, mocker):
        """Test that user agent is properly formatted"""
        import sys
        from src.wiki_api.wd_sparql import get_query_data

        mock_sparql_instance = mocker.MagicMock()
        mock_sparql_instance.query().convert.return_value = {}

        mock_sparql_class = mocker.patch("src.wiki_api.wd_sparql.SPARQLWrapper")
        mock_sparql_class.return_value = mock_sparql_instance

        get_query_data("SELECT * WHERE { }")

        # Check user agent format
        call_args = mock_sparql_class.call_args
        expected_agent = f"WDQS-example Python/{sys.version_info[0]}.{sys.version_info[1]}"
        assert call_args[1]["agent"] == expected_agent

    def test_endpoint_url(self, mocker):
        """Test that correct endpoint URL is used"""
        from src.wiki_api.wd_sparql import get_query_data

        mock_sparql_instance = mocker.MagicMock()
        mock_sparql_instance.query().convert.return_value = {}

        mock_sparql_class = mocker.patch("src.wiki_api.wd_sparql.SPARQLWrapper")
        mock_sparql_class.return_value = mock_sparql_instance

        get_query_data("SELECT * WHERE { }")

        # Check endpoint URL
        call_args = mock_sparql_class.call_args
        assert call_args[0][0] == "https://query.wikidata.org/sparql"


class TestGetQueryResult:
    """Tests for get_query_result function"""

    def test_extracts_bindings_from_response(self, mocker):
        """Test extracting bindings from query response"""
        from src.wiki_api.wd_sparql import get_query_result

        mock_data = {
            "results": {
                "bindings": [
                    {"item": {"value": "Q123"}},
                    {"item": {"value": "Q456"}},
                ]
            }
        }

        mocker.patch("src.wiki_api.wd_sparql.get_query_data", return_value=mock_data)

        query = "SELECT ?item WHERE { ?item wdt:P31 wd:Q5 }"
        result = get_query_result(query)

        assert len(result) == 2
        assert result[0] == {"item": {"value": "Q123"}}
        assert result[1] == {"item": {"value": "Q456"}}

    def test_empty_results(self, mocker):
        """Test handling empty query results"""
        from src.wiki_api.wd_sparql import get_query_result

        mock_data = {"results": {"bindings": []}}
        mocker.patch("src.wiki_api.wd_sparql.get_query_data", return_value=mock_data)

        query = "SELECT ?item WHERE { ?item wdt:P31 wd:Q999999 }"
        result = get_query_result(query)

        assert result == []

    def test_missing_results_key(self, mocker):
        """Test handling response without results key"""
        from src.wiki_api.wd_sparql import get_query_result

        mock_data = {}
        mocker.patch("src.wiki_api.wd_sparql.get_query_data", return_value=mock_data)

        query = "SELECT ?item WHERE { ?item wdt:P31 wd:Q5 }"
        result = get_query_result(query)

        assert result == []

    def test_missing_bindings_key(self, mocker):
        """Test handling response without bindings key"""
        from src.wiki_api.wd_sparql import get_query_result

        mock_data = {"results": {}}
        mocker.patch("src.wiki_api.wd_sparql.get_query_data", return_value=mock_data)

        query = "SELECT ?item WHERE { ?item wdt:P31 wd:Q5 }"
        result = get_query_result(query)

        assert result == []

    def test_calls_get_query_data(self, mocker):
        """Test that get_query_result calls get_query_data with correct query"""
        from src.wiki_api.wd_sparql import get_query_result

        mock_get_query_data = mocker.patch(
            "src.wiki_api.wd_sparql.get_query_data",
            return_value={"results": {"bindings": []}}
        )

        query = "SELECT ?item WHERE { ?item wdt:P31 wd:Q5 }"
        get_query_result(query)

        mock_get_query_data.assert_called_once_with(query)
