from django.core.exceptions import ValidationError
from django.db import models


class DiaSemana(models.TextChoices):
    LUNES = "LUNES", "Lunes"
    MARTES = "MARTES", "Martes"
    MIERCOLES = "MIERCOLES", "Miercoles"
    JUEVES = "JUEVES", "Jueves"
    VIERNES = "VIERNES", "Viernes"
    SABADO = "SABADO", "Sabado"
    DOMINGO = "DOMINGO", "Domingo"


class HorarioAtencion(models.Model):
    parqueadero = models.ForeignKey(
        "parqueaderos.Parqueadero",
        on_delete=models.CASCADE,
        related_name="horarios",
    )
    dia = models.CharField(max_length=20, choices=DiaSemana.choices)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["parqueadero", "dia"], name="uniq_horario_por_parqueadero_dia")
        ]
        indexes = [
            models.Index(fields=["parqueadero", "dia"]),
        ]

    def clean(self):
        super().clean()
        if self.hora_apertura and self.hora_cierre and self.hora_apertura >= self.hora_cierre:
            raise ValidationError(
                {"hora_cierre": "La hora de cierre debe ser posterior a la hora de apertura."}
            )

    def __str__(self):
        return f"{self.parqueadero} - {self.get_dia_display()}"

