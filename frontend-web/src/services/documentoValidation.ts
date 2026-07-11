const allowedExtensions = new Set(["pdf", "jpg", "jpeg", "png"]);
export const maxDocumentoBytes = 5 * 1024 * 1024;

export function validateDocumentoFile(file: File | null) {
  if (!file) {
    return "Selecciona un documento PDF, JPG o PNG para continuar.";
  }

  const extension = file.name.split(".").pop()?.toLowerCase() ?? "";
  if (!allowedExtensions.has(extension)) {
    return "El documento debe ser PDF, JPG o PNG. Selecciona un archivo valido.";
  }

  if (file.size > maxDocumentoBytes) {
    return "El documento supera el tamano maximo de 5 MB. Reduce el archivo e intenta nuevamente.";
  }

  return null;
}

