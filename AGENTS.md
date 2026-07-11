# Guía de trabajo para agentes — ParkingPaTi

**Última actualización:** 2026-07-10  
**Modo de ejecución:** desarrollo por agentes de IA, con entregables pequeños y verificables.

## Propósito

Este archivo define cómo deben trabajar los agentes de IA dentro del proyecto ParkingPaTi. Todo agente debe leer primero:

1. `.specify/memory/constitution.md`
2. `AGENTS.md`
3. `SKILL.md`
4. `specs/<feature>/spec.md`
5. `specs/<feature>/plan.md`

## Descripción general del sistema

ParkingPaTi permite a conductores localizar parqueaderos cercanos y consultar disponibilidad, tarifas y horarios; a propietarios administrar parqueaderos, espacios, tarifas y horarios; y a administradores validar información y documentos.

## Tecnologías de trabajo

- **Monorepo:** GitHub.
- **Backend:** Python 3.12, Django 5.x, Django REST Framework.
- **API:** REST JSON con documentación OpenAPI.
- **Autenticación:** JWT con access token de 15 minutos y refresh token.
- **Tiempo real:** Django Channels, RedisChannelLayer y Uvicorn ASGI.
- **Base de datos:** PostgreSQL 16.
- **Frontend web:** React 18, Vite, React Router, React Query, Zustand, Tailwind CSS.
- **Móvil:** React Native o Expo/React Native según decisión de implementación.
- **Mapas:** Leaflet.js / react-leaflet, tileserver-gl, Nominatim público para MVP.
- **Storage:** Cloudflare R2 como objetivo; Google Drive puede mantenerse como adaptador temporal.
- **Infra:** Docker Compose, Cloudflare Tunnel, GitHub Actions.
- **Pruebas:** pytest, Django TestCase/APITestCase, pruebas unitarias frontend, pruebas E2E mínimas.

## Estructura esperada del proyecto

```text
parkingpati/
├── .specify/
│   └── memory/
│       └── constitution.md
├── AGENTS.md
├── SKILL.md
├── backend/
├── frontend-web/
├── mobile/
├── docker/
├── docs/
└── specs/
```

## Roles de agentes

### Agente de especificación
Produce y mantiene `spec.md`, escenarios, requisitos funcionales, entidades clave y checklist.

**Entradas:** contexto del proyecto, requerimientos del usuario, constitución.  
**Salidas:** `spec.md`, actualización de `checklists/requirements.md`.  
**Criterio de completitud:** ningún requisito queda ambiguo sin suposición documentada.

### Agente de arquitectura
Produce `plan.md`, `research.md`, decisiones técnicas, componentes impactados y estrategia de verificación.

**Entradas:** `spec.md`, código existente, ADRs, restricciones de infraestructura.  
**Salidas:** `plan.md`, `research.md`.  
**Criterio de completitud:** toda decisión tiene razón, alternativa descartada y riesgo.

### Agente de backend
Implementa modelos, migraciones, serializers/DTO, servicios, repositorios, permisos, endpoints y pruebas.

**Entradas:** `data-model.md`, contratos API, `SKILL.md`.  
**Salidas:** código backend, migraciones, pruebas, documentación OpenAPI.  
**Criterio de completitud:** pruebas pasan, permisos aplicados, errores en español, contratos respetados.

### Agente de frontend web
Implementa vistas, componentes, hooks/controladores, servicios API, rutas y pruebas.

**Entradas:** prototipos HTML/PNG, contratos API, `plan.md`, `SKILL.md`.  
**Salidas:** pantallas funcionales, validación cliente, integración API.  
**Criterio de completitud:** flujo navegable, estados de carga/error/éxito, rutas protegidas.

### Agente móvil
Implementa pantallas móviles, permisos de ubicación, consumo de API y mapa/listado.

**Entradas:** contratos, prototipos, reglas de privacidad.  
**Salidas:** flujo móvil funcional y build verificable.  
**Criterio de completitud:** permisos solicitados en contexto, no al arranque; búsqueda en máximo 3 toques.

### Agente de tiempo real
Implementa Channels, Redis, consumers, signals/servicios de publicación, cliente WebSocket y pruebas E2E.

**Entradas:** feature 003 y 010.  
**Salidas:** canal WebSocket, eventos, test JS, prueba de latencia.  
**Criterio de completitud:** cambio de espacio se recibe por WebSocket sin polling.

