import { endpoints } from "../config/endpoints";
import { apiFetch } from "./api";

export type DisponibilidadParqueadero = "DISPONIBLE" | "CERRADO" | "LLENO";

export type DireccionPayload = {
  calle_principal: string;
  calle_secundaria?: string;
  nro_lote?: string;
};

export type UbicacionPayload = {
  latitud: string;
  longitud: string;
};

export type ParqueaderoPayload = {
  nombre: string;
  disponibilidad: DisponibilidadParqueadero;
  direccion: DireccionPayload;
  ubicacion: UbicacionPayload;
};

export type Parqueadero = ParqueaderoPayload & {
  id: number;
  propietario: number;
  propietario_username: string;
  estado: "ACTIVO" | "INACTIVO" | "SUSPENDIDO";
  validado: boolean;
  direccion: DireccionPayload & { id: number };
  ubicacion: UbicacionPayload & { id: number };
  fecha_creacion: string;
  fecha_actualizacion: string;
};

export async function listarMisParqueaderos() {
  return apiFetch<Parqueadero[]>(endpoints.parqueaderos.mios);
}

export async function crearParqueadero(payload: ParqueaderoPayload) {
  return apiFetch<Parqueadero>(endpoints.parqueaderos.list, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function editarParqueadero(id: number, payload: ParqueaderoPayload) {
  return apiFetch<Parqueadero>(endpoints.parqueaderos.detail(id), {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function cambiarEstadoParqueadero(id: number, disponibilidad: DisponibilidadParqueadero) {
  return apiFetch<Parqueadero>(endpoints.parqueaderos.estado(id), {
    method: "PATCH",
    body: JSON.stringify({ disponibilidad }),
  });
}

