from factory import Sequence
from factory.django import DjangoModelFactory


class ProviderFactory(DjangoModelFactory):
    class Meta:
        model = "polygon.Provider"
        django_get_or_create = ("name",)

    name = Sequence(lambda n: f"Provider #{n+1}")
