from dataclasses import dataclass
from typing import ClassVar


@dataclass
class BaseField:
    _counter: ClassVar[int] = 0
    verbose_name: str = ''
    help_text: str = ''

    def __post_init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls._counter
        self.storage_name = f'{prefix}#{index}'
        cls._counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)
