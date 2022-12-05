from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register("providers", views.ProviderViewSet)
router.register("service-areas", views.ReadOnlyServiceAreaViewSet, basename="service-areas")

provider_router = routers.NestedSimpleRouter(router, "providers", lookup="provider")
provider_router.register("service-areas", views.ServiceAreaNestedViewSet, basename="provider-service-areas")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(provider_router.urls)),
]
