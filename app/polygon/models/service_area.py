from decimal import Decimal

from django.contrib.gis.db import models
from django.core.validators import MinValueValidator

from .base import BaseModel


class ServiceArea(BaseModel):
    name = models.CharField(max_length=256, null=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=3, null=False, validators=[MinValueValidator(Decimal("0.000"))]
    )
    geo_info = models.MultiPolygonField(null=False)

    provider = models.ForeignKey(
        "Provider",
        on_delete=models.PROTECT,
        related_name="service_areas",
        related_query_name="ice_area",
    )
