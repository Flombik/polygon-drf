import typing as t
from http import HTTPStatus

from django.contrib.gis.geos import Point, Polygon, MultiPolygon

from polygon.tests.abstract_classes import AbstractListTestCase
from polygon.tests.factories import ServiceAreaFactory


class ServiceAreaListTestCase(AbstractListTestCase):
    results_key = "features"

    factory_class = ServiceAreaFactory
    uri = "/api/service-areas/"
    item_keys = ("name", "price")
    properties_key = "properties"
    feature_keys = ("id", "type", "geometry", properties_key)

    points_to_expected_length = {
        Point(0, 0): 3,
        Point(50, 50): 5,
        Point(100, 100): 3,
        Point(0, 100): 0,
    }

    @classmethod
    def setUpTestData(cls) -> None:
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

    def validate_response_results_item(self, item: t.Any) -> None:
        for key in self.feature_keys:
            self.assertIn(key, item)

        properties = item[self.properties_key]
        for key in self.item_keys:
            self.assertIn(key, properties)

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
