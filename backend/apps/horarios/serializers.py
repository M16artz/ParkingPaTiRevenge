from rest_framework import serializers

from apps.horarios.models import HorarioAtencion


class HorarioAtencionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioAtencion
        fields = ["id", "parqueadero", "dia", "hora_apertura", "hora_cierre"]
        read_only_fields = fields


class HorarioAtencionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioAtencion
        fields = ["parqueadero", "dia", "hora_apertura", "hora_cierre"]

