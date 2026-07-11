from rest_framework import serializers

from apps.espacios.models import Espacio


class EspacioReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espacio
        fields = ["id", "parqueadero", "numero_espacio", "estado"]
        read_only_fields = fields


class EspacioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espacio
        fields = ["parqueadero", "numero_espacio", "estado"]

