import factory
from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal

from .provider import ProviderFactory


class ServiceAreaFactory(DjangoModelFactory):
    class Meta:
        model = "polygon.ServiceArea"
        django_get_or_create = ("name",)

    name = Sequence(lambda n: f"ServiceArea #{n+1}")
    price = FuzzyDecimal(0, 9_999_999, 3)
    provider = factory.SubFactory(ProviderFactory)
