import typing as t

from polygon.models import ServiceArea

if t.TYPE_CHECKING:
    from django.db.models.query import QuerySet


def get_queryset() -> "QuerySet[ServiceArea]":
    return ServiceArea.objects.order_by("id")
