# Feature 002 — Backend base de dominio y API

**Prioridad:** P0  
**Estado:** Especificada  
**Tipo:** Feature funcional/técnica del producto  
**Tecnología:** No especificada en este archivo por decisión de constitución.

## Propósito

Crear y validar la base del dominio de usuarios, parqueaderos, espacios, horarios y tarifas.

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
Como usuario del sistema, quiero completar el flujo de **Backend base de dominio y API** para avanzar en la operación de ParkingPaTi sin depender de pasos manuales externos.

### HU2 — Retroalimentación
Como usuario del sistema, quiero recibir mensajes claros cuando una acción falle para saber qué debo corregir.

### HU3 — Seguridad y alcance
Como usuario autorizado, quiero que solo se me permita operar sobre recursos a los que tengo derecho para proteger datos de otros usuarios.

## Escenarios de aceptación

### Escenario 1: flujo exitoso
**Dado** que el usuario se encuentra en el flujo de backend base de dominio y api,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.
### Escenario 2: validación de datos inválidos
**Dado** que el usuario se encuentra en el flujo de backend base de dominio y api,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.
### Escenario 3: restricción de acceso
**Dado** que el usuario se encuentra en el flujo de backend base de dominio y api,
**Cuando** ejecuta la acción principal,
**Entonces** el sistema responde de forma clara, consistente y verificable.

## Requisitos funcionales

- RF01. El sistema debe permitir apps de dominio o mapear las existentes sin romper imports.
- RF02. El sistema debe incorporar índices de búsqueda en Parqueadero y Espacio.
- RF03. El sistema debe estar preparado para JWT con access token de 15 minutos.
- RF04. El sistema debe permitir serializers/DTO para lectura y escritura.
- RF05. El sistema debe permitir ViewSets con permisos por defecto.
- RF06. El sistema debe incorporar drf-spectacular y endpoint de schema.
- RF07. El sistema debe permitir pruebas de autenticación y permisos.

## Requisitos no funcionales aplicables

- RNF01. La interfaz asociada debe ser responsiva cuando exista pantalla de usuario.
- RNF03. Todo error debe explicar causa y acción correctiva.
- RNF07. Las comunicaciones y datos sensibles deben protegerse.
- RNF08. Debe aplicarse control de acceso por rol.
- RNF10. La solución debe ser modular y extensible.


## Entidades clave

- **Persona**: elemento necesario para cumplir la entrega.
- **Cuenta**: elemento necesario para cumplir la entrega.
- **Rol**: elemento necesario para cumplir la entrega.
- **Parqueadero**: elemento necesario para cumplir la entrega.
- **Direccion**: elemento necesario para cumplir la entrega.
- **Ubicacion**: elemento necesario para cumplir la entrega.
- **Espacio**: elemento necesario para cumplir la entrega.
- **HorarioAtencion**: elemento necesario para cumplir la entrega.
- **Documento**: elemento necesario para cumplir la entrega.

## Fuera de alcance

- Pagos en línea.
- Reservas anticipadas.
- Automatización con sensores o cámaras.
- Cambios no relacionados con esta feature.

## Resultado esperado

La feature queda lista para implementación por agentes, con alcance claro, criterios verificables y trazabilidad hacia plan técnico, modelo de datos, contratos, prototipos y checklist.
