from typing import Set

from redisorm.base.model import BaseModel


class Model(BaseModel):
    """增删改查"""

    @classmethod
    def filter(cls, include: Set[str] = None, exclude: Set[str] = None, **kwargs):
        # keys = cls.conn.keys(f"{cls.key_prefix}:*")
        pass
