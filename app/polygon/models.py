from django.contrib.gis.db import models


class ActiveInstancesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = models.Manager()
    active_objects = ActiveInstancesManager()


class Provider(BaseModel):
    name = models.CharField(max_length=256, unique=True, null=False)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    language = models.CharField(max_length=2, null=True)
    currency = models.CharField(max_length=3, null=True)


class ServiceArea(BaseModel):
    name = models.CharField(max_length=256, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    geo_info = models.MultiPolygonField(null=False)
