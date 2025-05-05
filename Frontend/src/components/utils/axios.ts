import axios from "axios";
import { addToast } from "@heroui/react";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // o la URL de tu backend
  withCredentials: true, // 🔑 Permite enviar cookies al backend
  headers: {
    "Content-Type": "application/json",
  },
});


api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 403) {
      addToast({
        title: "Acceso denegado",
        description: "No tienes permiso para acceder a este recurso.",
        timeout: 3000,
      });
    }

    if (error.response?.status === 401) {
      addToast({
        title: "No autenticado",
        description: "Tu sesión ha expirado. Inicia sesión de nuevo.",
        timeout: 3000,
      });
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

export default api;