### Agente de infraestructura
Implementa Docker, variables de entorno, tileserver, túnel, CI/CD y documentación de arranque.

**Entradas:** feature 001 y 004.  
**Salidas:** compose, Dockerfiles, `.env.example`, scripts, workflows.  
**Criterio de completitud:** entorno levanta desde cero con `.env.example` copiado a `.env`.

### Agente de pruebas
Diseña y ejecuta pruebas unitarias, integración, contrato, seguridad y smoke tests.

**Entradas:** contratos, criterios de aceptación, código implementado.  
**Salidas:** reportes de pruebas y bugs reproducibles.  
**Criterio de completitud:** cobertura de caminos felices y errores principales.

### Agente revisor
Verifica adherencia a constitución, seguridad, contrato, estilo y atomización.

**Entradas:** PR lógico o patch del agente ejecutor.  
**Salidas:** aprobación o lista de correcciones.  
**Criterio de completitud:** no hay deuda crítica ni contrato roto.

## Flujo de trabajo entre agentes

```text
Especificación → Arquitectura → Backend/Frontend/Móvil/Infra → Pruebas → Revisión → Integración
```

1. El agente de especificación crea o actualiza artefactos funcionales.
2. El agente de arquitectura define decisiones técnicas y divide tareas.
3. Los agentes ejecutores toman una tarea atómica.
4. El agente de pruebas valida el contrato y criterios de aceptación.
5. El agente revisor compara el resultado contra constitución, `SKILL.md` y contratos.
6. El agente integrador actualiza documentación y deja lista la siguiente tarea.

## Tareas atómicas permitidas

Una tarea atómica debe cumplir:

- Modifica un solo microdominio o una sola pantalla.
- Tiene entrada, salida y verificación claras.
- Puede completarse sin depender de decisiones abiertas.
- No mezcla refactor amplio con funcionalidad.
- No introduce secretos reales.

Ejemplos:

- Crear `.env.example` comentado con placeholders.
- Agregar modelo `CategoriaTarifa` y su migración.
- Crear endpoint `GET /api/parqueaderos/?lat=&lon=&radio=`.
- Crear hook `useDisponibilidadSocket`.
- Crear prototipo HTML de gestión de espacios.
- Agregar prueba de permiso para propietario.

## Definición de terminado para agentes

Una tarea se considera terminada cuando:

1. El código o documento está en la ruta acordada.
2. La tarea respeta los contratos.
3. Los errores se devuelven en español.
4. Los tests relevantes pasan o se documenta por qué no aplican.
5. No se versionan secretos, `.env`, archivos generados pesados ni credenciales.
6. La documentación afectada queda actualizada.
7. El agente incluye una nota corta de verificación.

## Entregables atomizados iniciales

### E01 — Base del monorepo e infraestructura mínima
- Crear carpetas `/backend`, `/frontend-web`, `/mobile`, `/docker`, `/docs`.
- Crear `.gitignore`.
- Crear `.env.example` comentado.
- Crear Docker Compose base.
- Crear scaffolding ASGI.

### E02 — Backend base
- Crear modelos principales.
- Crear índices.
- Configurar JWT.
- Crear serializers y ViewSets.
- Documentar OpenAPI.

### E03 — Tiempo real
- Configurar Channels + Redis.
- Crear consumer por parqueadero.
- Emitir evento `espacio_actualizado`.
- Probar cliente WebSocket.

### E04 — Mapas y cercanía
- Configurar tileserver-gl con extract Ecuador.
- Integrar Leaflet.
- Usar Nominatim público con debounce y rate limit.
- Crear endpoint de parqueaderos cercanos.

### E05 — Login y dashboard por roles
- Login web y móvil.
- Redirección administrador/propietario/anónimo.
- Protección de rutas.

### E06 — Registro y documentos
- Registro de usuario.
- Carga de documentos.
- Validación administrativa.

### E07 — Parqueadero
- Crear parqueadero.
- Editar configuración general.
- Cambiar disponibilidad.

### E08 — Tarifas
- Gestionar tarifa general, preferencial y pesados.
- Incorporar modelo `CategoriaTarifa`.

### E09 — Horarios
- Gestionar horarios por día.
- Validar rangos y duplicados.

### E10 — Espacios
- Crear, listar y cambiar estado de espacios.
- Sincronizar con tiempo real.

### E11 — Anónimos y búsqueda
- Ver mapa/listado sin iniciar sesión.
- Buscar y consultar detalle de parqueaderos.
