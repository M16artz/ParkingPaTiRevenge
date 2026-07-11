import { endpoints } from "../config/endpoints";
import { apiFetch, setAccessToken, setRefreshHandler } from "./api";
import { clearSession, loadProfile, loadRefreshToken, saveSession } from "./sessionStorage";
import type { Role } from "../config/routes";

export type AuthProfile = {
  id: number;
  username: string;
  correo: string;
  rol: Role;
  estado: string;
};

export type LoginResponse = {
  access: string;
  refresh: string;
  cuenta: AuthProfile;
};

export type RegisterPayload = {
  nombre: string;
  apellido: string;
  tipo_identificacion: "CEDULA" | "RUC" | "PASAPORTE";
  identificacion: string;
  username: string;
  correo: string;
  password: string;
  rol?: "PROPIETARIO" | "CONDUCTOR";
};

export type LoginPayload = {
  username: string;
  password: string;
};

export async function register(payload: RegisterPayload) {
  const response = await postJson<AuthProfile>(endpoints.auth.register, payload);
  return response;
}

export async function login(payload: LoginPayload) {
  const response = await postJson<LoginResponse>(endpoints.auth.token, payload);
  setAccessToken(response.access);
  saveSession(response.refresh, response.cuenta);
  return response;
}

export async function refreshAccessToken() {
  const refresh = loadRefreshToken();
  if (!refresh) return null;
  try {
    const response = await postJson<{ access: string }>(endpoints.auth.refresh, { refresh });
    setAccessToken(response.access);
    return response.access;
  } catch {
    logout();
    return null;
  }
}

export async function me() {
  return apiFetch<AuthProfile>(endpoints.auth.me);
}

export function restoreCachedProfile() {
  return loadProfile();
}

export function logout() {
  setAccessToken(null);
  clearSession();
}

async function postJson<T>(url: string, payload: unknown): Promise<T> {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(data?.detail ?? "No se pudo completar la solicitud. Revisa los datos e intenta nuevamente.");
  }
  return data as T;
}

setRefreshHandler(refreshAccessToken);

