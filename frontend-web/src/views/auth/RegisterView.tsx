import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { appRoutes } from "../../config/routes";
import { useAuthStore } from "../../store/authStore";

export function RegisterView() {
  const navigate = useNavigate();
  const register = useAuthStore((state) => state.register);
  const error = useAuthStore((state) => state.error);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    setLoading(true);
    try {
      await register({
        nombre: String(form.get("nombre")),
        apellido: String(form.get("apellido")),
        tipo_identificacion: "CEDULA",
        identificacion: String(form.get("identificacion")),
        username: String(form.get("username")),
        correo: String(form.get("correo")),
        password: String(form.get("password")),
        rol: form.get("rol") === "PROPIETARIO" ? "PROPIETARIO" : "CONDUCTOR",
      });
      setSuccess(true);
      window.setTimeout(() => navigate(appRoutes.login), 700);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <section className="panel form-panel" aria-labelledby="register-title">
        <p className="eyebrow">Registro</p>
        <h1 id="register-title">Crear cuenta de propietario</h1>
        <form className="form" onSubmit={onSubmit}>
          <div className="field-row">
            <label>
              Nombre
              <input name="nombre" required />
            </label>
            <label>
              Apellido
              <input name="apellido" required />
            </label>
          </div>
          <label>
            Identificacion
            <input name="identificacion" required />
          </label>
          <label>
            Usuario
            <input name="username" required />
          </label>
          <label>
            Correo
            <input name="correo" type="email" required />
          </label>
          <label>
            Contrasena
            <input name="password" type="password" minLength={8} required />
          </label>
          <label>
            Rol
            <select name="rol" defaultValue="PROPIETARIO">
              <option value="PROPIETARIO">Propietario</option>
              <option value="CONDUCTOR">Conductor</option>
            </select>
          </label>
          {error ? <p className="alert">{error}</p> : null}
          {success ? <p className="success">Cuenta creada. Inicia sesion para subir tu documento.</p> : null}
          <button className="button primary" disabled={loading} type="submit">
            {loading ? "Creando..." : "Crear cuenta"}
          </button>
        </form>
        <p className="footnote">
          <Link to={appRoutes.login}>Ya tengo cuenta</Link>
        </p>
      </section>
    </main>
  );
}
