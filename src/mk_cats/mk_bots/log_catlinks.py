"""

"""
import os
import stat
from datetime import datetime
from pathlib import Path

from ...helps import logger

Dir = Path(__file__).parent.parent.parent
statgroup = stat.S_IRWXU | stat.S_IRWXG
menet_dmy = datetime.now().strftime("%d-%m-%Y")
menet_m = datetime.now().strftime("%m")
menet_y = datetime.now().strftime("%Y")
menet_name = f"{menet_y}/{menet_m}/{menet_dmy}"
month_dir = f"{str(Dir)}/catlinks/{menet_y}/{menet_m}/"

if not os.path.isdir(month_dir):
    try:
        os.makedirs(month_dir)
        os.chmod(month_dir, statgroup)
        logger.warning(f"<<lightgreen>> month_dir:({month_dir}) created... ")
    except Exception as e:
        logger.debug(e)


def write_to_file(file, text):
    try:
        with open(file, "a", encoding="utf-8") as logfile:
            logfile.write(text)
        return True
    except Exception as e:
        logger.debug(e, text=f"<<lightyellow>> error logfile.write() to file: {file}")
        return False


def log_it(title, enca, Qid):
    tab = {"ar": title, "en": enca, "q": Qid}

    ss = f"{str(tab)}\n"

    file1 = f"{str(Dir)}/catlinks/{menet_name}.csv"
    file2 = f"{str(Dir)}/catlinks/{menet_y}/{menet_m}/{menet_dmy}.csv"
    file3 = f"{str(Dir)}/catlinks/{menet_dmy}.csv"

    if not os.path.isfile(file1):
        logger.debug("<<lightred>> file1 not exists, try to create the file.")
        try:
            with open(file1, "w", encoding="utf-8") as ffe:
                ffe.write(ss)
            ffe.close()

            logger.debug("<<lightgreen>> file1 created.")

            os.chmod(file1, statgroup)
            logger.debug("<<lightgreen>> chmoded to : stat.S_IRWXU | stat.S_IRWXG")
        except Exception as e:
            logger.debug(e)

    try_1 = write_to_file(file1, ss)

    if not try_1:
        try_1 = write_to_file(file2, ss)

    if not try_1:
        try_1 = write_to_file(file3, ss)
