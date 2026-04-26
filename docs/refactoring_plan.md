# خطة إعادة هيكلة `c18_new`

## ملخص تنفيذي

تهدف هذه الخطة إلى تحويل وحدة `src/c18_new` من حالة "النصوص البرمجية القديمة السريعة" إلى وحدة **صيانية، قابلة للاختبار، وخالية من التكرار**. تتركز الخطة على خمس مراحل متتالية: النظافة البرمجية، إزالة التكرار، تبسيط التعقيد، إعادة التنظيم الهيكلي، والاختبار. كل مرحلة مصممة لتكون ذاتية الكفاية قدر الإمكان بحيث يمكن تنفيذها على دفعات.

---

## 1. تحليل الوضع الراهن (التشخيص)

| الملف                        | المشكلة الرئيسية                                                                                                                                                       | الخطورة        |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| `cat_tools2.py`              | متغير عام قابل للتغيير (`tatone_ns`)، اسم دالة بصيغة `CamelCase`، لا يوجد معالجة أخطاء لاستدعاءات API.                                                                 | متوسطة         |
| `dontadd.py`                 | `except Exception` عارية، خلط منطق القراءة/الكتابة على القرص مع منطق SQL، اسم الدالة `Dont_add_to_pages_def` غير مطابق لـ PEP 8.                                       | متوسطة         |
| `cats_tools/ar_from_en.py`   | تكرار منطق التقطيع إلى دفعات (chunking) واستدعاء `find_LCN`. نوع الإرجاع غير متسق (`list` أو `False`).                                                                 | عالية          |
| `cats_tools/ar_from_en2.py`  | **تكرار شبه كامل** لـ `ar_from_en.py` مع اختلافات طفيفة فقط في مصدر الويكي (`en` vs `fr`). يحتوي على نسخة مكررة من `Categorized_Page_Generator`.                       | **عالية جداً** |
| `bots/english_page_title.py` | دوال عملاقة (`english_page_link_from_api` ~80 سطر)، تعشيش عميق، تكرار أنماط التعبيرات النمطية (Regex)، خلط مسؤوليات (جلب من API + Wikidata + التحقق + التخزين المؤقت). | عالية          |
| `bots/filter_cat.py`         | دالة أحادية (`filter_cats_text`) بطول 140 سطر، تعقيد حلقي عالٍ O(n²) بسبب `remove()` متكرر من قائمة أثناء التكرار، قوائم عامة قابلة للتعديل (`Skippe_Cat`).            | عالية          |
| `bots/text_to_temp_bot.py`   | سلسلة `elif` طويلة في `add_direct`، أسماء قوالب مُدمجة (hardcoded) متناثرة، خلط بين معالجة النصوص الخام واستخدام `wikitextparser`.                                     | متوسطة         |
| `tools_bots/temp_bot.py`     | تكرار شبه كامل بين `templatequery` و `templatequerymulti`. ذاكرة تخزين مؤقت على مستوى الوحدة (`templatequery_cache`).                                                  | متوسطة         |
| `tools_bots/sort_bot.py`     | خوارزمية فرز يدوية غريبة تعتمد على استبدال الأحرف بأرقام ثم الفرز الأبجدي، غير فعالة وهشة.                                                                             | متوسطة         |

---

## 2. الأهداف وغير الأهداف

### الأهداف

-   تطبيق **PEP 8** بالكامل على أسماء الدوال والمتغيرات.
-   **إزالة التكرار** بنسبة 100% بين `ar_from_en.py` و `ar_from_en2.py`، وبين `templatequery` و `templatequerymulti`.
-   تقليل **تعقيد الحلقي (Cyclomatic Complexity)** لأكبر ثلاث دوال بنسبة 50% على الأقل.
-   جعل المنطق **خالص (Pure)** حيثما أمكن ليسهل اختباره.
-   توحيد **معالجة الأخطاء** حول استدعاءات API والملفات.

### غير الأهداف (للمرحلة الحالية)

-   تغيير منطق الأعمال (Business Logic): يجب أن تظل سلوكيات التصفية والفرز مطابقة تماماً لما هي عليه الآن.
-   إعادة كتابة استدعاءات API الخارجية (`find_LCN`, `load_main_api`، إلخ).
-   إنشاء واجهة مستخدم جديدة أو تغيير معاملات سطر الأوامر.

---

## 3. المراحل التفصيلية للتنفيذ

### المرحلة 1: النظافة البرمجية والأساسيات (أسبوع 1)

**الملفات المستهدفة:** جميع ملفات `c18_new`

**المهام:**

