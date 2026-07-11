import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { DocumentoUploader } from "../../components/documentos/DocumentoUploader";
import { EstadoGeneralControl } from "../../components/parqueaderos/EstadoGeneralControl";
import { ParqueaderoForm } from "../../components/parqueaderos/ParqueaderoForm";
import { getDisponibilidadLabel } from "../../config/parqueaderoEstados";
import { listarDocumentos, reemplazarDocumento, subirDocumento, type Documento } from "../../services/documentoService";
import {
  cambiarEstadoParqueadero,
  crearParqueadero,
  editarParqueadero,
  listarMisParqueaderos,
  type DisponibilidadParqueadero,
  type Parqueadero,
  type ParqueaderoPayload,
} from "../../services/parqueaderoService";
import { useAuthStore } from "../../store/authStore";

export function PropietarioView() {
  const { profile, logout } = useAuthStore();
  const [documentos, setDocumentos] = useState<Documento[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [parqueaderos, setParqueaderos] = useState<Parqueadero[]>([]);
  const [parkingLoading, setParkingLoading] = useState(true);
  const [parkingSubmitting, setParkingSubmitting] = useState(false);
  const [parkingError, setParkingError] = useState("");
  const [parkingSuccess, setParkingSuccess] = useState("");
  const [selectedParqueaderoId, setSelectedParqueaderoId] = useState<number | null>(null);
  const documentoActual = useMemo(() => documentos[0], [documentos]);
  const parqueaderoActual = useMemo(
    () => parqueaderos.find((item) => item.id === selectedParqueaderoId) ?? parqueaderos[0],
    [parqueaderos, selectedParqueaderoId],
  );

  useEffect(() => {
    let active = true;
    setLoading(true);
    listarDocumentos()
      .then((items) => {
        if (active) setDocumentos(items);
      })
      .catch((err: Error) => {
        if (active) setError(err.message || "No se pudo consultar el estado del documento.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;
    setParkingLoading(true);
    listarMisParqueaderos()
      .then((items) => {
        if (!active) return;
        setParqueaderos(items);
        setSelectedParqueaderoId(items[0]?.id ?? null);
      })
      .catch((err: Error) => {
        if (active) setParkingError(err.message || "No se pudieron consultar tus parqueaderos.");
      })
      .finally(() => {
        if (active) setParkingLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  async function handleDocumentoSubmit(file: File) {
    setError("");
    setSuccess("");
    setSubmitting(true);
    try {
      const saved = documentoActual ? await reemplazarDocumento(documentoActual.id, file) : await subirDocumento(file);
      setDocumentos((current) => [saved, ...current.filter((item) => item.id !== saved.id)]);
      setSuccess("Documento recibido. Queda pendiente de validacion administrativa.");
    } catch (err) {
      const message = err instanceof Error ? err.message : "No se pudo subir el documento.";
      setError(`${message} Revisa el archivo e intenta nuevamente.`);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleParqueaderoSubmit(payload: ParqueaderoPayload) {
    setParkingError("");
    setParkingSuccess("");
    setParkingSubmitting(true);
    try {
      const saved = parqueaderoActual
        ? await editarParqueadero(parqueaderoActual.id, payload)
        : await crearParqueadero(payload);
      setParqueaderos((current) => [saved, ...current.filter((item) => item.id !== saved.id)]);
      setSelectedParqueaderoId(saved.id);
      setParkingSuccess(parqueaderoActual ? "Datos generales actualizados." : "Parqueadero creado correctamente.");
    } catch (err) {
      const message = err instanceof Error ? err.message : "No se pudo guardar el parqueadero.";
      setParkingError(`${message} Revisa los datos e intenta nuevamente.`);
    } finally {
      setParkingSubmitting(false);
    }
  }

  async function handleEstadoChange(disponibilidad: DisponibilidadParqueadero) {
    if (!parqueaderoActual) return;
    setParkingError("");
    setParkingSuccess("");
    setParkingSubmitting(true);
    try {
      const saved = await cambiarEstadoParqueadero(parqueaderoActual.id, disponibilidad);
      setParqueaderos((current) => current.map((item) => (item.id === saved.id ? saved : item)));
      setParkingSuccess(`Estado actualizado a ${getDisponibilidadLabel(saved.disponibilidad)}.`);
    } catch (err) {
      const message = err instanceof Error ? err.message : "No se pudo cambiar el estado.";
      setParkingError(`${message} Intenta nuevamente.`);
    } finally {
      setParkingSubmitting(false);
    }
  }

  return (
    <main className="shell">
      <section className="panel" aria-labelledby="owner-title">
        <p className="eyebrow">Propietario</p>
        <h1 id="owner-title">Panel de propietario</h1>
        <p className="summary">Sesion activa como {profile?.username}. Esta ruta requiere rol propietario.</p>
        <div className="owner-section">
          <h2>Configuracion general del parqueadero</h2>
          {parkingLoading ? <p className="summary">Consultando tus parqueaderos...</p> : null}
          {!parkingLoading && parqueaderos.length > 0 ? (
            <div className="parking-list">
              {parqueaderos.map((parqueadero) => (
                <button
                  className={`parking-item ${parqueadero.id === parqueaderoActual?.id ? "active" : ""}`}
                  key={parqueadero.id}
                  type="button"
                  onClick={() => setSelectedParqueaderoId(parqueadero.id)}
                >
                  <strong>{parqueadero.nombre}</strong>
                  <span>{getDisponibilidadLabel(parqueadero.disponibilidad)}</span>
                </button>
              ))}
            </div>
          ) : null}
          {!parkingLoading && !parqueaderoActual ? (
            <p className="summary">Crea tu primer parqueadero con datos generales, direccion y ubicacion.</p>
          ) : null}
          {parqueaderoActual ? (
            <div className="status-box">
              <strong>{parqueaderoActual.nombre}</strong>
              <span>
                {parqueaderoActual.direccion.calle_principal} · {parqueaderoActual.ubicacion.latitud},{" "}
                {parqueaderoActual.ubicacion.longitud}
              </span>
              <EstadoGeneralControl
                loading={parkingSubmitting}
                value={parqueaderoActual.disponibilidad}
                onChange={handleEstadoChange}
              />
            </div>
          ) : null}
          <ParqueaderoForm
            loading={parkingSubmitting}
            parqueadero={parqueaderoActual}
            onSubmit={handleParqueaderoSubmit}
          />
          {parkingError ? <p className="alert">{parkingError}</p> : null}
          {parkingSuccess ? <p className="success">{parkingSuccess}</p> : null}
        </div>
        <div className="document-status">
          <h2>Documento de validacion</h2>
          {loading ? <p className="summary">Consultando documento...</p> : null}
          {!loading && documentoActual ? (
            <div className={`status-box status-${documentoActual.estado.toLowerCase()}`}>
              <strong>{documentoActual.estado}</strong>
              <span>{documentoActual.nombre_original}</span>
              {documentoActual.estado === "PENDIENTE" ? (
                <p>Tu documento esta pendiente de revision administrativa.</p>
              ) : null}
              {documentoActual.estado === "VALIDADO" ? <p>Tu documento fue validado.</p> : null}
              {documentoActual.estado === "RECHAZADO" ? (
                <p>{documentoActual.motivo_rechazo || "El documento fue rechazado. Sube una version corregida."}</p>
              ) : null}
            </div>
          ) : null}
          {!loading && !documentoActual ? (
            <p className="summary">Sube un PDF, JPG o PNG para iniciar la validacion de tu cuenta.</p>
          ) : null}
          <DocumentoUploader documento={documentoActual} loading={submitting} onSubmit={handleDocumentoSubmit} />
          {error ? <p className="alert">{error}</p> : null}
          {success ? <p className="success">{success}</p> : null}
        </div>
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
