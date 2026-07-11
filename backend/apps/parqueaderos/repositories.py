from apps.common.repositories import BaseRepository
from apps.parqueaderos.models import Parqueadero


class ParqueaderoRepository(BaseRepository):
    model = Parqueadero

    def filter_by_propietario(self, cuenta):
        return self.model.objects.filter(propietario=cuenta).select_related("direccion", "ubicacion", "propietario").order_by("-fecha_creacion")

    def get_by_id_for_propietario(self, parqueadero_id, cuenta):
        return self.model.objects.select_related("direccion", "ubicacion", "propietario").filter(id=parqueadero_id, propietario=cuenta).first()

    def all_for_admin(self):
        return self.model.objects.select_related("direccion", "ubicacion", "propietario").order_by("-fecha_creacion")

    def filter_by_estado(self, estado):
        return self.model.objects.filter(estado=estado)

    def filter_by_validado(self, validado=True):
        return self.model.objects.filter(validado=validado)

    def filter_by_disponibilidad(self, disponibilidad):
        return self.model.objects.filter(disponibilidad=disponibilidad)
