---
name: parkingpati-spec-rules
description: "Reglas obligatorias para implementar backend, frontend web, móvil, infraestructura y pruebas de ParkingPaTi."
---

# Skill: Reglas de implementación para ParkingPaTi

## Reglas generales

1. Todo cambio debe respetar `.specify/memory/constitution.md`.
2. `spec.md` no debe mencionar frameworks, librerías ni lenguajes.
3. `plan.md` y `research.md` sí deben documentar tecnologías y decisiones.
4. Todo endpoint debe estar documentado en `contracts/`.
5. Todo error visible al usuario debe estar en español y debe sugerir una acción correctiva.
6. Ningún agente debe versionar `.env`, credenciales, tokens, claves privadas o documentos reales de usuarios.

## Backend

1. Mantener arquitectura en capas: `controllers` → `services` → `repositories` → `models`.
2. No colocar reglas de negocio dentro de `urls.py`.
3. No exponer modelos directamente sin DTO/serializer controlado.
4. Usar permisos por defecto autenticados, salvo endpoints públicos explícitos.
5. Los endpoints de gestión deben validar propietario o administrador.
6. JWT debe usar access token de 15 minutos.
7. Documentar API con OpenAPI.
8. Los cambios de `Espacio.estado` deben publicar evento de disponibilidad.
9. Usar `Uvicorn` como servidor ASGI para producción.
10. El `CHANNEL_LAYERS` de producción debe usar Redis.
11. Los modelos con búsquedas frecuentes deben declarar índices.
12. Las migraciones deben ser pequeñas y revisables.
13. Para tarifas paralelas por vehículo, usar `CategoriaTarifa`, no forzar `EstrategiaTarifa`.

### Modelo obligatorio para categorías de tarifa

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

## Frontend web

1. Las URLs deben centralizarse en `frontend-web/src/config/endpoints.ts`.
2. Las variables globales deben centralizarse en `frontend-web/src/config/app.ts` o `env.ts`.
3. Toda pantalla autenticada debe reutilizar layout con barra superior, menú lateral, contenido y footer.
4. Toda llamada API debe manejar estados de carga, éxito y error.
5. Los formularios deben validar antes de enviar.
6. Los servicios no deben contener lógica visual.
7. Los controladores/hooks no deben contener HTML.
8. Las vistas no deben construir URLs manualmente.
9. La ruta de propietarios debe estar protegida por rol `PROPIETARIO`.
10. La ruta de administración debe estar protegida por rol `ADMINISTRADOR`.

## Móvil

1. Solicitar ubicación solo cuando el usuario use búsqueda/mapa.
2. No bloquear la búsqueda si el usuario rechaza ubicación; permitir búsqueda manual.
3. No usar secretos en el bundle.
4. Las URLs base deben inyectarse en build o configuración segura.
5. El usuario anónimo puede consultar parqueaderos públicos, pero no gestionar datos.

## Mapas

1. El frontend consume tiles directamente desde tileserver-gl.
2. Nominatim público debe usarse con debounce mínimo de 800 ms y máximo 1 req/s.
3. El backend no debe actuar como proxy de Nominatim salvo decisión explícita futura.
4. El endpoint de cercanía debe ordenar por distancia.
5. Los parqueaderos no validados o inactivos no deben aparecer a usuarios anónimos.

## Infraestructura

1. Usar `.env.example` con placeholders comentados.
2. Fijar versiones de imágenes en Docker Compose.
3. PostgreSQL y Redis deben usar volúmenes persistentes.
4. `tileserver-gl` debe montar `.mbtiles`, no recalcularlo en cada arranque.
5. El comando backend productivo debe usar:
   `uvicorn backend.asgi:application --host 0.0.0.0 --port 8000 --workers 2`
6. Cloudflare Tunnel debe usar variable `CLOUDFLARE_TUNNEL_TOKEN`.

## Pruebas

1. Todo endpoint privado debe tener prueba de no autenticado.
2. Todo endpoint de propietario debe tener prueba de acceso cruzado denegado.
3. Todo contrato debe tener al menos una prueba de respuesta exitosa y una de error.
4. El flujo de WebSocket debe probar conexión, recepción y payload.
5. La búsqueda cercana debe probar orden por distancia.
6. Las tarifas deben probar unicidad por `(parqueadero, codigo)`.
