# خطة إعادة البناء والاختبار الشاملة
## Comprehensive Refactoring and Testing Plan

## نظرة عامة / Overview

هذه الخطة تهدف إلى إعادة هيكلة وإنشاء اختبارات شاملة لجميع وظائف المشروع باستثناء وحدة `new_api`. تم تحديد 142 دالة في 50 ملف Python تحتاج إلى تغطية اختبارية.

This plan aims to refactor and create comprehensive tests for all project functions excluding the `new_api` module. We identified 142 functions across 50 Python files that need test coverage.

---

## 0. تدفق التنفيذ الرئيسي / Main Execution Flow

### نقطة الدخول الرئيسية / Main Entry Point

**الدالة الأساسية:** `create_categories_from_list(liste, uselabs=False, callback=None)`
- **الموقع / Location:** `src/mk_cats/mknew.py`
- **الاسم القديم / Legacy name:** `ToMakeNewCat2222`

### تسلسل التنفيذ / Execution Sequence

```
run.py (main entry)
    ↓
create_categories_from_list()
    ↓
    → one_cat() - لكل تصنيف / For each category
        ↓
        → ar_make_lab() - إنشاء التسمية العربية / Create Arabic label
        ↓
        → check_en_temps() - فحص القالب الإنجليزي / Check English template
        ↓
        → get_ar_list_from_en() - الحصول على القائمة العربية / Get Arabic list
        ↓
        → process_catagories() - معالجة التصنيف / Process category
            ↓
            → make_ar() - إنشاء التصنيف العربي / Create Arabic category
                ↓
                → scan_ar_title() - فحص العنوان العربي / Scan Arabic title
                ↓
                → check_if_artitle_exists() - التحقق من وجود العنوان / Check title exists
                ↓
                → find_LCN() - البحث عن رابط اللغة / Find language link
                ↓
                → Get_Sitelinks_From_wikidata() - روابط ويكي بيانات / Wikidata sitelinks
                ↓
                → find_Page_Cat_without_hidden() - البحث عن تصنيفات الصفحة / Find page categories
                ↓
                → get_listenpageTitle() - الحصول على قائمة الأعضاء / Get member list
                ↓
                → new_category() - إنشاء صفحة التصنيف / Create category page
                    ↓
                    → make_text() - إنشاء نص التصنيف / Create category text
                    ↓
                    → himoBOT2.page_put() - حفظ الصفحة / Save page
                ↓
                → add_to_final_list() - إضافة للقائمة النهائية / Add to final list
                ↓
                → to_wd.Log_to_wikidata() - تسجيل في ويكي بيانات / Log to Wikidata
```

### الوحدات المشاركة في التدفق / Modules Involved in Flow

