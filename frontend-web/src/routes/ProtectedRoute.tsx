import { Navigate, Outlet, useLocation } from "react-router-dom";

import { appRoutes, type Role } from "../config/routes";
import { useAuthStore } from "../store/authStore";

type ProtectedRouteProps = {
  allowedRoles?: Role[];
};

export function ProtectedRoute({ allowedRoles }: ProtectedRouteProps) {
  const location = useLocation();
  const { initialized, isAuthenticated, profile } = useAuthStore();

  if (!initialized) {
    return <main className="shell">Cargando sesion...</main>;
  }

  if (!isAuthenticated || !profile) {
    return <Navigate to={appRoutes.login} replace state={{ from: location.pathname }} />;
  }

  if (allowedRoles && !allowedRoles.includes(profile.rol)) {
    return <Navigate to="/" replace state={{ unauthorized: true }} />;
  }

  return <Outlet />;
}

