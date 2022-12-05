from django.test import TestCase

from polygon.models import Provider
from polygon.tests.factories import ProviderFactory


class SoftDeleteTestCase(TestCase):
    batch_size = 2

    @classmethod
    def setUpTestData(cls) -> None:
        ProviderFactory.create_batch(size=cls.batch_size)

    def test_soft_delete(self):
        self.assertEqual(Provider.objects.count(), self.batch_size)
        self.assertEqual(Provider.objects_all.count(), self.batch_size)

        Provider.objects.first().delete()

        self.assertEqual(Provider.objects.count(), self.batch_size - 1)
        self.assertEqual(Provider.objects_all.count(), self.batch_size)
