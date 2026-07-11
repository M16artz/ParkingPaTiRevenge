from django.db import models


class EstadoEspacio(models.TextChoices):
    LIBRE = "LIBRE", "Libre"
    OCUPADO = "OCUPADO", "Ocupado"
    INACTIVO = "INACTIVO", "Inactivo"
    MANTENIMIENTO = "MANTENIMIENTO", "Mantenimiento"


class Espacio(models.Model):
    parqueadero = models.ForeignKey(
        "parqueaderos.Parqueadero",
        on_delete=models.CASCADE,
        related_name="espacios",
    )
    numero_espacio = models.CharField(max_length=30)
    estado = models.CharField(max_length=20, choices=EstadoEspacio.choices, default=EstadoEspacio.LIBRE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parqueadero", "numero_espacio"],
                name="uniq_espacio_por_parqueadero_numero",
            )
        ]
        indexes = [
            models.Index(fields=["parqueadero", "estado"]),
        ]

    def __str__(self):
        return f"{self.parqueadero} - {self.numero_espacio}"

