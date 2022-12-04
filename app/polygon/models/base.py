from django.contrib.gis.db import models
from django.utils.timezone import now


class ActiveInstancesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    objects = ActiveInstancesManager()
    objects_all = models.Manager()

    def delete(self, hard=False, **kwargs):  # pylint: disable=arguments-differ
        if hard:
            super().delete(**kwargs)
        else:
            self.deleted_at = now()
            self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
