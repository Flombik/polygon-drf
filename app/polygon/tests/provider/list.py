from polygon.tests.abstract_classes import AbstractListTestCase
from polygon.tests.factories import ProviderFactory


class ProviderListTestCase(AbstractListTestCase):
    factory_class = ProviderFactory
    uri = "/api/providers/"
    item_keys = ("name", "email", "phone_number", "language", "currency")
