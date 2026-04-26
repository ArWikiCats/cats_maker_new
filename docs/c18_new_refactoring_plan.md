# Refactoring Plan for `src/c18_new`

> **Note:** The user referred to this module as `b18_new`, but the actual path is `src/c18_new`. This plan targets the `src/c18_new` directory.

---

## 1. Executive Summary

The `c18_new` module is responsible for Arabic Wikipedia category generation, cross-wiki page linking (EN→AR, FR→AR), template and documentation handling, and filtering/sorting logic. The current code works but suffers from:

-   **Inconsistent naming** (camelCase vs. snake_case, typos)
-   **High code duplication** across `ar_from_en.py` and `ar_from_en2.py`
-   **Tight coupling** to global config and wiki APIs
-   **Magic numbers / hardcoded strings** (namespaces, template names, categories)
-   **Poor separation of concerns** (I/O, SQL, caching, and business logic mixed)
-   **Weak error handling** and return-type inconsistency

---

## 2. Proposed Directory Structure

```
src/c18_new/
├── __init__.py
├── constants.py              # Centralize magic strings, namespaces, templates
├── models.py                 # Small dataclasses: WikiPage, Category, Sitelink
├── core/
│   ├── __init__.py
│   ├── category_generator.py # Merged logic from cat_tools2 + ar_from_en2
│   ├── cross_wiki_linker.py  # Renamed/refactored english_page_title.py
│   └── category_filter.py    # Refactored filter_cat.py
├── tools/
│   ├── __init__.py
│   ├── sort.py               # Refactored sort_bot.py
│   ├── template_query.py     # Refactored temp_bot.py
│   └── doc_handler.py        # Refactored text_to_temp_bot.py
├── io/
│   ├── __init__.py
│   ├── json_store.py         # Refactored dontadd.py (file I/O only)
│   └── sql_queries.py        # SQL queries from dontadd.py
└── utils/
    ├── __init__.py
    └── text.py               # Shared text helpers (clean_category_input, etc.)
```

---

## 3. Refactoring Tasks

### 3.1 Centralize Constants (`constants.py`)

**Why:** Namespace IDs, template names, and category blacklists are scattered across 7 files.

**Action:**

-   Move `tatone_ns` from `cat_tools2.py`
-   Move `Skippe_Cat`, `page_false_templates` from `filter_cat.py`
-   Move `SKIP_CATEGORIES` from `temp_bot.py`
-   Move `tosearch_and_replace`, `to_search`, `pre_text` from `text_to_temp_bot.py`
-   Move `namespace_ids` from `ar_from_en2.py`
-   Add a `Namespace` enum or `IntEnum`:
    ```python
    from enum import IntEnum
    class Namespace(IntEnum):
        MAIN = 0
        TEMPLATE = 10
        CATEGORY = 14
        PORTAL = 100
    ```

---

### 3.2 Merge Duplicate Category Fetchers (`core/category_generator.py`)

**Why:** `cat_tools2.py::Categorized_Page_Generator` and `ar_from_en2.py::en_category_members` do the same API call with nearly identical logic.

**Action:**

-   Create a single `CategoryFetcher` class or module-level function.
-   Accept `namespaces: list[int]` as an argument instead of hardcoding `tatone_ns` vs `namespace_ids`.
-   Move `clean_category_input` from `ar_from_en.py` into `utils/text.py`.
-   Merge `Get_ar_list_from_en_list` and `get_ar_list_title_from_en_list` into one batch-translation helper.
-   Delete `cat_tools2.py` and `ar_from_en2.py` after migration.

**API sketch:**

```python
def fetch_category_members(en_title: str, wiki: str = "en", namespaces: list[int] | None = None) -> list[str]:
    ...

def translate_en_to_ar(titles: list[str], wiki: str = "en", batch_size: int = 50) -> list[str]:
    ...
```

---

### 3.3 Refactor Cross-Wiki Linker (`core/cross_wiki_linker.py`)

**Why:** `english_page_title.py` is 256 lines of deeply nested conditionals, mixed regex parsing, Wikidata calls, and caching. It returns `False`, `""`, or `str` unpredictably.

**Action:**

-   Rename file/module to `cross_wiki_linker.py` (generic, not EN-specific).
-   Extract `extract_wikidata_qid` into `utils/text.py`.
-   Split into three small, testable functions:
    1. `resolve_via_wikidata(text: str) -> str | None`
    2. `resolve_via_api(link: str, source: str, target: str) -> str | None`
    3. `get_english_page_title(...)` becomes a thin orchestrator.
-   **Standardize return type** to `str | None` instead of `False` / `""`.
-   Add type hints everywhere.

---

### 3.4 Refactor Category Filter (`core/category_filter.py`)

**Why:** `filter_cat.py` mutates `final_cats` in-place inside multiple nested loops, making it hard to follow and risky.

**Action:**

-   Convert to a **pure function** that returns a new list instead of mutating the input.
-   Extract each rule into a small predicate:
    ```python
    def is_template_cat(item: str, ns: int) -> bool: ...
    def is_deleted_cat(item: str) -> bool: ...
    def is_blacklisted_cat(item: str) -> bool: ...
    ```
-   Replace string-based template checks (`templatequerymulti`) with a proper batch API wrapper.
-   Add unit tests for each rule.

---

### 3.5 Refactor Template Query Caching (`tools/template_query.py`)

**Why:** `temp_bot.py` uses a global `defaultdict(dict)` and manual cache tuple management.

