"""
Tests for src/api_sql/mysql_client.py

اختبارات لملف mysql_client.py - استعلامات SQL

This module tests:
- _sql_connect_pymysql() - Connect and execute SQL queries
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from src.api_sql.mysql_client import (
    make_sql_connect,
)


class TestSqlConnectPymysql:
    """Tests for _sql_connect_pymysql function."""

    def test_returns_default_on_connection_error(self, mocker):
        """Test that _sql_connect_pymysql returns default value on connection error."""
        mocker.patch("pymysql.connect", side_effect=Exception("Connection failed"))

        from src.api_sql.mysql_client import _sql_connect_pymysql

        result = _sql_connect_pymysql("SELECT 1", db="test", host="localhost", Return=[])

        assert result == []

    def test_returns_custom_default_on_error(self, mocker):
        """Test that _sql_connect_pymysql returns custom default value on error."""
        mocker.patch("pymysql.connect", side_effect=Exception("Connection failed"))

        from src.api_sql.mysql_client import _sql_connect_pymysql

        result = _sql_connect_pymysql("SELECT 1", db="test", host="localhost", Return=["default"])

        assert result == ["default"]

    def test_uses_dict_cursor_when_requested(self, mocker):
        """Test that _sql_connect_pymysql uses DictCursor."""
        import pymysql.cursors

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = [{"col": "value"}]

        mock_connect = mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.mysql_client import _sql_connect_pymysql

        _sql_connect_pymysql("SELECT 1", db="test", host="localhost")

        # Check that DictCursor was used
        call_kwargs = mock_connect.call_args[1]
        assert call_kwargs["cursorclass"] == pymysql.cursors.DictCursor

    def test_executes_query_with_values(self, mocker):
        """Test that _sql_connect_pymysql passes values to execute."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = []

        mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.mysql_client import _sql_connect_pymysql

        _sql_connect_pymysql(
            "SELECT * FROM table WHERE id = %s",
            db="test",
            host="localhost",
            values=(123,)
        )

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM table WHERE id = %s",
            (123,)
        )

    def test_returns_fetchall_results(self, mocker):
        """Test that _sql_connect_pymysql returns fetchall results."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = [("row1",), ("row2",)]

        mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.mysql_client import _sql_connect_pymysql

        result = _sql_connect_pymysql("SELECT 1", db="test", host="localhost")

        assert result == [("row1",), ("row2",)]

    def test_returns_default_on_execute_error(self, mocker):
        """Test that _sql_connect_pymysql returns default on execute error."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.execute.side_effect = Exception("Execute error")

        mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.mysql_client import _sql_connect_pymysql

        result = _sql_connect_pymysql("SELECT 1", db="test", host="localhost", Return=["error"])

        assert result == ["error"]

    def test_returns_default_on_fetchall_error(self, mocker):
        """Test that _sql_connect_pymysql returns default on fetchall error."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.side_effect = Exception("Fetchall error")

        mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.mysql_client import _sql_connect_pymysql

        result = _sql_connect_pymysql("SELECT 1", db="test", host="localhost", Return=["fetch_error"])

        assert result == ["fetch_error"]

    def test_sets_charset_to_utf8mb4(self, mocker):
        """Test that _sql_connect_pymysql uses utf8mb4 charset."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = []

        mock_connect = mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.mysql_client import _sql_connect_pymysql

        _sql_connect_pymysql("SELECT 1", db="test", host="localhost")

        call_kwargs = mock_connect.call_args[1]
        assert call_kwargs["charset"] == "utf8mb4"

    def test_enables_autocommit(self, mocker):
        """Test that _sql_connect_pymysql enables autocommit."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = []

        mock_connect = mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.mysql_client import _sql_connect_pymysql

        _sql_connect_pymysql("SELECT 1", db="test", host="localhost")

        call_kwargs = mock_connect.call_args[1]
        assert call_kwargs["autocommit"] is True
