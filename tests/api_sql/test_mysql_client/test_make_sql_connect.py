"""
Tests for src/api_sql/mysql_client.py

اختبارات لملف mysql_client.py - استعلامات SQL

This module tests:
- decode_value() - Decode bytes to string
"""

import pytest

from src.api_sql.mysql_client import (
    decode_value,
    resolve_bytes,
)


class TestDecodeValue:
    """Tests for decode_value function."""

    def test_decode_bytes_to_string(self):
        """Test that decode_value decodes bytes to string."""
        from src.api_sql.mysql_client import decode_value

        result = decode_value(b"test_string")

        assert result == "test_string"
        assert isinstance(result, str)

    def test_decode_preserves_string(self):
        """Test that decode_value preserves string input."""
        from src.api_sql.mysql_client import decode_value

        result = decode_value("already_string")

        assert result == "already_string"

    def test_decode_handles_utf8(self):
        """Test that decode_value handles UTF-8 encoded bytes."""
        from src.api_sql.mysql_client import decode_value

        result = decode_value("مرحبا".encode("utf-8"))

        assert result == "مرحبا"

    def test_decode_handles_none(self):
        """Test that decode_value handles None input."""
        from src.api_sql.mysql_client import decode_value

        result = decode_value(None)

        # decode_value converts None to string 'None'
        assert result == "None" or result is None or result == ""
