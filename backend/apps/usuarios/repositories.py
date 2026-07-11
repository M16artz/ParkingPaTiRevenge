from apps.common.repositories import BaseRepository
from apps.usuarios.models import Cuenta, Persona, Rol


class PersonaRepository(BaseRepository):
    model = Persona

    def get_by_identificacion(self, identificacion):
        return self.model.objects.filter(identificacion=identificacion).first()


class RolRepository(BaseRepository):
    model = Rol

    def get_by_codigo(self, codigo):
        return self.model.objects.filter(codigo=codigo).first()


class CuentaRepository(BaseRepository):
    model = Cuenta

    def get_by_username_or_correo(self, value):
        return self.model.objects.filter(username=value).first() or self.model.objects.filter(correo=value).first()

    def get_by_user(self, user):
        return self.model.objects.select_related("persona", "rol").filter(user=user).first()

    def filter_by_rol(self, rol_codigo):
        return self.model.objects.filter(rol__codigo=rol_codigo)

    def filter_by_estado(self, estado):
        return self.model.objects.filter(estado=estado)
