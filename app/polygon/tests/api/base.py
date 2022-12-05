import typing as t
from abc import ABC, abstractmethod
from http import HTTPStatus

from django.test import TestCase

from polygon.tests.api.utils import urljoin

if t.TYPE_CHECKING:
    from factory import Factory


class BaseAPITestCase(TestCase, ABC):
    @property
    @abstractmethod
    def factory_class(self) -> "Factory":
        ...

    @property
    @abstractmethod
    def uri(self) -> str:
        ...

    @property
    @abstractmethod
    def item_keys(self) -> t.Sequence[str]:
        ...


class BaseAPIItemTestCase(BaseAPITestCase, ABC):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.item = cls.factory_class.create()

    def validate_item(self, item: dict[str, t.Any]) -> None:
        self.assertIsInstance(item, dict)
        self.assertIn("id", item)

        for key in self.item_keys:
            self.assertIn(key, item)

    def test_item_get(self):
        response = self.client.get(urljoin(self.uri, str(self.item.id)))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.validate_item(response_data)

    def test_item_put(self):
        response = self.client.patch(urljoin(self.uri, str(self.item.id)))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.validate_item(response_data)

    def test_item_patch(self):
        response = self.client.patch(urljoin(self.uri, str(self.item.id)))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.validate_item(response_data)

    def test_item_delete(self):
        response = self.client.delete(urljoin(self.uri, str(self.item.id)))
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)


class BaseAPIListTestCase(BaseAPITestCase, ABC):
    count_key = "count"
    next_page_key = "next"
    previous_page_key = "previous"
    results_key = "results"

    batch_size = 10

    @property
    def paginated_response_keys(self) -> t.Sequence[str]:
        return (
            self.count_key,
            self.next_page_key,
            self.previous_page_key,
        )

    @property
    def response_keys(self) -> t.Sequence[str]:
        return (
            self.results_key,
            *self.paginated_response_keys,
        )

    @classmethod
    def setUpTestData(cls) -> None:
        cls.factory_class.create_batch(size=cls.batch_size)

    validate_item = BaseAPIItemTestCase.validate_item

    def validate_response_data(self, data: dict) -> None:
        self.assertIsInstance(data, dict)

        for key in self.response_keys:
            self.assertIn(key, data)

    def validate_response_results(self, results: list) -> None:
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), self.batch_size)

        for item in results:
            self.validate_item(item)

    def test_list_get(self) -> None:
        response = self.client.get(self.uri, {"page_size": self.batch_size})
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.validate_response_data(response_data)

        response_results = response_data[self.results_key]
        self.validate_response_results(response_results)
