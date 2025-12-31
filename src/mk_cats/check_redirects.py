
from ..helps import logger
from ..new_api.page import NEW_API, SuperNEW_API


def _load_new_api(lang) -> SuperNEW_API:
    return NEW_API(lang, family="wikipedia")


def remove_redirect_pages(page_titles: list) -> list:
    """Remove redirect pages from a list of page titles."""
    api = _load_new_api("ar")

    result = api.Find_pages_exists_or_not(page_titles, get_redirect=True)

    non_redirects = [x for x, v in result.items() if v and x != "redirect"]
    logger.info(f"<<lightgreen>> Removed {len(page_titles) - len(non_redirects)} redirect pages.<<default>>")
    return non_redirects
