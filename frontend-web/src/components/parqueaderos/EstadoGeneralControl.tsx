import { disponibilidadOptions, getDisponibilidadLabel } from "../../config/parqueaderoEstados";
import type { DisponibilidadParqueadero } from "../../services/parqueaderoService";

type EstadoGeneralControlProps = {
  value: DisponibilidadParqueadero;
  loading?: boolean;
  onChange: (value: DisponibilidadParqueadero) => Promise<void>;
};

export function EstadoGeneralControl({ value, loading = false, onChange }: EstadoGeneralControlProps) {
  return (
    <div className="state-control" aria-label="Estado general del parqueadero">
      {disponibilidadOptions.map((option) => (
        <button
          className={`state-button ${option.value === value ? "active" : ""}`}
          disabled={loading || option.value === value}
          key={option.value}
          type="button"
          onClick={() => void onChange(option.value)}
          title={`Cambiar estado a ${getDisponibilidadLabel(option.value)}`}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

