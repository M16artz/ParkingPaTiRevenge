from rest_framework.permissions import BasePermission, IsAuthenticated

from apps.usuarios.models import CodigoRol


class IsAuthenticatedUser(IsAuthenticated):
    message = "Debes iniciar sesion para continuar."


class IsAdministrador(BasePermission):
    message = "No tienes permisos de administrador para realizar esta accion."

    def has_permission(self, request, view):
        cuenta = get_request_cuenta(request)
        return bool(request.user and request.user.is_authenticated and cuenta and cuenta.rol.codigo == CodigoRol.ADMINISTRADOR)


class IsPropietarioDelRecurso(BasePermission):
    message = "Solo el propietario del recurso puede realizar esta accion."

    def has_object_permission(self, request, view, obj):
        cuenta = get_request_cuenta(request)
        propietario = getattr(obj, "propietario", None)
        if propietario is None and hasattr(obj, "parqueadero"):
            propietario = getattr(obj.parqueadero, "propietario", None)
        return bool(request.user and request.user.is_authenticated and cuenta and propietario == cuenta)


class IsPropietario(BasePermission):
    message = "Debes tener rol propietario para realizar esta accion."

    def has_permission(self, request, view):
        cuenta = get_request_cuenta(request)
        return bool(request.user and request.user.is_authenticated and cuenta and cuenta.rol.codigo == CodigoRol.PROPIETARIO)


class IsConductorOAutenticado(BasePermission):
    message = "Debes iniciar sesion para realizar esta accion."

    def has_permission(self, request, view):
        cuenta = get_request_cuenta(request)
        return bool(request.user and request.user.is_authenticated and cuenta)


def get_request_cuenta(request):
    return getattr(request.user, "cuenta_perfil", None) or getattr(request.user, "cuenta", None)
