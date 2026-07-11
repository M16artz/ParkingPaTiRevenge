# Constitución del Proyecto — ParkingPaTi

**Versión:** 1.0  
**Fecha:** 2026-07-10  
**Estado:** Base normativa para agentes de IA

## 1. Propósito

ParkingPaTi es una plataforma web y móvil para consultar y administrar disponibilidad de parqueaderos privados en Loja, Ecuador. Esta constitución define los principios que todo agente de IA debe respetar al especificar, implementar, probar o modificar el sistema.

## 2. Principios fundamentales

### P1. Usuario primero, dominio antes que tecnología
Las funcionalidades deben expresarse desde el valor para conductores, propietarios y administradores. Las decisiones técnicas se documentan en `plan.md` y `research.md`, nunca como dependencia obligatoria dentro de `spec.md`.

### P2. Tiempo real verificable
La disponibilidad de espacios debe propagarse sin polling como mecanismo principal y debe poder verificarse de extremo a extremo. La meta funcional es que los cambios visibles para usuarios se reflejen en menos de 5 segundos.

### P3. Seguridad por defecto
Todo endpoint privado exige autenticación. Todo endpoint administrativo exige rol administrador. Todo endpoint de propietario debe validar propiedad del recurso. Los documentos reales, credenciales y `.env` nunca se versionan.

### P4. Arquitectura modular por microdominios
Cada microdominio debe encapsular modelos, validaciones, servicios, repositorios, DTO/serializadores, pruebas y contratos. Un cambio de UI no debe romper reglas de negocio y un cambio de persistencia no debe romper contratos públicos.

### P5. Agentes autónomos, entregables pequeños
Cada tarea asignada a un agente debe ser atómica, verificable y reversible. Un agente no debe mezclar varias responsabilidades en un mismo commit lógico.

### P6. Trazabilidad completa
Cada requisito funcional debe poder rastrearse a una historia, un escenario de aceptación, un contrato, una entidad de datos y una estrategia de verificación.

### P7. Mensajes en español y errores accionables
Los mensajes al usuario deben indicar qué ocurrió, por qué ocurrió y qué puede hacer para corregirlo.

### P8. Escalabilidad incremental
La solución inicial debe funcionar como MVP, pero no bloquear migraciones futuras: PostGIS, colas, observabilidad, pagos, reservas, sensores o balanceo horizontal.

## 3. Estándares de especificación

1. `spec.md` debe ser tecnológicamente agnóstico.
2. `plan.md` debe contener decisiones técnicas, componentes impactados, contratos, UI y verificación.
3. `research.md` debe justificar decisiones y alternativas descartadas.
4. `data-model.md` debe describir entidades, atributos, relaciones, validaciones y restricciones.
5. `contracts/` debe contener contratos de API o contratos operativos verificables.
6. `checklists/requirements.md` debe permitir revisar si la especificación está lista para implementación.
7. `docs/prototypes/` debe incluir HTML y PNG por pantalla clave.

## 4. Microdominios

### Identidad y acceso
Personas, cuentas, roles, autenticación, autorización y redirección por rol.

### Documentos y validación
Carga, consulta, reemplazo y validación de documentos de propietarios o parqueaderos.

### Parqueaderos
Registro del establecimiento, estado general, dirección, ubicación, validación administrativa y datos públicos.

### Espacios y disponibilidad
Gestión de espacios individuales, estados y eventos de disponibilidad en tiempo real.

### Tarifas
Tarifas base, incrementos, descuentos y categorías paralelas de tarifa: General, Preferencial y Pesados.

### Horarios
Días y rangos de atención por parqueadero.

### Mapas y búsqueda
Localización, geocodificación, tiles, búsqueda cercana y visualización de disponibilidad.

### Administración
Validación de parqueaderos, revisión de documentos y control de cuentas.

### Infraestructura
Monorepo, contenedores, variables de entorno, despliegue, túnel, servidor ASGI y observabilidad mínima.

## 5. Reglas de consistencia

- Ninguna feature debe crear endpoints sin contrato.
- Ninguna feature debe modificar una entidad sin actualizar `data-model.md`.
- Ninguna feature debe exponer información privada a usuarios anónimos.
- Ninguna implementación debe depender de datos hardcodeados cuando exista configuración o variable de entorno.
- Toda acción destructiva debe requerir confirmación en la UI y autorización en backend.
- Toda operación de tiempo real debe tener prueba REST + prueba WebSocket.
- Todo prototipo debe representar el flujo clave que se implementará, aunque sea de baja fidelidad.

## 6. Suposiciones del documento

- Se mantiene el monorepo solicitado con `/backend`, `/frontend-web`, `/mobile`, `/docker` y `/docs`.
- Donde el código actual usa `usuarios`, `parqueaderos`, `horarios`, `tarifas` y `documentos`, se mapea con los microdominios de seguridad, configuración y servicio sin forzar una reescritura inmediata.
- La planificación incorpora Cloudflare R2 como placeholder solicitado; si se mantiene Google Drive, se documenta como adaptador alternativo de almacenamiento.
- El MVP no incluye reservas, pagos ni hardware.
