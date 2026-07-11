from django.db import models
from apps.parqueaderos.models import Parqueadero


class TipoCategoriaTarifa(models.TextChoices):
    GENERAL = "GENERAL", "General"
    PREFERENCIAL = "PREFERENCIAL", "Tercera edad / discapacidad"
    PESADOS = "PESADOS", "Vehículos grandes / 4x4"


class CategoriaTarifa(models.Model):
    parqueadero = models.ForeignKey(
        Parqueadero,
        on_delete=models.CASCADE,
        related_name="categorias_tarifa",
    )
    codigo = models.CharField(max_length=20, choices=TipoCategoriaTarifa.choices)
    precio_hora = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        # Como máximo UNA tarifa por categoría y parqueadero.
        # Permite tener GENERAL + PREFERENCIAL + PESADOS al mismo tiempo.
        unique_together = ("parqueadero", "codigo")
        indexes = [models.Index(fields=["parqueadero", "codigo"])]

    def __str__(self):
        return f"{self.get_codigo_display()}: ${self.precio_hora}/hora - {self.parqueadero}"
