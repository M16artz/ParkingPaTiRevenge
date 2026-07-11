# Feature 003 — Disponibilidad en tiempo real con Channels y Redis

**Prioridad:** P0  
**Estado:** Especificada  
**Tipo:** Feature funcional/técnica del producto  
**Tecnología:** No especificada en este archivo por decisión de constitución.

## Propósito

Garantizar push instantáneo de cambios de espacios por parqueadero.

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
Como usuario del sistema, quiero completar el flujo de **Disponibilidad en tiempo real con Channels y Redis** para avanzar en la operación de ParkingPaTi sin depender de pasos manuales externos.

### HU2 — Retroalimentación
Como usuario del sistema, quiero recibir mensajes claros cuando una acción falle para saber qué debo corregir.

### HU3 — Seguridad y alcance
Como usuario autorizado, quiero que solo se me permita operar sobre recursos a los que tengo derecho para proteger datos de otros usuarios.

## Escenarios de aceptación

### Escenario 1: flujo exitoso
**Dado** que el usuario se encuentra en el flujo de disponibilidad en tiempo real con channels y redis,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.
### Escenario 2: validación de datos inválidos
**Dado** que el usuario se encuentra en el flujo de disponibilidad en tiempo real con channels y redis,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.
### Escenario 3: restricción de acceso
**Dado** que el usuario se encuentra en el flujo de disponibilidad en tiempo real con channels y redis,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.

## Requisitos funcionales

- RF01. El sistema debe estar preparado para `CHANNEL_LAYERS` con Redis.
- RF02. El sistema debe permitir `ParkingConsumer` o adaptar `DisponibilidadConsumer`.
- RF03. Definir grupos por `parqueadero_id`.
- RF04. Emitir payload `{espacio_id, parqueadero_id, estado, disponibles}`.
- RF05. El sistema debe incorporar signal o publicación desde servicio al cambiar estado.
- RF06. El sistema debe permitir script JS de prueba.
- RF07. Probar latencia menor a 5 segundos.

## Requisitos no funcionales aplicables

- RNF01. La interfaz asociada debe ser responsiva cuando exista pantalla de usuario.
- RNF03. Todo error debe explicar causa y acción correctiva.
- RNF07. Las comunicaciones y datos sensibles deben protegerse.
- RNF08. Debe aplicarse control de acceso por rol.
- RNF10. La solución debe ser modular y extensible.
- RNF06. Los cambios de disponibilidad deben reflejarse en máximo 5 segundos.

## Entidades clave

- **Espacio**: elemento necesario para cumplir la entrega.
- **Parqueadero**: elemento necesario para cumplir la entrega.
- **EventoDisponibilidad**: elemento necesario para cumplir la entrega.
- **SuscripcionParqueadero**: elemento necesario para cumplir la entrega.

## Fuera de alcance

- Pagos en línea.
- Reservas anticipadas.
- Automatización con sensores o cámaras.
- Cambios no relacionados con esta feature.

## Resultado esperado

La feature queda lista para implementación por agentes, con alcance claro, criterios verificables y trazabilidad hacia plan técnico, modelo de datos, contratos, prototipos y checklist.
