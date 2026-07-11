# Feature 004 — Mapas, tiles y búsqueda cercana

**Prioridad:** P1  
**Estado:** Especificada  
**Tipo:** Feature funcional/técnica del producto  
**Tecnología:** No especificada en este archivo por decisión de constitución.

## Propósito

Permitir búsqueda geográfica de parqueaderos y renderizado de mapa base local.

## Suposiciones razonables

- La implementación se hará sobre el monorepo ParkingPaTi.
- Cuando una regla dependa de permisos, el sistema verificará el rol y la propiedad del recurso.
- El MVP excluye reservas, pagos en línea e integración con hardware.
- Las decisiones tecnológicas se detallan en `plan.md` y `research.md`.

## Actores relevantes

- **Usuario autorizado**
- **Usuario público cuando aplique**
- **Administrador cuando aplique**

## Historias de usuario

### HU1 — Acción principal
Como usuario del sistema, quiero completar el flujo de **Mapas, tiles y búsqueda cercana** para avanzar en la operación de ParkingPaTi sin depender de pasos manuales externos.

### HU2 — Retroalimentación
Como usuario del sistema, quiero recibir mensajes claros cuando una acción falle para saber qué debo corregir.

### HU3 — Seguridad y alcance
Como usuario autorizado, quiero que solo se me permita operar sobre recursos a los que tengo derecho para proteger datos de otros usuarios.

## Escenarios de aceptación

### Escenario 1: flujo exitoso
**Dado** que el usuario se encuentra en el flujo de mapas, tiles y búsqueda cercana,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.
### Escenario 2: validación de datos inválidos
**Dado** que el usuario se encuentra en el flujo de mapas, tiles y búsqueda cercana,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.
### Escenario 3: restricción de acceso
**Dado** que el usuario se encuentra en el flujo de mapas, tiles y búsqueda cercana,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.

## Requisitos funcionales

- RF01. Descargar extract Ecuador OSM PBF.
- RF02. Convertir a MBTiles con tilemaker.
- RF03. Montar tileserver-gl con estilo osm-bright.
- RF04. Instalar e integrar Leaflet en web.
- RF05. El sistema debe permitir buscador con Nominatim, debounce 800 ms y 1 req/s.
- RF06. El sistema debe permitir endpoint de cercanía con distancia y filtros públicos.
- RF07. El sistema debe permitir marcadores por disponibilidad.

## Requisitos no funcionales aplicables

- RNF01. La interfaz asociada debe ser responsiva cuando exista pantalla de usuario.
- RNF03. Todo error debe explicar causa y acción correctiva.
- RNF07. Las comunicaciones y datos sensibles deben protegerse.
- RNF08. Debe aplicarse control de acceso por rol.
- RNF10. La solución debe ser modular y extensible.


## Entidades clave

- **Parqueadero**: elemento necesario para cumplir la entrega.
- **Ubicacion**: elemento necesario para cumplir la entrega.
- **Direccion**: elemento necesario para cumplir la entrega.
- **Disponibilidad**: elemento necesario para cumplir la entrega.
- **ResultadoBusqueda**: elemento necesario para cumplir la entrega.
- **Distancia**: elemento necesario para cumplir la entrega.

## Fuera de alcance

- Pagos en línea.
- Reservas anticipadas.
- Automatización con sensores o cámaras.
- Cambios no relacionados con esta feature.

## Resultado esperado

La feature queda lista para implementación por agentes, con alcance claro, criterios verificables y trazabilidad hacia plan técnico, modelo de datos, contratos, prototipos y checklist.
