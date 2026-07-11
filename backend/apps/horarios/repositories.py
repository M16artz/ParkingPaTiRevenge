from apps.common.repositories import BaseRepository
from apps.horarios.models import HorarioAtencion


class HorarioAtencionRepository(BaseRepository):
    model = HorarioAtencion

    def filter_by_parqueadero(self, parqueadero):
        return self.model.objects.filter(parqueadero=parqueadero)

    def get_by_dia(self, parqueadero, dia):
        return self.model.objects.filter(parqueadero=parqueadero, dia=dia).first()

