export const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api",
  wsBaseUrl: import.meta.env.VITE_WS_BASE_URL ?? "ws://localhost:8000/ws",
  tileserverUrl:
    import.meta.env.VITE_TILESERVER_URL ??
    "http://localhost:3000/styles/osm-bright/{z}/{x}/{y}.png",
  nominatimUrl:
    import.meta.env.VITE_NOMINATIM_URL ?? "https://nominatim.openstreetmap.org",
};

