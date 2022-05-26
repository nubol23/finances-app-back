import factory.django

from apps.users.models import User
from utils.tests.faker import faker


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    password = factory.PostGenerationMethodCall("set_password", "password")
    name = factory.LazyFunction(lambda: faker.name())
    is_active = True

    @factory.lazy_attribute
    def email(self):
        return f"{self.name}@mail.com"
