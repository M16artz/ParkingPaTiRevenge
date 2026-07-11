from django.db import models
from django.db.models import Q


class EstadoDocumento(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    VALIDADO = "VALIDADO", "Validado"
    RECHAZADO = "RECHAZADO", "Rechazado"


class Documento(models.Model):
    cuenta = models.ForeignKey("usuarios.Cuenta", on_delete=models.CASCADE, related_name="documentos")
    estado = models.CharField(max_length=20, choices=EstadoDocumento.choices, default=EstadoDocumento.PENDIENTE)
    es_valido = models.BooleanField(default=False)
    fecha_expiracion = models.DateField(null=True, blank=True)
    ruta = models.CharField(max_length=500)
    file_id = models.CharField(max_length=255)
    nombre_original = models.CharField(max_length=255, default="documento.pdf")
    content_type = models.CharField(max_length=100, default="application/pdf")
    tamano_bytes = models.PositiveIntegerField(default=0)
    motivo_rechazo = models.CharField(max_length=500, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cuenta"],
                condition=Q(es_valido=True),
                name="uniq_documento_valido_por_cuenta",
            )
        ]
        indexes = [
            models.Index(fields=["cuenta", "es_valido"]),
            models.Index(fields=["cuenta", "estado"]),
            models.Index(fields=["fecha_expiracion"]),
        ]

    def __str__(self):
        return f"Documento {self.estado.lower()} de {self.cuenta}"
