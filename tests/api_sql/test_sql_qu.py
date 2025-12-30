"""
Tests for src/api_sql/sql_qu.py

اختبارات لملف sql_qu.py - استعلامات SQL

This module tests:
- sql_connect_pymysql() - Connect and execute SQL queries
- decode_value() - Decode bytes to string
- can_use_sql_db - Flag for SQL database availability
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock


class TestSqlConnectPymysql:
    """Tests for sql_connect_pymysql function."""

    def test_returns_default_on_connection_error(self, mocker):
        """Test that sql_connect_pymysql returns default value on connection error."""
        mocker.patch("pymysql.connect", side_effect=Exception("Connection failed"))

        from src.api_sql.sql_qu import sql_connect_pymysql

        result = sql_connect_pymysql("SELECT 1", db="test", host="localhost", Return=[])

        assert result == []

    def test_returns_custom_default_on_error(self, mocker):
        """Test that sql_connect_pymysql returns custom default value on error."""
        mocker.patch("pymysql.connect", side_effect=Exception("Connection failed"))

        from src.api_sql.sql_qu import sql_connect_pymysql

        result = sql_connect_pymysql("SELECT 1", db="test", host="localhost", Return=["default"])

        assert result == ["default"]

    def test_uses_dict_cursor_when_requested(self, mocker):
        """Test that sql_connect_pymysql uses DictCursor when return_dict=True."""
        import pymysql.cursors

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = [{"col": "value"}]

        mock_connect = mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.sql_qu import sql_connect_pymysql

        sql_connect_pymysql("SELECT 1", db="test", host="localhost", return_dict=True)

        # Check that DictCursor was used
        call_kwargs = mock_connect.call_args[1]
        assert call_kwargs["cursorclass"] == pymysql.cursors.DictCursor

    def test_uses_regular_cursor_by_default(self, mocker):
        """Test that sql_connect_pymysql uses regular Cursor by default."""
        import pymysql.cursors

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = []

        mock_connect = mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.sql_qu import sql_connect_pymysql

        sql_connect_pymysql("SELECT 1", db="test", host="localhost")

        call_kwargs = mock_connect.call_args[1]
        assert call_kwargs["cursorclass"] == pymysql.cursors.Cursor

    def test_executes_query_with_values(self, mocker):
        """Test that sql_connect_pymysql passes values to execute."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = []

        mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.sql_qu import sql_connect_pymysql

        sql_connect_pymysql(
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
        """Test that sql_connect_pymysql returns fetchall results."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = [("row1",), ("row2",)]

        mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.sql_qu import sql_connect_pymysql

        result = sql_connect_pymysql("SELECT 1", db="test", host="localhost")

        assert result == [("row1",), ("row2",)]

    def test_returns_default_on_execute_error(self, mocker):
        """Test that sql_connect_pymysql returns default on execute error."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.execute.side_effect = Exception("Execute error")

        mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.sql_qu import sql_connect_pymysql

        result = sql_connect_pymysql("SELECT 1", db="test", host="localhost", Return=["error"])

        assert result == ["error"]

    def test_returns_default_on_fetchall_error(self, mocker):
        """Test that sql_connect_pymysql returns default on fetchall error."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.side_effect = Exception("Fetchall error")

        mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.sql_qu import sql_connect_pymysql

        result = sql_connect_pymysql("SELECT 1", db="test", host="localhost", Return=["fetch_error"])

        assert result == ["fetch_error"]

    def test_sets_charset_to_utf8mb4(self, mocker):
        """Test that sql_connect_pymysql uses utf8mb4 charset."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = []

        mock_connect = mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.sql_qu import sql_connect_pymysql

        sql_connect_pymysql("SELECT 1", db="test", host="localhost")

        call_kwargs = mock_connect.call_args[1]
        assert call_kwargs["charset"] == "utf8mb4"

    def test_enables_autocommit(self, mocker):
        """Test that sql_connect_pymysql enables autocommit."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = []

        mock_connect = mocker.patch("pymysql.connect", return_value=mock_conn)

        from src.api_sql.sql_qu import sql_connect_pymysql

        sql_connect_pymysql("SELECT 1", db="test", host="localhost")

        call_kwargs = mock_connect.call_args[1]
        assert call_kwargs["autocommit"] is True


class TestCanUseSqlDb:
    """Tests for can_use_sql_db flag."""

    def test_can_use_sql_db_is_dict(self):
        """Test that can_use_sql_db is a dictionary."""
        from src.api_sql.sql_qu import can_use_sql_db

        assert isinstance(can_use_sql_db, dict)

    def test_can_use_sql_db_has_key_1(self):
        """Test that can_use_sql_db has key 1."""
        from src.api_sql.sql_qu import can_use_sql_db

        assert 1 in can_use_sql_db

    def test_can_use_sql_db_value_is_boolean(self):
        """Test that can_use_sql_db[1] is a boolean."""
        from src.api_sql.sql_qu import can_use_sql_db

        assert isinstance(can_use_sql_db[1], bool)


class TestDecodeValue:
    """Tests for decode_value function."""

    def test_decode_bytes_to_string(self):
        """Test that decode_value decodes bytes to string."""
        from src.api_sql.sql_qu import decode_value

        result = decode_value(b"test_string")

        assert result == "test_string"
        assert isinstance(result, str)

    def test_decode_preserves_string(self):
        """Test that decode_value preserves string input."""
        from src.api_sql.sql_qu import decode_value

        result = decode_value("already_string")

        assert result == "already_string"

    def test_decode_handles_utf8(self):
        """Test that decode_value handles UTF-8 encoded bytes."""
        from src.api_sql.sql_qu import decode_value

        result = decode_value("مرحبا".encode("utf-8"))

        assert result == "مرحبا"

    def test_decode_handles_none(self):
        """Test that decode_value handles None input."""
        from src.api_sql.sql_qu import decode_value

        result = decode_value(None)

        # decode_value converts None to string 'None'
        assert result == "None" or result is None or result == ""
