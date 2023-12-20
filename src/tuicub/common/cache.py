from collections.abc import Hashable
from typing import Any

from cacheout import Cache as Cacheout  # type: ignore


class Cache:
    """An in-memory cache."""

    __slots__ = "_cache"

    def __init__(self, cache_engine: Cacheout):
        self._cache = cache_engine

    def get(self, key: Hashable, default: Any | None = None) -> Any | None:
        """Get a cached value for the key.

        Retrieves and returns a value for the given key. If no value is stored
        for the key, then the optional default value is returned.

        Args:
            key (Hashable): The key to retrieve the value for.
            default (Any | None): An optional fallback value.

        Returns:
            The cached value.
        """
        return self._cache.get(key=key, default=default)

    def set(self, key: Hashable, value: Any) -> None:
        """Cache a value for the given key."""
        self._cache.set(key=key, value=value)
