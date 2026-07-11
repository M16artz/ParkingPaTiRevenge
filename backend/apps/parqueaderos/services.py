from django.db import transaction

from apps.common.exceptions import DomainValidationError
from apps.common.services import BaseService
from apps.parqueaderos.models import Direccion, Parqueadero, Ubicacion
from apps.parqueaderos.repositories import ParqueaderoRepository


class ParqueaderoService(BaseService):
    repository = ParqueaderoRepository()

    def preparar_direccion(self, **data):
        return self.validate(Direccion(**data))

    def preparar_ubicacion(self, **data):
        return self.validate(Ubicacion(**data))

    def preparar_parqueadero(self, **data):
        return self.validate(Parqueadero(**data))

    def listar_mios(self, propietario):
        return self.repository.filter_by_propietario(propietario)

    def listar_para_admin(self):
        return self.repository.all_for_admin()

    @transaction.atomic
    def crear(self, propietario, data):
        direccion = self.preparar_direccion(**data["direccion"])
        ubicacion = self.preparar_ubicacion(**data["ubicacion"])
        direccion.save()
        ubicacion.save()
        parqueadero = self.preparar_parqueadero(
            propietario=propietario,
            nombre=data["nombre"],
            disponibilidad=data.get("disponibilidad"),
            direccion=direccion,
            ubicacion=ubicacion,
        )
        parqueadero.save()
        return parqueadero

    @transaction.atomic
    def editar_general(self, propietario, parqueadero_id, data):
        parqueadero = self.repository.get_by_id_for_propietario(parqueadero_id, propietario)
        if parqueadero is None:
            raise DomainValidationError("No se encontro el parqueadero o no tienes permiso para modificarlo.")

        if "nombre" in data:
            parqueadero.nombre = data["nombre"]
        if "disponibilidad" in data:
            parqueadero.disponibilidad = data["disponibilidad"]
        if "direccion" in data:
            for field, value in data["direccion"].items():
                setattr(parqueadero.direccion, field, value)
            self.validate(parqueadero.direccion)
            parqueadero.direccion.save()
        if "ubicacion" in data:
            for field, value in data["ubicacion"].items():
                setattr(parqueadero.ubicacion, field, value)
            self.validate(parqueadero.ubicacion)
            parqueadero.ubicacion.save()

        self.validate(parqueadero)
        parqueadero.save()
        return parqueadero

    def cambiar_estado_general(self, propietario, parqueadero_id, disponibilidad):
        parqueadero = self.repository.get_by_id_for_propietario(parqueadero_id, propietario)
        if parqueadero is None:
            raise DomainValidationError("No se encontro el parqueadero o no tienes permiso para cambiar su estado.")
        parqueadero.disponibilidad = disponibilidad
        self.validate(parqueadero)
        parqueadero.save(update_fields=["disponibilidad", "fecha_actualizacion"])
        return parqueadero
