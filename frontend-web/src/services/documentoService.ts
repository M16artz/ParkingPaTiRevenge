import { endpoints } from "../config/endpoints";
import { apiFetch } from "./api";

export type DocumentoEstado = "PENDIENTE" | "VALIDADO" | "RECHAZADO";

export type Documento = {
  id: number;
  cuenta: number;
  cuenta_username: string;
  estado: DocumentoEstado;
  es_valido: boolean;
  fecha_expiracion: string | null;
  nombre_original: string;
  content_type: string;
  tamano_bytes: number;
  motivo_rechazo: string;
  fecha_creacion: string;
  fecha_actualizacion: string;
};

export async function listarDocumentos() {
  return apiFetch<Documento[]>(endpoints.documentos.list);
}

export async function subirDocumento(file: File) {
  const formData = new FormData();
  formData.append("archivo", file);
  return apiFetch<Documento>(endpoints.documentos.list, {
    method: "POST",
    body: formData,
  });
}

export async function reemplazarDocumento(id: number, file: File) {
  const formData = new FormData();
  formData.append("archivo", file);
  return apiFetch<Documento>(endpoints.documentos.detail(id), {
    method: "PATCH",
    body: formData,
  });
}

export async function validarDocumento(id: number, estado: "VALIDADO" | "RECHAZADO", motivo_rechazo = "") {
  return apiFetch<Documento>(endpoints.documentos.validar(id), {
    method: "POST",
    body: JSON.stringify({ estado, motivo_rechazo }),
  });
}

