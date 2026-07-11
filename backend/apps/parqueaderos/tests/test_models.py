from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.parqueaderos.models import Parqueadero, Ubicacion
from tests.factories import crear_parqueadero


@pytest.mark.django_db
def test_ubicacion_valida_rangos_de_coordenadas():
    ubicacion = Ubicacion(latitud=Decimal("100.0"), longitud=Decimal("-79.2"))

    with pytest.raises(ValidationError):
        ubicacion.full_clean()


@pytest.mark.django_db
def test_parqueadero_tiene_indices_de_busqueda_base():
    index_fields = {tuple(index.fields) for index in Parqueadero._meta.indexes}

    assert ("estado",) in index_fields
    assert ("validado",) in index_fields
    assert ("disponibilidad",) in index_fields
    assert ("estado", "validado", "disponibilidad") in index_fields


@pytest.mark.django_db
def test_parqueadero_configuracion_minima_es_valida():
    parqueadero = crear_parqueadero()

    parqueadero.full_clean()

    assert parqueadero.validado is False
    assert parqueadero.estado == "INACTIVO"
    assert parqueadero.disponibilidad == "CERRADO"

