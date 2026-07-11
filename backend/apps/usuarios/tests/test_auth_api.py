from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.usuarios.models import CodigoRol, Cuenta, Rol
from tests.factories import crear_cuenta


@pytest.mark.django_db
def test_registro_crea_cuenta_base_sin_exponer_password(client):
    response = client.post(
        reverse("auth-register"),
        {
            "nombre": "Maria",
            "apellido": "Loja",
            "tipo_identificacion": "CEDULA",
            "identificacion": "1101122334",
            "username": "maria",
            "correo": "maria@example.com",
            "password": "Password123",
            "rol": "PROPIETARIO",
        },
        content_type="application/json",
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["username"] == "maria"
    assert payload["rol"] == "PROPIETARIO"
    assert "password_hash" not in payload
    cuenta = Cuenta.objects.get(username="maria")
    assert cuenta.user is not None
    assert cuenta.password_hash != "Password123"


@pytest.mark.django_db
def test_registro_publico_no_permite_administrador(client):
    response = client.post(
        reverse("auth-register"),
        {
            "nombre": "Admin",
            "apellido": "Nope",
            "tipo_identificacion": "CEDULA",
            "identificacion": "1101122335",
            "username": "admin-publico",
            "correo": "admin-publico@example.com",
            "password": "Password123",
            "rol": "ADMINISTRADOR",
        },
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "administradora" in str(response.json()).lower()


@pytest.mark.django_db
def test_login_jwt_devuelve_tokens_y_rol(client):
    crear_cuenta(username="propietario", correo="propietario@example.com", password="Password123")

    response = client.post(
        reverse("auth-token"),
        {"username": "propietario", "password": "Password123"},
        content_type="application/json",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["access"]
    assert payload["refresh"]
    assert payload["cuenta"]["rol"] == "PROPIETARIO"


@pytest.mark.django_db
def test_login_jwt_rechaza_credenciales_invalidas(client):
    crear_cuenta(username="propietario", correo="propietario@example.com", password="Password123")

    response = client.post(
        reverse("auth-token"),
        {"username": "propietario", "password": "Incorrecta123"},
        content_type="application/json",
    )

    assert response.status_code == 401
    assert "credenciales invalidas" in response.json()["detail"].lower()


@pytest.mark.django_db
def test_refresh_token_devuelve_access_nuevo(client):
    cuenta = crear_cuenta(username="propietario", correo="propietario@example.com")
    refresh = RefreshToken.for_user(cuenta.user)

    response = client.post(reverse("auth-refresh"), {"refresh": str(refresh)}, content_type="application/json")

    assert response.status_code == 200
    assert response.json()["access"]


@pytest.mark.django_db
def test_refresh_token_invalido_falla_seguro(client):
    response = client.post(reverse("auth-refresh"), {"refresh": "token-invalido"}, content_type="application/json")

    assert response.status_code == 401
    assert "inicia sesion" in response.json()["detail"].lower()


@pytest.mark.django_db
def test_me_requiere_token(client):
    response = client.get(reverse("cuenta-me"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_me_devuelve_perfil_autenticado(client):
    cuenta = crear_cuenta(username="propietario", correo="propietario@example.com")
    access = AccessToken.for_user(cuenta.user)

    response = client.get(reverse("cuenta-me"), HTTP_AUTHORIZATION=f"Bearer {access}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["username"] == "propietario"
    assert payload["rol"] == "PROPIETARIO"
    assert "password_hash" not in payload


@pytest.mark.django_db
def test_token_expirado_no_permite_acceder_a_me(client):
    cuenta = crear_cuenta(username="propietario", correo="propietario@example.com")
    access = AccessToken.for_user(cuenta.user)
    access.set_exp(from_time=access.current_time - timedelta(minutes=20), lifetime=timedelta(minutes=1))

    response = client.get(reverse("cuenta-me"), HTTP_AUTHORIZATION=f"Bearer {access}")

    assert response.status_code == 401


@pytest.mark.django_db
def test_login_acepta_correo_como_identificador(client):
    crear_cuenta(username="propietario", correo="propietario@example.com", password="Password123")

    response = client.post(
        reverse("auth-token"),
        {"username": "propietario@example.com", "password": "Password123"},
        content_type="application/json",
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_registro_crea_rol_conductor_por_defecto(client):
    response = client.post(
        reverse("auth-register"),
        {
            "nombre": "Condu",
            "apellido": "Ctor",
            "tipo_identificacion": "CEDULA",
            "identificacion": "1101122336",
            "username": "conductor",
            "correo": "conductor@example.com",
            "password": "Password123",
        },
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json()["rol"] == "CONDUCTOR"
    assert Rol.objects.filter(codigo=CodigoRol.CONDUCTOR).exists()

