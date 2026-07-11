# Modelo de datos — Registro de usuarios y envío de documentos

## Objetivo

Definir entidades, atributos, relaciones, validaciones y restricciones necesarias para implementar la feature.

## Entidades

### Persona

**Atributos mínimos:** id, nombre, apellido, tipo_identificacion, identificacion, estado.  
**Validaciones:** campos obligatorios no vacíos; referencias existentes; estados dentro de catálogo cuando aplique.  
**Restricciones:** respetar permisos, unicidad y consistencia transaccional.
### Cuenta

**Atributos mínimos:** id, persona_id, parqueadero_id, documento_id, username, correo, rol, estado, password_hash.  
**Validaciones:** campos obligatorios no vacíos; referencias existentes; estados dentro de catálogo cuando aplique.  
**Restricciones:** respetar permisos, unicidad y consistencia transaccional.
### Documento

**Atributos mínimos:** id, es_valido, fecha_expiracion, ruta, file_id.  
**Validaciones:** campos obligatorios no vacíos; referencias existentes; estados dentro de catálogo cuando aplique.  
**Restricciones:** respetar permisos, unicidad y consistencia transaccional.
### EstadoValidacion

**Atributos mínimos:** id, fecha_creacion, fecha_actualizacion.  
**Validaciones:** campos obligatorios no vacíos; referencias existentes; estados dentro de catálogo cuando aplique.  
**Restricciones:** respetar permisos, unicidad y consistencia transaccional.

## Relaciones

- Las entidades operativas se relacionan con `Parqueadero` cuando pertenecen a un establecimiento.
- Las entidades de seguridad se relacionan con `Cuenta` y `Persona`.
- Los datos públicos de búsqueda deben derivarse únicamente de parqueaderos activos y validados.
- Los eventos de disponibilidad se derivan de cambios persistidos en `Espacio`.

## Validaciones generales

- Identificadores referenciados deben existir.
- El usuario debe tener permiso sobre el recurso.
- Los campos de dinero deben ser decimales positivos.
- Las horas de apertura deben ser anteriores a las de cierre, salvo regla futura explícita para 24h.
- Las coordenadas deben estar en rangos válidos de latitud y longitud.
- Los estados deben pertenecer a catálogos definidos.

## Restricciones e índices

- `Espacio`: único por `(parqueadero, numero_espacio)` e índice recomendado por `(parqueadero, estado)`.
- `Parqueadero`: índices en campos de búsqueda, validación, estado y disponibilidad.
- `HorarioAtencion`: único por `(parqueadero, dia)`.
- `CategoriaTarifa`: único por `(parqueadero, codigo)` e índice compuesto.
- `Documento`: un documento vigente por cuenta en el MVP.

## Reglas de migración

- Toda migración debe ser pequeña y reversible cuando sea posible.
- Si se renombra un campo, agregar migración de datos o documentar impacto.
- No eliminar campos sin validar dependencias de frontend y contratos.
