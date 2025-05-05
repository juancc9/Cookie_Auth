import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/components/utils/axios"; 
import { addToast } from "@heroui/react";
import { Cosecha } from "@/types/cultivo/Cosecha"; 

const API_URL = "http://127.0.0.1:8000/cultivo/cosechas/";

const fetchCosechas = async (): Promise<Cosecha[]> => {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("No se encontró el token de autenticación.");
  const response = await api.get(API_URL, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

const registrarCosecha = async (cosecha: Cosecha) => {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("No se encontró el token de autenticación.");

  const formData = new FormData();
  formData.append("id_cultivo", cosecha.id_cultivo.toString());
  formData.append("cantidad", cosecha.cantidad.toString());
  formData.append("unidades_de_medida", cosecha.unidades_de_medida);
  formData.append("fecha", cosecha.fecha);

  return api.post(API_URL, formData, {
    headers: {
      "Content-Type":"application/json",
      Authorization: `Bearer ${token}`,
    },
  });
};

const actualizarCosecha = async (id: number, cosecha: Cosecha) => {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("No se encontró el token de autenticación.");

  const formData = new FormData();
  formData.append("id_cultivo", cosecha.id_cultivo.toString());
  formData.append("cantidad", cosecha.cantidad.toString());
  formData.append("unidades_de_medida", cosecha.unidades_de_medida);
  formData.append("fecha", cosecha.fecha);

  return api.put(`${API_URL}${id}/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });
};

const eliminarCosecha = async (id: number) => {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("No se encontró el token de autenticación.");

  return api.delete(`${API_URL}${id}/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const useCosechas = () => {
  return useQuery<Cosecha[], Error>({
    queryKey: ["cosechas"],
    queryFn: fetchCosechas,
  });
};

export const useRegistrarCosecha = () => {
  return useMutation({
    mutationFn: registrarCosecha,
    onSuccess: () => {
      addToast({ title: "Éxito", description: "Cosecha registrada con éxito", timeout: 3000 });
    },
    onError: (error: any) => {
      if (error.response?.status === 403) {
        addToast({
          title: "Acceso denegado",
          description: "No tienes permiso para realizar esta acción, contacta a un adminstrador.",
          timeout: 3000,
        });
      } else {
        addToast({
          title: "Error",
          description: "Error al registrar la cosecha",
          timeout: 3000,
        });
      }
    },
  });
};

export const useActualizarCosecha = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, cosecha }: { id: number; cosecha: Cosecha }) => actualizarCosecha(id, cosecha),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cosechas"] });
      addToast({ title: "Éxito", description: "Cosecha actualizada con éxito", timeout: 3000 });
    },
    onError: (error: any) => {
      if (error.response?.status === 403) {
        addToast({
          title: "Acceso denegado",
          description: "No tienes permiso para realizar esta acción, contacta a un adminstrador.",
          timeout: 3000,
        });
      } else {
        addToast({
          title: "Error",
          description: "Error al actualizar la cosecha",
          timeout: 3000,
        });
      }
    },
  });
};

export const useEliminarCosecha = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => eliminarCosecha(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cosechas"] });
      addToast({ title: "Éxito", description: "Cosecha eliminada con éxito", timeout: 3000 });
    },
    onError: (error: any) => {
      if (error.response?.status === 403) {
        addToast({
          title: "Acceso denegado",
          description: "No tienes permiso para realizar esta acción, contacta a un adminstrador.",
          timeout: 3000,
        });
      } else {
        addToast({
          title: "Error",
          description: "Error al eliminar la cosecha",
          timeout: 3000,
        });
      }
    },
  });
};