1. **الثوابت والأرقام السحرية:** أنشئ ملف `src/c18_new/constants.py` (أو أضف إلى إعدادات مركزية) يحتوي على:
    - معرفات النطاقات: `NS_MAIN = 0`, `NS_CAT = 14`, `NS_TEMPLATE = 10`.
    - بادئات التصنيفات: `CAT_PREFIX_AR = "تصنيف:"`, `CAT_PREFIX_EN = "Category:"`.
    - أسماء القوالب المُدمجة كثوابت (`frozenset`) بدلاً من القوائم العامة القابلة للتعديل.
2. **إعادة التسمية:** حوّل جميع أسماء الدوال إلى `snake_case`:
    - `Categorized_Page_Generator` → `generate_categorized_pages`
    - `Dont_add_to_pages_def` → `get_dont_add_pages`
    - `Get_ar_list_from_en_list` → `get_ar_list_from_en_list`
    - `english_page_link_from_api` → `_resolve_page_link_via_api`
    - `filter_cats_text` → `filter_category_text`
3. **التلميحات النوعية (Type Hints):** أضف `list[str]`, `Optional[str]`, `dict[str, Any]` لجميع التواقيع العامة.
4. **توحيد الإرجاع:** لا تعُد `False` بدلاً من قائمة أو سلسلة نصية. استخدم `list[str]` فارغة أو `None`.
5. **جعل القوائم العامة غير قابلة للتغيير:** حوّل `Skippe_Cat` و `page_false_templates` و `tatone_ns` إلى `tuple` أو `frozenset`. إذا كان منطق الاستدعاء يتطلب تعديلاً ديناميكياً (مثل `stubs`)، استخدم دالة بنّاء (`factory function`) أو `copy` بدلاً من التعديل على الوحدة أثناء الاستيراد.

**معيار النجاح:** يمر `ruff check src/c18_new` و `mypy src/c18_new` (إذا تم تفعيله) بدون أخطاء شكلية.

---

### المرحلة 2: إزالة التكرار وتجنيد الأجزاء المشتركة (أسبوع 2)

**المهمة 2.1: دمج `ar_from_en.py` و `ar_from_en2.py`**

-   أنشئ وحدة موحدة: `src/c18_new/mappers/en_to_ar_mapper.py`.
-   استخرج دالة موحدة واحدة:
    ```python
    def fetch_ar_titles_from_en_category(enpage_title: str, wiki: str = "en") -> list[str]:
        ...
    ```
-   استخرج دالة التقطيع إلى دفعات الموحدة:
    ```python
    def batch_fetch_langlinks(titles: list[str], source_wiki: str, target_lang: str = "ar", batch_size: int = 50) -> list[str]:
        ...
    ```
-   احذف `ar_from_en2.py` بالكامل، واجعل `ar_from_en.py` يستورد من `en_to_ar_mapper` للتوافقية المؤقتة (أو حدّث مستورديها مباشرة إذا كان عددهم قليلاً).

**المهمة 2.2: دمج `templatequery` و `templatequerymulti`**

في `tools_bots/temp_bot.py`:

-   اجعل `templatequery` تستدعي `templatequerymulti` وتُرجع الحقل `templates` فقط:
    ```python
    def templatequery(enlink: str, sitecode: str = "ar") -> list[str] | bool:
        multi_result = templatequerymulti(enlink, sitecode)
        if not multi_result:
            return False
        return multi_result.get(enlink, {}).get("templates", False)
    ```
-   أخرج منطق التخزين المؤقت إلى كلاس بسيط `TemplateCache` أو استخدم `functools.lru_cache` بدلاً من `defaultdict` العام.

**المهمة 2.3: إعادة استخدام مولد التصنيفات**

في `ar_from_en2.py` (قبل حذفه)، كانت توجد نسخة مكررة من `Categorized_Page_Generator`. تأكد أن جميع مكامِلات الوحدة تستخدم `cat_tools2.generate_categorized_pages` فقط.

**معيار النجاح:** عدد أسطر الكود في `c18_new` يقل بنسبة 15-20% دون فقدان وظائف.

---

### المرحلة 3: تبسيط التعقيد (أسبوع 3)

**المهمة 3.1: إعادة هيكلة `filter_cats_text`**

في `bots/filter_cat.py`:

1. حوّل كل قاعدة تصفية إلى دالة بريديكات (Predicate) منفصلة:
    ```python
    def is_template_category(cat: str, ns: int) -> bool: ...
    def is_deleted_category(cat: str, deleted_pages: set[str]) -> bool: ...
    def has_false_template(cat: str, false_templates: frozenset[str]) -> bool: ...
    def is_already_in_text(cat: str, text: str) -> bool: ...
    ```
2. استبدل الحذف المتكرر من القائمة ببناء **قائمة جديدة**:

    ```python
    def filter_category_text(cats: list[str], ns: int, text: str) -> list[str]:
        deleted = set(get_deleted_pages())
        false_temps = frozenset(page_false_templates)
        # جلب القوالب مرة واحدة
        templates_map = templatequerymulti("|".join(cats), "ar") or {}

        survivors = []
        for cat in cats:
            if any(predicate(cat) for predicate in get_predicates(ns, text, deleted, false_temps)):
                continue
            # فحص القوالب
            if is_bad_template(templates_map.get(cat, {})):
                continue
            survivors.append(cat)
        return survivors
    ```

