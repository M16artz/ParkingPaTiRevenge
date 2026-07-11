# Checklist de requisitos — Gestión de horarios de atención

## Calidad funcional

- [ ] La feature tiene propósito claro.
- [ ] Hay al menos una historia de usuario.
- [ ] Hay escenarios de aceptación para éxito, error y permisos.
- [ ] Los requisitos son verificables.
- [ ] El alcance fuera de MVP está declarado.

## Calidad técnica

- [ ] `plan.md` define componentes impactados.
- [ ] `research.md` justifica decisiones.
- [ ] `data-model.md` contiene entidades, relaciones y restricciones.
- [ ] `contracts/` contiene endpoints o contrato operativo verificable.
- [ ] Las tareas están atomizadas para agentes.

## Seguridad

- [ ] Se declara si el endpoint es público o privado.
- [ ] Los permisos por rol están definidos.
- [ ] No se requiere almacenar secretos reales.
- [ ] Los datos privados no se exponen a anónimos.

## UI/prototipo

- [ ] Existe al menos un HTML por pantalla clave.
- [ ] Existe al menos un PNG por pantalla clave.
- [ ] La pantalla contempla error/carga/estado vacío cuando aplique.

## Listo para implementación

- [ ] Un agente puede tomar una tarea sin pedir aclaraciones.
- [ ] Hay criterio de aceptación para cierre.
- [ ] Hay estrategia de verificación.
- [ ] La feature respeta la constitución.
