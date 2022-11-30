from redisorm.connection import connect
from redisorm.fields import StringField, IntField
from redisorm.models import Model


def test_use_model():
    connect(db=3)

    class Person(Model):
        name = StringField()
        age = IntField()

        class Meta:
            key_prefix = "UpUp:person:"

    class Person2(Model):
        name = StringField()

    person = Person(name='John', age=20)
    p2 = Person2(name='John')
    person.age = 30
    person.save()
    p2.save()


def test_a():
    class TestA:
        name = StringField()
        age = IntField()

        def __init__(self, name, age):
            self.name = name
            self.age = age

    t = TestA(name='John', age=20)

    print(t.name)
