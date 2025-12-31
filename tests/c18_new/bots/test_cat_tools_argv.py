"""
Tests for src/c18_new/bots/cat_tools_argv.py

This module tests command line argument parsing for category tools.
"""

import pytest

from src.c18_new.bots.cat_tools_argv import (
    AAr_site,
    EEn_site,
    FR_site,
    Use_Labels,
    use_sqldb,
    Make_New_Cat,
    To,
    Depth,
    offseet,
)


class TestAArSite:
    """Tests for AAr_site configuration"""

    def test_has_required_keys(self):
        """Test that AAr_site has required keys"""
        assert 1 in AAr_site
        assert "family" in AAr_site
        assert "code" in AAr_site

    def test_default_family_is_wikipedia(self):
        """Test that default family is wikipedia"""
        assert AAr_site["family"] == "wikipedia"

    def test_default_code_is_ar(self):
        """Test that default code is ar"""
        assert AAr_site["code"] == "ar"


class TestEEnSite:
    """Tests for EEn_site configuration"""

    def test_has_required_keys(self):
        """Test that EEn_site has required keys"""
        assert 1 in EEn_site
        assert "family" in EEn_site
        assert "code" in EEn_site

    def test_default_family_is_wikipedia(self):
        """Test that default family is wikipedia"""
        assert EEn_site["family"] == "wikipedia"

    def test_default_code_is_en(self):
        """Test that default code is en"""
        assert EEn_site["code"] == "en"


class TestFRSite:
    """Tests for FR_site configuration"""

    def test_has_use_key(self):
        """Test that FR_site has use key"""
        assert "use" in FR_site

    def test_has_family_key(self):
        """Test that FR_site has family key"""
        assert "family" in FR_site

    def test_has_code_key(self):
        """Test that FR_site has code key"""
        assert "code" in FR_site

    def test_default_code_is_fr(self):
        """Test that default code is fr"""
        assert FR_site["code"] == "fr"


class TestUseLabels:
    """Tests for Use_Labels configuration"""

    def test_is_dict(self):
        """Test that Use_Labels is a dict"""
        assert isinstance(Use_Labels, dict)

    def test_has_key_1(self):
        """Test that Use_Labels has key 1"""
        assert 1 in Use_Labels

    def test_default_value_is_false(self):
        """Test that default value is False"""
        assert Use_Labels[1] is False


class TestUseSqldb:
    """Tests for use_sqldb configuration"""

    def test_is_dict(self):
        """Test that use_sqldb is a dict"""
        assert isinstance(use_sqldb, dict)

    def test_has_key_1(self):
        """Test that use_sqldb has key 1"""
        assert 1 in use_sqldb

    def test_default_value_is_true(self):
        """Test that default value is True"""
        assert use_sqldb[1] is True


class TestMakeNewCat:
    """Tests for Make_New_Cat configuration"""

    def test_is_dict(self):
        """Test that Make_New_Cat is a dict"""
        assert isinstance(Make_New_Cat, dict)

    def test_has_key_1(self):
        """Test that Make_New_Cat has key 1"""
        assert 1 in Make_New_Cat

    def test_default_value_is_true(self):
        """Test that default value is True"""
        assert Make_New_Cat[1] is True


class TestTo:
    """Tests for To configuration"""

    def test_is_dict(self):
        """Test that To is a dict"""
        assert isinstance(To, dict)

    def test_has_key_1(self):
        """Test that To has key 1"""
        assert 1 in To

    def test_default_value(self):
        """Test that default value is reasonable"""
        assert isinstance(To[1], int)


class TestDepth:
    """Tests for Depth configuration"""

    def test_is_dict(self):
        """Test that Depth is a dict"""
        assert isinstance(Depth, dict)

    def test_has_key_1(self):
        """Test that Depth has key 1"""
        assert 1 in Depth

    def test_default_value_is_zero(self):
        """Test that default value is 0"""
        assert Depth[1] == 0


class TestOffseet:
    """Tests for offseet configuration"""

    def test_is_dict(self):
        """Test that offseet is a dict"""
        assert isinstance(offseet, dict)

    def test_has_key_1(self):
        """Test that offseet has key 1"""
        assert 1 in offseet

    def test_default_value_is_zero(self):
        """Test that default value is 0"""
        assert offseet[1] == 0
