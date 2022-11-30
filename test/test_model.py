from redisorm.connection import connect
from redisorm.fields import StringField, IntField
from redisorm.models import Model


class Person(Model):
    name = StringField()
    age = IntField()

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
    person = Person(name='John', age=20)
    person.age = 30
    person.save()
    person2 = Person2(name='John', age=20)
    person2.save()
    person3 = Person3(name='John', age=20)
    person3.save()
    rows = Person.filter(name='John')
    for r in rows:
        print(r)


def test_instance_delete():
    person = Person(name='John', age=20)
    person.save()
    person.delete()
