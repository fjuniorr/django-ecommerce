import factory
from . import base


class UserFactory(factory.Factory):
    class Meta:
        model = base.User

    firstname = "John"
    lastname = "Doe"
