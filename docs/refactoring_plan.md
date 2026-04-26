# c18_new Refactoring Plan

## Executive Summary

This plan aims to transform the `src/c18_new` module from a legacy "quick-script" state into a **maintainable, testable, and DRY** codebase. It is organized into five sequential phases: code hygiene, duplication removal, complexity reduction, structural reorganization, and testing. Each phase is designed to be as self-contained as possible so it can be delivered in incremental batches.

---

## 1. Current State Diagnosis

| File                         | Primary Issue                                                                                                                                                                      | Severity     |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| `cat_tools2.py`              | Mutable global (`tatone_ns`), `CamelCase` function name, no API error handling.                                                                                                    | Medium       |
| `dontadd.py`                 | Bare `except Exception`, mixes disk I/O logic with SQL logic, non-PEP-8 name `Dont_add_to_pages_def`.                                                                              | Medium       |
| `cats_tools/ar_from_en.py`   | Duplicated chunking/batching logic and `find_LCN` call pattern. Inconsistent return types (`list` vs `False`).                                                                     | High         |
| `cats_tools/ar_from_en2.py`  | **Near-complete duplication** of `ar_from_en.py` with only minor wiki-source differences (`en` vs `fr`). Contains a duplicated `Categorized_Page_Generator`.                       | **Critical** |
| `bots/english_page_title.py` | Giant functions (`english_page_link_from_api` ~80 lines), deep nesting, repeated regex patterns, mixed responsibilities (API + Wikidata + validation + caching).                   | High         |
| `bots/filter_cat.py`         | Single 140-line function `filter_cats_text`, high cyclomatic complexity, O(n²) loops due to repeated `remove()` from a list during iteration, mutable global lists (`Skippe_Cat`). | High         |
| `bots/text_to_temp_bot.py`   | Long `elif` chain in `add_direct`, scattered hardcoded template names, mixing raw string parsing with `wikitextparser`.                                                            | Medium       |
| `tools_bots/temp_bot.py`     | Near-duplication between `templatequery` and `templatequerymulti`. Module-level mutable cache (`templatequery_cache`).                                                             | Medium       |
| `tools_bots/sort_bot.py`     | Bespoke sorting algorithm that replaces characters with digits then sorts alphabetically; inefficient and fragile.                                                                 | Medium       |

---

## 2. Goals and Non-Goals

### Goals

-   Apply **PEP 8** naming conventions across all functions and variables.
-   **Eliminate duplication** between `ar_from_en.py` and `ar_from_en2.py`, and between `templatequery` and `templatequerymulti`.
-   Reduce **cyclomatic complexity** of the top three functions by at least 50%.
-   Make logic **pure** wherever possible to ease unit testing.
-   Standardize **error handling** around API calls and file I/O.

### Non-Goals (for this phase)

-   Change business logic: filtering and sorting behavior must remain pixel-for-pixel identical.
-   Rewrite external API wrappers (`find_LCN`, `load_main_api`, etc.).
-   Introduce new CLI arguments or UI changes.

---

## 3. Detailed Implementation Phases

### Phase 1: Code Hygiene & Basics (Week 1)

**Target files:** All files in `c18_new`

**Tasks:**

1. **Constants & Magic Numbers:** Create `src/c18_new/constants.py` (or add to centralized settings) containing:
    - Namespace IDs: `NS_MAIN = 0`, `NS_CAT = 14`, `NS_TEMPLATE = 10`.
    - Category prefixes: `CAT_PREFIX_AR = "تصنيف:"`, `CAT_PREFIX_EN = "Category:"`.
    - Hardcoded template names as `frozenset` constants instead of mutable global lists.
2. **Rename symbols:** Convert all function names to `snake_case`:
    - `Categorized_Page_Generator` → `generate_categorized_pages`
    - `Dont_add_to_pages_def` → `get_dont_add_pages`
    - `Get_ar_list_from_en_list` → `get_ar_list_from_en_list`
    - `english_page_link_from_api` → `_resolve_page_link_via_api`
    - `filter_cats_text` → `filter_category_text`
3. **Type hints:** Add `list[str]`, `Optional[str]`, `dict[str, Any]` to all public signatures.
4. **Normalize return types:** Do not return `False` instead of a list or string. Return empty `list[str]` or `None`.
5. **Freeze globals:** Convert `Skippe_Cat`, `page_false_templates`, and `tatone_ns` into `tuple` or `frozenset`. If callers need dynamic mutation (e.g., `stubs`), use a factory function or `copy` instead of mutating the module at import time.

**Success criteria:** `ruff check src/c18_new` and `mypy src/c18_new` (if enabled) pass without style errors.

---

### Phase 2: Deduplication & Shared Utilities (Week 2)

