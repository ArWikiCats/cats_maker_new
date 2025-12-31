"""
Centralized configuration module for the project.

This module provides a central place for all configuration settings,
making it easier to manage and modify settings across the codebase.
"""

from .settings import (
    Settings,
    WikipediaConfig,
    WikidataConfig,
    DatabaseConfig,
    settings,
)

__all__ = [
    "Settings",
    "WikipediaConfig",
    "WikidataConfig",
    "DatabaseConfig",
    "settings",
]
