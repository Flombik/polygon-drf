import typing as t

from polygon.models import Provider

if t.TYPE_CHECKING:
    from django.db.models.query import QuerySet


def get_queryset() -> "QuerySet[Provider]":
    return Provider.objects.order_by("id")


def get_provider_by_id(id_: int) -> "Provider":
    return Provider.objects.get(id=id_)
