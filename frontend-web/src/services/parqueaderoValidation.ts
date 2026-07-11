import type { ParqueaderoPayload } from "./parqueaderoService";

export function validateParqueaderoPayload(payload: ParqueaderoPayload) {
  if (!payload.nombre.trim()) {
    return "Ingresa el nombre comercial del parqueadero.";
  }
  if (!payload.direccion.calle_principal.trim()) {
    return "Ingresa la calle principal de la direccion.";
  }

  const latitud = Number(payload.ubicacion.latitud);
  const longitud = Number(payload.ubicacion.longitud);
  if (!Number.isFinite(latitud) || latitud < -90 || latitud > 90) {
    return "Ingresa una latitud valida entre -90 y 90.";
  }
  if (!Number.isFinite(longitud) || longitud < -180 || longitud > 180) {
    return "Ingresa una longitud valida entre -180 y 180.";
  }

  return null;
}

