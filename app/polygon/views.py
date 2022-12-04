from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination

from .filters import service_area as service_area_filters
from .selectors import provider as provider_selectors, service_area as service_area_selectors
from .serializers import provider as provider_serializers, service_area as service_area_serializers


class ProviderViewSet(ModelViewSet):
    # pylint: disable=too-many-ancestors
    queryset = provider_selectors.get_queryset()
    serializer_class = provider_serializers.ProviderSerializer
    permission_classes = [permissions.AllowAny]


class ServiceAreaViewSet(ModelViewSet):
    # pylint: disable=too-many-ancestors
    queryset = service_area_selectors.get_queryset()
    serializer_class = service_area_serializers.ServiceAreaSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = GeoJsonPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = service_area_filters.ServiceAreaFilter
