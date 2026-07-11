from rest_framework.permissions import BasePermission

from apps.usuarios.models import CodigoRol
from apps.usuarios.permissions import get_request_cuenta


class IsPropietarioCuenta(BasePermission):
    message = "Debes tener rol propietario para gestionar documentos."

    def has_permission(self, request, view):
        cuenta = get_request_cuenta(request)
        return bool(request.user and request.user.is_authenticated and cuenta and cuenta.rol.codigo == CodigoRol.PROPIETARIO)


class IsAdministradorCuenta(BasePermission):
    message = "Debes tener rol administrador para validar documentos."

    def has_permission(self, request, view):
        cuenta = get_request_cuenta(request)
        return bool(request.user and request.user.is_authenticated and cuenta and cuenta.rol.codigo == CodigoRol.ADMINISTRADOR)

