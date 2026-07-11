from apps.common.repositories import BaseRepository
from apps.espacios.models import Espacio


class EspacioRepository(BaseRepository):
    model = Espacio

    def filter_by_parqueadero(self, parqueadero):
        return self.model.objects.filter(parqueadero=parqueadero)

    def filter_by_estado(self, parqueadero, estado):
        return self.model.objects.filter(parqueadero=parqueadero, estado=estado)

    def get_by_numero(self, parqueadero, numero_espacio):
        return self.model.objects.filter(parqueadero=parqueadero, numero_espacio=numero_espacio).first()

