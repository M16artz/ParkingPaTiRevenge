# Research — Gestión de tarifas por categoría

## Contexto

Agregar `CategoriaTarifa` para General, Preferencial y Pesados, coexistiendo con estrategia base.

## Decisiones justificadas

### Decisión 1: Modularidad por microdominio
Se mantiene la división funcional para que los agentes puedan trabajar sin pisarse. Cada feature actualiza solo los archivos relacionados con su microdominio.

### Decisión 2: Contrato antes que implementación
Los contratos en `contracts/` son la fuente de verdad para backend, frontend web y móvil. Esto reduce errores de integración entre agentes.

### Decisión 3: Seguridad y permisos desde el inicio
La implementación no deja endpoints abiertos por comodidad. Los recursos privados requieren autenticación y los recursos de propietario validan pertenencia.

## Alternativas consideradas

- Implementar primero pantallas sin contratos: descartado porque aumenta integración rota entre agentes.
- Concentrar toda la lógica en controladores: descartado porque rompe la arquitectura por capas.
- Crear tareas grandes por módulo completo: descartado porque dificulta revisión de agentes y rollback.

## Riesgos investigados

- **Riesgo investigado:** Reusar jerarquía `EstrategiaTarifa` rompería simultaneidad de categorías.. **Mitigación:** tratarlo como criterio de revisión antes de merge.
- **Riesgo investigado:** Duplicar categorías por parqueadero generaría ambigüedad en precios.. **Mitigación:** tratarlo como criterio de revisión antes de merge.
- **Riesgo investigado:** Mezclar porcentaje y precio final sin regla clara.. **Mitigación:** tratarlo como criterio de revisión antes de merge.


## Decisión específica: `CategoriaTarifa`

Se agrega un modelo nuevo porque General, Preferencial y Pesados son precios paralelos por categoría y pueden coexistir. La jerarquía `EstrategiaTarifa`, `IncrementoTarifa` y `DescuentoTarifa` representa una estrategia excluyente por parqueadero y no debe forzarse para categorías simultáneas.

### Código objetivo

```python
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
        unique_together = ("parqueadero", "codigo")
        indexes = [models.Index(fields=["parqueadero", "codigo"])]

    def __str__(self):
        return f"{self.get_codigo_display()}: ${self.precio_hora}/hora - {self.parqueadero}"
```


## Rationale final

La decisión técnica propuesta permite implementar Gestión de tarifas por categoría de forma incremental, verificable y consistente con la constitución del proyecto.
