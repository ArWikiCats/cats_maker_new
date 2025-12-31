# خطة إعادة الهيكلة
## Refactoring Plan

## نظرة عامة / Overview

هذه الخطة تحتوي على التفاصيل التقنية لإعادة هيكلة المشروع، بما في ذلك تدفق التنفيذ، البنية المعمارية، التحسينات المطلوبة، والتوثيق الفني.

This plan contains technical details for refactoring the project, including execution flow, architecture, required improvements, and technical documentation.

---

## 1. تدفق التنفيذ الرئيسي / Main Execution Flow

### 1.1 نقطة الدخول الرئيسية / Main Entry Point

**الدالة الأساسية:** `create_categories_from_list(liste, uselabs=False, callback=None)`
- **الموقع / Location:** `src/mk_cats/mknew.py`
- **الاسم القديم / Legacy name:** `ToMakeNewCat2222`
- **الوصف:** نقطة الدخول الأساسية لمعالجة قائمة من التصنيفات الإنجليزية وإنشاء نظائرها العربية

### 1.2 تسلسل التنفيذ الكامل / Complete Execution Sequence

```
run.py (main entry)
    ↓
create_categories_from_list(liste, uselabs, callback)
    ├─ تهيئة: lenth = len(liste)
    └─ حلقة: for num, en_title in enumerate(liste, 1):
        ↓
        one_cat(en_title, num, lenth, uselabs, callback)
            ├─ فحص: if en_title in DONE_D → return False
            ├─ إضافة: DONE_D.append(en_title)
            ↓
            ar_make_lab(en_title) → labb
            ├─ resolve_arabic_category_label() [ArWikiCats]
            └─ Get_Sitelinks_From_wikidata() [wd_bots]
            ↓
            check_en_temps(en_title) → bool
            ├─ فحص القوالب الإنجليزية
            └─ return True/False
            ↓
            get_ar_list_from_en(en_title, us_sql=True, wiki="en")
            ├─ استعلامات SQL أو API
            └─ return list of Arabic pages
            ↓
            process_catagories(en_title, labb, num, lenth, callback)
                ├─ حلقة متكررة: for i in range(0, Range[1]):
                │   ↓
                │   make_ar(en_page_title, ar_title, callback)
                │       ├─ scan_ar_title(ar_title) → checked_title
                │       │   └─ Get_Sitelinks_From_wikidata()
                │       ├─ check_if_artitle_exists(en_title, ar_title) → bool
                │       │   ├─ get_page_info_from_wikipedia()
                │       │   └─ return exists or not
                │       ├─ find_LCN(en_link) → ar_title
                │       │   └─ submitAPI() with langlinks
                │       ├─ Get_Sitelinks_From_wikidata(title, qid)
                │       │   └─ Get Qid, labels, descriptions
                │       ├─ find_Page_Cat_without_hidden(en_link)
                │       │   └─ Get categories without hidden ones
                │       ├─ get_listenpageTitle(ar_title, en_title)
                │       │   ├─ get_ar_list_from_cat() [b18_new]
                │       │   ├─ MakeLitApiWay() [b18_new]
                │       │   └─ return members list
                │       ↓
                │       new_category(en_title, ar_title, categories, qid, family)
                │           ├─ generate_category_text(en_title, ar_title, qid)
                │           │   ├─ categorytext.py logic
                │           │   ├─ generate_portal_content() for portals
                │           │   └─ fetch_commons_category() from Wikidata
                │           ├─ page_put(title, text, summary)
                │           │   └─ Save page to Wikipedia
                │           └─ return created title or False
                │       ↓
                │       add_to_final_list(members, ar_title, callback)
                │       │   └─ Add categories to pages
                │       ↓
                │       add_SubSub(en_cats, new_cat)
                │       │   └─ Track subcategories
                │       ↓
                │       make_ar_list_newcat2(ar_title, en_title)
                │       │   └─ Get members from new category
                │       ↓
                │       to_wd.Log_to_wikidata(ar_title, en_title, qid)
                │           └─ Update Wikidata with sitelink
                │
                └─ جمع النتائج: enriched_titles.extend(...)
```

