from pathlib import Path

from django.conf import settings

from apps.common.exceptions import DomainValidationError


def validar_archivo_documento(archivo):
    if not archivo:
        raise DomainValidationError("Debes seleccionar un documento PDF, JPG o PNG para continuar.")

    extension = Path(archivo.name or "").suffix.lower().lstrip(".")
    permitidas = {item.lower() for item in settings.DOCUMENTOS_ALLOWED_EXTENSIONS}
    if extension not in permitidas:
        raise DomainValidationError("El documento debe ser PDF, JPG o PNG. Selecciona un archivo valido.")

    if archivo.size > settings.DOCUMENTOS_MAX_UPLOAD_BYTES:
        max_mb = settings.DOCUMENTOS_MAX_UPLOAD_BYTES / (1024 * 1024)
        raise DomainValidationError(f"El documento supera el tamano maximo de {max_mb:.0f} MB. Reduce el archivo e intenta nuevamente.")

    return extension

