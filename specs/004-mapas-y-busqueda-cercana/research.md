# Research — Mapas, tiles y búsqueda cercana

## Contexto

tileserver-gl con extract Ecuador, Leaflet, Nominatim público con debounce y endpoint cercano.

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

- **Riesgo investigado:** Nominatim público impone políticas de uso; debe limitarse tasa.. **Mitigación:** tratarlo como criterio de revisión antes de merge.
- **Riesgo investigado:** Generar MBTiles puede ser pesado; no hacerlo en runtime.. **Mitigación:** tratarlo como criterio de revisión antes de merge.
- **Riesgo investigado:** Distancias en Python pueden degradarse si el dataset crece mucho.. **Mitigación:** tratarlo como criterio de revisión antes de merge.


## Decisión específica: mapas

El backend no actúa como proxy de tiles ni de Nominatim. El cliente consume tileserver-gl directamente y llama Nominatim con debounce y límite de tasa. El backend solo expone recursos propios de ParkingPaTi.


## Rationale final

La decisión técnica propuesta permite implementar Mapas, tiles y búsqueda cercana de forma incremental, verificable y consistente con la constitución del proyecto.
