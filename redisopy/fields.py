from dataclasses import dataclass

from redisopy.base.field import BaseField


@dataclass
class BooleanField(BaseField):

    def from_redis_to_py(self, value):
        return bool(value)

    def from_py_to_redis(self, value):
        return '1' if value else ''


@dataclass
class StringField(BaseField):

    def from_redis_to_py(self, value):
        return str(value)


@dataclass
class IntField(BaseField):

    def from_redis_to_py(self, value):
        return int(value)


@dataclass
class FloatField(BaseField):

    def from_redis_to_py(self, value):
        return float(value)
