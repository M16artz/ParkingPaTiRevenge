from django.core.exceptions import ValidationError
from django.db import models


class TipoCategoriaTarifa(models.TextChoices):
    GENERAL = "GENERAL", "General"
    PREFERENCIAL = "PREFERENCIAL", "Tercera edad / discapacidad"
    PESADOS = "PESADOS", "Vehiculos grandes / 4x4"


class CategoriaTarifa(models.Model):
    parqueadero = models.ForeignKey(
        "parqueaderos.Parqueadero",
        on_delete=models.CASCADE,
        related_name="categorias_tarifa",
    )
    codigo = models.CharField(max_length=20, choices=TipoCategoriaTarifa.choices)
    precio_hora = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["parqueadero", "codigo"], name="uniq_tarifa_por_parqueadero_codigo")
        ]
        indexes = [
            models.Index(fields=["parqueadero", "codigo"]),
        ]

    def clean(self):
        super().clean()
        if self.precio_hora is not None and self.precio_hora <= 0:
            raise ValidationError({"precio_hora": "El precio por hora debe ser mayor a cero."})

    def __str__(self):
        return f"{self.get_codigo_display()}: ${self.precio_hora}/hora - {self.parqueadero}"

