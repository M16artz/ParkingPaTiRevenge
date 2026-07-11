import { config } from "../config";

export const endpoints = {
  auth: {
    register: `${config.apiBaseUrl}/auth/register/`,
    token: `${config.apiBaseUrl}/auth/token/`,
    refresh: `${config.apiBaseUrl}/auth/refresh/`,
    me: `${config.apiBaseUrl}/cuentas/me/`,
  },
  documentos: {
    list: `${config.apiBaseUrl}/documentos/`,
    detail: (id: number) => `${config.apiBaseUrl}/documentos/${id}/`,
    validar: (id: number) => `${config.apiBaseUrl}/documentos/${id}/validar/`,
  },
  parqueaderos: {
    list: `${config.apiBaseUrl}/parqueaderos/`,
    mios: `${config.apiBaseUrl}/parqueaderos/mios/`,
    detail: (id: number) => `${config.apiBaseUrl}/parqueaderos/${id}/`,
    estado: (id: number) => `${config.apiBaseUrl}/parqueaderos/${id}/estado/`,
  },
};
