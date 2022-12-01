from redisopy.base.field import BaseField


class BooleanField(BaseField):
    field_type = bool


class StringField(BaseField):
    field_type = str


class IntField(BaseField):
    field_type = int


class FloatField(BaseField):
    field_type = float
