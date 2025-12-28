"""
"""
import sys

sys.argv.append("ask")
sys.path.append("D:/categories_bot/make2_new")

from new_all import work_bot as new_all

from src.mk_cats import ToMakeNewCat2222
from src.wd_api_bot import get_quarry_results

new_all_tab = {1: False}


def new_all_work_on_title(title, **Kwargs):
    if not new_all_tab[1]:
        new_all_tab[1] = new_all
    # ---
    new_all_tab[1].work_on_title(title=title, dont_create=True, **Kwargs)


def main():
    categories_list = []

    for arg in sys.argv:
        argn, _, value = arg.partition(":")

        if argn.startswith("-"):
            argn = argn[1:]

        # python3 core8/pwb.py I:/core/bots/cats_maker/run.py -depth:5 quarry:357357
        # python3 core8/pwb.py I:/core/bots/cats_maker/run.py -depth:5 quarry:231528
        # python3 core8/pwb.py I:/core/bots/cats_maker/run.py -depth:5 quarry:299753
        # python3 core8/pwb.py I:/core/bots/cats_maker/run.py -depth:5 quarry:475921
        # python3 core8/pwb.py I:/core/bots/cats_maker/run.py -depth:5 quarry:320152
        # python3 core8/pwb.py I:/core/bots/cats_maker/run.py -depth:5 quarry:300040
        # python3 core8/pwb.py I:/core/bots/cats_maker/run.py -depth:5 encat:Department_stores_of_the_United_States

        if argn == "quarry":
            List = get_quarry_results(value)
            for cat in List:
                categories_list.append(cat)
            print(f"Add {len(List)} cat from get_quarry_results to categories_list.")

        elif argn == "encat":
            categories_list.append(value)

    categories_list = [f"Category:{x}" if not x.startswith("Category:") else x for x in categories_list]
    if categories_list:
        print(f"categories_list work with {len(categories_list)} cats.")
        ToMakeNewCat2222(categories_list, callback=new_all_work_on_title)


if __name__ == "__main__":
    main()
