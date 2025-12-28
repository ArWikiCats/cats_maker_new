#!/usr/bin/python3
"""
!
"""
import re

from ...helps import logger
from .load_data import cacaca, years_Baco


def Make_years_temp(title, tex, return_title=False):
    logger.output(f' Make_years_temp:{title} , tex:"{tex}"', "blue")
    if title.find("ق م") != -1 or title.find("ق.م") != -1:
        if return_title:
            return "", ""
        else:
            return ""

    t_1 = f"تصنيف:{tex}"
    ttt = t_1 + r"(عام |سنة |)(\d+)\s*(في |)(.*|)$"
    ye = re.sub(ttt, r"\g<2>", title)

    bld = re.sub(ttt, r"\g<4>", title)
    if ye == title:
        ye = ""
    Y, YY = "", ""
    template = f"{cacaca[tex]}بلد"
    logger.output(f" Make_years_temp:{title} , ye:{ye}, tex:{tex}", "blue")

    if ye in years_Baco:
        logger.output(f"ye in years_Baco {years_Baco[ye]}")
        if len(ye) == 4:
            Y = ye[3]
            YY = ye[0] + ye[1] + ye[2]
        elif len(ye) == 3:
            Y = ye[2]
            YY = ye[0] + ye[1]
        elif len(ye) == 2:
            Y = ye[1]
            YY = ye[0]
        elif len(ye) == 1:
            Y = ye
            YY = ""
        if bld.startswith("حسب"):
            bld = f"{bld}|في="

        text = f"{{{{{template}|{YY}|{Y}|{bld}}}}}"  # noqa
        logger.output(f' Y:"{YY}" ,YY:"{Y}", bld:"{bld}" ', "red")
        if not bld:
            template = f"{cacaca[tex]}سنة"
            text = f"{{{{{template}|{YY}|{Y}}}}}"  # noqa
        logger.output(text)

        if return_title:
            return text, template
        else:
            return text

    if return_title:
        return "{{تصنيف موسم}}", "تصنيف موسم"
    else:
        return "{{تصنيف موسم}}"
