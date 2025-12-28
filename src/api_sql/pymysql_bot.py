"""

"""
import copy

import pymysql
import pymysql.cursors

from ..helps import logger


def sql_connect_pymysql(
    query, return_dict=False, values=None, main_args={}, credentials={}, conversions=None, many=False, **kwargs
):
    args = copy.deepcopy(main_args)
    args["cursorclass"] = pymysql.cursors.DictCursor if return_dict else pymysql.cursors.Cursor
    if conversions:
        args["conv"] = conversions

    params = values or None  # Simplify condition

    try:
        connection = pymysql.connect(**args, **credentials)
    except Exception as e:
        logger.warning(e)
        return []

    with connection as conn, conn.cursor() as cursor:
        # skip sql errors
        try:
            if many:
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params)

        except Exception as e:
            logger.warning(e)
            return []

        try:
            results = cursor.fetchall()
        except Exception as e:
            logger.warning(e)
            return []

    return results
