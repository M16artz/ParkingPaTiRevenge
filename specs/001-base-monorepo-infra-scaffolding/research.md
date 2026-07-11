# Research — Base del monorepo e infraestructura mínima

## Contexto

Crear estructura base, `.gitignore`, `.env.example`, Docker Compose, Dockerfiles y scaffolding ASGI.

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

- **Riesgo investigado:** Desalineación entre nombres de carpetas actuales y estructura objetivo.. **Mitigación:** tratarlo como criterio de revisión antes de merge.
- **Riesgo investigado:** Variables incompletas que impidan levantar el entorno.. **Mitigación:** tratarlo como criterio de revisión antes de merge.
- **Riesgo investigado:** Versiones flotantes de imágenes Docker.. **Mitigación:** tratarlo como criterio de revisión antes de merge.



## Rationale final

La decisión técnica propuesta permite implementar Base del monorepo e infraestructura mínima de forma incremental, verificable y consistente con la constitución del proyecto.
