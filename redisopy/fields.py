from dataclasses import dataclass

from redisopy.base.field import BaseField


class BooleanField(BaseField):
    field_type = bool

    def from_redis_to_py(self, value):
        return bool(value)

    def from_py_to_redis(self, value):
        return '1' if value else ''


class StringField(BaseField):
    field_type = str

    def from_redis_to_py(self, value):
        return str(value)


class IntField(BaseField):
    field_type = int

    def from_redis_to_py(self, value):
        return int(value)


class FloatField(BaseField):
    field_type = float

    def from_redis_to_py(self, value):
        return float(value)
