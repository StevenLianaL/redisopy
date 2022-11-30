from redis.client import StrictRedis

from redisorm.base.field import BaseField
from redisorm.connection import DEFAULT_CONNECTION


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        for key, value in attrs.items():
            if isinstance(value, BaseField):
                setattr(cls, key, value)
        return super().__new__(cls, name, bases, attrs)


class BaseModel(metaclass=ModelMeta):
    keys = set()  # field set

    class Meta:
        # key_prefix
        pass

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.keys.add(key)
            setattr(self, key, value)

    def __str__(self):
        return f"{self.__class__.__name__}{str(self.fields)}"

    def save(self):
        self.conn.hset(self.key, mapping=self.fields)

    def create(self, **kwargs):
        pass

    @property
    def key_prefix(self) -> str:
        meta = getattr(self, "Meta", None)
        if meta:
            key_prefix = getattr(meta, "key_prefix", self.__class__.__name__.lower())
        else:
            key_prefix = self.__class__.__name__.lower()
        return key_prefix

    @property
    def key(self) -> str:
        prefix = self.key_prefix
        keys = self.conn.keys(f"{prefix}:*")
        ids = [int(key.split(":")[-1]) for key in keys]
        new_id = max(ids) + 1 if ids else 1
        return f"{prefix}:{new_id}"

    @property
    def conn(self) -> StrictRedis:
        return DEFAULT_CONNECTION[0]

    @property
    def fields(self):
        data = {}
        for k in self.keys:
            data[k] = getattr(self, k)
        return data
