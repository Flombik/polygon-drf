from polygon.tests.api.base import BaseAPIListTestCase
from polygon.tests.factories import ProviderFactory


class ProviderListTestCase(BaseAPIListTestCase):
    factory_class = ProviderFactory
    uri = "/api/providers/"
    item_keys = ("name", "email", "phone_number", "language", "currency")
