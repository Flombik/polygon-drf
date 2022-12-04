import typing as t
from abc import ABC, abstractmethod
from http import HTTPStatus

from django.test import TestCase

if t.TYPE_CHECKING:
    from factory import Factory


class AbstractListTestCase(TestCase, ABC):
    count_key = "count"
    next_page_key = "next"
    previous_page_key = "previous"
    results_key = "results"

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

    @classmethod
    def setUpTestData(cls) -> None:
        cls.factory_class.create_batch(size=5)

    def validate_response_data(self, data: t.Any) -> None:
        self.assertIsInstance(data, dict)

        for key in self.response_keys:
            self.assertIn(key, data)

    def validate_response_results(self, results: t.Any) -> None:
        self.assertIsInstance(results, list)

        for item in results:
            self.validate_response_results_item(item)

    def validate_response_results_item(self, item: t.Any) -> None:
        self.assertIsInstance(item, dict)
        self.assertIn("id", item)

        for key in self.item_keys:
            self.assertIn(key, item)

    def test_list_data(self) -> None:
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.validate_response_data(response_data)

        response_results = response_data[self.results_key]
        self.validate_response_results(response_results)
