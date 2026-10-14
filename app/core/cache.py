"""Small, failure-tolerant Redis helpers for JSON API responses."""

import json
import logging
from typing import Any

from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings

logger = logging.getLogger(__name__)
_redis_client: Redis | None = None


def _client() -> Redis | None:
    """Create the client lazily so Redis stays an optional performance layer."""
    global _redis_client

    if not settings.CACHE_ENABLED:
        return None

    if _redis_client is None:
        _redis_client = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
        )
    return _redis_client


def get_json(key: str) -> Any | None:
    try:
        value = _client()
        if value is None:
            return None
        cached = value.get(key)
        return json.loads(cached) if cached else None
    except (RedisError, json.JSONDecodeError):
        logger.warning("Redis cache read failed for key %s", key)
        return None


def set_json(key: str, payload: Any, ttl_seconds: int) -> None:
    try:
        value = _client()
        if value is not None:
            value.setex(key, ttl_seconds, json.dumps(payload, default=str))
    except (RedisError, TypeError, ValueError):
        logger.warning("Redis cache write failed for key %s", key)


def delete(*keys: str) -> None:
    try:
        value = _client()
        if value is not None and keys:
            value.delete(*keys)
    except RedisError:
        logger.warning("Redis cache invalidation failed for keys %s", keys)
