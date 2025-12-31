"""
Unified Cache Manager for the project.

This module provides a centralized caching system with:
- In-memory caching with TTL (Time-To-Live) support
- Pattern-based cache invalidation
- A decorator for function-level caching
- Thread-safe operations

Example:
    >>> from src.cache import cache_manager, cached
    >>> 
    >>> # Direct cache usage
    >>> cache_manager.set("user:123", {"name": "Test"}, ttl=3600)
    >>> cache_manager.get("user:123")
    {'name': 'Test'}
    >>> 
    >>> # Decorator usage
    >>> @cached(ttl=3600)
    ... def get_sitelinks(qid: str) -> dict:
    ...     # API call here
    ...     return {"qid": qid}
"""

import fnmatch
import threading
import time
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class CacheEntry:
    """Represents a single cache entry with value and expiration time.

    Attributes:
        value: The cached value.
        expires_at: Unix timestamp when the entry expires, or None for no expiration.
    """

    __slots__ = ("value", "expires_at")

    def __init__(self, value: Any, ttl: Optional[int] = None):
        """Initialize a cache entry.

        Args:
            value: The value to cache.
            ttl: Time-to-live in seconds. None means no expiration.
        """
        self.value = value
        self.expires_at: Optional[float] = time.time() + ttl if ttl is not None else None

    def is_expired(self) -> bool:
        """Check if the cache entry has expired.

        Returns:
            True if expired, False otherwise.
        """
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at


