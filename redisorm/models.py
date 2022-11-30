from typing import Set

from redisorm.base.model import BaseModel


class Model(BaseModel):
    """增删改查"""

    @classmethod
    def filter(cls, include: Set[str] = None, exclude: Set[str] = None, **kwargs):
        """
        :param include/exclude: can use one
        :param kwargs: filter by field
        :return:
        """
        conn = cls.class_var.conn
        keys = conn.keys(f"{cls.class_var.key_prefix}:*")
        res = []
        for key in keys:
            is_match = True
            if include:
                row = conn.hmget(key, include)
            elif exclude:
                sub_keys = cls.class_var.keys - exclude
                row = conn.hmget(key, sub_keys)
            else:
                row = conn.hgetall(key)

            row['id'] = int(key.split(":")[-1])

            for k, v in kwargs.items():
                if row[k] != v:
                    is_match = False
                    break
            if is_match:
                res.append(cls(**row))
        return res
