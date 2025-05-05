import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/components/utils/axios"; 
import { addToast } from "@heroui/react";
import { Bancal } from "@/types/cultivo/Bancal"; 

const API_URL = "http://127.0.0.1:8000/cultivo/Bancal/";

const fetchBancales = async (): Promise<Bancal[]> => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    throw new Error("No se encontró el token de autenticación.");
  }

  const response = await api.get(API_URL, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

const registrarBancal = async (bancal: Bancal) => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    throw new Error("No se encontró el token de autenticación.");
  }

  return api.post(API_URL, bancal, {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
};

export const useBancales = () => {
  return useQuery<Bancal[], Error>({
    queryKey: ["bancales"],
    queryFn: fetchBancales,
  });
};

export const useRegistrarBancal = () => {

  return useMutation({
    mutationFn: (bancal: Bancal) => registrarBancal(bancal),
    onSuccess: () => {
      addToast({
        title: "Éxito",
        description: "Bancal registrado con éxito",
      });
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
          description: "Error al registrar el bancal",
          timeout: 3000,
        });
      }
    },
  });
};

const actualizarBancal = async (id: number, bancal: any) => {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("No se encontró el token de autenticación.");

  try {
    const response = await api.put(`${API_URL}${id}/`, bancal, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error: any) {
    console.error("Error en la API:", error.response?.data);
    throw error;
  }
};

export const useActualizarBancal = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, bancal }: { id: number; bancal: any }) => actualizarBancal(id, bancal),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["bancales"] });
      addToast({ title: "Éxito", description: "Bancal actualizado con éxito", timeout: 3000 });
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
          description: "Error al actualizar el bancal",
          timeout: 3000,
        });
      }
    },
  });
};

const eliminarBancal = async (id: number) => {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("No se encontró el token de autenticación.");

  return api.delete(`${API_URL}${id}/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const useEliminarBancal = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => eliminarBancal(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["bancales"] });
      addToast({ title: "Éxito", description: "Bancal eliminado con éxito", timeout: 3000 });
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
          description: "Error al eliminar el bancal",
          timeout: 3000,
        });
      }
    },
  });
};
