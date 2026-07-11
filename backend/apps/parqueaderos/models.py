from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class EstadoParqueadero(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    INACTIVO = "INACTIVO", "Inactivo"
    SUSPENDIDO = "SUSPENDIDO", "Suspendido"


class DisponibilidadParqueadero(models.TextChoices):
    DISPONIBLE = "DISPONIBLE", "Disponible"
    LLENO = "LLENO", "Lleno"
    CERRADO = "CERRADO", "Cerrado"


class Direccion(models.Model):
    calle_principal = models.CharField(max_length=120)
    calle_secundaria = models.CharField(max_length=120, blank=True)
    nro_lote = models.CharField(max_length=40, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        partes = [self.calle_principal, self.calle_secundaria, self.nro_lote]
        return ", ".join(parte for parte in partes if parte)


class Ubicacion(models.Model):
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["latitud", "longitud"]),
        ]

    def clean(self):
        super().clean()
        if self.latitud is not None and not (Decimal("-90") <= self.latitud <= Decimal("90")):
            raise ValidationError({"latitud": "La latitud debe estar entre -90 y 90."})
        if self.longitud is not None and not (Decimal("-180") <= self.longitud <= Decimal("180")):
            raise ValidationError({"longitud": "La longitud debe estar entre -180 y 180."})

    def __str__(self):
        return f"{self.latitud}, {self.longitud}"


class Parqueadero(models.Model):
    propietario = models.ForeignKey(
        "usuarios.Cuenta",
        on_delete=models.PROTECT,
        related_name="parqueaderos",
    )
    nombre = models.CharField(max_length=120)
    estado = models.CharField(
        max_length=20,
        choices=EstadoParqueadero.choices,
        default=EstadoParqueadero.INACTIVO,
    )
    validado = models.BooleanField(default=False)
    disponibilidad = models.CharField(
        max_length=20,
        choices=DisponibilidadParqueadero.choices,
        default=DisponibilidadParqueadero.CERRADO,
    )
    direccion = models.OneToOneField(Direccion, on_delete=models.PROTECT, related_name="parqueadero")
    ubicacion = models.OneToOneField(Ubicacion, on_delete=models.PROTECT, related_name="parqueadero")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["nombre"]),
            models.Index(fields=["estado"]),
            models.Index(fields=["validado"]),
            models.Index(fields=["disponibilidad"]),
            models.Index(fields=["estado", "validado", "disponibilidad"]),
        ]

    def __str__(self):
        return self.nombre

