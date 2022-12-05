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

        count_after_delete = self.batch_size - 1
        self.assertEqual(Provider.objects.count(), count_after_delete)
        self.assertEqual(Provider.objects_all.count(), self.batch_size)

    def test_hard_delete(self):
        self.assertEqual(Provider.objects.count(), self.batch_size)
        self.assertEqual(Provider.objects_all.count(), self.batch_size)

        Provider.objects.first().delete(hard=True)

        count_after_delete = self.batch_size - 1
        self.assertEqual(Provider.objects.count(), count_after_delete)
        self.assertEqual(Provider.objects_all.count(), count_after_delete)

    def test_restore(self):
        self.assertEqual(Provider.objects.count(), self.batch_size)
        self.assertEqual(Provider.objects_all.count(), self.batch_size)

        provider = Provider.objects.first()
        provider.delete()
        provider.restore()

        self.assertEqual(Provider.objects.count(), self.batch_size)
