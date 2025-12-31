"""
Tests for src/api_sql/sql_qu.py

TODO: write tests
"""

import pytest

from src.api_sql.sql_qu import (
    make_sql_connect,
    sql_connect_pymysql,
    decode_value,
    resolve_bytes,
)
