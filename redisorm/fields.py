from dataclasses import dataclass

from redisorm.base.field import BaseField


@dataclass
class BooleanField(BaseField):
    pass


@dataclass
class StringField(BaseField):
    pass


@dataclass
class IntField(BaseField):
    pass


@dataclass
class FloatField(BaseField):
    pass
