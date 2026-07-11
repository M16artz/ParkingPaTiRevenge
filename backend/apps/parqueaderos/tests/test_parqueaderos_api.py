import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from apps.parqueaderos.models import DisponibilidadParqueadero, Parqueadero
from apps.usuarios.models import CodigoRol
from tests.factories import crear_cuenta, crear_parqueadero


def auth_header(cuenta):
    access = AccessToken.for_user(cuenta.user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access}"}


def parqueadero_payload(nombre="Parking Nuevo", disponibilidad=DisponibilidadParqueadero.CERRADO):
    return {
        "nombre": nombre,
        "disponibilidad": disponibilidad,
        "direccion": {
            "calle_principal": "Bolivar",
            "calle_secundaria": "Rocafuerte",
            "nro_lote": "12-34",
        },
        "ubicacion": {
            "latitud": "-3.993130",
            "longitud": "-79.204220",
        },
    }


@pytest.mark.django_db
def test_propietario_autenticado_crea_parqueadero(client):
    propietario = crear_cuenta(username="owner-create", correo="owner-create@example.com")

    response = client.post(
        reverse("parqueaderos-list"),
        parqueadero_payload(disponibilidad=DisponibilidadParqueadero.DISPONIBLE),
        content_type="application/json",
        **auth_header(propietario),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["nombre"] == "Parking Nuevo"
    assert payload["propietario"] == propietario.id
    assert payload["validado"] is False
    assert payload["disponibilidad"] == DisponibilidadParqueadero.DISPONIBLE
    assert payload["direccion"]["calle_principal"] == "Bolivar"
    assert Parqueadero.objects.filter(propietario=propietario, nombre="Parking Nuevo").exists()


@pytest.mark.django_db
def test_usuario_anonimo_no_puede_modificar_parqueaderos(client):
    parqueadero = crear_parqueadero()

    create = client.post(reverse("parqueaderos-list"), parqueadero_payload(), content_type="application/json")
    edit = client.patch(
        reverse("parqueaderos-detail", kwargs={"parqueadero_id": parqueadero.id}),
        {"nombre": "Nope"},
        content_type="application/json",
    )
    state = client.patch(
        reverse("parqueaderos-estado", kwargs={"parqueadero_id": parqueadero.id}),
        {"disponibilidad": DisponibilidadParqueadero.LLENO},
        content_type="application/json",
    )

    assert create.status_code == 401
    assert edit.status_code == 401
    assert state.status_code == 401


@pytest.mark.django_db
def test_conductor_no_puede_crear_parqueadero(client):
    conductor = crear_cuenta(
        username="driver-parking",
        correo="driver-parking@example.com",
        rol_codigo=CodigoRol.CONDUCTOR,
    )

    response = client.post(
        reverse("parqueaderos-list"),
        parqueadero_payload(),
        content_type="application/json",
        **auth_header(conductor),
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_endpoint_mios_lista_solo_parqueaderos_del_propietario(client):
    propietario = crear_cuenta(username="owner-list", correo="owner-list@example.com")
    otro = crear_cuenta(username="owner-other", correo="owner-other@example.com")
    propio = crear_parqueadero(nombre="Propio", propietario=propietario)
    crear_parqueadero(nombre="Ajeno", propietario=otro)

    response = client.get(reverse("parqueaderos-mios"), **auth_header(propietario))

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [propio.id]


@pytest.mark.django_db
def test_administrador_puede_consultar_parqueaderos(client):
    admin = crear_cuenta(username="admin-parking", correo="admin-parking@example.com", rol_codigo=CodigoRol.ADMINISTRADOR)
    crear_parqueadero(nombre="Uno")
    crear_parqueadero(nombre="Dos", propietario=crear_cuenta(username="owner-dos", correo="owner-dos@example.com"))

    response = client.get(reverse("parqueaderos-list"), **auth_header(admin))

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.django_db
def test_propietario_edita_datos_generales_de_su_parqueadero(client):
    propietario = crear_cuenta(username="owner-edit", correo="owner-edit@example.com")
    parqueadero = crear_parqueadero(propietario=propietario)

    response = client.patch(
        reverse("parqueaderos-detail", kwargs={"parqueadero_id": parqueadero.id}),
        {
            "nombre": "Parking Editado",
            "direccion": {"calle_principal": "Sucre", "calle_secundaria": "", "nro_lote": "8"},
            "ubicacion": {"latitud": "-4.000000", "longitud": "-79.100000"},
        },
        content_type="application/json",
        **auth_header(propietario),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["nombre"] == "Parking Editado"
    assert payload["direccion"]["calle_principal"] == "Sucre"
    assert payload["ubicacion"]["latitud"] == "-4.000000"


@pytest.mark.django_db
def test_propietario_no_modifica_parqueadero_de_otro(client):
    propietario = crear_cuenta(username="owner-a", correo="owner-a@example.com")
    otro = crear_cuenta(username="owner-b", correo="owner-b@example.com")
    parqueadero = crear_parqueadero(nombre="Ajeno", propietario=otro)

    response = client.patch(
        reverse("parqueaderos-detail", kwargs={"parqueadero_id": parqueadero.id}),
        {"nombre": "Intruso"},
        content_type="application/json",
        **auth_header(propietario),
    )

    assert response.status_code == 403
    parqueadero.refresh_from_db()
    assert parqueadero.nombre == "Ajeno"


@pytest.mark.django_db
def test_propietario_cambia_estado_general_de_su_parqueadero(client):
    propietario = crear_cuenta(username="owner-state", correo="owner-state@example.com")
    parqueadero = crear_parqueadero(propietario=propietario)

    response = client.patch(
        reverse("parqueaderos-estado", kwargs={"parqueadero_id": parqueadero.id}),
        {"disponibilidad": DisponibilidadParqueadero.LLENO},
        content_type="application/json",
        **auth_header(propietario),
    )

    assert response.status_code == 200
    assert response.json()["disponibilidad"] == DisponibilidadParqueadero.LLENO


@pytest.mark.django_db
def test_estado_general_invalido_es_rechazado(client):
    propietario = crear_cuenta(username="owner-invalid-state", correo="owner-invalid-state@example.com")
    parqueadero = crear_parqueadero(propietario=propietario)

    response = client.patch(
        reverse("parqueaderos-estado", kwargs={"parqueadero_id": parqueadero.id}),
        {"disponibilidad": "ABIERTO"},
        content_type="application/json",
        **auth_header(propietario),
    )

    assert response.status_code == 400
    assert "abierto, cerrado o lleno" in str(response.json()).lower()


@pytest.mark.django_db
def test_coordenadas_invalidas_devuelven_400(client):
    propietario = crear_cuenta(username="owner-coords", correo="owner-coords@example.com")
    payload = parqueadero_payload()
    payload["ubicacion"]["latitud"] = "100.000000"

    response = client.post(
        reverse("parqueaderos-list"),
        payload,
        content_type="application/json",
        **auth_header(propietario),
    )

    assert response.status_code == 400
    assert "revisa" in response.json()["detail"].lower()
