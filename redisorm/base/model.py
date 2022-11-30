from redisorm.base.field import BaseField
from redisorm.utils.model_var import ModelClassVar


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        for key, value in attrs.items():
            if isinstance(value, BaseField):
                setattr(cls, key, value)
        attrs["class_var"] = ModelClassVar(cls_name=name, meta=attrs.get("Meta", None))
        return super().__new__(cls, name, bases, attrs)

    class Meta:
        # key_prefix
        pass


class BaseModel(metaclass=ModelMeta):
    """
    基础操作，主要是实例方法
    @property 标记的都是实例变量
    """
    class_var = None
    _record_id: int = None
    _key: str = ""  # redis instance key

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.class_var.keys.add(key)
            setattr(self, key, value)

    def __str__(self):
        return f"{self.__class__.__name__}{str(self.fields)}"

    def __repr__(self):
        return str(self)

    def save(self, ex: int = 0) -> int:
        save_data = {}
        for k, v in self.fields.items():
            if isinstance(v, bool):
                save_data[k] = '1' if v else ''
            else:
                save_data[k] = v
        self.class_var.conn.hset(self.key, mapping=save_data)
        if ex:
            self.class_var.conn.expire(self.key, ex)
        return self.record_id

    def delete(self):
        self.class_var.conn.delete(self.key)

    @property
    def record_id(self):
        return self._record_id

    @record_id.setter
    def record_id(self, value: int):
        self._record_id = value

    @property
    def key(self) -> str:
        if not self._key:
            prefix = self.class_var.key_prefix
            if self.record_id:
                self._key = f"{prefix}{self.record_id}"
            else:
                keys = self.class_var.conn.keys(f"{prefix}*")
                ids = [int(key.split(":")[-1]) for key in keys]
                self.record_id = max(ids) + 1 if ids else 1
                self._key = f"{prefix}{self.record_id}"
        return self._key

    @property
    def fields(self):
        data = {}
        for k in self.class_var.keys:
            data[k] = getattr(self, k)
        return data
