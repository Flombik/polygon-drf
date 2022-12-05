import typing as t

from django.contrib.gis.geos import Polygon, MultiPolygon

from polygon.tests.api.base import BaseAPIItemTestCase
from polygon.tests.api.utils import urljoin
from polygon.tests.factories import ServiceAreaFactory


class ServiceAreaItemTestCase(BaseAPIItemTestCase):
    factory_class = ServiceAreaFactory
    item_keys = ("name", "price")
    properties_key = "properties"
    feature_keys = ("id", "type", "geometry", properties_key)

    @property
    def uri(self) -> str:
        provider_id = str(self.item.provider.id)
        return urljoin("/api/providers/", provider_id, "/service-areas/")

    @classmethod
    def setUpTestData(cls) -> None:
        # pylint: disable=duplicate-code
        cls.item = cls.factory_class.create(
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

    def validate_item(self, item: t.Any) -> None:
        for key in self.feature_keys:
            self.assertIn(key, item)

        properties = item[self.properties_key]
        for key in self.item_keys:
            self.assertIn(key, properties)
