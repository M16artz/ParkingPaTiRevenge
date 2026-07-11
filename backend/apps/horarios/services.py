from apps.common.services import BaseService
from apps.horarios.models import HorarioAtencion
from apps.horarios.repositories import HorarioAtencionRepository


class HorarioAtencionService(BaseService):
    repository = HorarioAtencionRepository()

    def preparar_horario(self, **data):
        return self.validate(HorarioAtencion(**data))

