#!/usr/bin/python3
"""

"""

import json
from pathlib import Path

Dir = Path(__file__).parent

with open(f"{Dir}/New_Portal_List.json", "r", encoding="utf-8") as c:
    New_Portal_List = json.load(c)

portal_ar_list = []
# ---
portal_en_list = []
portal_en_to_ar = {}
# ---
for ar in New_Portal_List:
    en = New_Portal_List[ar]["en"]
    fr = New_Portal_List[ar]["fr"]
    # ---
    portal_ar_list.append(ar)
    # ---
    if en:
        portal_en_list.append(en)
        portal_en_to_ar[en] = ar

portal_en_to_ar_lower = {x.lower(): v for x, v in portal_en_to_ar.items()}
