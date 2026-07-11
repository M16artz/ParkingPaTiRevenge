from django.db import transaction

from apps.common.exceptions import DomainValidationError
from apps.common.services import BaseService
from apps.documentos.models import Documento, EstadoDocumento
from apps.documentos.repositories import DocumentoRepository
from apps.documentos.storage import DocumentoStorage
from apps.documentos.validators import validar_archivo_documento


class DocumentoService(BaseService):
    repository = DocumentoRepository()
    storage = DocumentoStorage()

    def preparar_documento(self, **data):
        return self.validate(Documento(**data))

    @transaction.atomic
    def subir_documento(self, cuenta, archivo):
        extension = validar_archivo_documento(archivo)
        metadata = self.storage.guardar(cuenta, archivo, extension)
        documento = Documento(
            cuenta=cuenta,
            estado=EstadoDocumento.PENDIENTE,
            es_valido=False,
            motivo_rechazo="",
            **metadata,
        )
        self.validate(documento)
        documento.save()
        return documento

    @transaction.atomic
    def reemplazar_documento(self, cuenta, documento_id, archivo):
        documento = self.repository.get_by_id_for_cuenta(documento_id, cuenta)
        if documento is None:
            raise DomainValidationError("No se encontro el documento o no tienes permiso para modificarlo.")

        extension = validar_archivo_documento(archivo)
        metadata = self.storage.guardar(cuenta, archivo, extension)
        for field, value in metadata.items():
            setattr(documento, field, value)
        documento.estado = EstadoDocumento.PENDIENTE
        documento.es_valido = False
        documento.motivo_rechazo = ""
        self.validate(documento)
        documento.save()
        return documento

    def listar_propios(self, cuenta):
        return self.repository.filter_by_cuenta(cuenta)

    def listar_pendientes(self):
        return self.repository.get_pending()

    def validar_documento(self, documento_id, estado, motivo_rechazo=""):
        documento = self.repository.get_by_id(documento_id)
        if documento is None:
            raise DomainValidationError("No se encontro el documento solicitado.")
        if estado not in {EstadoDocumento.VALIDADO, EstadoDocumento.RECHAZADO}:
            raise DomainValidationError("Debes aprobar o rechazar el documento.")
        documento.estado = estado
        documento.es_valido = estado == EstadoDocumento.VALIDADO
        documento.motivo_rechazo = "" if documento.es_valido else motivo_rechazo.strip()
        documento.save(update_fields=["estado", "es_valido", "motivo_rechazo", "fecha_actualizacion"])
        return documento
