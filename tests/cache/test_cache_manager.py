"""
Tests for the unified CacheManager module.
"""

import time
import pytest


class TestCacheEntry:
    """Tests for CacheEntry class."""

    def test_entry_with_no_ttl_never_expires(self):
        """Test that entry without TTL never expires."""
        from src.cache.cache_manager import CacheEntry

        entry = CacheEntry("value", ttl=None)
        assert not entry.is_expired()

    def test_entry_with_ttl_not_expired(self):
        """Test that entry with TTL is not expired immediately."""
        from src.cache.cache_manager import CacheEntry

        entry = CacheEntry("value", ttl=60)
        assert not entry.is_expired()

    def test_entry_with_ttl_expires(self):
        """Test that entry expires after TTL."""
        from src.cache.cache_manager import CacheEntry

        entry = CacheEntry("value", ttl=0)  # TTL of 0 expires immediately
        # Small sleep to ensure expiration
        time.sleep(0.01)
        assert entry.is_expired()

    def test_entry_stores_value(self):
        """Test that entry correctly stores value."""
        from src.cache.cache_manager import CacheEntry

        entry = CacheEntry({"key": "value"}, ttl=60)
        assert entry.value == {"key": "value"}


class TestCacheManagerBasics:
    """Basic tests for CacheManager."""

    def test_set_and_get(self):
        """Test basic set and get operations."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        cache.set("key", "value")
        assert cache.get("key") == "value"

    def test_get_nonexistent_key_returns_none(self):
        """Test that getting nonexistent key returns None."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        assert cache.get("nonexistent") is None

    def test_set_overwrites_existing(self):
        """Test that set overwrites existing value."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        cache.set("key", "value1")
        cache.set("key", "value2")
        assert cache.get("key") == "value2"

    def test_delete_existing_key(self):
        """Test deleting an existing key."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        cache.set("key", "value")
        assert cache.delete("key") is True
        assert cache.get("key") is None

    def test_delete_nonexistent_key(self):
        """Test deleting a nonexistent key returns False."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        assert cache.delete("nonexistent") is False

    def test_clear(self):
        """Test clearing all entries."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None
        assert cache.size() == 0

    def test_size(self):
        """Test size returns correct count."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        assert cache.size() == 0
        cache.set("key1", "value1")
        assert cache.size() == 1
        cache.set("key2", "value2")
        assert cache.size() == 2

    def test_contains_existing_key(self):
        """Test contains returns True for existing key."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        cache.set("key", "value")
        assert cache.contains("key") is True

    def test_contains_nonexistent_key(self):
        """Test contains returns False for nonexistent key."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        assert cache.contains("nonexistent") is False


class TestCacheManagerTTL:
    """Tests for CacheManager TTL functionality."""

    def test_default_ttl_is_applied(self):
        """Test that default TTL is applied when not specified."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager(default_ttl=3600)
        cache.set("key", "value")
        # Value should be accessible
        assert cache.get("key") == "value"

    def test_custom_ttl_on_set(self):
        """Test custom TTL can be set on individual entries."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager(default_ttl=3600)
        cache.set("key", "value", ttl=1)
        assert cache.get("key") == "value"

    def test_entry_expires_after_ttl(self):
        """Test that entry expires after TTL."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager(default_ttl=3600)
        # Create entry that expires immediately (1 millisecond)
        cache._cache["key"] = __import__("src.cache.cache_manager", fromlist=["CacheEntry"]).CacheEntry("value", ttl=0)
        time.sleep(0.01)  # Wait for expiration
        assert cache.get("key") is None

    def test_ttl_zero_means_no_expiration(self):
        """Test that TTL=0 means no expiration."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager(default_ttl=1)  # Short default TTL
        cache.set("key", "value", ttl=0)  # No expiration
        time.sleep(0.01)  # Wait a bit
        assert cache.get("key") == "value"


class TestCacheManagerInvalidation:
    """Tests for CacheManager invalidation functionality."""

    def test_invalidate_exact_match(self):
        """Test invalidating exact key match."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        count = cache.invalidate("key1")
        assert count == 1
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"

    def test_invalidate_wildcard_pattern(self):
        """Test invalidating with wildcard pattern."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        cache.set("user:1", "a")
        cache.set("user:2", "b")
        cache.set("item:1", "c")
        count = cache.invalidate("user:*")
        assert count == 2
        assert cache.get("user:1") is None
        assert cache.get("user:2") is None
        assert cache.get("item:1") == "c"

    def test_invalidate_question_mark_pattern(self):
        """Test invalidating with ? pattern (single char match)."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        cache.set("key1", "a")
        cache.set("key2", "b")
        cache.set("key10", "c")
        count = cache.invalidate("key?")
        assert count == 2
        assert cache.get("key1") is None
        assert cache.get("key2") is None
        assert cache.get("key10") == "c"

    def test_invalidate_no_matches(self):
        """Test invalidating with pattern that matches nothing."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        cache.set("key1", "value1")
        count = cache.invalidate("nonexistent*")
        assert count == 0
        assert cache.get("key1") == "value1"


class TestCacheManagerMaxSize:
    """Tests for CacheManager max size eviction."""

    def test_eviction_when_max_size_exceeded(self):
        """Test that oldest entries are evicted when max size is exceeded."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager(max_size=3)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        cache.set("key4", "value4")  # Should trigger eviction
        assert cache.size() == 3
        # key1 (oldest) should be evicted
        assert cache.get("key1") is None
        assert cache.get("key4") == "value4"


