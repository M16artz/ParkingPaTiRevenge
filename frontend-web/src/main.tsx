import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { useEffect } from "react";

import { appRoutes } from "./config/routes";
import { ProtectedRoute } from "./routes/ProtectedRoute";
import { useAuthStore } from "./store/authStore";
import "./styles.css";
import { LoginView } from "./views/auth/LoginView";
import { RegisterView } from "./views/auth/RegisterView";
import { AdminView } from "./views/private/AdminView";
import { PropietarioView } from "./views/private/PropietarioView";
import { HomeView } from "./views/public/HomeView";

const queryClient = new QueryClient();

function App() {
  const initialize = useAuthStore((state) => state.initialize);
  useEffect(() => {
    void initialize();
  }, [initialize]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path={appRoutes.home} element={<HomeView />} />
        <Route path={appRoutes.login} element={<LoginView />} />
        <Route path={appRoutes.register} element={<RegisterView />} />
        <Route element={<ProtectedRoute allowedRoles={["ADMINISTRADOR"]} />}>
          <Route path={appRoutes.admin} element={<AdminView />} />
        </Route>
        <Route element={<ProtectedRoute allowedRoles={["PROPIETARIO"]} />}>
          <Route path={appRoutes.propietario} element={<PropietarioView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
);
