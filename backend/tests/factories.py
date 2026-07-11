from datetime import date, time
from decimal import Decimal

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.hashers import make_password

from apps.documentos.models import Documento, EstadoDocumento
from apps.espacios.models import Espacio
from apps.horarios.models import DiaSemana, HorarioAtencion
from apps.parqueaderos.models import Direccion, Parqueadero, Ubicacion
from apps.tarifas.models import CategoriaTarifa, TipoCategoriaTarifa
from apps.usuarios.models import CodigoRol, Cuenta, Persona, Rol, TipoIdentificacion


def crear_rol(codigo=CodigoRol.PROPIETARIO):
    return Rol.objects.create(codigo=codigo)


def crear_persona(identificacion="1100000001"):
    return Persona.objects.create(
        nombre="Ada",
        apellido="Lovelace",
        tipo_identificacion=TipoIdentificacion.CEDULA,
        identificacion=identificacion,
    )


def crear_cuenta(
    username="propietario",
    correo="propietario@example.com",
    rol_codigo=CodigoRol.PROPIETARIO,
    password="Password123",
):
    persona = crear_persona(identificacion=f"ID-{username}")
    rol, _ = Rol.objects.get_or_create(codigo=rol_codigo)
    user = User.objects.create_user(username=username, email=correo, password=password)
    return Cuenta.objects.create(
        user=user,
        persona=persona,
        username=username,
        correo=correo,
        rol=rol,
        password_hash=make_password(password),
    )


def crear_usuario_anonimo():
    return AnonymousUser()


def crear_parqueadero(nombre="Parking Centro", propietario=None):
    propietario = propietario or crear_cuenta()
    direccion = Direccion.objects.create(calle_principal="Bolivar", calle_secundaria="Rocafuerte", nro_lote="12")
    ubicacion = Ubicacion.objects.create(latitud=Decimal("-3.993130"), longitud=Decimal("-79.204220"))
    return Parqueadero.objects.create(
        propietario=propietario,
        nombre=nombre,
        direccion=direccion,
        ubicacion=ubicacion,
    )


def crear_espacio(parqueadero=None, numero_espacio="A-01"):
    return Espacio.objects.create(parqueadero=parqueadero or crear_parqueadero(), numero_espacio=numero_espacio)


def crear_horario(parqueadero=None, dia=DiaSemana.LUNES):
    return HorarioAtencion.objects.create(
        parqueadero=parqueadero or crear_parqueadero(),
        dia=dia,
        hora_apertura=time(8, 0),
        hora_cierre=time(18, 0),
    )


def crear_categoria_tarifa(parqueadero=None, codigo=TipoCategoriaTarifa.GENERAL):
    return CategoriaTarifa.objects.create(
        parqueadero=parqueadero or crear_parqueadero(),
        codigo=codigo,
        precio_hora=Decimal("1.50"),
    )


def crear_documento(cuenta=None, es_valido=False):
    return Documento.objects.create(
        cuenta=cuenta or crear_cuenta(),
        es_valido=es_valido,
        estado=EstadoDocumento.VALIDADO if es_valido else EstadoDocumento.PENDIENTE,
        fecha_expiracion=date(2027, 1, 1),
        ruta="documentos/placeholder.pdf",
        file_id="file-placeholder",
        nombre_original="documento.pdf",
        content_type="application/pdf",
        tamano_bytes=128,
    )
