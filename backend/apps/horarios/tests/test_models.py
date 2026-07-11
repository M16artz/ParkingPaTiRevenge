from datetime import time

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.horarios.models import DiaSemana, HorarioAtencion
from tests.factories import crear_horario, crear_parqueadero


@pytest.mark.django_db
def test_horario_es_unico_por_parqueadero_y_dia():
    parqueadero = crear_parqueadero()
    crear_horario(parqueadero=parqueadero, dia=DiaSemana.LUNES)

    with pytest.raises(IntegrityError):
        HorarioAtencion.objects.create(
            parqueadero=parqueadero,
            dia=DiaSemana.LUNES,
            hora_apertura=time(9, 0),
            hora_cierre=time(17, 0),
        )


@pytest.mark.django_db
def test_horario_valida_apertura_anterior_a_cierre():
    horario = HorarioAtencion(
        parqueadero=crear_parqueadero(),
        dia=DiaSemana.MARTES,
        hora_apertura=time(18, 0),
        hora_cierre=time(8, 0),
    )

    with pytest.raises(ValidationError):
        horario.full_clean()