3. هذا يحول التعقيد من O(n²) إلى O(n) تقريباً ويجعل اختبار كل قاعدة بالعزل ممكناً.

**المهمة 3.2: تقسيم `english_page_title.py`**

في `bots/english_page_title.py`:

1. استخرج جميع أنماط regex إلى قائمة مُركّبة في أعلى الملف:
    ```python
    QID_PATTERNS = [
        re.compile(r"..."),
        ...
    ]
    ```
2. قسّم `english_page_link_from_api` إلى دوال فرعية صغيرة:
    - `_check_local_cache(tubb)`
    - `_fetch_from_api(link, firstsite_code)`
    - `_fetch_from_text(text)`
    - `_validate_via_wikidata(result, ...)`
    - `_update_caches(tubb, result, ...)`
3. قلّل التعشيش باستخدام `return` المبكر (Guard Clauses).

**المهمة 3.3: تنظيف `text_to_temp_bot.py`**

في `bots/text_to_temp_bot.py`:

1. استبدل سلسلة `elif` في `add_direct` بقاموس (Dictionary Dispatch) أو قائمة من tuples:
    ```python
    INSERTION_MARKERS = [
        ("{{توثيق", lambda text, idx: ...),
        ("{{توثيق شريط}}", lambda text, idx: ...),
        ...
    ]
    ```
2. استخدم `wikitextparser` بشكل أكثر اتساقاً بدلاً من `str.find` عند البحث عن قوالب.
3. استخرج النصوص الطويلة (`pre_text`) إلى ملفات قوالب منفصلة إذا أمكن، أو على الأقل ثابت مسماة بشكل واضح.

**المهمة 3.4: استبدال خوارزمية الفرز في `sort_bot.py`**

في `tools_bots/sort_bot.py`:

-   استبدل المنطق اليدوي بـ **مفتاح فرز (Sort Key)** واضح:

    ```python
    _ARABIC_ORDER = str.maketrans({
        'آ': '02', 'ا': '03', 'أ': '04', ... # الخريطة الكاملة
    })

    def collation_key(text: str) -> str:
        # يمكن تحسينه لاحقاً باستخدام pyuca إن أُضيفت المكتبة
        return text.translate(_ARABIC_ORDER)
    ```

-   استخدم `sorted(categorylist, key=collation_key)` بدلاً من التلاعب بالسلاسل النصية والأصفار.

**معيار النجاح:** انخفاض تقرير تعقيد الحلقي (مثلاً عبر `radon cc`) لأكبر 3 دوال بأكثر من 50%.

---

### المرحلة 4: إعادة التنظيم الهيكلي (أسبوع 4)

الشكل الحالي للمجلدات غير واضح المعالم (`bots` مقابل `tools_bots` مقابل `cats_tools`). اقترح إعادة ترتيب أوهن بحيث يعكس **الغرض** لا **التاريخ**.

**الخطة المقترحة (مع الحفاظ على التوافقية):**

```
src/c18_new/
├── __init__.py              # تصدير الواجهة العامة فقط
├── constants.py             # الثوابت والقوائم السوداء
├── category_fetcher.py      # (was cat_tools2.py) جلب أعضاء التصنيف من API
├── exclusions.py            # (was dontadd.py) القائمة السوداء وJSON/SQL
├── filters/
│   ├── __init__.py
│   ├── category_filter.py   # (was filter_cat.py) الدالة الرئيسية
│   └── predicates.py        # قواعد التصفية المنفردة
├── mappers/
│   ├── __init__.py
│   └── en_to_ar.py          # (merged ar_from_en + ar_from_en2)
├── resolvers/
│   ├── __init__.py
│   └── page_links.py        # (was english_page_title.py) حل روابط اللغة
├── injectors/
│   ├── __init__.py
│   ├── template_categories.py # (was text_to_temp_bot.py)
│   └── sorter.py            # (was sort_bot.py)
└── queries/
    ├── __init__.py
    └── template_query.py    # (was temp_bot.py)
```

**استراتيجية الترحيل:**

1. أنشئ المجلدات والملفات الجديدة.
2. انقل الكود إليها.
3. في الملفات القديمة، اترك **استيرادات إعادة توجيه** (Re-export aliases) مع تحذير إهمال (`warnings.warn("Deprecated import...", DeprecationWarning)`):
    ```python
    # bots/filter_cat.py (قديم)
    from ..filters.category_filter import filter_category_text as filter_cats_text
    ```
