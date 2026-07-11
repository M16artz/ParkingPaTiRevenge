import { FormEvent, useEffect, useState } from "react";

import { disponibilidadOptions } from "../../config/parqueaderoEstados";
import type { Parqueadero, ParqueaderoPayload } from "../../services/parqueaderoService";
import { validateParqueaderoPayload } from "../../services/parqueaderoValidation";

type ParqueaderoFormProps = {
  parqueadero?: Parqueadero;
  loading?: boolean;
  onSubmit: (payload: ParqueaderoPayload) => Promise<void>;
};

const emptyPayload: ParqueaderoPayload = {
  nombre: "",
  disponibilidad: "CERRADO",
  direccion: {
    calle_principal: "",
    calle_secundaria: "",
    nro_lote: "",
  },
  ubicacion: {
    latitud: "-3.993130",
    longitud: "-79.204220",
  },
};

export function ParqueaderoForm({ parqueadero, loading = false, onSubmit }: ParqueaderoFormProps) {
  const [form, setForm] = useState<ParqueaderoPayload>(emptyPayload);
  const [localError, setLocalError] = useState("");

  useEffect(() => {
    if (!parqueadero) {
      setForm(emptyPayload);
      return;
    }
    setForm({
      nombre: parqueadero.nombre,
      disponibilidad: parqueadero.disponibilidad,
      direccion: {
        calle_principal: parqueadero.direccion.calle_principal,
        calle_secundaria: parqueadero.direccion.calle_secundaria ?? "",
        nro_lote: parqueadero.direccion.nro_lote ?? "",
      },
      ubicacion: {
        latitud: String(parqueadero.ubicacion.latitud),
        longitud: String(parqueadero.ubicacion.longitud),
      },
    });
  }, [parqueadero]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const validation = validateParqueaderoPayload(form);
    if (validation) {
      setLocalError(validation);
      return;
    }
    setLocalError("");
    await onSubmit(form);
  }

  return (
    <form className="form compact-form" onSubmit={submit}>
      <label>
        Nombre comercial
        <input
          required
          value={form.nombre}
          onChange={(event) => setForm({ ...form, nombre: event.target.value })}
        />
      </label>
      <label>
        Estado general
        <select
          value={form.disponibilidad}
          onChange={(event) =>
            setForm({ ...form, disponibilidad: event.target.value as ParqueaderoPayload["disponibilidad"] })
          }
        >
          {disponibilidadOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>
      <div className="field-row">
        <label>
          Calle principal
          <input
            required
            value={form.direccion.calle_principal}
            onChange={(event) =>
              setForm({ ...form, direccion: { ...form.direccion, calle_principal: event.target.value } })
            }
          />
        </label>
        <label>
          Calle secundaria
          <input
            value={form.direccion.calle_secundaria}
            onChange={(event) =>
              setForm({ ...form, direccion: { ...form.direccion, calle_secundaria: event.target.value } })
            }
          />
        </label>
      </div>
      <div className="field-row">
        <label>
          Nro. lote
          <input
            value={form.direccion.nro_lote}
            onChange={(event) => setForm({ ...form, direccion: { ...form.direccion, nro_lote: event.target.value } })}
          />
        </label>
        <label>
          Latitud
          <input
            required
            inputMode="decimal"
            value={form.ubicacion.latitud}
            onChange={(event) => setForm({ ...form, ubicacion: { ...form.ubicacion, latitud: event.target.value } })}
          />
        </label>
      </div>
      <label>
        Longitud
        <input
          required
          inputMode="decimal"
          value={form.ubicacion.longitud}
          onChange={(event) => setForm({ ...form, ubicacion: { ...form.ubicacion, longitud: event.target.value } })}
        />
      </label>
      {localError ? <p className="alert">{localError}</p> : null}
      <button className="button primary" disabled={loading} type="submit">
        {loading ? "Guardando..." : parqueadero ? "Guardar cambios" : "Crear parqueadero"}
      </button>
    </form>
  );
}

