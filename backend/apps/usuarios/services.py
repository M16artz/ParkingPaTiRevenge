from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.exceptions import DomainValidationError
from apps.common.services import BaseService
from apps.usuarios.models import CodigoRol, Cuenta, Persona, Rol
from apps.usuarios.repositories import CuentaRepository, PersonaRepository, RolRepository


class PersonaService(BaseService):
    repository = PersonaRepository()

    def crear_persona(self, **data):
        persona = Persona(**data)
        return self.validate(persona)


class RolService(BaseService):
    repository = RolRepository()

    def obtener_o_crear_rol(self, codigo):
        rol = self.repository.get_by_codigo(codigo)
        if rol:
            return rol
        rol = Rol(codigo=codigo)
        return self.validate(rol)


class CuentaService(BaseService):
    repository = CuentaRepository()

    def preparar_cuenta(self, **data):
        if self.repository.get_by_username_or_correo(data.get("username")):
            raise DomainValidationError("El nombre de usuario ya existe. Usa otro nombre.")
        if self.repository.get_by_username_or_correo(data.get("correo")):
            raise DomainValidationError("El correo ya existe. Usa otro correo.")
        cuenta = Cuenta(**data)
        return self.validate(cuenta)


class AuthService(BaseService):
    cuenta_repository = CuentaRepository()
    persona_repository = PersonaRepository()
    rol_repository = RolRepository()

    @transaction.atomic
    def registrar_cuenta(self, data):
        rol_codigo = data.get("rol", CodigoRol.CONDUCTOR)
        if rol_codigo == CodigoRol.ADMINISTRADOR:
            raise DomainValidationError("No puedes registrar una cuenta administradora desde este formulario.")

        if self.persona_repository.get_by_identificacion(data["identificacion"]):
            raise DomainValidationError("La identificacion ya esta registrada. Usa otra identificacion.")
        if self.cuenta_repository.get_by_username_or_correo(data["username"]):
            raise DomainValidationError("El nombre de usuario ya esta registrado. Usa otro nombre.")
        if self.cuenta_repository.get_by_username_or_correo(data["correo"]):
            raise DomainValidationError("El correo ya esta registrado. Usa otro correo.")

        rol, _ = Rol.objects.get_or_create(codigo=rol_codigo)
        persona = Persona.objects.create(
            nombre=data["nombre"],
            apellido=data["apellido"],
            tipo_identificacion=data["tipo_identificacion"],
            identificacion=data["identificacion"],
        )
        user = User.objects.create_user(
            username=data["username"],
            email=data["correo"],
            password=data["password"],
        )
        cuenta = Cuenta.objects.create(
            user=user,
            persona=persona,
            username=data["username"],
            correo=data["correo"],
            rol=rol,
            password_hash=make_password(data["password"]),
        )
        return cuenta

    def login(self, username, password):
        cuenta = self.cuenta_repository.get_by_username_or_correo(username)
        if not cuenta or not cuenta.user or not check_password(password, cuenta.password_hash):
            raise DomainValidationError(
                "Credenciales invalidas. Revisa tu usuario y contrasena e intenta nuevamente."
            )
        if not cuenta.user.is_active:
            raise DomainValidationError("La cuenta esta inactiva. Contacta al administrador.")

        refresh = RefreshToken.for_user(cuenta.user)
        refresh["cuenta_id"] = cuenta.id
        refresh["rol"] = cuenta.rol.codigo
        access = refresh.access_token
        access["cuenta_id"] = cuenta.id
        access["rol"] = cuenta.rol.codigo
        return {
            "access": str(access),
            "refresh": str(refresh),
            "cuenta": cuenta,
        }

    def perfil_desde_user(self, user):
        cuenta = self.cuenta_repository.get_by_user(user)
        if not cuenta:
            raise DomainValidationError("No existe un perfil asociado a esta sesion. Vuelve a iniciar sesion.")
        return cuenta
