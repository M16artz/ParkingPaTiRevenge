from apps.common.services import BaseService
from apps.tarifas.models import CategoriaTarifa
from apps.tarifas.repositories import CategoriaTarifaRepository


class CategoriaTarifaService(BaseService):
    repository = CategoriaTarifaRepository()

    def preparar_categoria(self, **data):
        return self.validate(CategoriaTarifa(**data))

