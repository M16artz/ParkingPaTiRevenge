from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class DocumentoStorage:
    def guardar(self, cuenta, archivo, extension):
        storage = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
        relative_path = Path(settings.DOCUMENTOS_LOCAL_SUBDIR) / str(cuenta.id) / f"{uuid4().hex}.{extension}"
        saved_name = storage.save(str(relative_path).replace("\\", "/"), archivo)
        return {
            "ruta": storage.url(saved_name),
            "file_id": saved_name,
            "nombre_original": archivo.name,
            "content_type": getattr(archivo, "content_type", "") or "application/octet-stream",
            "tamano_bytes": archivo.size,
        }

