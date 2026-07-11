from apps.common.services import BaseService
from apps.espacios.models import Espacio
from apps.espacios.repositories import EspacioRepository


class EspacioService(BaseService):
    repository = EspacioRepository()

    def preparar_espacio(self, **data):
        return self.validate(Espacio(**data))

    def preparar_cambio_estado(self, espacio, nuevo_estado):
        espacio.estado = nuevo_estado
        return self.validate(espacio)

