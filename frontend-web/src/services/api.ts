import { clearSession, loadRefreshToken } from "./sessionStorage";

let accessToken: string | null = null;
let refreshHandler: (() => Promise<string | null>) | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
}

export function getAccessToken() {
  return accessToken;
}

export function setRefreshHandler(handler: () => Promise<string | null>) {
  refreshHandler = handler;
}

export async function apiFetch<T>(url: string, options: RequestInit = {}, retry = true): Promise<T> {
  const headers = new Headers(options.headers);
  const isFormData = options.body instanceof FormData;
  if (!isFormData) {
    headers.set("Content-Type", headers.get("Content-Type") ?? "application/json");
  }
  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }

  const response = await fetch(url, { ...options, headers });
  if (response.status === 401 && retry && refreshHandler && loadRefreshToken()) {
    const nextAccess = await refreshHandler();
    if (nextAccess) {
      return apiFetch<T>(url, options, false);
    }
  }

  if (!response.ok) {
    if (response.status === 401) {
      setAccessToken(null);
      clearSession();
    }
    const payload = await safeJson(response);
    throw new Error(readErrorMessage(payload) ?? "No se pudo completar la solicitud. Intenta nuevamente.");
  }

  return response.json() as Promise<T>;
}

async function safeJson(response: Response): Promise<Record<string, unknown> | null> {
  try {
    return (await response.json()) as Record<string, unknown>;
  } catch {
    return null;
  }
}

function readErrorMessage(payload: Record<string, unknown> | null) {
  if (!payload) return null;
  if (typeof payload.detail === "string") return payload.detail;
  const firstValue = Object.values(payload)[0];
  if (Array.isArray(firstValue) && typeof firstValue[0] === "string") return firstValue[0];
  if (typeof firstValue === "string") return firstValue;
  return null;
}
