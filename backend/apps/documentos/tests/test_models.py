import pytest
from django.db import IntegrityError

from apps.documentos.models import Documento, EstadoDocumento
from tests.factories import crear_cuenta, crear_documento


@pytest.mark.django_db
def test_documento_guarda_metadata_sin_binarios():
    documento = crear_documento(es_valido=False)

    documento.full_clean()

    assert documento.ruta.endswith(".pdf")
    assert documento.file_id == "file-placeholder"
    assert documento.estado == EstadoDocumento.PENDIENTE


@pytest.mark.django_db
def test_solo_un_documento_valido_por_cuenta():
    cuenta = crear_cuenta()
    crear_documento(cuenta=cuenta, es_valido=True)

    with pytest.raises(IntegrityError):
        Documento.objects.create(
            cuenta=cuenta,
            es_valido=True,
            estado=EstadoDocumento.VALIDADO,
            fecha_expiracion="2027-01-01",
            ruta="documentos/otro.pdf",
            file_id="otro-file",
        )
