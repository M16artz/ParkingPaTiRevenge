import pytest
from django.db import IntegrityError

from apps.usuarios.models import CodigoRol, Cuenta, Persona, Rol, TipoIdentificacion
from apps.usuarios.serializers import CuentaReadSerializer
from tests.factories import crear_cuenta, crear_persona


@pytest.mark.django_db
def test_persona_identificacion_es_unica():
    crear_persona(identificacion="1100000001")

    with pytest.raises(IntegrityError):
        Persona.objects.create(
            nombre="Grace",
            apellido="Hopper",
            tipo_identificacion=TipoIdentificacion.CEDULA,
            identificacion="1100000001",
        )


@pytest.mark.django_db
def test_cuenta_username_y_correo_son_unicos():
    crear_cuenta(username="propietario", correo="uno@example.com")
    rol = Rol.objects.get(codigo=CodigoRol.PROPIETARIO)
    persona = crear_persona(identificacion="1100000002")

    with pytest.raises(IntegrityError):
        Cuenta.objects.create(
            persona=persona,
            username="propietario",
            correo="dos@example.com",
            rol=rol,
            password_hash="hash",
        )


@pytest.mark.django_db
def test_roles_requeridos_estan_en_catalogo():
    codigos = {choice[0] for choice in CodigoRol.choices}

    assert {"ADMINISTRADOR", "PROPIETARIO", "CONDUCTOR"}.issubset(codigos)


@pytest.mark.django_db
def test_cuenta_read_serializer_no_expone_password_hash():
    cuenta = crear_cuenta()

    data = CuentaReadSerializer(cuenta).data

    assert "password_hash" not in data
    assert str(cuenta) == "propietario"

