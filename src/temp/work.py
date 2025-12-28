#!/usr/bin/python3
"""

بوت لإضافة قالب السنوات للتصنيفات

python3 core8/pwb.py c18/temp/work -ns:14 -strat:تصنيف:الألفية_2
python3 core8/pwb.py c18/temp/work -ns:14 -start:تصنيف:2016


"""
import re

from ..helps import logger
from ..wiki_api import arAPI, gent, himoBOT2
from . import main_make_temp


def main3(*args):
    """Process and handle various templates based on command-line arguments.

    This function serves as the main entry point for processing a list of
    templates related to historical events, classifications, and other
    categories. It checks for specific command-line arguments to determine
    whether to save changes or perform other actions. The function retrieves
    titles from a generator, fetches associated text from an API, and checks
    for the presence of templates in the retrieved text. If certain
    conditions are met, it adds new content to the API and outputs relevant
    information to the console.

    Args:
        *args: Variable length argument list that can include command-line arguments.
    """

    p_i = "(تأسيس|انحلال|تأسيسات|انحلالات|)"
    p_2 = "(قرن|عقد|بلد|حسب|قارة)"
    templates = [
        "تصنيف انحلالات القرن",
        "تصفح تص عقد",
        "تصنيف موسم",
        "سنوات في القرن",
        "تأسيس",
        "discat",
        "انحلال",
        "BDYearsInDecade",
        "Navseasoncats",
        "الألفية",
        "السنة",
        "موضوع",
        "10 سنوات",
        "10 سنوات",
        "10سنوات",
        "10ye",
        "year",
        "تصنيف",
        "تصنيف شهر",
        "MonthCategoryNav",
        "EstcatCountry2ndMillennium",
        "Estcat",
        "ترويسة تصنيف عقد",
        "10سنوات",
        "10 سنوات 2",
        "10سنوات 2",
        "10 سنوات في موضوع",
        "10سنوات في موضوع",
        "انحلال الألفية 1",
        "انحلال بلد",
        "انحلال بلد الألفية 1",
        "انحلال بلد الألفية 2",
        "انحلال بلد الألفية 3",
        "انحلال بلد عقد",
        "انحلال بلد قرن",
        "انحلال سنة",
        "انحلال عقد",
        "انحلال قرن",
        "بلد عقد",
        "بلد قرن",
        "تأسيس الألفية 1",
        "تأسيس بلد",
        "تأسيس بلد الألفية 1",
        "تأسيس بلد الألفية 2",
        "تأسيس بلد الألفية 3",
        "تأسيس بلد عقد",
        "تأسيس بلد قرن",
        "تأسيس حسب البلد قرن",
        "تأسيس سنة",
        "تأسيس عقد",
        "تأسيس عقد حسب البلد",
        "تأسيس قرن",
        "ترويسة تصنيف عقد",
        "تصفح تص عقد",
        "تصفح تص عقد 2",
        "تصنيف السنة",
        "تصنيف انحلالات القرن",
        "تصنيف موسم",
        "سنوات في القرن",
        "عقد",
        "قوالب تصانيف زمنية",
        "مواليد سنة",
        "مواليد عقد",
        "مواليد قرن",
        "موضوع في 10 سنوات",
        "موضوع في 10سنوات",
        "موضوع في قرن",
        "سنوات في الأفلام",
        "وفيات عقد",
        "وفيات قرن",
        "تحويل تصنيف",
        p_i + r"\s*" + p_2,
    ]
    logger.output("<<lightgreen>> main3")
    # ---
    generator = gent.get_gent(listonly=True, *args)
    numb = 0
    # ---
    for title in generator:
        numb += 1
        logger.output(f" {numb} title:" + title)
        text = himoBOT2.GetarPageText(title, sitecode="ar")  #
        text = re.sub(r"تصنيف كومنز", "co", text)

        No_Temp = True

        if title.find("هـ") != -1:
            continue

        if text.find("{{سنوات في") != -1:
            continue

        if text.find("{{وفيات") != -1:
            continue

        for temp2 in templates:
            if re.sub(r"\{\{" + temp2, "", text) != text:
                logger.output(f' find temp:"{temp2}" in page. ')
                No_Temp = False
                break

        if No_Temp:
            temp = ""
            add, temp = main_make_temp("", title)
            logger.output(add, temp)
            if temp:
                if re.sub(r"\n", "", add).strip() != "":
                    summary = f"بوت:أضاف [[قالب:{temp}]]"
                    logger.output(" ================================== ")
                    logger.output(text)
                    logger.output(" ================================== ")
                    logger.showDiff(text, add + "\n" + text)
                    arAPI.Add_To_Head(add + "\n", summary, title, False)


if __name__ == "__main__":
    main3()
