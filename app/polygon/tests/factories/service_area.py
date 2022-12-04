from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal


class ServiceAreaFactory(DjangoModelFactory):
    class Meta:
        model = "polygon.ServiceArea"
        django_get_or_create = ("name",)

    name = Sequence(lambda n: f"ServiceArea #{n+1}")
    price = FuzzyDecimal(0, 9_999_999, 3)
