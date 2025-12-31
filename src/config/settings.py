"""
Centralized settings configuration for the project.

This module provides dataclass-based configuration for all project settings,
including Wikipedia, Wikidata, and database configurations.

Example:
    >>> from src.config import settings
    >>> print(settings.wikipedia.ar_code)
    'ar'
    >>> print(settings.wikidata.endpoint)
    'https://www.wikidata.org/w/api.php'
"""

import os
import sys
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class WikipediaConfig:
    """Configuration for Wikipedia API connections.

    Attributes:
        ar_family: Arabic Wikipedia family (default: "wikipedia")
        ar_code: Arabic Wikipedia language code (default: "ar")
        en_family: English Wikipedia family (default: "wikipedia")
        en_code: English Wikipedia language code (default: "en")
        user_agent: User agent string for API requests
        default_timeout: Default timeout for API requests in seconds
    """

    ar_family: str = "wikipedia"
    ar_code: str = "ar"
    en_family: str = "wikipedia"
    en_code: str = "en"
    user_agent: str = "Himo bot/1.0 (https://himo.toolforge.org/; tools.himo@toolforge.org)"
    default_timeout: int = 10


@dataclass
class WikidataConfig:
    """Configuration for Wikidata API connections.

    Attributes:
        endpoint: Wikidata API endpoint URL
        sparql_endpoint: SPARQL query endpoint URL
        timeout: Default timeout for Wikidata requests
        maxlag: Maximum lag for Wikidata API requests
    """

    endpoint: str = "https://www.wikidata.org/w/api.php"
    sparql_endpoint: str = "https://query.wikidata.org/sparql"
    timeout: int = 30
    maxlag: int = 5


@dataclass
class DatabaseConfig:
    """Configuration for database connections.

    Attributes:
        host: Database host (optional, derived from wiki code if not set)
        port: Database port
        use_sql: Whether to use SQL database for queries
    """

    host: Optional[str] = None
    port: int = 3306
    use_sql: bool = True


@dataclass
class Settings:
    """Main settings container for all project configurations.

    This class aggregates all configuration dataclasses and provides
    global settings that apply across the project.

    Attributes:
        wikipedia: Wikipedia API configuration
        wikidata: Wikidata API configuration
        database: Database connection configuration
        range_limit: Maximum number of iterations for category processing
        debug: Enable debug mode
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """

    wikipedia: WikipediaConfig = field(default_factory=WikipediaConfig)
    wikidata: WikidataConfig = field(default_factory=WikidataConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)

    # Global settings
    range_limit: int = 5
    debug: bool = False
    log_level: str = "INFO"

    def __post_init__(self):
        """Process command-line arguments and environment variables."""
        self._process_env_vars()
        self._process_argv()

    def _process_env_vars(self):
        """Load configuration from environment variables."""
        # Wikipedia config
        if os.environ.get("WIKIPEDIA_AR_CODE"):
            self.wikipedia.ar_code = os.environ["WIKIPEDIA_AR_CODE"]
        if os.environ.get("WIKIPEDIA_EN_CODE"):
            self.wikipedia.en_code = os.environ["WIKIPEDIA_EN_CODE"]
        if os.environ.get("WIKIPEDIA_AR_FAMILY"):
            self.wikipedia.ar_family = os.environ["WIKIPEDIA_AR_FAMILY"]
        if os.environ.get("WIKIPEDIA_EN_FAMILY"):
            self.wikipedia.en_family = os.environ["WIKIPEDIA_EN_FAMILY"]
        if os.environ.get("WIKIPEDIA_USER_AGENT"):
            self.wikipedia.user_agent = os.environ["WIKIPEDIA_USER_AGENT"]
        if os.environ.get("WIKIPEDIA_TIMEOUT"):
            self.wikipedia.default_timeout = int(os.environ["WIKIPEDIA_TIMEOUT"])

        # Wikidata config
        if os.environ.get("WIKIDATA_ENDPOINT"):
            self.wikidata.endpoint = os.environ["WIKIDATA_ENDPOINT"]
        if os.environ.get("WIKIDATA_SPARQL_ENDPOINT"):
            self.wikidata.sparql_endpoint = os.environ["WIKIDATA_SPARQL_ENDPOINT"]
        if os.environ.get("WIKIDATA_TIMEOUT"):
            self.wikidata.timeout = int(os.environ["WIKIDATA_TIMEOUT"])
        if os.environ.get("WIKIDATA_MAXLAG"):
            self.wikidata.maxlag = int(os.environ["WIKIDATA_MAXLAG"])

        # Database config
        if os.environ.get("DATABASE_HOST"):
            self.database.host = os.environ["DATABASE_HOST"]
        if os.environ.get("DATABASE_PORT"):
            self.database.port = int(os.environ["DATABASE_PORT"])
        if os.environ.get("DATABASE_USE_SQL"):
            self.database.use_sql = os.environ["DATABASE_USE_SQL"].lower() in ("true", "1", "yes")

        # Global settings
        if os.environ.get("RANGE_LIMIT"):
            self.range_limit = int(os.environ["RANGE_LIMIT"])
        if os.environ.get("DEBUG"):
            self.debug = os.environ["DEBUG"].lower() in ("true", "1", "yes")
        if os.environ.get("LOG_LEVEL"):
            self.log_level = os.environ["LOG_LEVEL"]

    def _process_argv(self):
        """Process command-line arguments for configuration overrides."""
        for arg in sys.argv:
            arg_name, _, value = arg.partition(":")

            # Range limit
            if arg_name == "-range" and value:
                self.range_limit = int(value)

            # Debug mode
            if arg_name in ("-debug", "--debug"):
                self.debug = True

            # SQL usage
            if arg_name == "-nosql":
                self.database.use_sql = False
            if arg_name == "usesql":
                self.database.use_sql = True

            # Wikidata test environment
            if arg_name in ("testwikidata", "-testwikidata"):
                self.wikidata.endpoint = "https://test.wikidata.org/w/api.php"

            # Maxlag configuration
            if arg_name == "maxlag2":
                self.wikidata.maxlag = 1


# Global settings instance
settings = Settings()
