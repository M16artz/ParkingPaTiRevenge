from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models


class EstadoCuenta(models.TextChoices):
    ACTIVA = "ACTIVA", "Activa"
    INACTIVA = "INACTIVA", "Inactiva"
    SUSPENDIDA = "SUSPENDIDA", "Suspendida"


class TipoIdentificacion(models.TextChoices):
    CEDULA = "CEDULA", "Cedula"
    RUC = "RUC", "RUC"
    PASAPORTE = "PASAPORTE", "Pasaporte"


class CodigoRol(models.TextChoices):
    ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
    PROPIETARIO = "PROPIETARIO", "Propietario"
    CONDUCTOR = "CONDUCTOR", "Conductor"


class Persona(models.Model):
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    tipo_identificacion = models.CharField(max_length=20, choices=TipoIdentificacion.choices)
    identificacion = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9-]+$",
                message="La identificacion solo puede contener letras, numeros y guiones.",
            )
        ],
    )
    estado = models.CharField(max_length=20, choices=EstadoCuenta.choices, default=EstadoCuenta.ACTIVA)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["identificacion"]),
            models.Index(fields=["estado"]),
        ]

    def __str__(self):
        return f"{self.nombre} {self.apellido}".strip()


class Rol(models.Model):
    codigo = models.CharField(max_length=30, choices=CodigoRol.choices, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["codigo"])]

    def __str__(self):
        return self.get_codigo_display()


class Cuenta(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cuenta_perfil",
        null=True,
        blank=True,
    )
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="cuenta")
    username = models.CharField(max_length=80, unique=True)
    correo = models.EmailField(unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name="cuentas")
    estado = models.CharField(max_length=20, choices=EstadoCuenta.choices, default=EstadoCuenta.ACTIVA)
    password_hash = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["correo"]),
            models.Index(fields=["rol", "estado"]),
        ]

    def __str__(self):
        return self.username
