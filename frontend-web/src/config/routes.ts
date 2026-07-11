export type Role = "ADMINISTRADOR" | "PROPIETARIO" | "CONDUCTOR";

export const appRoutes = {
  home: "/",
  login: "/login",
  register: "/register",
  admin: "/admin",
  propietario: "/propietario",
};

export const protectedRoutes: Record<string, Role[]> = {
  [appRoutes.admin]: ["ADMINISTRADOR"],
  [appRoutes.propietario]: ["PROPIETARIO"],
};

export function getRedirectForRole(role?: Role | null) {
  if (role === "ADMINISTRADOR") return appRoutes.admin;
  if (role === "PROPIETARIO") return appRoutes.propietario;
  return appRoutes.home;
}

