import { create } from "zustand";

import { getRedirectForRole } from "../config/routes";
import * as authService from "../services/authService";
import type { AuthProfile, LoginPayload, RegisterPayload } from "../services/authService";

type AuthState = {
  profile: AuthProfile | null;
  initialized: boolean;
  error: string | null;
  isAuthenticated: boolean;
  initialize: () => Promise<void>;
  login: (payload: LoginPayload) => Promise<string>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
  profile: null,
  initialized: false,
  error: null,
  isAuthenticated: false,

  initialize: async () => {
    const cached = authService.restoreCachedProfile();
    if (!cached) {
      set({ initialized: true, profile: null, isAuthenticated: false });
      return;
    }
    const access = await authService.refreshAccessToken();
    if (!access) {
      set({ initialized: true, profile: null, isAuthenticated: false });
      return;
    }
    try {
      const profile = await authService.me();
      set({ initialized: true, profile, isAuthenticated: true });
    } catch {
      authService.logout();
      set({ initialized: true, profile: null, isAuthenticated: false });
    }
  },

  login: async (payload) => {
    set({ error: null });
    try {
      const response = await authService.login(payload);
      set({ profile: response.cuenta, isAuthenticated: true });
      return getRedirectForRole(response.cuenta.rol);
    } catch (error) {
      const message = error instanceof Error ? error.message : "No se pudo iniciar sesion.";
      set({ error: message, isAuthenticated: false });
      throw error;
    }
  },

  register: async (payload) => {
    set({ error: null });
    try {
      await authService.register(payload);
    } catch (error) {
      const message = error instanceof Error ? error.message : "No se pudo registrar la cuenta.";
      set({ error: message });
      throw error;
    }
  },

  logout: () => {
    authService.logout();
    set({ profile: null, isAuthenticated: false, error: null });
  },
}));

