from rest_framework import serializers

from apps.tarifas.models import CategoriaTarifa


class CategoriaTarifaReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTarifa
        fields = ["id", "parqueadero", "codigo", "precio_hora"]
        read_only_fields = fields


class CategoriaTarifaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTarifa
        fields = ["parqueadero", "codigo", "precio_hora"]

    def validate_precio_hora(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio por hora debe ser mayor a cero.")
        return value

