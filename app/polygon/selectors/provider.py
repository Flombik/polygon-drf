import typing as t

from polygon.models import Provider

if t.TYPE_CHECKING:
    from django.db.models.query import QuerySet


def get_queryset() -> "QuerySet[Provider]":
    return Provider.active_objects.order_by("id")
