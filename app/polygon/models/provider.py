from django.contrib.gis.db import models

from .base import BaseModel


class Provider(BaseModel):
    name = models.CharField(max_length=256, unique=True, null=False)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    language = models.CharField(max_length=2, null=True)
    currency = models.CharField(max_length=3, null=True)
