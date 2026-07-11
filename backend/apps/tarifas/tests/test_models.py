from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.tarifas.models import CategoriaTarifa, TipoCategoriaTarifa
from tests.factories import crear_categoria_tarifa, crear_parqueadero


@pytest.mark.django_db
def test_categoria_tarifa_es_unica_por_parqueadero_y_codigo():
    parqueadero = crear_parqueadero()
    crear_categoria_tarifa(parqueadero=parqueadero, codigo=TipoCategoriaTarifa.GENERAL)

    with pytest.raises(IntegrityError):
        CategoriaTarifa.objects.create(
            parqueadero=parqueadero,
            codigo=TipoCategoriaTarifa.GENERAL,
            precio_hora=Decimal("2.00"),
        )


@pytest.mark.django_db
def test_categoria_tarifa_valida_precio_positivo_y_catalogo():
    tarifa = CategoriaTarifa(
        parqueadero=crear_parqueadero(),
        codigo=TipoCategoriaTarifa.PESADOS,
        precio_hora=Decimal("0.00"),
    )

    with pytest.raises(ValidationError):
        tarifa.full_clean()

    codigos = {choice[0] for choice in TipoCategoriaTarifa.choices}
    assert {"GENERAL", "PREFERENCIAL", "PESADOS"}.issubset(codigos)

