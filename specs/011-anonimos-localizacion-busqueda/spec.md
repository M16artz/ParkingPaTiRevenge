# Feature 011 — Usuarios anónimos: localización y búsqueda de parqueaderos

**Prioridad:** P1  
**Estado:** Especificada  
**Tipo:** Feature funcional/técnica del producto  
**Tecnología:** No especificada en este archivo por decisión de constitución.

## Propósito

Permitir a conductores sin cuenta buscar parqueaderos y ver información pública.

## Suposiciones razonables

- La implementación se hará sobre el monorepo ParkingPaTi.
- Cuando una regla dependa de permisos, el sistema verificará el rol y la propiedad del recurso.
- El MVP excluye reservas, pagos en línea e integración con hardware.
- Las decisiones tecnológicas se detallan en `plan.md` y `research.md`.

## Actores relevantes

- **Propietario**
- **Administrador**
- **Conductor anónimo**

## Historias de usuario

### HU1 — Acción principal
Como usuario del sistema, quiero completar el flujo de **Usuarios anónimos: localización y búsqueda de parqueaderos** para avanzar en la operación de ParkingPaTi sin depender de pasos manuales externos.

### HU2 — Retroalimentación
Como usuario del sistema, quiero recibir mensajes claros cuando una acción falle para saber qué debo corregir.

### HU3 — Seguridad y alcance
Como usuario autorizado, quiero que solo se me permita operar sobre recursos a los que tengo derecho para proteger datos de otros usuarios.

## Escenarios de aceptación

### Escenario 1: flujo exitoso
**Dado** que el usuario se encuentra en el flujo de usuarios anónimos: localización y búsqueda de parqueaderos,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.
### Escenario 2: validación de datos inválidos
**Dado** que el usuario se encuentra en el flujo de usuarios anónimos: localización y búsqueda de parqueaderos,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.
### Escenario 3: restricción de acceso
**Dado** que el usuario se encuentra en el flujo de usuarios anónimos: localización y búsqueda de parqueaderos,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.

## Requisitos funcionales

- RF01. El sistema debe permitir home pública con CTA de búsqueda.
- RF02. Solicitar ubicación solo al usar buscar cerca.
- RF03. Permitir buscar por dirección si rechaza ubicación.
- RF04. Mostrar lista y mapa.
- RF05. Mostrar detalle con tarifas, horarios y espacios libres.
- RF06. Suscribirse a WebSocket en detalle.
- RF07. Probar máximo 3 toques hasta resultados.

## Requisitos no funcionales aplicables

- RNF01. La interfaz asociada debe ser responsiva cuando exista pantalla de usuario.
- RNF03. Todo error debe explicar causa y acción correctiva.
- RNF07. Las comunicaciones y datos sensibles deben protegerse.
- RNF08. Debe aplicarse control de acceso por rol.
- RNF10. La solución debe ser modular y extensible.
- RNF06. Los cambios de disponibilidad deben reflejarse en máximo 5 segundos.

## Entidades clave

- **ConductorAnonimo**: elemento necesario para cumplir la entrega.
- **ParqueaderoPublico**: elemento necesario para cumplir la entrega.
- **Ubicacion**: elemento necesario para cumplir la entrega.
- **TarifaPublica**: elemento necesario para cumplir la entrega.
- **HorarioPublico**: elemento necesario para cumplir la entrega.
- **Disponibilidad**: elemento necesario para cumplir la entrega.

## Fuera de alcance

- Pagos en línea.
- Reservas anticipadas.
- Automatización con sensores o cámaras.
- Cambios no relacionados con esta feature.

## Resultado esperado

La feature queda lista para implementación por agentes, con alcance claro, criterios verificables y trazabilidad hacia plan técnico, modelo de datos, contratos, prototipos y checklist.
