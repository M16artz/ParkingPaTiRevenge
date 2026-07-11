from apps.common.repositories import BaseRepository
from apps.tarifas.models import CategoriaTarifa


class CategoriaTarifaRepository(BaseRepository):
    model = CategoriaTarifa

    def filter_by_parqueadero(self, parqueadero):
        return self.model.objects.filter(parqueadero=parqueadero)

    def get_by_codigo(self, parqueadero, codigo):
        return self.model.objects.filter(parqueadero=parqueadero, codigo=codigo).first()

