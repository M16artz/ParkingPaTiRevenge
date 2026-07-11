import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from apps.documentos.models import Documento, EstadoDocumento
from apps.usuarios.models import CodigoRol
from tests.factories import crear_cuenta, crear_documento


def auth_header(cuenta):
    access = AccessToken.for_user(cuenta.user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access}"}


def archivo(nombre="cedula.pdf", contenido=b"%PDF-1.4", content_type="application/pdf"):
    return SimpleUploadedFile(nombre, contenido, content_type=content_type)


def multipart_patch(client, url, data, cuenta):
    return client.patch(
        url,
        encode_multipart(BOUNDARY, data),
        content_type=MULTIPART_CONTENT,
        **auth_header(cuenta),
    )


@pytest.mark.django_db
def test_registro_propietario_sigue_funcionando(client):
    response = client.post(
        reverse("auth-register"),
        {
            "nombre": "Dora",
            "apellido": "Propietaria",
            "tipo_identificacion": "CEDULA",
            "identificacion": "1104455667",
            "username": "dora",
            "correo": "dora@example.com",
            "password": "Password123",
            "rol": "PROPIETARIO",
        },
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json()["rol"] == "PROPIETARIO"


@pytest.mark.django_db
@override_settings(MEDIA_ROOT=None)
def test_propietario_sube_documento_pdf_y_queda_pendiente(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    cuenta = crear_cuenta(username="propietario-doc", correo="propietario-doc@example.com")

    response = client.post(
        reverse("documentos-list"),
        {"archivo": archivo()},
        **auth_header(cuenta),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["estado"] == EstadoDocumento.PENDIENTE
    assert payload["es_valido"] is False
    assert payload["nombre_original"] == "cedula.pdf"
    assert Documento.objects.filter(cuenta=cuenta, estado=EstadoDocumento.PENDIENTE).exists()


@pytest.mark.django_db
@override_settings(MEDIA_ROOT=None)
def test_propietario_sube_documento_jpg_y_png(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    cuenta = crear_cuenta(username="propietario-img", correo="propietario-img@example.com")

    jpg = client.post(
        reverse("documentos-list"),
        {"archivo": archivo("cedula.jpg", b"jpg", "image/jpeg")},
        **auth_header(cuenta),
    )
    png = client.post(
        reverse("documentos-list"),
        {"archivo": archivo("cedula.png", b"png", "image/png")},
        **auth_header(cuenta),
    )

    assert jpg.status_code == 201
    assert png.status_code == 201
    assert {item["nombre_original"] for item in (jpg.json(), png.json())} == {"cedula.jpg", "cedula.png"}


@pytest.mark.django_db
@override_settings(MEDIA_ROOT=None)
def test_archivo_invalido_es_rechazado(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    cuenta = crear_cuenta(username="propietario-invalid", correo="propietario-invalid@example.com")

    response = client.post(
        reverse("documentos-list"),
        {"archivo": archivo("malware.exe", b"nope", "application/octet-stream")},
        **auth_header(cuenta),
    )

    assert response.status_code == 400
    assert "pdf, jpg o png" in str(response.json()).lower()


@pytest.mark.django_db
def test_subida_sin_sesion_devuelve_401(client):
    response = client.post(reverse("documentos-list"), {"archivo": archivo()})

    assert response.status_code == 401


@pytest.mark.django_db
@override_settings(MEDIA_ROOT=None)
def test_propietario_lista_solo_documentos_propios(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    cuenta = crear_cuenta(username="propietario-list", correo="propietario-list@example.com")
    otro = crear_cuenta(username="otro-list", correo="otro-list@example.com")
    propio = crear_documento(cuenta=cuenta)
    crear_documento(cuenta=otro)

    response = client.get(reverse("documentos-list"), **auth_header(cuenta))

    assert response.status_code == 200
    ids = [item["id"] for item in response.json()]
    assert ids == [propio.id]


@pytest.mark.django_db
@override_settings(MEDIA_ROOT=None)
def test_propietario_reemplaza_documento_propio_y_vuelve_a_pendiente(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    cuenta = crear_cuenta(username="propietario-replace", correo="propietario-replace@example.com")
    documento = crear_documento(cuenta=cuenta, es_valido=True)

    response = multipart_patch(
        client,
        reverse("documentos-detail", kwargs={"documento_id": documento.id}),
        {"archivo": archivo("nuevo.png", b"png", "image/png")},
        cuenta,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["estado"] == EstadoDocumento.PENDIENTE
    assert payload["es_valido"] is False
    assert payload["nombre_original"] == "nuevo.png"


@pytest.mark.django_db
@override_settings(MEDIA_ROOT=None)
def test_usuario_no_puede_modificar_documento_de_otro(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    cuenta = crear_cuenta(username="propietario-a", correo="propietario-a@example.com")
    otro = crear_cuenta(username="propietario-b", correo="propietario-b@example.com")
    documento = crear_documento(cuenta=otro)

    response = multipart_patch(
        client,
        reverse("documentos-detail", kwargs={"documento_id": documento.id}),
        {"archivo": archivo("nuevo.pdf", b"pdf")},
        cuenta,
    )

    assert response.status_code == 403
    documento.refresh_from_db()
    assert documento.nombre_original == "documento.pdf"


@pytest.mark.django_db
def test_solo_administrador_valida_documento(client):
    admin = crear_cuenta(username="admin-doc", correo="admin-doc@example.com", rol_codigo=CodigoRol.ADMINISTRADOR)
    propietario = crear_cuenta(username="propietario-validate", correo="propietario-validate@example.com")
    documento = crear_documento(cuenta=propietario)

    denied = client.post(
        reverse("documentos-validar", kwargs={"documento_id": documento.id}),
        {"estado": EstadoDocumento.VALIDADO},
        content_type="application/json",
        **auth_header(propietario),
    )
    approved = client.post(
        reverse("documentos-validar", kwargs={"documento_id": documento.id}),
        {"estado": EstadoDocumento.VALIDADO},
        content_type="application/json",
        **auth_header(admin),
    )

    assert denied.status_code == 403
    assert approved.status_code == 200
    assert approved.json()["estado"] == EstadoDocumento.VALIDADO
