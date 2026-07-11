import { FormEvent, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { appRoutes } from "../../config/routes";
import { useAuthStore } from "../../store/authStore";

export function LoginView() {
  const navigate = useNavigate();
  const location = useLocation();
  const login = useAuthStore((state) => state.login);
  const error = useAuthStore((state) => state.error);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    try {
      const redirect = await login({ username, password });
      const from = (location.state as { from?: string } | null)?.from;
      navigate(from && from !== appRoutes.login ? from : redirect, { replace: true });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <section className="panel form-panel" aria-labelledby="login-title">
        <p className="eyebrow">Sesion</p>
        <h1 id="login-title">Iniciar sesion</h1>
        <form className="form" onSubmit={onSubmit}>
          <label>
            Usuario o correo
            <input value={username} onChange={(event) => setUsername(event.target.value)} required />
          </label>
          <label>
            Contrasena
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </label>
          {error ? <p className="alert">{error}</p> : null}
          <button className="button primary" disabled={loading} type="submit">
            {loading ? "Ingresando..." : "Ingresar"}
          </button>
        </form>
        <p className="footnote">
          <Link to={appRoutes.register}>Crear una cuenta base</Link>
        </p>
      </section>
    </main>
  );
}

