import random
from dataclasses import dataclass, field
from typing import Set, Any

from redis.client import StrictRedis

from redisorm.connection import DEFAULT_CONNECTION


@dataclass
class ModelClassVar:
    """Model class level var"""
    cls: Any = None
    meta: Any = None
    keys: Set[str] = field(default_factory=set)

    def __hash__(self):
        return hash(self.cls, random.randint(0, 100))

    def __eq__(self, other):
        return self.cls == other.cls

    @property
    def conn(self) -> StrictRedis:
        """Get alive redis connection by connect"""
        return DEFAULT_CONNECTION[0]

    @property
    def key_prefix(self) -> str:
        if self.meta:
            key_prefix = getattr(self.meta, "key_prefix", self.cls.__name__.lower())
        else:
            key_prefix = f"{self.cls.__name__.lower()}:"
        return key_prefix
