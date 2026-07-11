// Cliente de prueba WebSocket para ParkingPaTi.
// Uso esperado en navegador o Node con librería WebSocket:
//   const parqueaderoId = 1;
//   const ws = new WebSocket(`ws://localhost:8000/ws/parqueaderos/${parqueaderoId}/`);

const parqueaderoId = 1;
const url = `ws://localhost:8000/ws/parqueaderos/${parqueaderoId}/`;

const socket = new WebSocket(url);

socket.addEventListener("open", () => {
  console.log("[ParkingPaTi WS] conectado:", url);
});

socket.addEventListener("message", (event) => {
  const payload = JSON.parse(event.data);
  console.log("[ParkingPaTi WS] evento recibido:", payload);

  if (!payload.espacio_id || !payload.estado) {
    console.error("Payload inválido: faltan espacio_id o estado");
  }
});

socket.addEventListener("close", () => {
  console.log("[ParkingPaTi WS] conexión cerrada");
});

socket.addEventListener("error", (error) => {
  console.error("[ParkingPaTi WS] error:", error);
});
