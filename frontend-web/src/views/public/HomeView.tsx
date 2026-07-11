import { Link, useLocation } from "react-router-dom";

import { appRoutes, getRedirectForRole } from "../../config/routes";
import { useAuthStore } from "../../store/authStore";

export function HomeView() {
  const { profile, isAuthenticated, logout } = useAuthStore();
  const location = useLocation();
  const unauthorized = Boolean(location.state && "unauthorized" in location.state);

  return (
    <main className="shell">
      <section className="panel" aria-labelledby="home-title">
        <p className="eyebrow">ParkingPaTi</p>
        <h1 id="home-title">Acceso seguro</h1>
        <p className="summary">
          Ingresa para acceder al area correspondiente a tu rol. La exploracion publica sigue
          disponible sin sesion.
        </p>

        {unauthorized ? (
          <p className="alert">No tienes permiso para esa ruta. Revisa tu rol o inicia otra sesion.</p>
        ) : null}

        <div className="actions">
          {isAuthenticated && profile ? (
            <>
              <Link className="button primary" to={getRedirectForRole(profile.rol)}>
                Ir a mi panel
              </Link>
              <button className="button" type="button" onClick={logout}>
                Cerrar sesion
              </button>
            </>
          ) : (
            <>
              <Link className="button primary" to={appRoutes.login}>
                Iniciar sesion
              </Link>
              <Link className="button" to={appRoutes.register}>
                Crear cuenta
              </Link>
            </>
          )}
        </div>
      </section>
    </main>
  );
}

