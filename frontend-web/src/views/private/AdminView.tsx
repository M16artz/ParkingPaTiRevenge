import { Link } from "react-router-dom";

import { useAuthStore } from "../../store/authStore";

export function AdminView() {
  const { profile, logout } = useAuthStore();

  return (
    <main className="shell">
      <section className="panel" aria-labelledby="admin-title">
        <p className="eyebrow">Administracion</p>
        <h1 id="admin-title">Panel de administracion</h1>
        <p className="summary">Sesion activa como {profile?.username}. Esta ruta requiere rol administrador.</p>
        <div className="actions">
          <Link className="button" to="/">
            Inicio
          </Link>
          <button className="button" type="button" onClick={logout}>
            Cerrar sesion
          </button>
        </div>
      </section>
    </main>
  );
}

