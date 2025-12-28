#!/usr/bin/python3
"""

"""
import json
import os
import stat
import sys

from ...helps import logger

# ---
statgroup = stat.S_IRWXU | stat.S_IRWXG
# ---


def load_json(filename, empty_data="list"):
    data = {} if empty_data == "dict" else []
    # ---
    if "test" in sys.argv:
        print(f"temps_params.py, jsonfile: {filename}")
    # ---
    if not os.path.isfile(filename):
        print(f"File not found: {filename}")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f)
            os.chmod(filename, statgroup)
        except Exception as e:
            print(e)
    # ---
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(e)
    # ---
    return data


def log_to_file(data, filename):
    # ---
    delete = False
    # ---
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            logger.info(f"<<green>> wrote to {filename}")
    except PermissionError:
        logger.info(f"<<red>> PermissionError writing to {filename}")
        delete = True
    except Exception as e:
        logger.warning(f"<<red>> Error writing to {filename}: {e}")
    # ---
    if delete:
        try:
            os.remove(filename)
            # ---
            logger.info(f"<<lightgreen>> deleted {filename}")
            # ---
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f)
                logger.info(f"<<green>> wrote to {filename}")
            # ---
            os.chmod(filename, statgroup)
        except Exception as e:
            logger.warning(f"<<red>> Error deleting/writing to {filename}: {e}")
