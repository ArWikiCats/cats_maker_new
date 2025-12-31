#!/usr/bin/python3
"""

"""
import functools
from typing import Any
import pymysql

from pathlib import Path
from pymysql.cursors import DictCursor
from ..helps import logger


@functools.lru_cache(maxsize=1)
def load_db_config() -> dict[str, Any]:
    # --- 1) تحقق من ملف الإنتاج ~/replica.my.cnf ---
    replica_cnf_path = Path.home() / "replica.my.cnf"
    if replica_cnf_path.exists():
        return {
            "read_default_file": replica_cnf_path,
            "charset": "utf8mb4",
            "use_unicode": True,
            "autocommit": True,
            "cursorclass": DictCursor
        }

    return {
        "host": "localhost",
        "user": "root",
        "password": "root11",
        "database": "arlexemes",
        "charset": "utf8mb4",
        "use_unicode": True,
        "autocommit": True,
        "cursorclass": DictCursor
    }


def sql_connect_pymysql(query, db="", host="", Return=[], values=None):
    # ---
    logger.debug("start sql_connect_pymysql:")
    # ---
    params = None
    # ---
    if values:
        params = values
    # ---
    # connect to the database server without error
    # ---
    DB_CONFIG = load_db_config(db, host)
    # ---
    try:
        connection = pymysql.connect(**DB_CONFIG)
    except Exception as e:
        logger.exception(e)
        return Return
    # ---
    with connection as conn, conn.cursor() as cursor:
        # ---
        # skip sql errors
        try:
            cursor.execute(query, params)

        except Exception as e:
            logger.exception(e)
            return Return
        # ---
        results = Return
        # ---
        try:
            results = cursor.fetchall()

        except Exception as e:
            logger.exception(e)
            return Return
        # ---
        # yield from cursor
        return results


def decode_value(value):
    try:
        value = value.decode("utf-8")  # Assuming UTF-8 encoding
    except BaseException:
        try:
            value = str(value)
        except BaseException:
            return ""
    return value


def resolve_bytes(rows):
    decoded_rows = []
    # ---
    for row in rows:
        decoded_row = {}
        for key, value in row.items():
            if isinstance(value, bytes):
                value = decode_value(value)
            decoded_row[key] = value
        decoded_rows.append(decoded_row)
    # ---
    return decoded_rows


def make_sql_connect(query, db="", host="", Return=[], values=None):
    # ---
    if not query:
        logger.debug("query == ''")
        return Return
    # ---
    logger.debug("<<lightyellow>> newsql::")
    # ---
    rows = sql_connect_pymysql(query, db=db, host=host, Return=Return, values=values)
    # ---
    rows = resolve_bytes(rows)
    # ---
    return rows