**Task 2.1: Merge `ar_from_en.py` and `ar_from_en2.py`**

-   Create a unified module: `src/c18_new/mappers/en_to_ar_mapper.py`.
-   Extract a single public function:
    ```python
    def fetch_ar_titles_from_en_category(enpage_title: str, wiki: str = "en") -> list[str]:
        ...
    ```
-   Extract a shared batching helper:
    ```python
    def batch_fetch_langlinks(titles: list[str], source_wiki: str, target_lang: str = "ar", batch_size: int = 50) -> list[str]:
        ...
    ```
-   Delete `ar_from_en2.py` entirely. Make `ar_from_en.py` import from `en_to_ar_mapper` temporarily for backward compatibility (or update its consumers directly if there are few).

**Task 2.2: Merge `templatequery` and `templatequerymulti`**

In `tools_bots/temp_bot.py`:

-   Make `templatequery` call `templatequerymulti` and return only the `templates` field:
    ```python
    def templatequery(enlink: str, sitecode: str = "ar") -> list[str] | bool:
        multi_result = templatequerymulti(enlink, sitecode)
        if not multi_result:
            return False
        return multi_result.get(enlink, {}).get("templates", False)
    ```
-   Extract caching logic into a small `TemplateCache` class or use `functools.lru_cache` instead of a module-level `defaultdict`.

**Task 2.3: Reuse the category generator**

In `ar_from_en2.py` (before deletion), a duplicated `Categorized_Page_Generator` existed. Ensure all consumers across the project use `cat_tools2.generate_categorized_pages` exclusively.

**Success criteria:** Code volume in `c18_new` drops by 15–20% with no functional loss.

---

### Phase 3: Complexity Reduction (Week 3)

**Task 3.1: Refactor `filter_cats_text`**

In `bots/filter_cat.py`:

1. Turn each filtering rule into a standalone predicate function:
    ```python
    def is_template_category(cat: str, ns: int) -> bool: ...
    def is_deleted_category(cat: str, deleted_pages: set[str]) -> bool: ...
    def has_false_template(cat: str, false_templates: frozenset[str]) -> bool: ...
    def is_already_in_text(cat: str, text: str) -> bool: ...
    ```
2. Replace repeated list removal with **building a new list**:

    ```python
    def filter_category_text(cats: list[str], ns: int, text: str) -> list[str]:
        deleted = set(get_deleted_pages())
        false_temps = frozenset(page_false_templates)
        # Fetch templates once
        templates_map = templatequerymulti("|".join(cats), "ar") or {}

        survivors = []
        for cat in cats:
            if any(predicate(cat) for predicate in get_predicates(ns, text, deleted, false_temps)):
                continue
            # Template-based checks
            if is_bad_template(templates_map.get(cat, {})):
                continue
            survivors.append(cat)
        return survivors
    ```

3. This changes complexity from roughly O(n²) to O(n) and makes each rule independently testable.

**Task 3.2: Break down `english_page_title.py`**

In `bots/english_page_title.py`:

1. Extract all regex patterns into a composed list at the top of the file:
    ```python
    QID_PATTERNS = [
        re.compile(r"..."),
        ...
    ]
    ```
2. Split `english_page_link_from_api` into smaller helpers:
    - `_check_local_cache(tubb)`
    - `_fetch_from_api(link, firstsite_code)`
    - `_fetch_from_text(text)`
    - `_validate_via_wikidata(result, ...)`
    - `_update_caches(tubb, result, ...)`
3. Reduce nesting by using early returns (guard clauses).

**Task 3.3: Clean up `text_to_temp_bot.py`**

In `bots/text_to_temp_bot.py`:

1. Replace the `elif` chain in `add_direct` with a dictionary dispatch or a list of `(marker, handler)` tuples:
    ```python
    INSERTION_MARKERS = [
        ("{{توثيق", lambda text, idx: ...),
        ("{{توثيق شريط}}", lambda text, idx: ...),
        ...
    ]
    ```
2. Use `wikitextparser` consistently instead of `str.find` when searching for templates.
3. Extract long text blocks (`pre_text`) into separate template files if feasible, or at least into a clearly named constant.

**Task 3.4: Replace the sorting algorithm in `sort_bot.py`**

In `tools_bots/sort_bot.py`:

-   Replace the manual algorithm with a clear **sort key**:

    ```python
    _ARABIC_ORDER = str.maketrans({
        'آ': '02', 'ا': '03', 'أ': '04', ... # full mapping
    })

    def collation_key(text: str) -> str:
        # Can be upgraded later to pyuca if the library is added
        return text.translate(_ARABIC_ORDER)
    ```

-   Use `sorted(categorylist, key=collation_key)` instead of string padding and zero tricks.