**Action:**

-   Encapsulate cache in a `TemplateCache` class.
-   Use `@functools.lru_cache` or a simple dict with a clear key scheme (`f"{sitecode}:{title}"`).
-   Remove duplication between `templatequery` and `templatequerymulti`.
-   Provide a single entry point:
    ```python
    def get_templates(titles: str | list[str], sitecode: str = "ar") -> dict[str, list[str]] | list[str] | None:
        ...
    ```

---

### 3.6 Refactor Documentation/Template Text Handling (`tools/doc_handler.py`)

**Why:** `text_to_temp_bot.py` has large hardcoded string literals and many `elif` branches for template insertion.

**Action:**

-   Move `pre_text` into a Jinja2 template file or a separate `.txt` asset.
-   Replace long `if/elif` chains with a **strategy map**:
    ```python
    INSERTION_PATTERNS = {
        "{{توثيق": insert_before_tag,
        "{{توثيق شريط": insert_before_tag,
        ...
    }
    ```
-   Use `wikitextparser` more consistently instead of manual string slicing.
-   Split `add_direct` and `add_to_doc_page` into smaller helpers.

---

### 3.7 Refactor Sorting (`tools/sort.py`)

**Why:** `sort_bot.py` implements a custom alphabetical sort by character substitution, which is brittle and ignores Unicode collation.

**Action:**

-   Replace the hand-rolled sort with Python’s built-in `sorted(..., key=...)` using `pyicu` or `locale.strxfrm` if ICU is available.
-   If ICU is too heavy, keep the substitution logic but extract it into a well-named `arabic_sort_key` function with a docstring explaining the custom alphabet order.
-   Avoid mutating the category list during the star/self-insert logic; build a new ordered list instead.

---

### 3.8 Refactor Dont-Add List I/O (`io/json_store.py` + `io/sql_queries.py`)

**Why:** `dontadd.py` handles JSON file I/O, SQL querying, file permissions, date checking, and caching all in one file.

**Action:**

-   **Split responsibilities:**
    -   `io/json_store.py`: `JsonStore` class with `load()`, `save()`, `is_stale(days=1)`.
    -   `io/sql_queries.py`: `fetch_dont_add_pages()` — pure SQL, no file logic.
-   Replace broad `except Exception` with specific exceptions (`PermissionError`, `json.JSONDecodeError`).
-   Use `pathlib` consistently instead of mixing `os.path` and `Path`.
-   Replace the daily cache invalidation logic with `functools.lru_cache` + a TTL wrapper, or keep it explicit but testable.

---

### 3.9 Add Data Models (`models.py`)

Introduce lightweight dataclasses to reduce dict-plumbing:

```python
@dataclass
class WikiPage:
    title: str
    namespace: int
    langlinks: dict[str, str]

@dataclass
class Category:
    title: str
    templates: list[str]
```

This makes the API layer (`find_LCN`, etc.) easier to mock in tests.

---

### 3.10 Add Unit Tests

Create a `tests/c18_new/` suite covering:

-   `clean_category_input` edge cases
-   `filter_cats_text` rule matrix
-   `sort_text` ordering
-   `extract_wikidata_qid` regex matching
-   `add_to_doc_page` template insertion logic

Use `pytest` and `unittest.mock` to patch API calls.

---

### 3.11 Code Style & Tooling

-   **Rename all camelCase functions** to `snake_case` (PEP 8).
-   **Fix typos:** `Skippe_Cat` → `skipped_categories`, `lenth` → `length`, `sito_code` → `site_code`.
-   **Add `__all__`** to each module to define public APIs.
-   **Run `ruff`** (or `flake8` + `black`) for formatting and linting.

---

## 4. Migration Order (Recommended)

| Phase | Task                                                                    | Risk   |
| ----- | ----------------------------------------------------------------------- | ------ |
| 1     | Extract `constants.py` + `utils/text.py`                                | Low    |
| 2     | Refactor `dontadd.py` → `io/`                                           | Low    |
| 3     | Merge `cat_tools2.py` + `ar_from_en2.py` → `core/category_generator.py` | Medium |
| 4     | Refactor `english_page_title.py` → `core/cross_wiki_linker.py`          | Medium |
| 5     | Refactor `filter_cat.py` → `core/category_filter.py`                    | Medium |
| 6     | Refactor `temp_bot.py` → `tools/template_query.py`                      | Low    |
| 7     | Refactor `sort_bot.py` → `tools/sort.py`                                | Low    |
| 8     | Refactor `text_to_temp_bot.py` → `tools/doc_handler.py`                 | Medium |
| 9     | Add `models.py` and wire into all modules                               | Low    |
| 10    | Write tests + run linter                                                | Low    |

---

## 5. Acceptance Criteria

-   [ ] No camelCase function names remain in `c18_new`.
-   [ ] `cat_tools2.py` and `ar_from_en2.py` are removed; their logic lives in `core/category_generator.py`.
-   [ ] All hardcoded namespace IDs, template names, and category names are imported from `constants.py`.
-   [ ] `filter_cats_text` no longer mutates its input list.
-   [ ] `english_page_link` family of functions returns `str | None` consistently.
-   [ ] `dontadd.py` is split into `io/json_store.py` and `io/sql_queries.py`.
-   [ ] `py.test tests/c18_new/` passes with >80% coverage.
-   [ ] `ruff check src/c18_new` reports zero errors.

---

_Plan created on 2026-04-26_
