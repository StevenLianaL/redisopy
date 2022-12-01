from abc import abstractmethod


class TypeValidator(object):
    """Validate/Convert that the value is of the correct type."""

    def __init__(self, t):
        self.type = t

    def is_true_type(self, value):
        return isinstance(value, self.type)

    def from_redis_to_py(self, value):
        return NotImplemented

    def from_py_to_redis(self, value):
        return str(value)
