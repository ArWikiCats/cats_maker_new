"""
Tests for the centralized settings configuration module.
"""

import os
import sys
import pytest


class TestWikipediaConfig:
    """Tests for WikipediaConfig dataclass."""

    def test_default_ar_family(self):
        """Test default Arabic family is wikipedia."""
        from src.config.settings import WikipediaConfig

        config = WikipediaConfig()
        assert config.ar_family == "wikipedia"

    def test_default_ar_code(self):
        """Test default Arabic code is ar."""
        from src.config.settings import WikipediaConfig

        config = WikipediaConfig()
        assert config.ar_code == "ar"

    def test_default_en_family(self):
        """Test default English family is wikipedia."""
        from src.config.settings import WikipediaConfig

        config = WikipediaConfig()
        assert config.en_family == "wikipedia"

    def test_default_en_code(self):
        """Test default English code is en."""
        from src.config.settings import WikipediaConfig

        config = WikipediaConfig()
        assert config.en_code == "en"

    def test_default_user_agent(self):
        """Test default user agent is set."""
        from src.config.settings import WikipediaConfig

        config = WikipediaConfig()
        assert "Himo bot" in config.user_agent

    def test_default_timeout(self):
        """Test default timeout is 10."""
        from src.config.settings import WikipediaConfig

        config = WikipediaConfig()
        assert config.default_timeout == 10

    def test_custom_values(self):
        """Test custom values can be set."""
        from src.config.settings import WikipediaConfig

        config = WikipediaConfig(
            ar_family="wikiquote",
            ar_code="ar",
            en_family="wikiquote",
            en_code="en",
            user_agent="Custom Agent",
            default_timeout=30,
        )
        assert config.ar_family == "wikiquote"
        assert config.en_family == "wikiquote"
        assert config.user_agent == "Custom Agent"
        assert config.default_timeout == 30


class TestWikidataConfig:
    """Tests for WikidataConfig dataclass."""

    def test_default_endpoint(self):
        """Test default Wikidata endpoint."""
        from src.config.settings import WikidataConfig

        config = WikidataConfig()
        assert config.endpoint == "https://www.wikidata.org/w/api.php"

    def test_default_sparql_endpoint(self):
        """Test default SPARQL endpoint."""
        from src.config.settings import WikidataConfig

        config = WikidataConfig()
        assert config.sparql_endpoint == "https://query.wikidata.org/sparql"

    def test_default_timeout(self):
        """Test default timeout is 30."""
        from src.config.settings import WikidataConfig

        config = WikidataConfig()
        assert config.timeout == 30

    def test_default_maxlag(self):
        """Test default maxlag is 5."""
        from src.config.settings import WikidataConfig

        config = WikidataConfig()
        assert config.maxlag == 5

    def test_custom_endpoint(self):
        """Test custom endpoint can be set."""
        from src.config.settings import WikidataConfig

        config = WikidataConfig(endpoint="https://test.wikidata.org/w/api.php")
        assert config.endpoint == "https://test.wikidata.org/w/api.php"


class TestDatabaseConfig:
    """Tests for DatabaseConfig dataclass."""

    def test_default_host_is_none(self):
        """Test default host is None."""
        from src.config.settings import DatabaseConfig

        config = DatabaseConfig()
        assert config.host is None

    def test_default_port(self):
        """Test default port is 3306."""
        from src.config.settings import DatabaseConfig

        config = DatabaseConfig()
        assert config.port == 3306

    def test_default_use_sql(self):
        """Test default use_sql is True."""
        from src.config.settings import DatabaseConfig

        config = DatabaseConfig()
        assert config.use_sql is True

    def test_custom_host(self):
        """Test custom host can be set."""
        from src.config.settings import DatabaseConfig

        config = DatabaseConfig(host="localhost")
        assert config.host == "localhost"