class CacheManager:
    """Unified cache manager with TTL support and pattern-based invalidation.

    This class provides a centralized caching mechanism for the project,
    supporting in-memory caching with optional TTL (Time-To-Live) for entries.

    Attributes:
        default_ttl: Default TTL in seconds for cache entries (default: 3600).
        max_size: Maximum number of entries in the cache (default: 10000).

    Example:
        >>> cache = CacheManager(default_ttl=1800)
        >>> cache.set("key1", "value1")
        >>> cache.get("key1")
        'value1'
        >>> cache.set("key2", "value2", ttl=60)  # Custom TTL
        >>> cache.invalidate("key*")  # Invalidate keys matching pattern
    """

    def __init__(self, default_ttl: int = 3600, max_size: int = 10000):
        """Initialize the cache manager.

        Args:
            default_ttl: Default TTL in seconds for cache entries.
            max_size: Maximum number of entries in the cache.
        """
        self._cache: dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self.default_ttl = default_ttl
        self.max_size = max_size

    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache.

        Args:
            key: The cache key to retrieve.

        Returns:
            The cached value if found and not expired, None otherwise.

        Example:
            >>> cache.set("test", "value")
            >>> cache.get("test")
            'value'
            >>> cache.get("nonexistent")
            None
        """
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            if entry.is_expired():
                del self._cache[key]
                return None
            return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache.

        Args:
            key: The cache key.
            value: The value to cache.
            ttl: Time-to-live in seconds. If None, uses default_ttl.
                 Pass 0 for no expiration.

        Example:
            >>> cache.set("user:123", {"name": "Test"})
            >>> cache.set("temp", "value", ttl=60)  # Expires in 60 seconds
            >>> cache.set("permanent", "value", ttl=0)  # Never expires
        """
        with self._lock:
            # Use default TTL if not specified, None if ttl=0 (no expiration)
            effective_ttl = self.default_ttl if ttl is None else (None if ttl == 0 else ttl)
            self._cache[key] = CacheEntry(value, effective_ttl)
            self._evict_if_needed()

    def delete(self, key: str) -> bool:
        """Delete a specific key from the cache.

        Args:
            key: The cache key to delete.

        Returns:
            True if the key was found and deleted, False otherwise.

        Example:
            >>> cache.set("test", "value")
            >>> cache.delete("test")
            True
            >>> cache.delete("nonexistent")
            False
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def invalidate(self, pattern: str) -> int:
        """Invalidate cache entries matching a pattern.

        Supports glob-style patterns (*, ?, [seq], [!seq]).

        Args:
            pattern: Glob pattern to match cache keys.

        Returns:
            Number of entries invalidated.

        Example:
            >>> cache.set("user:1", "a")
            >>> cache.set("user:2", "b")
            >>> cache.set("item:1", "c")
            >>> cache.invalidate("user:*")
            2
        """
        with self._lock:
            keys_to_delete = [key for key in self._cache if fnmatch.fnmatch(key, pattern)]
            for key in keys_to_delete:
                del self._cache[key]
            return len(keys_to_delete)

    def clear(self) -> None:
        """Clear all entries from the cache.

        Example:
            >>> cache.set("key1", "value1")
            >>> cache.set("key2", "value2")
            >>> cache.clear()
            >>> cache.get("key1")
            None
        """
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        """Get the current number of entries in the cache.

        Returns:
            Number of entries in the cache.

        Example:
            >>> cache.set("key1", "value1")
            >>> cache.size()
            1
        """
        with self._lock:
            return len(self._cache)

    def contains(self, key: str) -> bool:
        """Check if a key exists in the cache (and is not expired).

        Args:
            key: The cache key to check.

        Returns:
            True if the key exists and is not expired, False otherwise.

        Example:
            >>> cache.set("test", "value")
            >>> cache.contains("test")
            True
            >>> cache.contains("nonexistent")
            False
        """
        return self.get(key) is not None

    def _evict_if_needed(self) -> None:
        """Evict entries if cache exceeds max_size.

        This method removes expired entries first, then oldest entries
        if still over capacity.
        """
        if len(self._cache) <= self.max_size:
            return

        # First, remove expired entries
        expired_keys = [key for key, entry in self._cache.items() if entry.is_expired()]
        for key in expired_keys:
            del self._cache[key]

        # If still over capacity, remove oldest entries (FIFO)
        while len(self._cache) > self.max_size:
            # dict maintains insertion order in Python 3.7+
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]

    def cached(self, ttl: Optional[int] = None, key_prefix: str = "") -> Callable[[F], F]:
        """Decorator to cache function results.

        Args:
            ttl: Time-to-live in seconds. If None, uses default_ttl.
            key_prefix: Optional prefix for cache keys.

        Returns:
            Decorated function with caching.

        Example:
            >>> cache = CacheManager()
            >>> @cache.cached(ttl=300)
            ... def expensive_operation(x: int) -> int:
            ...     return x * 2
            >>> expensive_operation(5)  # Computed
            10
            >>> expensive_operation(5)  # From cache
            10
        """

        def decorator(func: F) -> F:
            # Store the function name and prefix for cache operations
            func_prefix = f"{key_prefix}:{func.__name__}" if key_prefix else func.__name__

            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                # Generate cache key from function name and arguments
                cache_key = self._generate_cache_key(func.__name__, key_prefix, args, kwargs)
                # Try to get from cache
                result = self.get(cache_key)
                if result is not None:
                    return result
                # Compute and cache
                result = func(*args, **kwargs)
                if result is not None:
                    self.set(cache_key, result, ttl)
                return result

            # Add cache_clear method for compatibility with functools.lru_cache
            def cache_clear() -> None:
                """Clear cached entries for this function."""
                self.invalidate(f"{func_prefix}:*")

            # Add cache_info method for compatibility (returns simplified info)
            def cache_info():
                """Return cache statistics (simplified version)."""
                return {"size": self.size(), "maxsize": self.max_size}

            wrapper.cache_clear = cache_clear  # type: ignore
            wrapper.cache_info = cache_info  # type: ignore

            return wrapper  # type: ignore

        return decorator

    def _generate_cache_key(self, func_name: str, prefix: str, args: tuple, kwargs: dict) -> str:
        """Generate a cache key from function name and arguments.

        Args:
            func_name: Name of the function.
            prefix: Optional prefix for the key.
            args: Positional arguments.
            kwargs: Keyword arguments.

        Returns:
            A string cache key.
        """
        parts = [prefix, func_name] if prefix else [func_name]
        # Add positional arguments
        for arg in args:
            parts.append(str(arg))
        # Add keyword arguments (sorted for consistency)
        for key in sorted(kwargs.keys()):
            parts.append(f"{key}={kwargs[key]}")
        return ":".join(parts)


# Global cache manager instance
cache_manager = CacheManager()


def cached(ttl: Optional[int] = None, key_prefix: str = "") -> Callable[[F], F]:
    """Module-level decorator for caching function results.

    This is a convenience wrapper around the global cache_manager.cached decorator.

    Args:
        ttl: Time-to-live in seconds. If None, uses default_ttl.
        key_prefix: Optional prefix for cache keys.

    Returns:
        Decorated function with caching.

    Example:
        >>> from src.cache import cached
        >>> @cached(ttl=3600)
        ... def get_sitelinks(qid: str) -> dict:
        ...     # API call here
        ...     return {"qid": qid}
    """
    return cache_manager.cached(ttl=ttl, key_prefix=key_prefix)
