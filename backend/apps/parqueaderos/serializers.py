from rest_framework import serializers

from apps.parqueaderos.models import Direccion, DisponibilidadParqueadero, Parqueadero, Ubicacion


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ["id", "calle_principal", "calle_secundaria", "nro_lote"]


class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = ["id", "latitud", "longitud"]


class DireccionPayloadSerializer(serializers.Serializer):
    calle_principal = serializers.CharField(max_length=120)
    calle_secundaria = serializers.CharField(max_length=120, required=False, allow_blank=True)
    nro_lote = serializers.CharField(max_length=40, required=False, allow_blank=True)


class UbicacionPayloadSerializer(serializers.Serializer):
    latitud = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitud = serializers.DecimalField(max_digits=9, decimal_places=6)


class ParqueaderoReadSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer(read_only=True)
    ubicacion = UbicacionSerializer(read_only=True)
    propietario_username = serializers.CharField(source="propietario.username", read_only=True)

    class Meta:
        model = Parqueadero
        fields = [
            "id",
            "propietario",
            "propietario_username",
            "nombre",
            "estado",
            "validado",
            "disponibilidad",
            "direccion",
            "ubicacion",
            "fecha_creacion",
            "fecha_actualizacion",
        ]
        read_only_fields = fields


class ParqueaderoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parqueadero
        fields = ["propietario", "nombre", "estado", "disponibilidad", "direccion", "ubicacion"]


class ParqueaderoCreateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=120)
    disponibilidad = serializers.ChoiceField(
        choices=DisponibilidadParqueadero.choices,
        default=DisponibilidadParqueadero.CERRADO,
    )
    direccion = DireccionPayloadSerializer()
    ubicacion = UbicacionPayloadSerializer()


class ParqueaderoUpdateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=120, required=False)
    disponibilidad = serializers.ChoiceField(choices=DisponibilidadParqueadero.choices, required=False)
    direccion = DireccionPayloadSerializer(required=False)
    ubicacion = UbicacionPayloadSerializer(required=False)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("Debes enviar al menos un dato para actualizar el parqueadero.")
        return attrs


class ParqueaderoEstadoSerializer(serializers.Serializer):
    disponibilidad = serializers.ChoiceField(
        choices=DisponibilidadParqueadero.choices,
        error_messages={"invalid_choice": "El estado debe ser Abierto, Cerrado o Lleno."},
    )
