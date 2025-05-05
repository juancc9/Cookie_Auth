import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api from "@/components/utils/axios"; 
import { addToast } from "@heroui/react";
import { Bodega } from "@/types/inventario/Bodega";

const API_URL = "http://127.0.0.1:8000/inventario/bodega/";

const fetchBodegas = async (): Promise<Bodega[]> => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    const response = await api.get(API_URL, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

export const useBodegas = () => {
    return useQuery<Bodega[], Error>({
        queryKey: ["bodegas"],
        queryFn: fetchBodegas,
        staleTime: 1000 * 60,
    });
};

const registrarBodega = async (bodega: Bodega) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    const response = await api.post(API_URL, bodega, {
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};

export const useRegistrarBodega = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: registrarBodega,
        onSuccess: () => {
            addToast({ title: "Éxito", description: "Bodega registrada con éxito" });
            queryClient.invalidateQueries({ queryKey: ["bodegas"] });
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
                description: "Error al registrar la bodega",
                timeout: 3000,
              });
            }
          },
        });
      };

const actualizarBodega = async (bodega: Bodega) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    const response = await api.put(`${API_URL}${bodega.id}/`, bodega, {
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};

export const useActualizarBodega = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: actualizarBodega,
        onSuccess: () => {
            addToast({ title: "Éxito", description: "Bodega actualizada con éxito" });
            queryClient.invalidateQueries({ queryKey: ["bodegas"] });
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
                description: "Error al actualizar la bodega",
                timeout: 3000,
              });
            }
          },
        });
      };

const eliminarBodega = async (id: number) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    await api.delete(`${API_URL}${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
    });
};

export const useEliminarBodega = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: eliminarBodega,
        onSuccess: () => {
            addToast({ title: "Éxito", description: "Bodega eliminada con éxito" });
            queryClient.invalidateQueries({ queryKey: ["bodegas"] });
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
                description: "Error al eliminar la bodega",
                timeout: 3000,
              });
            }
          },
        });
      };


      