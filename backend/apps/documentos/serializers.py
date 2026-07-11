from rest_framework import serializers

from apps.common.exceptions import DomainValidationError
from apps.documentos.models import Documento, EstadoDocumento
from apps.documentos.validators import validar_archivo_documento


class DocumentoReadSerializer(serializers.ModelSerializer):
    cuenta_username = serializers.CharField(source="cuenta.username", read_only=True)

    class Meta:
        model = Documento
        fields = [
            "id",
            "cuenta",
            "cuenta_username",
            "estado",
            "es_valido",
            "fecha_expiracion",
            "nombre_original",
            "content_type",
            "tamano_bytes",
            "motivo_rechazo",
            "fecha_creacion",
            "fecha_actualizacion",
        ]
        read_only_fields = fields


class DocumentoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = ["cuenta", "es_valido", "fecha_expiracion", "ruta", "file_id"]
        extra_kwargs = {"ruta": {"write_only": True}}


class DocumentoUploadSerializer(serializers.Serializer):
    archivo = serializers.FileField()

    def validate_archivo(self, value):
        try:
            validar_archivo_documento(value)
        except DomainValidationError as exc:
            raise serializers.ValidationError(str(exc)) from exc
        return value


class DocumentoValidacionSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(choices=[EstadoDocumento.VALIDADO, EstadoDocumento.RECHAZADO])
    motivo_rechazo = serializers.CharField(required=False, allow_blank=True, max_length=500)