class TestSettings:
    """Tests for Settings dataclass."""

    def test_has_wikipedia_config(self):
        """Test Settings has wikipedia config."""
        from src.config.settings import Settings, WikipediaConfig

        s = Settings()
        assert isinstance(s.wikipedia, WikipediaConfig)

    def test_has_wikidata_config(self):
        """Test Settings has wikidata config."""
        from src.config.settings import Settings, WikidataConfig

        s = Settings()
        assert isinstance(s.wikidata, WikidataConfig)

    def test_has_database_config(self):
        """Test Settings has database config."""
        from src.config.settings import Settings, DatabaseConfig

        s = Settings()
        assert isinstance(s.database, DatabaseConfig)

    def test_default_range_limit(self):
        """Test default range_limit is 5."""
        from src.config.settings import Settings

        s = Settings()
        assert s.range_limit == 5

    def test_default_debug(self):
        """Test default debug is False."""
        from src.config.settings import Settings

        s = Settings()
        assert s.debug is False

    def test_default_log_level(self):
        """Test default log_level is INFO."""
        from src.config.settings import Settings

        s = Settings()
        assert s.log_level == "INFO"


class TestSettingsEnvVars:
    """Tests for Settings environment variable processing."""

    def test_env_wikipedia_ar_code(self, monkeypatch):
        """Test WIKIPEDIA_AR_CODE environment variable."""
        monkeypatch.setenv("WIKIPEDIA_AR_CODE", "arz")
        from src.config.settings import Settings

        s = Settings()
        assert s.wikipedia.ar_code == "arz"

    def test_env_wikidata_endpoint(self, monkeypatch):
        """Test WIKIDATA_ENDPOINT environment variable."""
        monkeypatch.setenv("WIKIDATA_ENDPOINT", "https://custom.wikidata.org/api")
        from src.config.settings import Settings

        s = Settings()
        assert s.wikidata.endpoint == "https://custom.wikidata.org/api"

    def test_env_database_use_sql_true(self, monkeypatch):
        """Test DATABASE_USE_SQL environment variable with true."""
        monkeypatch.setenv("DATABASE_USE_SQL", "true")
        from src.config.settings import Settings

        s = Settings()
        assert s.database.use_sql is True

    def test_env_database_use_sql_false(self, monkeypatch):
        """Test DATABASE_USE_SQL environment variable with false."""
        monkeypatch.setenv("DATABASE_USE_SQL", "false")
        from src.config.settings import Settings

        s = Settings()
        assert s.database.use_sql is False

    def test_env_range_limit(self, monkeypatch):
        """Test RANGE_LIMIT environment variable."""
        monkeypatch.setenv("RANGE_LIMIT", "10")
        from src.config.settings import Settings

        s = Settings()
        assert s.range_limit == 10

    def test_env_debug_true(self, monkeypatch):
        """Test DEBUG environment variable with true."""
        monkeypatch.setenv("DEBUG", "true")
        from src.config.settings import Settings

        s = Settings()
        assert s.debug is True

    def test_env_log_level(self, monkeypatch):
        """Test LOG_LEVEL environment variable."""
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        from src.config.settings import Settings

        s = Settings()
        assert s.log_level == "DEBUG"


class TestGlobalSettings:
    """Tests for the global settings instance."""

    def test_settings_instance_exists(self):
        """Test that global settings instance exists."""
        from src.config import settings

        assert settings is not None

    def test_settings_is_settings_type(self):
        """Test that global settings is Settings type."""
        from src.config import settings, Settings

        assert isinstance(settings, Settings)

    def test_settings_has_default_wikipedia(self):
        """Test settings has default Wikipedia config."""
        from src.config import settings

        assert settings.wikipedia.ar_code == "ar"
        assert settings.wikipedia.en_code == "en"

    def test_settings_has_default_wikidata(self):
        """Test settings has default Wikidata config."""
        from src.config import settings

        assert "wikidata.org" in settings.wikidata.endpoint

    def test_settings_has_default_database(self):
        """Test settings has default Database config."""
        from src.config import settings

        assert settings.database.port == 3306


class TestModuleExports:
    """Tests for module exports."""

    def test_exports_settings(self):
        """Test settings is exported."""
        from src.config import settings

        assert settings is not None

    def test_exports_settings_class(self):
        """Test Settings class is exported."""
        from src.config import Settings

        assert Settings is not None

    def test_exports_wikipedia_config(self):
        """Test WikipediaConfig is exported."""
        from src.config import WikipediaConfig

        assert WikipediaConfig is not None

    def test_exports_wikidata_config(self):
        """Test WikidataConfig is exported."""
        from src.config import WikidataConfig

        assert WikidataConfig is not None

    def test_exports_database_config(self):
        """Test DatabaseConfig is exported."""
        from src.config import DatabaseConfig

        assert DatabaseConfig is not None
