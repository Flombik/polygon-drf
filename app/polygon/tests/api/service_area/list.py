from http import HTTPStatus

from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from polygon.tests.api.base import BaseAPIListTestCase
from polygon.tests.factories import ServiceAreaFactory

from .item import ServiceAreaItemTestCase


class ServiceAreaListTestCase(BaseAPIListTestCase):
    results_key = "features"

    factory_class = ServiceAreaFactory
    uri = "/api/service-areas/"
    item_keys = ServiceAreaItemTestCase.item_keys
    properties_key = ServiceAreaItemTestCase.properties_key
    feature_keys = ServiceAreaItemTestCase.feature_keys

    points_to_expected_length = {
        Point(0, 0): 3,
        Point(50, 50): 5,
        Point(100, 100): 3,
        Point(0, 100): 0,
    }

    @classmethod
    def setUpTestData(cls) -> None:
        # pylint: disable=duplicate-code
        cls.factory_class.create_batch(
            size=2,
            geo_info=MultiPolygon(
                Polygon(
                    (
                        (0, 0),
                        (0, 50),
                        (50, 50),
                        (50, 0),
                        (0, 0),
                    )
                )
            ),
        )
        cls.factory_class.create_batch(
            size=2,
            geo_info=MultiPolygon(
                Polygon(
                    (
                        (50, 50),
                        (50, 100),
                        (100, 100),
                        (100, 50),
                        (50, 50),
                    )
                )
            ),
        )
        cls.factory_class.create_batch(
            size=1,
            geo_info=MultiPolygon(
                Polygon(
                    (
                        (0, 0),
                        (0, 25),
                        (75, 100),
                        (100, 100),
                        (100, 75),
                        (25, 0),
                        (0, 0),
                    )
                )
            ),
        )
        cls.batch_size = 5

    validate_item = ServiceAreaItemTestCase.validate_item

    def test_list_filtering_with_point(self):
        for point, expected_length in self.points_to_expected_length.items():
            response = self.client.get(self.uri, {"point": f"{point.x},{point.y}"})
            self.assertEqual(response.status_code, HTTPStatus.OK)

            response_data = response.json()
            features = response_data[self.results_key]
            self.assertEqual(len(features), expected_length)

    def test_list_filtering_with_geo_info(self):
        for point, expected_length in self.points_to_expected_length.items():
            response = self.client.get(self.uri, {"geo_info": point.geojson})
            self.assertEqual(response.status_code, HTTPStatus.OK)

            response_data = response.json()
            features = response_data[self.results_key]
            self.assertEqual(len(features), expected_length)

    def test_list_filtering_with_incorrect_point(self):
        response = self.client.get(self.uri, {"point": "1"})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response = self.client.get(self.uri, {"point": "1,1,1"})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
