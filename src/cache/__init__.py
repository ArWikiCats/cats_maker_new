"""
Unified caching module for the project.

This module provides a centralized caching system with TTL support,
pattern-based invalidation, and a decorator for function-level caching.

Example:
    >>> from src.cache import cache_manager, cached
    >>> @cached(ttl=3600)
    ... def get_data(key: str) -> dict:
    ...     return {"key": key}
    >>> cache_manager.set("test_key", "test_value", ttl=300)
    >>> cache_manager.get("test_key")
    'test_value'
"""

from .cache_manager import CacheManager, cached, cache_manager

__all__ = [
    "CacheManager",
    "cached",
    "cache_manager",
]
