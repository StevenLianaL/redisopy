from redisorm.base.field import BaseField


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        for key, value in attrs.items():
            if isinstance(value, BaseField):
                setattr(cls, key, value)
        return super().__new__(cls, name, bases, attrs)


class BaseModel(metaclass=ModelMeta):
    cls_name: str = ""
    keys = set()  # field set

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.keys.add(key)
            setattr(self, key, value)

    def __str__(self):
        data = {}
        for k in self.keys:
            data[k] = getattr(self, k)
        return f"{self.__class__.__name__}{str(data)}"

    def save(self):
        pass

    def create(self, **kwargs):
        pass

    class Meta:
        pass
