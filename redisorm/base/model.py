from redisorm.base.field import BaseField
from redisorm.utils.model_var import ModelClassVar


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        for key, value in attrs.items():
            if isinstance(value, BaseField):
                setattr(cls, key, value)
        return super().__new__(cls, name, bases, attrs)


class BaseModel(metaclass=ModelMeta):
    """
    基础操作，主要是实例方法
    @property 标记的都是实例变量
    """
    class_var = ModelClassVar()
    _key: str = ""  # redis instance key

    class Meta:
        # key_prefix
        pass

    def __init__(self, **kwargs):
        self.class_var.meta = getattr(self, "Meta", None)
        for key, value in kwargs.items():
            self.class_var.keys.add(key)
            setattr(self, key, value)

    def __str__(self):
        return f"{self.__class__.__name__}{str(self.fields)}"

    def save(self, ex: int = 0):
        self.class_var.conn.hset(self.key, mapping=self.fields)
        if ex:
            self.class_var.conn.expire(self.key, ex)

    @property
    def key(self) -> str:
        if not self._key:
            prefix = self.class_var.key_prefix
            keys = self.class_var.conn.keys(f"{prefix}:*")
            ids = [int(key.split(":")[-1]) for key in keys]
            new_id = max(ids) + 1 if ids else 1
            self._key = f"{prefix}:{new_id}"
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value

    @classmethod
    @property
    def fields(self):
        data = {}
        for k in self.class_var.keys:
            data[k] = getattr(self, k)
        return data
