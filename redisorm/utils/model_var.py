from typing import Set, Any

from redis.client import StrictRedis

from redisorm.connection import DEFAULT_CONNECTION


class ModelClassVar:
    """Model class level var"""
    meta: Any = None
    keys: Set[str] = set()

    @property
    def conn(self) -> StrictRedis:
        """Get alive redis connection by connect"""
        return DEFAULT_CONNECTION[0]

    @property
    def key_prefix(self) -> str:
        if self.meta:
            key_prefix = getattr(self.meta, "key_prefix", self.__class__.__name__.lower())
        else:
            key_prefix = self.__class__.__name__.lower()
        return key_prefix
