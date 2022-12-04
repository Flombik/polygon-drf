from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("providers", views.ProviderViewSet)
router.register("service-areas", views.ServiceAreaViewSet)
