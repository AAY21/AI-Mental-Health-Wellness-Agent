# src/utils/cache.py

"""
Simple local caching system for agent operations.
Used to avoid repeated LLM calls for similar inputs.
Works with in-memory + optional on-disk JSON caching.
"""

import os
import json
import hashlib
from datetime import datetime


CACHE_DIR = "cache_store"
CACHE_FILE = os.path.join(CACHE_DIR, "cache.json")


class CacheManager:

    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)

        if not os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "w") as f:
                json.dump({}, f)

        with open(CACHE_FILE, "r") as f:
            self.cache = json.load(f)

    def _hash(self, text: str) -> str:
        """Create a stable hash for keys."""
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def get(self, key: str):
        """Retrieve value from cache if exists."""
        hashed = self._hash(key)
        return self.cache.get(hashed)

    def set(self, key: str, value):
        """Store value in cache."""
        hashed = self._hash(key)
        self.cache[hashed] = {
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }
        with open(CACHE_FILE, "w") as f:
            json.dump(self.cache, f, indent=4)

    def clear(self):
        """Clear entire cache."""
        self.cache = {}
        with open(CACHE_FILE, "w") as f:
            json.dump({}, f)


# global cache instance
cache = CacheManager()