4. بعد دورة إصدار واحدة، احذف الملفات القديمة.

**معيار النجاح:** جميع الاستيرادات القديمة تعمل (مع تحذير) وجميع الاستيرادات الجديدة نظيفة.

---

### المرحلة 5: الاختبار والتحقق (أسبوع 5)

**المهام:**

1. **اختبارات الوحدة:** لكل دالة "خالصة" (Pure Function) تم استخراجها، اكتب اختباراً:
    - `clean_category_input` → اختبار إزالة البادئات.
    - `sort_text` → اختبار الفرز الأبجدي العربي.
    - `is_template_category` → اختبار True/False لحالات مختلفة.
    - `collation_key` → اختبار ترتيب الأحرف.
2. **اختبارات التكامل:** شغّل مسار `run.py -encat:Science` (أو أي تصنيف تجريبي) **قبل وبعد** كل مرحلة للتأكد من تطابق المخرجات.
3. **اختبارات الأداء:** قسّم وقت تنفيذ `filter_cats_text` و `sort_text` على قائمة كبيرة (مثلاً 1000 تصنيف) للتأكد من أن التحسينات لم تؤثر سلباً.
4. **CI/CD:** تأكد من أن `pytest tests/c18_new/` يمر بنجاح في GitHub Actions.

**معيار النجاح:** تغطية الاختبارات لـ `c18_new` لا تقل عن 80%، ونجاح جميع الاختبارات القديمة والجديدة.

---

## 4. قائمة المهام السريعة (Quick-Win Checklist)

يمكن تنفيذ هذه المهام فوراً حتى قبل بدء المراحل الكبرى:

-   [ ] استبدال `tatone_ns` القابل للتغيير بثابت `frozenset` أو دالة.
-   [ ] استبدال `Skippe_Cat` القائمة بـ `tuple`.
-   [ ] استبدال `page_false_templates.remove("بذرة")` (التعديل أثناء الاستيراد) بمنطق شرطي داخل الدالة.
-   [ ] حذف `__pycache__` من المستودع وإضافته إلى `.gitignore` إن لم يكن موجوداً.
-   [ ] إضافة `__all__` إلى `__init__.py` الملفات لتحديد الصادرات العلنية.

---

## 5. المخاطر واستراتيجيات التخفيف

| المخاطر                                                   | التأثير | التخفيف                                                                                               |
| --------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------- |
| كسر استيرادات `mk_cats` أو `b18_new`                      | عالٍ    | الاحتفاظ بملفات توجيه (Re-export) قديمة لمدة دورة إصدار كاملة مع `DeprecationWarning`.                |
| تغيير سلوك التصفية بسبب إعادة الترتيب                     | متوسط   | اختبار تكاملي على تصنيف حقيقي (مثلاً `Science`) قبل وبعد، ومقارنة المخرجات.                           |
| تدهور الأداء بسبب بناء قوائم جديدة بدلاً من الحذف المباشر | منخفض   | قياس الأداء على بيانات كبيرة؛ البناء الجديد عادةً أسرع بكثير بسبب تجنب O(n²).                         |
| فقدان معلومات التسجيل (Logging) أثناء التقسيم             | منخفض   | الحفاظ على استدعاءات `logger.info/debug` في الدالة الرئيسية وعدم نقلها إلى الدوال البريديكات الصغيرة. |

---

## 6. المعايير النهائية للنجاح

1. **نظافة الشيفرة:** لا توجد دوال `CamelCase` في `c18_new`، ولا أرقام سحرية.
2. **خلو من التكرار:** لا يوجد تكرار بين `ar_from_en` و `ar_from_en2`، ولا بين `templatequery` و `templatequerymulti`.
3. **الأداء:** `filter_cats_text` أسرع بنسبة 30% على الأقل مع القوائم الكبيرة.
4. **الاختبار:** تمر جميع الاختبارات الحالية (`880+`) بالإضافة إلى 20+ اختبار جديد خاص بالمنطق المستخرج.
5. **التوثيق:** جميع الدوال العامة تحتوي على docstrings واضحة باللغة العربية أو الإنجليزية (حسب اتفاقية المشروع).

---

## 7. الخلاصة

`c18_new` ليست في حالة سيئة جداً، لكنها تراكمت عليها "ديون تقنية" واضحة: التكرار، الأسماء غير المطابقة للمعايير، والدوال العملاقة. بتطبيق هذه الخطة على خمس مراحل، ستتحول الوحدة إلى كود **نظيف، قابل للاختبار، وسهل الصيانة** دون المساس بمنطق الأعمال الحساس الذي يدير تصنيفات ويكيبيديا العربية.

> **نصيحة:** ابدأ بالمرحلة 1 والـ Quick-Wins فوراً؛ فهي آمنة تماماً وتوفر قاعدة نظيفة للمراحل اللاحقة.
