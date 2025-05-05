import { useQuery } from "@tanstack/react-query";
import api from "@/components/utils/axios"; 
import { addToast } from "@heroui/react";
import { Ingreso } from "@/types/reportes/Ingreso";

const API_URL = "http://127.0.0.1:8000/finanzas/venta/datos_graficas/";

const fetchVentaGraficas = async (fechaInicio: string, fechaFin: string): Promise<Ingreso> => {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("No se encontró el token de autenticación.");
  
  const response = await api.get(API_URL, {
    params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin },
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const useVentaGraficas = (fechaInicio: string, fechaFin: string) => {
  return useQuery<Ingreso, Error>({
    queryKey: ["ventaGraficas", fechaInicio, fechaFin],
    queryFn: () => fetchVentaGraficas(fechaInicio, fechaFin),
    meta: {
      errorMessage: "Error al cargar los datos de ventas para las gráficas"
    },
    throwOnError: (error) => {
      addToast({ 
        title: "Error", 
        description: error.message || "Error al cargar los datos de ventas", 
        timeout: 3000 
      });
      return false; 
    }
  });
};