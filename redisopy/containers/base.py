from abc import abstractmethod

from redisopy.base.mixin import ConnMixin


class RedisBaseContainer:
    """"""
    conn = ConnMixin()

    def __init__(self, key: str):
        self.key = key
        self.init_redis_value()

    @abstractmethod
    def init_redis_value(self):
        return NotImplemented
