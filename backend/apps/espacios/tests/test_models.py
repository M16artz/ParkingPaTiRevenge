import pytest
from django.db import IntegrityError

from apps.espacios.models import Espacio, EstadoEspacio
from tests.factories import crear_espacio, crear_parqueadero


@pytest.mark.django_db
def test_espacio_es_unico_por_parqueadero_y_numero():
    parqueadero = crear_parqueadero()
    crear_espacio(parqueadero=parqueadero, numero_espacio="A-01")

    with pytest.raises(IntegrityError):
        Espacio.objects.create(parqueadero=parqueadero, numero_espacio="A-01")


@pytest.mark.django_db
def test_espacio_tiene_catalogo_de_estados_e_indice_compuesto():
    codigos = {choice[0] for choice in EstadoEspacio.choices}
    index_fields = {tuple(index.fields) for index in Espacio._meta.indexes}

    assert {"LIBRE", "OCUPADO", "INACTIVO", "MANTENIMIENTO"}.issubset(codigos)
    assert ("parqueadero", "estado") in index_fields

