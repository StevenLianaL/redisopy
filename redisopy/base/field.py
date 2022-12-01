from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Any

from redisopy.errors import TypeNotMatchError
from redisopy.utils.validation import TypeValidator


class FieldMeta(type):

    def __new__(cls, name, bases, attrs):
        attrs["validator"] = TypeValidator(attrs.get("field_type", None))
        return super().__new__(cls, name, bases, attrs)


class BaseField(metaclass=FieldMeta):
    _counter: int = 0
    field_type: type = None
    validator: TypeValidator = None

    def __init__(self, *, required=False, default=None, verbose_name='', help_text=''):
        self.required = required
        self.default = default
        self.verbose_name = verbose_name
        self.help_text = help_text

        cls = self.__class__
        prefix = cls.__name__
        index = cls._counter
        self.storage_name = f'{prefix}#{index}'
        cls._counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.from_redis_to_py(getattr(instance, self.storage_name, ''))

    def __set__(self, instance, value):
        if not self.validator.is_true_type(value):
            raise TypeNotMatchError(f"{value} is type {type(value)}, not {self.field_type}")
        setattr(instance, self.storage_name, value)

    @abstractmethod
    def from_redis_to_py(self, value):
        return NotImplemented

    def from_py_to_redis(self, value):
        return str(value)