**Success criteria:** Cyclomatic complexity report (e.g., via `radon cc`) for the top 3 functions drops by more than 50%.

---

### Phase 4: Structural Reorganization (Week 4)

The current folder names are historically grown and unclear (`bots` vs `tools_bots` vs `cats_tools`). Propose a clearer layout that reflects **purpose** rather than **history**.

**Proposed layout (with backward compatibility):**

```
src/c18_new/
├── __init__.py              # Export only the public interface
├── constants.py             # Constants and blacklists
├── category_fetcher.py      # (was cat_tools2.py) API category member fetching
├── exclusions.py            # (was dontadd.py) Blacklists and JSON/SQL loading
├── filters/
│   ├── __init__.py
│   ├── category_filter.py   # (was filter_cat.py) main filtering function
│   └── predicates.py        # individual filtering rules
├── mappers/
│   ├── __init__.py
│   └── en_to_ar.py          # (merged ar_from_en + ar_from_en2)
├── resolvers/
│   ├── __init__.py
│   └── page_links.py        # (was english_page_title.py) language link resolution
├── injectors/
│   ├── __init__.py
│   ├── template_categories.py # (was text_to_temp_bot.py)
│   └── sorter.py            # (was sort_bot.py)
└── queries/
    ├── __init__.py
    └── template_query.py    # (was temp_bot.py)
```

**Migration strategy:**

1. Create the new directories and files.
2. Move code into them.
3. In the old files, leave **re-export aliases** with a deprecation warning:
    ```python
    # bots/filter_cat.py (legacy)
    from ..filters.category_filter import filter_category_text as filter_cats_text
    ```
4. After one release cycle, delete the legacy files.

**Success criteria:** All old imports still work (with a warning) and all new imports are clean.

---

### Phase 5: Testing & Validation (Week 5)

**Tasks:**

1. **Unit tests:** For every extracted "pure" function, write a test:
    - `clean_category_input` → test prefix stripping.
    - `sort_text` → test Arabic alphabetical order.
    - `is_template_category` → test True/False for different inputs.
    - `collation_key` → test character ordering.
2. **Integration tests:** Run the pipeline with `run.py -encat:Science` (or any trial category) **before and after** each phase to confirm output parity.
3. **Performance tests:** Benchmark `filter_cats_text` and `sort_text` on a large list (e.g., 1,000 categories) to ensure optimizations did not regress performance.
4. **CI/CD:** Confirm `pytest tests/c18_new/` passes in GitHub Actions.

**Success criteria:** `c18_new` test coverage is at least 80%, and all old and new tests pass.

---

## 4. Quick-Win Checklist

These can be executed immediately before the larger phases begin:

-   [ ] Replace mutable `tatone_ns` with an immutable `frozenset` or a function.
-   [ ] Replace mutable `Skippe_Cat` list with a `tuple`.
-   [ ] Replace `page_false_templates.remove("بذرة")` (mutation at import time) with conditional logic inside the function.
-   [ ] Remove `__pycache__` directories from the repository and ensure they are in `.gitignore`.
-   [ ] Add `__all__` to `__init__.py` files to define public exports.

---

## 5. Risks & Mitigations

| Risk                                           | Impact | Mitigation                                                                                                            |
| ---------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------- |
| Breaking imports in `mk_cats` or `b18_new`     | High   | Keep legacy re-export files for one full release cycle with `DeprecationWarning`.                                     |
| Changing filtering behavior due to reordering  | Medium | Run an integration test on a real category (e.g., `Science`) before and after; compare outputs.                       |
| Performance regression from building new lists | Low    | Benchmark on large datasets; new list building is usually much faster because it avoids O(n²) removal.                |
| Losing logging context during splitting        | Low    | Keep `logger.info/debug` calls in the top-level orchestrator functions; do not move them into tiny predicate helpers. |

---

## 6. Final Success Criteria

1. **Code cleanliness:** No `CamelCase` functions in `c18_new`, no magic numbers.
2. **DRY:** No duplication between `ar_from_en` and `ar_from_en2`, and none between `templatequery` and `templatequerymulti`.
3. **Performance:** `filter_cats_text` is at least 30% faster on large lists.
4. **Testing:** All existing tests (`880+`) still pass, plus 20+ new unit tests for extracted pure logic.
5. **Documentation:** All public functions have clear docstrings in the project's documentation language.

---

## 7. Conclusion

`c18_new` is not in terrible shape, but it carries visible technical debt: duplication, non-standard naming, and oversized functions. By applying this five-phase plan, the module will become **clean, testable, and easy to maintain** without touching the sensitive business logic that drives Arabic Wikipedia categorization.

> **Recommendation:** Start with Phase 1 and the Quick-Wins immediately; they are completely safe and provide a clean foundation for the later phases.
