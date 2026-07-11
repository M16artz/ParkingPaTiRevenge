import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from apps.common.exceptions import DomainValidationError
from apps.documentos.validators import validar_archivo_documento


@pytest.mark.parametrize(
    ("nombre", "content_type"),
    [
        ("cedula.pdf", "application/pdf"),
        ("cedula.jpg", "image/jpeg"),
        ("cedula.jpeg", "image/jpeg"),
        ("cedula.png", "image/png"),
    ],
)
def test_validador_acepta_pdf_jpg_png(nombre, content_type):
    archivo = SimpleUploadedFile(nombre, b"contenido", content_type=content_type)

    extension = validar_archivo_documento(archivo)

    assert extension in {"pdf", "jpg", "jpeg", "png"}


def test_validador_rechaza_extension_invalida():
    archivo = SimpleUploadedFile("cedula.exe", b"contenido", content_type="application/octet-stream")

    with pytest.raises(DomainValidationError) as exc:
        validar_archivo_documento(archivo)

    assert "pdf, jpg o png" in str(exc.value).lower()


@override_settings(DOCUMENTOS_MAX_UPLOAD_BYTES=4)
def test_validador_rechaza_tamano_excesivo():
    archivo = SimpleUploadedFile("cedula.pdf", b"contenido-largo", content_type="application/pdf")

    with pytest.raises(DomainValidationError) as exc:
        validar_archivo_documento(archivo)

    assert "tamano maximo" in str(exc.value).lower()

