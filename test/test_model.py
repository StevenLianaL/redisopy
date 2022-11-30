from redisorm.fields import StringField, IntField
from redisorm.models import Model


def test_use_model():
    class Person(Model):
        name = StringField()
        age = IntField()

    person = Person(name='John', age=20)

    person.age = 30
    print(person)


def test_a():
    class TestA:
        name = StringField()
        age = IntField()

        def __init__(self, name, age):
            self.name = name
            self.age = age

    t = TestA(name='John', age=20)

    print(t.name)
