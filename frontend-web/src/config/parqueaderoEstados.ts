import type { DisponibilidadParqueadero } from "../services/parqueaderoService";

export const disponibilidadOptions: Array<{ value: DisponibilidadParqueadero; label: string }> = [
  { value: "DISPONIBLE", label: "Abierto" },
  { value: "CERRADO", label: "Cerrado" },
  { value: "LLENO", label: "Lleno" },
];

export function getDisponibilidadLabel(value: DisponibilidadParqueadero) {
  return disponibilidadOptions.find((option) => option.value === value)?.label ?? value;
}

