from rest_framework_gis.serializers import GeoFeatureModelSerializer

from polygon.models import ServiceArea


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ServiceArea
        geo_field = "geo_info"

        fields = ["id", "name", "price", "provider_id"]
        read_only = ["provider_id"]