### 1.3 الوحدات المشاركة في التدفق / Modules Involved in Flow

1. **run.py** - نقطة الدخول / Entry point
   - قراءة المعاملات من sys.argv
   - جلب البيانات من Quarry أو مباشرة
   - استدعاء create_categories_from_list()

2. **mk_cats/mknew.py** - المنطق الرئيسي / Main logic
   - create_categories_from_list() - نقطة البداية
   - one_cat() - معالجة تصنيف واحد
   - process_catagories() - المعالجة المتكررة
   - make_ar() - إنشاء التصنيف العربي
   - ar_make_lab() - إنشاء التسمية

3. **mk_cats/create_category_page.py** - إنشاء الصفحات
   - new_category() - إنشاء صفحة التصنيف
   - make_category() - المنطق الأساسي للإنشاء

4. **mk_cats/categorytext.py** - توليد النصوص
   - generate_category_text() - توليد نص التصنيف
   - generate_portal_content() - بوابات
   - fetch_commons_category() - جلب P373 من Wikidata

5. **b18_new/** - معالجة التصنيفات والروابط / Category and link processing
   - LCN_new.py: find_LCN(), find_Page_Cat_without_hidden()
   - cat_tools.py: add_SubSub(), get_SubSub_value()
   - cat_tools_enlist.py: get_listenpageTitle()
   - cat_tools_enlist2.py: MakeLitApiWay()
   - add_bot.py: add_to_final_list()
   - sql_cat.py: get_ar_list_from_en(), make_ar_list_newcat2()

6. **c18_new/** - أدوات التصنيفات / Category tools
   - bots/english_page_title.py
   - bots/filter_cat.py
   - bots/text_to_temp_bot.py
   - cats_tools/ar_from_en.py
   - tools_bots/sql_bot.py

7. **wd_bots/** - تكامل ويكي بيانات / Wikidata integration
   - wd_api_bot.py: Get_Sitelinks_From_wikidata()
   - to_wd.py: Log_to_wikidata()
   - get_bots.py: Wikidata queries

8. **wiki_api/** - استدعاءات API / API calls
   - himoBOT2.py: page_put(), get_page_info_from_wikipedia()

9. **api_sql/** - قاعدة البيانات / Database operations
   - wiki_sql.py: sql_new(), sql_new_title_ns()
   - sql_qu.py: make_sql_connect()

10. **helps/** - أدوات مساعدة / Helper utilities
    - log.py: LoggerWrap
    - jsonl_data.py: save(), load data
    - printe_helper.py: make_str()

---

## 2. البنية المعمارية / Architecture

### 2.1 طبقات النظام / System Layers

```
┌─────────────────────────────────────────┐
│         Entry Point Layer               │
│         run.py, __main__                │
└─────────────┬───────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      Business Logic Layer               │
│      mk_cats/mknew.py                   │
│      - create_categories_from_list()    │
│      - one_cat(), process_catagories()  │
│      - make_ar(), ar_make_lab()         │
└─────────────┬───────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      Page Creation Layer                │
│      mk_cats/create_category_page.py    │
│      mk_cats/categorytext.py            │
└─────────────┬───────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      Data Processing Layer              │
│      b18_new/, c18_new/                 │
│      - Category processing              │
│      - Link resolution                  │
│      - Member list management           │
└─────────────┬───────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      External Services Layer            │
│      - wiki_api/ (MediaWiki API)        │
│      - wd_bots/ (Wikidata API)          │
│      - api_sql/ (Database)              │
└─────────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      Utilities Layer                    │
│      helps/, utils/, temp/              │
└─────────────────────────────────────────┘
```

### 2.2 تدفق البيانات / Data Flow

```
English Category Name
    ↓
[ar_make_lab] → Arabic Label (from Wikidata/ArWikiCats)
    ↓
[get_ar_list_from_en] → List of Arabic article titles
    ↓
[find_LCN, Get_Sitelinks] → Language links, Qid
    ↓
[find_Page_Cat_without_hidden] → Parent categories (English)
    ↓
[get_listenpageTitle] → Member pages
    ↓
[generate_category_text] → Category page text (with templates)
    ↓
[page.save] → Save to ar.wikipedia
    ↓
[Log_to_wikidata] → Update Wikidata sitelink
```

---

## 3. إعادة الهيكلة المطلوبة / Required Refactoring

### 3.1 فصل المنطق / Separation of Concerns

#### مشاكل حالية / Current Issues:
- خلط منطق الأعمال مع استدعاءات API
- تبعيات دائرية بين الوحدات
- صعوبة الاختبار بسبب الاعتماديات المباشرة

#### الحلول المقترحة / Proposed Solutions:

**1. إنشاء طبقة Data Access منفصلة:**
```python
# src/data_access/wikipedia_repository.py
class WikipediaRepository:
    def get_page_categories(self, title: str, lang: str) -> list:
        """Get categories for a page"""
        pass

    def save_page(self, title: str, text: str, summary: str) -> bool:
        """Save a page to Wikipedia"""
        pass

# src/data_access/wikidata_repository.py
class WikidataRepository:
    def get_sitelinks(self, qid: str) -> dict:
        """Get sitelinks from Wikidata"""
        pass

    def get_label(self, qid: str, lang: str) -> str:
        """Get label for a Qid"""
        pass
```

**2. استخدام Dependency Injection:**
```python
# Before
def make_ar(en_page_title, ar_title, callback=None):
    # استدعاء مباشر
    result = Get_Sitelinks_From_wikidata(...)

# After
def make_ar(en_page_title, ar_title, wikidata_repo, callback=None):
    # استخدام repository
    result = wikidata_repo.get_sitelinks(...)
```

**3. فصل المنطق عن I/O:**
```python
# src/mk_cats/business_logic/category_processor.py
class CategoryProcessor:
    def __init__(self, wiki_repo, wikidata_repo, db_repo):
        self.wiki = wiki_repo
        self.wikidata = wikidata_repo
        self.db = db_repo

    def process_category(self, en_title: str) -> dict:
        """Pure business logic without I/O"""
        # Logic here
        pass
```

### 3.2 معالجة الأخطاء / Error Handling

#### مشاكل حالية / Current Issues:
- معالجة أخطاء غير متناسقة
- بعض الأخطاء يتم تجاهلها
- صعوبة تتبع الأخطاء

#### الحلول المقترحة / Proposed Solutions:

**1. استثناءات مخصصة:**
```python
# src/exceptions.py
class CatsMakerException(Exception):
    """Base exception for the project"""
    pass

class WikipediaAPIError(CatsMakerException):
    """Wikipedia API related errors"""
    pass

class WikidataAPIError(CatsMakerException):
    """Wikidata API related errors"""
    pass

class DatabaseError(CatsMakerException):
    """Database related errors"""
    pass

class CategoryNotFoundError(CatsMakerException):
    """Category not found"""
    pass
```

**2. معالج أخطاء موحد:**
```python
# src/error_handler.py
class ErrorHandler:
    def __init__(self, logger):
        self.logger = logger

    def handle_api_error(self, error: Exception, context: dict):
        """Handle API errors consistently"""
        self.logger.error(f"API Error: {error}", extra=context)
        # Retry logic, fallback, etc.

    def handle_database_error(self, error: Exception, context: dict):
        """Handle database errors"""
        self.logger.error(f"DB Error: {error}", extra=context)
```

### 3.3 التخزين المؤقت / Caching

#### مشاكل حالية / Current Issues:
- تخزين مؤقت غير متناسق
- بعض الاستدعاءات المتكررة لا تستخدم cache
- صعوبة إدارة ال cache

#### الحلول المقترحة / Proposed Solutions:

**1. نظام تخزين مؤقت موحد:**
```python
# src/cache/cache_manager.py
from functools import lru_cache
from typing import Optional, Any

class CacheManager:
    def __init__(self, backend='memory'):
        self.backend = backend
        self._cache = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        return self._cache.get(key)

    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL"""
        self._cache[key] = value

    def invalidate(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        pass

# استخدام decorators
from cache.cache_manager import cache_manager

@cache_manager.cached(ttl=3600)
def get_sitelinks(qid: str) -> dict:
    # API call here
    pass
```

### 3.4 التكوين / Configuration

#### مشاكل حالية / Current Issues:
- إعدادات مبعثرة في الكود
- قيم ثابتة hardcoded
- صعوبة تغيير الإعدادات

#### الحلول المقترحة / Proposed Solutions:

**1. ملف تكوين مركزي:**
```python
# config/settings.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class WikipediaConfig:
    ar_family: str = "wikipedia"
    ar_code: str = "ar"
    en_family: str = "wikipedia"
    en_code: str = "en"
    user_agent: str = "CatsMaker/1.0"

@dataclass
class WikidataConfig:
    endpoint: str = "https://www.wikidata.org/w/api.php"
    sparql_endpoint: str = "https://query.wikidata.org/sparql"
    timeout: int = 30

@dataclass
class DatabaseConfig:
    host: Optional[str] = None
    port: int = 3306
    use_sql: bool = True

@dataclass
class Settings:
    wikipedia: WikipediaConfig = WikipediaConfig()
    wikidata: WikidataConfig = WikidataConfig()
    database: DatabaseConfig = DatabaseConfig()

    # Global settings
    range_limit: int = 5
    debug: bool = False
    log_level: str = "INFO"

settings = Settings()
```

**2. تحميل من ملفات بيئة:**
```python
# .env
WIKIPEDIA_AR_CODE=ar
WIKIDATA_ENDPOINT=https://www.wikidata.org/w/api.php
DATABASE_HOST=localhost
RANGE_LIMIT=5
DEBUG=false
```

### 3.5 التوثيق / Documentation

#### مشاكل حالية / Current Issues:
- بعض الدوال بدون docstrings
- توثيق غير متناسق
- نقص الأمثلة

#### الحلول المقترحة / Proposed Solutions:

**1. معيار توثيق موحد:**
```python
def create_categories_from_list(liste: list[str], uselabs: bool = False, callback: Optional[callable] = None) -> None:
    """
    معالجة قائمة من التصنيفات الإنجليزية وإنشاء نظائرها العربية.
    Process a list of English categories and create their Arabic counterparts.

    Args:
        liste: قائمة بأسماء التصنيفات الإنجليزية / List of English category names
        uselabs: استخدام التسميات من ArWikiCats / Use labels from ArWikiCats
        callback: دالة اختيارية للاستدعاء بعد كل تصنيف / Optional callback after each category

    Returns:
        None

    Raises:
        CategoryNotFoundError: إذا لم يتم العثور على التصنيف / If category not found
        WikipediaAPIError: عند فشل استدعاء API / On API call failure

    Examples:
        >>> categories = ["Category:Science", "Category:Mathematics"]
        >>> create_categories_from_list(categories)

        >>> def my_callback(title, **kwargs):
        ...     print(f"Processed: {title}")
        >>> create_categories_from_list(categories, callback=my_callback)

    Notes:
        - يتم تخطي التصنيفات المكررة / Duplicate categories are skipped
        - التصنيفات المعالجة تُضاف إلى DONE_D / Processed categories added to DONE_D

    See Also:
        - one_cat(): معالجة تصنيف واحد / Process one category
        - process_catagories(): المعالجة المتكررة / Recursive processing
    """
    pass
```

**2. توثيق البنية:**
```markdown
# docs/architecture.md
# البنية المعمارية للمشروع / Project Architecture

## نظرة عامة / Overview
...

## الوحدات / Modules
...

## تدفق البيانات / Data Flow
...
```

### 3.6 الأداء / Performance

#### نقاط التحسين / Optimization Points:

**1. Batch Processing:**
```python
# Before: معالجة فردية
for qid in qids:
    data = Get_Item_API_From_Qid(qid)

# After: معالجة دفعات
batch_size = 50
for i in range(0, len(qids), batch_size):
    batch = qids[i:i+batch_size]
    data = Get_Items_API_From_Qids(batch)  # معالجة دفعة واحدة
```

**2. Async/Await للعمليات المتوازية:**
```python
import asyncio

async def process_categories_async(categories: list[str]):
    """معالجة عدة تصنيفات بالتوازي"""
    tasks = [process_one_category_async(cat) for cat in categories]
    results = await asyncio.gather(*tasks)
    return results
```

**3. تحسين استعلامات SQL:**
```python
# Before: استعلامات متعددة
for title in titles:
    result = sql_new(f"SELECT * FROM page WHERE page_title = '{title}'")

# After: استعلام واحد
placeholders = ','.join(['%s'] * len(titles))
query = f"SELECT * FROM page WHERE page_title IN ({placeholders})"
results = sql_new(query, values=titles)
```

---

## 4. جودة الكود / Code Quality

### 4.1 Type Hints

إضافة type hints لجميع الدوال:

```python
from typing import List, Dict, Optional, Tuple, Callable

def ar_make_lab(title: str, **kwargs) -> Optional[str]:
    """إنشاء تسمية عربية / Create Arabic label"""
    pass

def get_ar_list_from_en(
    encat: str,
    us_sql: bool = True,
    wiki: str = "en"
) -> List[str]:
    """الحصول على قائمة عربية من تصنيف إنجليزي"""
    pass
```

### 4.2 Code Style

اتباع PEP 8 و Black formatter:

```python
# استخدام Black formatter
# استخدام isort لترتيب imports
# اتباع معايير PEP 8
```

### 4.3 Linting

```bash
# استخدام ruff للفحص السريع
ruff check src/

# استخدام mypy للتحقق من الأنواع
mypy src/

# استخدام pylint للفحص الشامل
pylint src/
```

---

## 5. الخلاصة / Summary

### 5.1 التحسينات المطلوبة / Required Improvements

- [ ] فصل منطق الأعمال عن I/O
- [ ] إنشاء طبقة repository منفصلة
- [ ] توحيد معالجة الأخطاء
- [ ] نظام تخزين مؤقت موحد
- [ ] ملف تكوين مركزي
- [ ] إضافة type hints
- [ ] توثيق شامل لجميع الدوال
- [ ] تحسين الأداء (batch, async)
- [ ] إزالة الكود المكرر
- [ ] تحسين أسماء المتغيرات

### 5.2 الفوائد المتوقعة / Expected Benefits

✅ **قابلية الاختبار / Testability**
- سهولة كتابة unit tests
- سهولة mocking للتبعيات

✅ **قابلية الصيانة / Maintainability**
- كود أوضح وأسهل للفهم
- سهولة إضافة ميزات جديدة

✅ **الأداء / Performance**
- تقليل الاستدعاءات المتكررة
- معالجة دفعات
- عمليات متوازية

✅ **الموثوقية / Reliability**
- معالجة أخطاء أفضل
- تتبع أفضل للمشاكل
- استرداد من الأخطاء

---

**آخر تحديث / Last Updated:** 2025-12-30
**الحالة / Status:** 🟢 جاهزة للتنفيذ / Ready for Implementation

**ملف مرتبط / Related File:** `testing_plan.md` - يحتوي على خطة الاختبار الشاملة
