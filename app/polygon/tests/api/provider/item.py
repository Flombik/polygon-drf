from polygon.tests.api.base import BaseAPIItemTestCase
from polygon.tests.factories import ProviderFactory


class ProviderItemTestCase(BaseAPIItemTestCase):
    factory_class = ProviderFactory
    uri = "/api/providers/"
    item_keys = ("name", "email", "phone_number", "language", "currency")