1. **run.py** - نقطة الدخول / Entry point
2. **mk_cats/mknew.py** - المنطق الرئيسي / Main logic
3. **b18_new/** - معالجة التصنيفات والروابط / Category and link processing
4. **c18_new/** - أدوات التصنيفات / Category tools
5. **wd_bots/** - تكامل ويكي بيانات / Wikidata integration
6. **wiki_api/** - استدعاءات API / API calls
7. **api_sql/** - قاعدة البيانات / Database operations
8. **helps/** - أدوات مساعدة / Helper utilities

### أهمية هذا التدفق للاختبار / Importance for Testing

- ✅ الاختبارات يجب أن تغطي التدفق الكامل من البداية للنهاية
- ✅ اختبارات التكامل يجب أن تحاكي هذا المسار
- ✅ كل دالة في المسار تحتاج اختبارات وحدة مستقلة
- ✅ Mock الخدمات الخارجية (API, Database, Wikidata) ضروري

---

## 1. الوحدات الرئيسية المستهدفة / Target Modules

### 1.1 api_sql - قاعدة البيانات / Database Module
**الملفات / Files:**
- `wiki_sql.py`
- `sql_qu.py`
- `wikidb.py`
- `lite_db_bot.py`

**الدوال الرئيسية / Main Functions:**
- `add_nstext_to_title()` - إضافة نص النطاق إلى العنوان
- `make_labsdb_dbs_p()` - إنشاء اتصال قاعدة البيانات
- `sql_new()` - تنفيذ استعلامات SQL
- `sql_new_title_ns()` - استعلام العناوين مع النطاقات
- `sql_connect_pymysql()` - اتصال PyMySQL
- `make_sql_connect()` - إنشاء اتصال SQL

**خطة الاختبار / Test Plan:**
- [ ] اختبار إضافة نطاقات للغة العربية والإنجليزية
- [ ] اختبار معالجة النطاق "0" (المقالات)
- [ ] اختبار إنشاء سلاسل اتصال قاعدة البيانات
- [ ] اختبار تنفيذ استعلامات SQL بقيم مختلفة
- [ ] اختبار معالجة الأخطاء عند فشل الاتصال
- [ ] اختبار تحويل البايتات إلى نصوص
- [ ] Mock قاعدة البيانات لتجنب الاتصالات الحقيقية
- [ ] اختبار LiteDB للتخزين المؤقت

**أولوية / Priority:** عالية / High

---

### 1.2 b18_new - معالجة التصنيفات / Category Processing
**الملفات / Files:**
- `LCN_new.py`
- `cat_tools.py`
- `cat_tools_enlist.py`
- `cat_tools_enlist2.py`
- `add_bot.py`
- `sql_cat.py`

**الدوال الرئيسية / Main Functions:**
- `find_LCN()` - البحث عن روابط اللغات
- `find_Page_Cat_without_hidden()` - البحث عن تصنيفات الصفحة
- `get_ar_list_from_cat()` - الحصول على قائمة عربية من تصنيف
- `get_ar_list_from_en()` - الحصول على قائمة عربية من تصنيف إنجليزي
- `add_to_page()` - إضافة تصنيف لصفحة
- `work_in_one_cat()` - معالجة تصنيف واحد
- `get_SubSub_value()` / `get_SubSub_keys()` - إدارة التصنيفات الفرعية

**خطة الاختبار / Test Plan:**
- [ ] اختبار البحث عن روابط اللغات بين ويكيبيديا العربية والإنجليزية
- [ ] اختبار التعامل مع التصنيفات المخفية
- [ ] اختبار القائمة السوداء للقوالب (templateblacklist)
- [ ] اختبار القائمة السوداء للأسماء (nameblcklist)
- [ ] اختبار التخزين المؤقت (WikiApiCache)
- [ ] اختبار معالجة العناوين بنطاقات مختلفة
- [ ] Mock استدعاءات API
- [ ] اختبار حالات الفشل والاستثناءات

**أولوية / Priority:** عالية جداً / Very High

---

### 1.3 c18_new - أدوات التصنيفات / Category Tools
**الملفات / Files:**
- `cat_tools2.py`
- `bots/cat_tools_argv.py`
- `bots/english_page_title.py`
- `bots/filter_cat.py`
- `bots/text_to_temp_bot.py`
- `bots_helps/dontadd.py`
- `bots_helps/funcs.py`
- `cats_tools/ar_from_en.py`
- `cats_tools/ar_from_en2.py`
- `cats_tools/en_link_bot.py`
- `network_calls/sub_cats_bot.py`
- `tools_bots/encat_like.py`
- `tools_bots/sort_bot.py`
- `tools_bots/sql_bot.py`
- `tools_bots/temp_bot.py`

**الدوال الرئيسية / Main Functions:**
- `get_english_page_title()` - الحصول على عنوان الصفحة الإنجليزية
- `filter_cats_text()` - تصفية التصنيفات من النص
- `add_to_text_temps()` - إضافة التصنيفات للقوالب
- `find_doc_and_add()` - البحث عن صفحة التوثيق
- `add_text_to_template()` - إضافة نص للقالب
- `english_page_link()` - الحصول على رابط الصفحة الإنجليزية
- `Get_ar_list_title_from_en_list()` - تحويل قائمة إنجليزية لعربية
- `make_ar_list_from_en_cat()` - إنشاء قائمة عربية من تصنيف إنجليزي

**خطة الاختبار / Test Plan:**
- [ ] اختبار الحصول على العناوين الإنجليزية
- [ ] اختبار تصفية التصنيفات من نصوص مختلفة
- [ ] اختبار إضافة التصنيفات للقوالب
- [ ] اختبار معالجة صفحات التوثيق (/doc)
- [ ] اختبار تحويل قوائم من الإنجليزية للعربية
- [ ] اختبار معالجة الروابط بين اللغات
- [ ] اختبار القائمة السوداء (Dont_add_to_pages_def)
- [ ] Mock استدعاءات الشبكة
- [ ] اختبار معالجة ملفات JSON

**أولوية / Priority:** عالية جداً / Very High

---

### 1.4 helps - المساعدات / Helper Utilities
**الملفات / Files:**
- `log.py`
- `printe_helper.py`
- `jsonl_data.py`

**الدوال الرئيسية / Main Functions:**
- `LoggerWrap` class - غلاف للتسجيل
- `make_str()` - تنسيق النصوص الملونة
- `get_color_table()` - جدول الألوان
- `save()` - حفظ بيانات JSON
- `dump_data()` - تفريغ البيانات

**خطة الاختبار / Test Plan:**
- [ ] اختبار LoggerWrap مع مستويات تسجيل مختلفة
- [ ] اختبار تنسيق النصوص الملونة
- [ ] اختبار showDiff() لعرض الفروق
- [ ] اختبار تعطيل/تفعيل المسجل
- [ ] اختبار حفظ وتحميل بيانات JSON/JSONL
- [ ] اختبار معالجة الأخطاء في الحفظ والتحميل

**أولوية / Priority:** متوسطة / Medium

---

### 1.5 mk_cats - إنشاء التصنيفات / Category Creation
**⭐ الوحدة الأساسية - تحتوي على نقطة الدخول الرئيسية**

**الملفات / Files:**
- `categorytext.py`
- `create_category_page.py`
- `mknew.py` ⭐ **الملف الرئيسي / Main File**
- `mk_bots/filter_en.py`
- `mk_bots/log_catlinks.py`
- `utils/check_en.py`
- `utils/portal_list.py`

**الدوال الرئيسية / Main Functions:**

**في mknew.py:**
- `create_categories_from_list()` ⭐ **نقطة الدخول الرئيسية / Main Entry Point**
- `one_cat()` - معالجة تصنيف واحد / Process one category
- `process_catagories()` - معالجة التصنيف بشكل متكرر / Process category recursively
- `make_ar()` - إنشاء تصنيف عربي / Create Arabic category
- `ar_make_lab()` - إنشاء تسمية عربية / Create Arabic label
- `scan_ar_title()` - فحص العنوان العربي / Scan Arabic title
- `check_if_artitle_exists()` - التحقق من وجود العنوان / Check title exists

**في create_category_page.py:**
- `new_category()` - إنشاء صفحة تصنيف جديدة / Create new category page
- `make_category()` - إنشاء تصنيف / Create category
- `add_text_to_cat()` - إضافة نص للتصنيف / Add text to category

**في categorytext.py:**
- `make_text()` - إنشاء نص التصنيف / Create category text
- `Make_temp()` - إنشاء قالب / Create template
- `Make_Portal()` - إنشاء بوابة / Create portal
- `getP373()` - الحصول على P373 من ويكي بيانات / Get P373 from Wikidata

**خطة الاختبار / Test Plan:**
- [ ] **اختبار create_categories_from_list() - الدالة الأساسية**
- [ ] **اختبار one_cat() - معالجة تصنيف واحد**
- [ ] **اختبار process_catagories() - المعالجة المتكررة**
- [ ] **اختبار make_ar() - إنشاء تصنيف عربي**
- [ ] اختبار ar_make_lab() - إنشاء التسمية العربية
- [ ] اختبار scan_ar_title() - فحص العناوين
- [ ] اختبار check_if_artitle_exists() - التحقق من الوجود
- [ ] اختبار new_category() - إنشاء صفحة التصنيف
- [ ] اختبار make_text() - إنشاء نص التصنيف
- [ ] اختبار Make_temp() و Make_Portal()
- [ ] اختبار check_en_temps() - فحص القوالب الإنجليزية
- [ ] اختبار getP373() - الحصول على P373 من Wikidata
- [ ] Mock جميع استدعاءات الخدمات الخارجية
- [ ] اختبارات تكامل للتدفق الكامل من create_categories_from_list
- [ ] اختبار معالجة قوائم التصنيفات المختلفة

**أولوية / Priority:** عالية جداً ⭐⭐⭐ / Very High ⭐⭐⭐

---

### 1.6 temp - القوالب / Templates
**الملفات / Files:**
- `bots/new.py`
- `bots/temp_cent.py`
- `bots/temp_decades.py`
- `bots/temp_elff.py`
- `bots/temp_years.py`
- `bots/load_data.py`

**الدوال الرئيسية / Main Functions:**
- `Make_Cent_temp()` - إنشاء قالب قرن
- `Make_Elff_temp()` - إنشاء قالب ألفية
- `Make_years_temp()` - إنشاء قالب سنة
- `MakedecadesTemp()` - إنشاء قالب عقد
- `main_make_temp()` - الدالة الرئيسية لإنشاء القوالب
- `TemplatesMaker` class - صانع القوالب

**خطة الاختبار / Test Plan:**
- [ ] اختبار إنشاء قوالب القرون (Centuries)
- [ ] اختبار إنشاء قوالب العقود (Decades)
- [ ] اختبار إنشاء قوالب السنوات (Years)
- [ ] اختبار إنشاء قوالب الألفيات (Millennia)
- [ ] اختبار معالجة أسماء مختلفة للقرون والعقود
- [ ] اختبار توليد نص القالب بشكل صحيح
- [ ] اختبار تحميل البيانات (load_data)
- [ ] اختبار حالات الفشل والاستثناءات

**ملاحظة:** هذه الوحدة لديها بالفعل بعض الاختبارات في `tests/temp/`

**أولوية / Priority:** متوسطة / Medium

---

### 1.7 wd_bots - بوتات ويكي بيانات / Wikidata Bots
**الملفات / Files:**
- `bot_wd.py`
- `get_bots.py`
- `newdesc.py`
- `qs_bot.py`
- `submit_bot.py`
- `to_wd.py`
- `wb_rest_api.py`
- `wd_api_bot.py`
- `wd_desc.py`
- `wd_login_wrap.py`
- `wd_newapi_bot.py`
- `wd_sparql_bot.py`
- `utils/handle_wd_errors.py`
- `utils/lag_bot.py`
- `utils/out_json.py`

**الدوال الرئيسية / Main Functions:**
- `Get_infos_wikidata()` - الحصول على معلومات من ويكي بيانات
- `Get_Sitelinks_From_wikidata()` - الحصول على روابط المواقع
- `Get_Item_API_From_Qid()` - الحصول على عنصر من QID
- `Get_Items_API_From_Qids()` - الحصول على عناصر من QIDs
- `Get_P373_API()` - الحصول على P373
- `Get_Property_API()` - الحصول على خاصية
- `Get_Claim_API()` - الحصول على ادعاء
- `outbot_json()` - إخراج JSON
- `find_lag()` - البحث عن التأخير
- `do_lag()` - معالجة التأخير
- `format_sitelinks()` - تنسيق روابط المواقع
- `format_labels_descriptions()` - تنسيق التسميات والأوصاف

**خطة الاختبار / Test Plan:**
- [ ] اختبار الحصول على معلومات من Wikidata API
- [ ] اختبار الحصول على sitelinks
- [ ] اختبار الحصول على labels و descriptions
- [ ] اختبار الحصول على properties و claims
- [ ] اختبار معالجة أخطاء Wikidata API
- [ ] اختبار معالجة lag و maxlag
- [ ] اختبار تنسيق البيانات
- [ ] Mock جميع استدعاءات Wikidata API
- [ ] اختبار SPARQL queries
- [ ] اختبار REST API الجديد

**أولوية / Priority:** عالية / High

---

### 1.8 wiki_api - واجهة برمجة التطبيقات / Wikipedia API
**الملفات / Files:**
- `arAPI.py`
- `himoBOT2.py`
- `wd_sparql.py`

**الدوال الرئيسية / Main Functions:**
- `submitAPI()` - إرسال طلب API
- `Get_Newpages()` - الحصول على صفحات جديدة
- `Get_page_info_from_wikipedia_new()` - الحصول على معلومات الصفحة
- `GetPagelinks()` - الحصول على روابط الصفحة
- `get_en_link_from_ar_text()` - الحصول على رابط إنجليزي من نص عربي
- `Add_To_Head()` - إضافة نص في البداية
- `Add_To_Bottom()` - إضافة نص في النهاية
- `create_Page()` - إنشاء صفحة
- `page_put()` - حفظ صفحة
- `get_query_data()` - الحصول على بيانات من SPARQL
- `get_query_result()` - الحصول على نتائج SPARQL

**خطة الاختبار / Test Plan:**
- [ ] اختبار إرسال طلبات API (GET/POST)
- [ ] اختبار الحصول على معلومات الصفحات
- [ ] اختبار الحصول على الصفحات الجديدة
- [ ] اختبار إضافة نص للصفحات (رأس/نهاية)
- [ ] اختبار إنشاء صفحات جديدة
- [ ] اختبار حفظ التعديلات
- [ ] اختبار SPARQL queries
- [ ] Mock جميع استدعاءات MediaWiki API
- [ ] اختبار معالجة الأخطاء والاستثناءات
- [ ] اختبار إدارة الجلسات (sessions)

**أولوية / Priority:** عالية جداً / Very High

---

### 1.9 utils - الأدوات المساعدة / Utilities
**الملفات / Files:**
- `skip_cats.py`

**الدوال الرئيسية / Main Functions:**
- القوائم السوداء والثوابت

**خطة الاختبار / Test Plan:**
- [ ] اختبار القوائم السوداء
- [ ] اختبار الثوابت المستخدمة في المشروع

**أولوية / Priority:** منخفضة / Low

---

## 2. استراتيجية الاختبار / Testing Strategy

### 2.1 أنواع الاختبارات / Test Types

#### Unit Tests (اختبارات الوحدات)
- اختبار كل دالة بشكل مستقل
- استخدام mocks للتبعيات الخارجية
- تغطية حالات النجاح والفشل

#### Integration Tests (اختبارات التكامل)
- اختبار تفاعل الوحدات مع بعضها
- اختبار تدفق البيانات بين الوحدات
- استخدام بيانات اختبار واقعية (مع mocking للخدمات الخارجية)

#### Fixture Tests (اختبارات البيانات الثابتة)
- إنشاء بيانات اختبار قابلة لإعادة الاستخدام
- استخدام pytest fixtures
- بيانات اختبار للتصنيفات والصفحات والقوالب

### 2.2 أدوات الاختبار / Testing Tools

```python
# الأدوات المطلوبة / Required Tools:
- pytest (الإطار الرئيسي / Main framework)
- pytest-cov (تغطية الكود / Code coverage)
- pytest-mock (mocking)
- responses (mock HTTP requests)
- freezegun (mock datetime)
```

### 2.3 Mocking Strategy (استراتيجية المحاكاة)

**الخدمات التي تحتاج Mock:**
1. Wikipedia API calls
2. Wikidata API calls
3. Database connections (MySQL/SQLite)
4. File system operations
5. Network requests
6. External services

**مثال على Mock:**
```python
@pytest.fixture
def mock_wikipedia_api(mocker):
    """Mock Wikipedia API calls"""
    return mocker.patch('src.wiki_api.arAPI.submitAPI')

@pytest.fixture
def mock_wikidata_api(mocker):
    """Mock Wikidata API calls"""
    return mocker.patch('src.wd_bots.wd_api_bot.Get_infos_wikidata')

@pytest.fixture
def mock_database(mocker):
    """Mock database connections"""
    return mocker.patch('src.api_sql.sql_qu.make_sql_connect')
```

---

## 3. هيكل ملفات الاختبار / Test File Structure

```
tests/
├── conftest.py                    # مشترك / Shared fixtures
├── integration/                   # ⭐ اختبارات التكامل / Integration tests
│   ├── __init__.py
│   └── test_main_flow.py         # اختبار التدفق الرئيسي الكامل
├── api_sql/
│   ├── __init__.py
│   ├── test_wiki_sql.py          # اختبار wiki_sql.py
│   ├── test_sql_qu.py            # اختبار sql_qu.py
│   ├── test_wikidb.py            # اختبار wikidb.py
│   └── test_lite_db_bot.py       # اختبار lite_db_bot.py
├── b18_new/
│   ├── __init__.py
│   ├── test_LCN_new.py           # اختبار LCN_new.py
│   ├── test_cat_tools.py         # اختبار cat_tools.py
│   ├── test_cat_tools_enlist.py  # اختبار cat_tools_enlist.py
│   ├── test_cat_tools_enlist2.py # اختبار cat_tools_enlist2.py
│   ├── test_add_bot.py           # اختبار add_bot.py
│   └── test_sql_cat.py           # اختبار sql_cat.py
├── c18_new/
│   ├── __init__.py
│   ├── test_cat_tools2.py        # اختبار cat_tools2.py
│   ├── bots/
│   │   ├── test_cat_tools_argv.py
│   │   ├── test_english_page_title.py
│   │   ├── test_filter_cat.py
│   │   └── test_text_to_temp_bot.py
│   ├── bots_helps/
│   │   ├── test_dontadd.py
│   │   └── test_funcs.py
│   ├── cats_tools/
│   │   ├── test_ar_from_en.py
│   │   ├── test_ar_from_en2.py
│   │   └── test_en_link_bot.py
│   ├── network_calls/
│   │   └── test_sub_cats_bot.py
│   └── tools_bots/
│       ├── test_encat_like.py
│       ├── test_sort_bot.py
│       ├── test_sql_bot.py
│       └── test_temp_bot.py
├── helps/
│   ├── __init__.py
│   ├── test_log.py               # اختبار log.py
│   ├── test_printe_helper.py     # اختبار printe_helper.py
│   └── test_jsonl_data.py        # اختبار jsonl_data.py
├── mk_cats/
│   ├── __init__.py
│   ├── test_categorytext.py      # اختبار categorytext.py
│   ├── test_create_category_page.py
│   ├── test_mknew.py             # اختبار mknew.py
│   ├── mk_bots/
│   │   ├── test_filter_en.py
│   │   └── test_log_catlinks.py
│   └── utils/
│       ├── test_check_en.py
│       └── test_portal_list.py
├── temp/                         # موجود بالفعل / Already exists
│   ├── test_make_cent_temp.py    # ✓ موجود
│   ├── test_makedecades_temp.py  # ✓ موجود
│   ├── test_make_elff_temp.py    # ✓ موجود
│   └── test_make_years_temp.py   # ✓ موجود
├── utils/
│   ├── __init__.py
│   └── test_skip_cats.py
├── wd_bots/
│   ├── __init__.py
│   ├── test_bot_wd.py
│   ├── test_get_bots.py
│   ├── test_newdesc.py
│   ├── test_qs_bot.py
│   ├── test_submit_bot.py
│   ├── test_to_wd.py
│   ├── test_wb_rest_api.py
│   ├── test_wd_api_bot.py
│   ├── test_wd_desc.py
│   ├── test_wd_login_wrap.py
│   ├── test_wd_newapi_bot.py
│   ├── test_wd_sparql_bot.py
│   └── utils/
│       ├── test_handle_wd_errors.py
│       ├── test_lag_bot.py
│       └── test_out_json.py
└── wiki_api/
    ├── __init__.py
    ├── test_arAPI.py             # اختبار arAPI.py
    ├── test_himoBOT2.py          # اختبار himoBOT2.py
    └── test_wd_sparql.py         # اختبار wd_sparql.py
```

---

## 4. خطة التنفيذ / Implementation Plan

### المرحلة 1: التحضير (Preparation)
**المدة: 1-2 أيام / Duration: 1-2 days**

- [x] تحليل الكود الحالي
- [x] إنشاء خطة الاختبار هذه
- [ ] إعداد بيئة الاختبار
- [ ] إنشاء `conftest.py` مع fixtures مشتركة
- [ ] إعداد أدوات mocking

### المرحلة 2: الاختبارات الأساسية (Core Tests)
**المدة: 3-5 أيام / Duration: 3-5 days**

**الأولوية العالية جداً (البدء هنا):**
- [ ] **mk_cats** ⭐ (الوحدة الأساسية - تحتوي على create_categories_from_list)
- [ ] **b18_new** (معالجة التصنيفات - مطلوبة من mk_cats)
- [ ] **c18_new** (أدوات التصنيفات - مطلوبة من mk_cats)
- [ ] **wiki_api** (استدعاءات API الأساسية - مطلوبة لحفظ الصفحات)

### المرحلة 3: اختبارات قاعدة البيانات والخدمات
**المدة: 2-3 أيام / Duration: 2-3 days**

**الأولوية العالية:**
- [ ] api_sql (قاعدة البيانات)
- [ ] wd_bots (ويكي بيانات - مطلوبة من mk_cats)

### المرحلة 4: الاختبارات التكميلية
**المدة: 2-3 أيام / Duration: 2-3 days**

**الأولوية المتوسطة:**
- [ ] helps (المساعدات)
- [ ] temp (تحسين الاختبارات الموجودة)

**الأولوية المنخفضة:**
- [ ] utils (الأدوات المساعدة)

### المرحلة 5: التكامل والتحسين
**المدة: 2-3 أيام / Duration: 2-3 days**

- [ ] اختبارات التكامل بين الوحدات
- [ ] تحسين تغطية الكود (هدف: >80%)
- [ ] مراجعة وتحسين الاختبارات
- [ ] توثيق الاختبارات

---

## 5. معايير جودة الاختبار / Test Quality Standards

### 5.1 تغطية الكود / Code Coverage
- **الهدف:** 80% أو أكثر لكل وحدة
- **الأدوات:** pytest-cov
- **التقرير:** تقرير HTML تفصيلي

### 5.2 معايير الاختبار / Test Standards
- كل دالة يجب أن يكون لها على الأقل:
  - اختبار واحد للحالة الطبيعية (happy path)
  - اختبار واحد للحالة الخاطئة (error case)
  - اختبارات للحالات الحدية (edge cases)

### 5.3 تسمية الاختبارات / Test Naming
```python
# نمط التسمية / Naming pattern:
def test_<function_name>_<scenario>_<expected_result>():
    """
    اختبار <وصف الحالة>
    Test <scenario description>
    """
    pass

# أمثلة / Examples:
def test_add_nstext_to_title_with_namespace_0_returns_original_title():
    """اختبار إرجاع العنوان الأصلي عند استخدام namespace 0"""
    pass

def test_find_LCN_with_invalid_site_raises_exception():
    """اختبار رفع استثناء عند استخدام موقع غير صالح"""
    pass
```

### 5.4 توثيق الاختبارات / Test Documentation
- كل ملف اختبار يجب أن يحتوي على docstring يشرح:
  - ما الذي يتم اختباره
  - الحالات المغطاة
  - المتطلبات الخاصة

---

## 6. إعادة الهيكلة المطلوبة / Required Refactoring

### 6.1 فصل المنطق / Separation of Concerns
- [ ] فصل منطق الأعمال عن استدعاءات API
- [ ] إنشاء طبقة data access منفصلة
- [ ] تحسين قابلية الاختبار

### 6.2 معالجة الأخطاء / Error Handling
- [ ] توحيد معالجة الأخطاء
- [ ] إضافة استثناءات مخصصة
- [ ] تحسين رسائل الأخطاء

### 6.3 التوثيق / Documentation
- [ ] إضافة docstrings لجميع الدوال
- [ ] توثيق المعاملات والقيم المُرجعة
- [ ] إضافة أمثلة استخدام

### 6.4 التحسينات / Improvements
- [ ] إزالة الكود المكرر (DRY principle)
- [ ] تحسين أسماء المتغيرات والدوال
- [ ] تحسين الأداء حيث أمكن

---

## 7. التكوين / Configuration

### 7.1 pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --cov=src
    --cov-report=html
    --cov-report=term
    --cov-report=xml
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    api: Tests requiring API access (mocked)
    db: Tests requiring database (mocked)
```

### 7.2 متطلبات الاختبار / Test Requirements
```txt
# requirements-test.txt
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.1
responses>=0.23.1
freezegun>=1.2.2
faker>=19.3.0
```

---

## 8. أمثلة على الاختبارات / Test Examples

### مثال 1: اختبار دالة بسيطة
```python
# tests/api_sql/test_wiki_sql.py
import pytest
from src.api_sql.wiki_sql import add_nstext_to_title

class TestAddNsTextToTitle:
    """اختبارات لدالة add_nstext_to_title"""
    
    def test_with_namespace_0_returns_original_title(self):
        """اختبار إرجاع العنوان الأصلي مع namespace 0"""
        result = add_nstext_to_title("محمد", "0", "ar")
        assert result == "محمد"
    
    def test_with_category_namespace_ar(self):
        """اختبار إضافة نص تصنيف للغة العربية"""
        result = add_nstext_to_title("علوم", "14", "ar")
        assert result == "تصنيف:علوم"
    
    def test_with_template_namespace_en(self):
        """اختبار إضافة نص قالب للغة الإنجليزية"""
        result = add_nstext_to_title("Science", "10", "en")
        assert result == "Template:Science"
    
    def test_with_invalid_namespace(self):
        """اختبار مع namespace غير موجود"""
        result = add_nstext_to_title("Test", "999", "ar")
        # يجب أن يرجع العنوان الأصلي أو يتعامل بشكل مناسب
        assert result == "Test"
```

### مثال 2: اختبار مع Mock
```python
# tests/b18_new/test_LCN_new.py
import pytest
from src.b18_new.LCN_new import find_LCN

class TestFindLCN:
    """اختبارات لدالة find_LCN"""
    
    @pytest.fixture
    def mock_api_response(self):
        """Mock response من Wikipedia API"""
        return {
            "query": {
                "pages": {
                    "123": {
                        "title": "العلوم",
                        "langlinks": [
                            {"lang": "en", "*": "Science"}
                        ]
                    }
                }
            }
        }
    
    def test_find_LCN_success(self, mocker, mock_api_response):
        """اختبار البحث عن رابط لغة بنجاح"""
        # Mock API call
        mock_submit = mocker.patch(
            'src.b18_new.LCN_new.submitAPI',
            return_value=mock_api_response
        )
        
        result = find_LCN("Science", lllang="ar", first_site_code="en")
        
        assert result == "العلوم"
        mock_submit.assert_called_once()
    
    def test_find_LCN_no_langlink(self, mocker):
        """اختبار عدم وجود رابط لغة"""
        mock_response = {
            "query": {
                "pages": {
                    "123": {
                        "title": "Test",
                        "langlinks": []
                    }
                }
            }
        }
        
        mocker.patch(
            'src.b18_new.LCN_new.submitAPI',
            return_value=mock_response
        )
        
        result = find_LCN("Test", lllang="ar", first_site_code="en")
        assert result is None or result == ""
```

### مثال 3: اختبار مع Fixture
```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_category_data():
    """بيانات تصنيف للاختبار"""
    return {
        "en_title": "Science",
        "ar_title": "علوم",
        "namespace": "14",
        "members": ["Physics", "Chemistry", "Biology"]
    }

@pytest.fixture
def mock_database(mocker):
    """Mock لقاعدة البيانات"""
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch(
        'src.api_sql.sql_qu.make_sql_connect',
        return_value=mock_conn
    )
    
    return mock_cursor

# tests/c18_new/test_cat_tools2.py
def test_using_fixtures(sample_category_data, mock_database):
    """مثال على استخدام fixtures"""
    # استخدام البيانات والmocks
    assert sample_category_data["en_title"] == "Science"
```

---

## 9. المقاييس والنتائج المتوقعة / Metrics and Expected Outcomes

### 9.1 مقاييس النجاح / Success Metrics
- ✅ تغطية كود 80%+ لجميع الوحدات
- ✅ جميع الاختبارات تنجح (100% pass rate)
- ✅ لا توجد اختبارات متقطعة (flaky tests)
- ✅ زمن تنفيذ الاختبارات < 5 دقائق
- ✅ توثيق شامل لجميع الاختبارات

### 9.2 التقارير / Reports
- تقرير تغطية HTML
- تقرير نتائج الاختبارات
- تقرير الأداء

### 9.3 CI/CD Integration
- إضافة الاختبارات إلى GitHub Actions
- فحص تلقائي للـ Pull Requests
- منع الدمج إذا فشلت الاختبارات

---

## 10. الملاحظات والتحديات / Notes and Challenges

### 10.1 التحديات المتوقعة / Expected Challenges
1. **الاعتماديات الخارجية:** الكثير من الدوال تعتمد على Wikipedia API و Wikidata API
   - **الحل:** استخدام mocking شامل

2. **قاعدة البيانات:** اتصالات قواعد البيانات الحقيقية
   - **الحل:** استخدام SQLite في الذاكرة أو mocking

3. **الكود القديم:** بعض الأجزاء قد تحتاج إعادة هيكلة قبل الاختبار
   - **الحل:** إعادة هيكلة تدريجية

4. **التبعيات المتشابكة:** بعض الوحدات مترابطة بشكل كبير
   - **الحل:** استخدام dependency injection حيث أمكن

### 10.2 ملاحظات مهمة / Important Notes
- تم استثناء `new_api` كما طُلب
- بعض الاختبارات موجودة بالفعل في `tests/temp/` و `tests/new_api/`
- يجب مراعاة عدم كسر الكود الموجود أثناء إعادة الهيكلة
- الاختبارات يجب أن تكون سريعة ومستقلة

### 10.3 موارد إضافية / Additional Resources
- [pytest documentation](https://docs.pytest.org/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)
- [responses](https://github.com/getsentry/responses)
- [Best practices for testing](https://docs.python-guide.org/writing/tests/)

---

## 11. الخلاصة / Summary

هذه الخطة تغطي:
- **142 دالة** في **50 ملف Python**
- **9 وحدات رئيسية** (باستثناء new_api)
- **~60-70 ملف اختبار جديد** سيتم إنشاؤها
- **تقدير الوقت:** 10-14 يوم عمل
- **الهدف:** تغطية 80%+ واختبارات شاملة

### نقطة الدخول الرئيسية / Main Entry Point
⭐ **`create_categories_from_list()`** في `src/mk_cats/mknew.py` هي الدالة الأساسية التي تبدأ منها كل العمليات

### ترتيب الأولويات (محدّث) / Priority Order (Updated):
1. **عالية جداً ⭐⭐⭐:** 
   - **mk_cats** (الوحدة الأساسية - تحتوي على نقطة الدخول الرئيسية)
   - **b18_new** (معالجة التصنيفات - مطلوبة من mk_cats)
   - **c18_new** (أدوات التصنيفات - مطلوبة من mk_cats)
   - **wiki_api** (استدعاءات API - مطلوبة لحفظ الصفحات)
2. **عالية:** api_sql, wd_bots
3. **متوسطة:** helps, temp
4. **منخفضة:** utils

### التدفق الرئيسي للاختبار / Main Testing Flow
الاختبارات يجب أن تتبع تدفق التنفيذ الطبيعي:
```
create_categories_from_list → one_cat → process_catagories → make_ar → new_category
```

---

**آخر تحديث / Last Updated:** 2025-12-30
**الحالة / Status:** 🟢 محدّثة ومراجعة / Updated and Reviewed
