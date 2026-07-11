import { ChangeEvent, FormEvent, useState } from "react";

import type { Documento } from "../../services/documentoService";
import { validateDocumentoFile } from "../../services/documentoValidation";

type DocumentoUploaderProps = {
  documento?: Documento;
  loading?: boolean;
  onSubmit: (file: File) => Promise<void>;
};

export function DocumentoUploader({ documento, loading = false, onSubmit }: DocumentoUploaderProps) {
  const [file, setFile] = useState<File | null>(null);
  const [localError, setLocalError] = useState("");

  function onFileChange(event: ChangeEvent<HTMLInputElement>) {
    const selected = event.target.files?.[0] ?? null;
    setFile(selected);
    setLocalError(validateDocumentoFile(selected) ?? "");
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const validation = validateDocumentoFile(file);
    if (validation || !file) {
      setLocalError(validation ?? "Selecciona un documento valido para continuar.");
      return;
    }
    await onSubmit(file);
    setFile(null);
    event.currentTarget.reset();
  }

  return (
    <form className="document-uploader" onSubmit={submit}>
      <label>
        Documento de identidad o soporte legal
        <input accept=".pdf,.jpg,.jpeg,.png" name="archivo" type="file" onChange={onFileChange} />
      </label>
      {file ? (
        <p className="file-summary">
          {file.name} · {(file.size / 1024).toFixed(1)} KB
        </p>
      ) : null}
      {localError ? <p className="alert">{localError}</p> : null}
      <button className="button primary" disabled={loading || Boolean(localError)} type="submit">
        {loading ? "Enviando..." : documento ? "Reemplazar documento" : "Subir documento"}
      </button>
    </form>
  );
}

