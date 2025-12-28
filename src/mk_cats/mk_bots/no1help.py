"""

"""
from ...wd_bots import NewHimoAPIBot
from ...helps import logger
from ..mk_bots.wd_desc import wwdesc
from ..utils import tools, wikimedia_category_descraptions

WD_API_Bot = NewHimoAPIBot(Mr_or_bot="bot", www="www")

ns_text_tab_1 = {
    "0": "",
    "1": "نقاش",
    "2": "مستخدم",
    "3": "نقاش المستخدم",
    "4": "ويكيبيديا",
    "5": "نقاش ويكيبيديا",
    "6": "ملف",
    "7": "نقاش الملف",
    "10": "قالب",
    "11": "نقاش القالب",
    "12": "مساعدة",
    "13": "نقاش المساعدة",
    "14": "تصنيف",
    "15": "نقاش التصنيف",
    "100": "بوابة",
    "101": "نقاش البوابة",
    "828": "وحدة",
    "829": "نقاش الوحدة",
    "2600": "موضوع",
    "1728": "فعالية",
    "1729": "نقاش الفعالية",
}
ns_text_tab = {}
for ns, title in ns_text_tab_1.items():
    ns_text_tab[int(ns)] = title
    ns_text_tab[str(ns)] = title


def add_desc_to_cat(q):
    NewDesc = {}
    addedlangs = []
    for lang in wikimedia_category_descraptions.keys():
        NewDesc[lang] = {"language": lang, "value": wikimedia_category_descraptions[lang]}
        addedlangs.append(lang)

    wwdesc(NewDesc, q, 1, [], tage="newitems")


def Make_New_item(artitle, entitle, family=""):
    logger.debug(f'<<lightgreen>>* Make_New_item:ar:"{artitle}", english:"{entitle}".')

    enwiki = "enwiki"
    arwiki = "arwiki"

    if family and family != "wikipedia":
        enwiki = f"en{family}"
        arwiki = f"ar{family}"

    data = {}
    data["sitelinks"] = {}
    data["claims"] = {}
    data["claims"]["P31"] = [tools.makejson("P31", "Q4167836")]  # تصنيف
    data["labels"] = {}
    data["sitelinks"][enwiki] = {"site": enwiki, "title": entitle}
    data["sitelinks"][arwiki] = {"site": arwiki, "title": artitle}

    data["labels"]["ar"] = {"language": "ar", "value": artitle}
    data["labels"]["en"] = {"language": "en", "value": entitle}

    summary = f"Bot: New item from [[w:en:{entitle}|{enwiki}]]/[[w:ar:{artitle}|{arwiki}]]."

    sao = WD_API_Bot.New_API(data, summary, returnid=True, nowait=True, tage="newitems")

    if sao and sao.startswith("Q"):
        add_desc_to_cat(sao)


def add_ns(arlist):
    new = []

    for x, ns in arlist.items():
        if ns in ns_text_tab:
            x = f"{ns_text_tab[ns]}:{x}"

        new.append(x.replace("_", " "))

    return new
