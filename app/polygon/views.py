from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_gis.pagination import GeoJsonPagination

from .filters import service_area as service_area_filters
from .selectors import provider as provider_selectors, service_area as service_area_selectors
from .serializers import provider as provider_serializers, service_area as service_area_serializers


class ProviderViewSet(ModelViewSet):
    queryset = provider_selectors.get_queryset()
    serializer_class = provider_serializers.ProviderSerializer
    permission_classes = [permissions.AllowAny]


class ServiceAreaConfigMixin:
    serializer_class = service_area_serializers.ServiceAreaSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = GeoJsonPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = service_area_filters.ServiceAreaFilter

    def get_queryset(self):
        queryset = service_area_selectors.get_queryset()

        if (provider_pk := self.kwargs.get("provider_pk")) is not None:
            try:
                provider = provider_selectors.get_provider_by_id(provider_pk)
            except provider_selectors.Provider.DoesNotExist:
                raise NotFound

            queryset = queryset.filter(provider=provider)

        return queryset


class ServiceAreaNestedViewSet(ServiceAreaConfigMixin, ModelViewSet):
    def perform_create(self, serializer):
        try:
            provider = provider_selectors.get_provider_by_id(self.kwargs.get("provider_pk"))
        except provider_selectors.Provider.DoesNotExist:
            raise NotFound

        serializer.save(provider=provider)


class ReadOnlyServiceAreaViewSet(ServiceAreaConfigMixin, ReadOnlyModelViewSet):
    ...
