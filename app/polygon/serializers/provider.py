from polygon.models import Provider
from rest_framework import serializers


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "language",
            "currency",
        ]