class TestCacheManagerDecorator:
    """Tests for CacheManager cached decorator."""

    def test_cached_decorator_caches_result(self):
        """Test that cached decorator caches function results."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        call_count = 0

        @cache.cached(ttl=3600)
        def expensive_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call - should execute function
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1

        # Second call with same args - should return cached
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Not incremented

    def test_cached_decorator_different_args(self):
        """Test that cached decorator caches different args separately."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        call_count = 0

        @cache.cached(ttl=3600)
        def add(a: int, b: int) -> int:
            nonlocal call_count
            call_count += 1
            return a + b

        result1 = add(1, 2)
        result2 = add(3, 4)
        result3 = add(1, 2)  # Same as first

        assert result1 == 3
        assert result2 == 7
        assert result3 == 3
        assert call_count == 2  # Only 2 unique calls

    def test_cached_decorator_with_kwargs(self):
        """Test that cached decorator handles kwargs correctly."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        call_count = 0

        @cache.cached(ttl=3600)
        def greet(name: str, greeting: str = "Hello") -> str:
            nonlocal call_count
            call_count += 1
            return f"{greeting}, {name}!"

        result1 = greet("Alice")
        result2 = greet("Alice", greeting="Hi")
        result3 = greet("Alice")  # Same as first

        assert result1 == "Hello, Alice!"
        assert result2 == "Hi, Alice!"
        assert result3 == "Hello, Alice!"
        assert call_count == 2

    def test_cached_decorator_with_key_prefix(self):
        """Test that cached decorator uses key prefix."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()

        @cache.cached(ttl=3600, key_prefix="api")
        def get_data(key: str) -> str:
            return f"data:{key}"

        result = get_data("test")
        assert result == "data:test"
        # Verify cache key has prefix
        assert cache.contains("api:get_data:test")

    def test_cached_decorator_none_result_not_cached(self):
        """Test that None results are not cached."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        call_count = 0

        @cache.cached(ttl=3600)
        def return_none() -> None:
            nonlocal call_count
            call_count += 1
            return None

        return_none()
        return_none()
        # None results should not be cached, so function called twice
        assert call_count == 2


class TestModuleLevelCached:
    """Tests for module-level cached decorator."""

    def test_module_cached_decorator(self):
        """Test that module-level cached decorator works."""
        from src.cache import cached, cache_manager

        call_count = 0

        @cached(ttl=3600)
        def module_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 3

        result1 = module_function(10)
        result2 = module_function(10)

        assert result1 == 30
        assert result2 == 30
        assert call_count == 1

        # Clean up
        cache_manager.clear()


class TestGlobalCacheManager:
    """Tests for global cache_manager instance."""

    def test_global_cache_manager_exists(self):
        """Test that global cache_manager instance exists."""
        from src.cache import cache_manager

        assert cache_manager is not None

    def test_global_cache_manager_is_cache_manager_type(self):
        """Test that global cache_manager is CacheManager type."""
        from src.cache import cache_manager, CacheManager

        assert isinstance(cache_manager, CacheManager)

    def test_global_cache_manager_default_ttl(self):
        """Test global cache_manager has default TTL of 3600."""
        from src.cache import cache_manager

        assert cache_manager.default_ttl == 3600

    def test_global_cache_manager_default_max_size(self):
        """Test global cache_manager has default max_size of 10000."""
        from src.cache import cache_manager

        assert cache_manager.max_size == 10000


class TestModuleExports:
    """Tests for module exports."""

    def test_exports_cache_manager(self):
        """Test cache_manager is exported."""
        from src.cache import cache_manager

        assert cache_manager is not None

    def test_exports_cache_manager_class(self):
        """Test CacheManager class is exported."""
        from src.cache import CacheManager

        assert CacheManager is not None

    def test_exports_cached_decorator(self):
        """Test cached decorator is exported."""
        from src.cache import cached

        assert cached is not None
        assert callable(cached)


class TestCacheKeyGeneration:
    """Tests for cache key generation."""

    def test_key_generation_with_args(self):
        """Test cache key generation with positional arguments."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        key = cache._generate_cache_key("func", "", (1, "test"), {})
        assert key == "func:1:test"

    def test_key_generation_with_kwargs(self):
        """Test cache key generation with keyword arguments."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        key = cache._generate_cache_key("func", "", (), {"a": 1, "b": 2})
        assert key == "func:a=1:b=2"

    def test_key_generation_with_prefix(self):
        """Test cache key generation with prefix."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        key = cache._generate_cache_key("func", "prefix", (1,), {})
        assert key == "prefix:func:1"

    def test_key_generation_kwargs_sorted(self):
        """Test that kwargs are sorted in key generation."""
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        key1 = cache._generate_cache_key("func", "", (), {"z": 1, "a": 2})
        key2 = cache._generate_cache_key("func", "", (), {"a": 2, "z": 1})
        assert key1 == key2 == "func:a=2:z=1"


class TestThreadSafety:
    """Tests for thread safety."""

    def test_concurrent_access(self):
        """Test that cache is thread-safe for concurrent access."""
        import threading
        from src.cache.cache_manager import CacheManager

        cache = CacheManager()
        errors = []

        def writer():
            try:
                for i in range(100):
                    cache.set(f"key:{threading.current_thread().name}:{i}", i)
            except Exception as e:
                errors.append(e)

        def reader():
            try:
                for i in range(100):
                    cache.get(f"key:{threading.current_thread().name}:{i}")
            except Exception as e:
                errors.append(e)

        threads = []
        for i in range(5):
            threads.append(threading.Thread(target=writer, name=f"writer-{i}"))
            threads.append(threading.Thread(target=reader, name=f"reader-{i}"))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0
