from django.contrib.gis.db import models

from .base import BaseModel


class ServiceArea(BaseModel):
    name = models.CharField(max_length=256, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    geo_info = models.MultiPolygonField(null=False)
