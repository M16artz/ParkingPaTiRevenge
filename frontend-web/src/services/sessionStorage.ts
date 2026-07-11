import type { AuthProfile } from "./authService";

const REFRESH_KEY = "parkingpati.refresh";
const PROFILE_KEY = "parkingpati.profile";

export function saveSession(refresh: string, profile: AuthProfile) {
  window.localStorage.setItem(REFRESH_KEY, refresh);
  window.localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
}

export function loadRefreshToken() {
  return window.localStorage.getItem(REFRESH_KEY);
}

export function loadProfile(): AuthProfile | null {
  const raw = window.localStorage.getItem(PROFILE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as AuthProfile;
  } catch {
    clearSession();
    return null;
  }
}

export function clearSession() {
  window.localStorage.removeItem(REFRESH_KEY);
  window.localStorage.removeItem(PROFILE_KEY);
}

