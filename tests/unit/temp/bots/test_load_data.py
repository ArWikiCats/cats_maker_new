"""
Unit tests for src/temp/bots/load_data.py module.
"""

from src.temp.bots.load_data import (
    MakedecadesTemp,
    Make_Cent_temp,
    Make_Elff_temp,
    Make_years_temp,
    TemplatesMaker,
    main_make_temp,
)


class TestTemplatesMakerInit:
    def test_has_elfffff(self):
        assert isinstance(TemplatesMaker.elfffff, dict)
        assert -1 in TemplatesMaker.elfffff
        assert 1 in TemplatesMaker.elfffff

    def test_has_decades_list(self):
        assert isinstance(TemplatesMaker.decades_list, dict)
        assert 1 in TemplatesMaker.decades_list
        assert -1 in TemplatesMaker.decades_list

    def test_has_cacaca(self):
        assert "تأسيسات " in TemplatesMaker.cacaca
        assert "انحلالات " in TemplatesMaker.cacaca


class TestInitializeData:
    def test_builds_years_baco(self):
        bot = TemplatesMaker()
        bot._initialize_data()
        assert len(bot.years_Baco) > 0

    def test_builds_baco_decades(self):
        bot = TemplatesMaker()
        bot._initialize_data()
        assert len(bot.Baco_decades) > 0

    def test_builds_baco_centries(self):
        bot = TemplatesMaker()
        bot._initialize_data()
        assert len(bot.Baco_centries) > 0

    def test_idempotent(self):
        bot = TemplatesMaker()
        bot._initialize_data()
        count1 = len(bot.years_Baco)
        bot._initialize_data()
        count2 = len(bot.years_Baco)
        assert count1 == count2


class TestMakeElffTemp:
    def test_millennium_1(self):
        result, temp = Make_Elff_temp("تصنيف:الألفية الأولى")
        assert "الألفية 1" in result

    def test_millennium_2(self):
        result, temp = Make_Elff_temp("تصنيف:الألفية الثانية")
        assert "الألفية 2" in result

    def test_millennium_3(self):
        result, temp = Make_Elff_temp("تصنيف:الألفية الثالثة")
        assert "الألفية 3" in result

    def test_non_millennium_returns_season(self):
        result, temp = Make_Elff_temp("تصنيف:علوم")
        assert "تصنيف موسم" in result


class TestMakedecadesTemp:
    def test_basic_decade(self):
        result, temp = MakedecadesTemp("تصنيف:عقد 1990")
        assert "عقد" in result

    def test_non_decade_returns_season(self):
        result, temp = MakedecadesTemp("تصنيف:علوم")
        assert "تصنيف موسم" in result


class TestMakeCentTemp:
    def test_basic_century(self):
        result, temp = Make_Cent_temp("تصنيف:القرن 19")
        assert "قرن" in result

    def test_non_century_returns_season(self):
        result, temp = Make_Cent_temp("تصنيف:علوم")
        assert "تصنيف موسم" in result


class TestMakeYearsTemp:
    def test_returns_empty_for_bc(self):
        result = Make_years_temp("تصنيف:100 ق م", "تأسيسات ")
        assert result == ""

    def test_non_year_returns_season(self):
        result = Make_years_temp("تصنيف:علوم", "تأسيسات ")
        assert "تصنيف موسم" in result


class TestMainMakeTemp:
    def test_coronavirus_returns_empty(self):
        result, temp = main_make_temp("", "تصنيف:فيروس كورونا")
        assert result == ""

    def test_numeric_prefix_returns_season(self):
        result, temp = main_make_temp("", "تصنيف:123 test")
        assert "تصنيف موسم" in result

    def test_decade_title(self):
        result, temp = main_make_temp("", "تصنيف:عقد 1990")
        assert "عقد" in result

    def test_century_title(self):
        result, temp = main_make_temp("", "تصنيف:القرن 19")
        assert "قرن" in result

    def test_millennium_title(self):
        result, temp = main_make_temp("", "تصنيف:الألفية الأولى")
        assert "الألفية" in result

    def test_normal_category_returns_empty(self):
        result, temp = main_make_temp("", "تصنيف:علوم")
        assert result == ""
