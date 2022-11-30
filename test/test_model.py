from redisorm.connection import connect
from redisorm.fields import StringField, IntField, BooleanField
from redisorm.models import Model


class Person(Model):
    name = StringField()
    age = IntField()
    is_active = BooleanField()

    class Meta:
        key_prefix = "UpUp:person:"


class Person2(Model):
    name = StringField()
    age = IntField()

    class Meta:
        key_prefix = "UpUp:person2:"


class Person3(Model):
    name = StringField()
    age = IntField()


connect(db=3)


def test_use_model():
    person = Person(name='John', age=20, is_active=True)
    person.save()
    person2 = Person(name='John', age=20, is_active=False)
    person2.save()
    person2 = Person2(name='John', age=20)
    person2.save()
    person3 = Person3(name='John', age=20)
    person3.save()
    rows = Person.filter()
    for r in rows:
        print(r)


def test_instance_delete():
    person = Person(name='John', age=20)
    person.save()
    person.delete()


def test_get_instance():
    person = Person(name='test', age=99)
    person.save()
    person2 = Person.get_by_id(r_id=person.record_id)
    print(person2)


def test_bool():
    key = "test_bool"
    conn = connect(db=3)
    conn.set(key, 1)
    for val in [1, 0, '']:
        conn.set(key, val)
        print(conn.get(key), bool(conn.get(key)))
