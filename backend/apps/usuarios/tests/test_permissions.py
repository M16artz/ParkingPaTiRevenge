import pytest
from rest_framework.test import APIRequestFactory

from apps.usuarios.permissions import IsAdministrador, IsAuthenticatedUser, IsPropietario
from tests.factories import crear_cuenta, crear_usuario_anonimo


@pytest.mark.django_db
def test_permiso_administrador_solo_pasa_para_admin():
    request = APIRequestFactory().get("/")
    request.user = crear_cuenta(
        username="admin",
        correo="admin@example.com",
        rol_codigo="ADMINISTRADOR",
    ).user

    assert IsAdministrador().has_permission(request, None) is True

    request.user = crear_cuenta(
        username="propietario",
        correo="propietario@example.com",
        rol_codigo="PROPIETARIO",
    ).user
    assert IsAdministrador().has_permission(request, None) is False


@pytest.mark.django_db
def test_permiso_propietario_solo_pasa_para_propietario():
    request = APIRequestFactory().get("/")
    request.user = crear_cuenta(
        username="propietario",
        correo="propietario@example.com",
        rol_codigo="PROPIETARIO",
    ).user

    assert IsPropietario().has_permission(request, None) is True

    request.user = crear_cuenta(
        username="conductor",
        correo="conductor@example.com",
        rol_codigo="CONDUCTOR",
    ).user
    assert IsPropietario().has_permission(request, None) is False


def test_anonimo_no_pasa_permiso_autenticado():
    request = APIRequestFactory().get("/")
    request.user = crear_usuario_anonimo()

    assert IsAuthenticatedUser().has_permission(request, None) is False

