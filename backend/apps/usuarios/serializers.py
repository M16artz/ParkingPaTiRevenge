from rest_framework import serializers

from apps.usuarios.models import CodigoRol, Cuenta, Persona, Rol, TipoIdentificacion


class PersonaReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            "id",
            "nombre",
            "apellido",
            "tipo_identificacion",
            "identificacion",
            "estado",
        ]
        read_only_fields = fields


class PersonaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ["nombre", "apellido", "tipo_identificacion", "identificacion", "estado"]


class RolReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ["id", "codigo"]
        read_only_fields = fields


class CuentaReadSerializer(serializers.ModelSerializer):
    persona = PersonaReadSerializer(read_only=True)
    rol = RolReadSerializer(read_only=True)

    class Meta:
        model = Cuenta
        fields = ["id", "persona", "username", "correo", "rol", "estado"]
        read_only_fields = fields


class CuentaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ["persona", "username", "correo", "rol", "estado", "password_hash"]
        extra_kwargs = {"password_hash": {"write_only": True}}


class RegistroCuentaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=80)
    apellido = serializers.CharField(max_length=80)
    tipo_identificacion = serializers.ChoiceField(choices=TipoIdentificacion.choices)
    identificacion = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=80)
    correo = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    rol = serializers.ChoiceField(choices=CodigoRol.choices, default=CodigoRol.CONDUCTOR)

    def validate_rol(self, value):
        if value == CodigoRol.ADMINISTRADOR:
            raise serializers.ValidationError("No puedes registrar una cuenta administradora desde este formulario.")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class TokenRefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class PerfilCuentaSerializer(serializers.ModelSerializer):
    persona = PersonaReadSerializer(read_only=True)
    rol = serializers.CharField(source="rol.codigo", read_only=True)

    class Meta:
        model = Cuenta
        fields = ["id", "username", "correo", "rol", "estado", "persona"]
        read_only_fields = fields
