# Research — Disponibilidad en tiempo real con Channels y Redis

## Contexto

Configurar RedisChannelLayer, crear consumer, publicar evento `espacio_actualizado` y validar con cliente JS.

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

- **Riesgo investigado:** Usar Gunicorn/WSGI impediría WebSockets.. **Mitigación:** tratarlo como criterio de revisión antes de merge.
- **Riesgo investigado:** Emitir eventos desde signal sin detectar cambios reales puede duplicar mensajes.. **Mitigación:** tratarlo como criterio de revisión antes de merge.
- **Riesgo investigado:** Múltiples workers requieren Redis, no InMemoryChannelLayer.. **Mitigación:** tratarlo como criterio de revisión antes de merge.


## Decisión específica: RedisChannelLayer

Se usa Redis como channel layer para permitir múltiples workers Uvicorn y evitar que las suscripciones queden aisladas por proceso. `InMemoryChannelLayer` solo queda permitido en pruebas unitarias o entorno local muy controlado.


## Rationale final

La decisión técnica propuesta permite implementar Disponibilidad en tiempo real con Channels y Redis de forma incremental, verificable y consistente con la constitución del proyecto.
