import typing as t

from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.geos import Point
from django_filters import rest_framework as filters
from rest_framework.exceptions import ParseError
from rest_framework_gis import filters as geo_filters

from polygon.models import ServiceArea

if t.TYPE_CHECKING:
    from django.db.models.query import QuerySet


class ServiceAreaFilter(geo_filters.GeoFilterSet):
    class Meta:
        model = ServiceArea
        fields = ["geo_info"]
        filter_overrides = {
            GeometryField: {
                "filter_class": geo_filters.GeometryFilter,
                "extra": lambda f: {
                    "lookup_expr": "intersects",
                },
            }
        }

    point = filters.CharFilter(method="filter_point_intersects")

    @staticmethod
    def filter_point_intersects(queryset: "QuerySet[t.Any]", name: str, value: str):
        try:
            (x, y) = (float(n) for n in value.split(","))
        except ValueError:
            raise ParseError("Invalid string supplied for parameter {0}".format(name))

        point = Point(x, y)
        queryset = queryset.filter(geo_info__intersects=point)

        return queryset
