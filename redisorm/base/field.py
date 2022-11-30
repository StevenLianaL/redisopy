from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Any


@dataclass
class BaseField:
    _counter: ClassVar[int] = 0
    required: bool = False
    default: Any = None
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
        return self.from_redis_to_py(getattr(instance, self.storage_name, ''))

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)

    @abstractmethod
    def from_redis_to_py(self, value):
        return NotImplemented
