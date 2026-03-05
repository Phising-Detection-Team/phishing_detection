"""
Redis caching service for the Flask application.

Provides a thin wrapper around redis-py with JSON serialization,
TTL management, and key-prefix namespacing.

Usage in routes:
    from app.services.cache_service import cache

    @bp.route('/items')
    def list_items():
        cached = cache.get('items:all')
        if cached:
            return jsonify(cached)
        ...
        cache.set('items:all', data, ttl=60)
"""

import json
import logging

logger = logging.getLogger(__name__)

KEY_PREFIX = 'phishing:'


class CacheService:
    """Manages a Redis connection and provides get/set/delete with JSON serialization."""

    def __init__(self):
        self._client = None

    def init_app(self, app):
        """
        Connect to Redis using the app's REDIS_URL config.

        Stores the raw redis client on app.config['REDIS_CLIENT']
        so the health check can access it.
        """
        redis_url = app.config.get('REDIS_URL', '')
        if not redis_url:
            app.logger.warning('REDIS_URL not set — caching disabled.')
            app.config['REDIS_CLIENT'] = None
            return

        try:
            import redis
            self._client = redis.from_url(redis_url, decode_responses=True)
            self._client.ping()
            app.config['REDIS_CLIENT'] = self._client
            app.logger.info('Redis connected successfully.')
        except ImportError:
            app.logger.warning('redis package not installed — caching disabled. Run: pip install redis')
            app.config['REDIS_CLIENT'] = None
        except Exception as e:
            app.logger.warning(f'Redis connection failed ({e}) — caching disabled.')
            self._client = None
            app.config['REDIS_CLIENT'] = None

    def _key(self, key: str) -> str:
        return f'{KEY_PREFIX}{key}'

    def get(self, key: str):
        """Get a cached value. Returns None on miss or if Redis is unavailable."""
        if self._client is None:
            return None
        try:
            raw = self._client.get(self._key(key))
            if raw is None:
                return None
            return json.loads(raw)
        except Exception as e:
            logger.debug(f'Cache get failed for {key}: {e}')
            return None

    def set(self, key: str, value, ttl: int = 60):
        """Store a value with a TTL (seconds). Silently fails if Redis is unavailable."""
        if self._client is None:
            return
        try:
            self._client.setex(self._key(key), ttl, json.dumps(value, default=str))
        except Exception as e:
            logger.debug(f'Cache set failed for {key}: {e}')

    def delete(self, key: str):
        """Delete a single cache key."""
        if self._client is None:
            return
        try:
            self._client.delete(self._key(key))
        except Exception as e:
            logger.debug(f'Cache delete failed for {key}: {e}')

    def delete_pattern(self, pattern: str):
        """Delete all keys matching a pattern (e.g. 'rounds:*')."""
        if self._client is None:
            return
        try:
            full_pattern = self._key(pattern)
            keys = self._client.keys(full_pattern)
            if keys:
                self._client.delete(*keys)
        except Exception as e:
            logger.debug(f'Cache delete_pattern failed for {pattern}: {e}')

    @property
    def is_available(self) -> bool:
        if self._client is None:
            return False
        try:
            self._client.ping()
            return True
        except Exception:
            return False


cache = CacheService()
