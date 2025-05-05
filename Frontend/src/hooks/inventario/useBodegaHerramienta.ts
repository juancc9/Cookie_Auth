import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api from "@/components/utils/axios"; 
import { addToast } from "@heroui/react";
import { BodegaHerramienta } from "@/types/inventario/BodegaHerramienta";

const API_URL = "http://127.0.0.1:8000/inventario/bodega_herramienta/";

const fetchBodegaHerramienta = async (): Promise<BodegaHerramienta[]> => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    const response = await api.get(API_URL, {
        headers: { Authorization: `Bearer ${token}` },
    });

    return response.data;
};

export const useBodegaHerramienta = () => {
    return useQuery<BodegaHerramienta[], Error>({
        queryKey: ["bodegaHerramienta"],
        queryFn: fetchBodegaHerramienta,
        staleTime: 1000 * 60,
    });
};

const registrarBodegaHerramienta = async ({ bodega, herramienta, cantidad }: Omit<BodegaHerramienta, "id">) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    const payload = {
        bodega,
        herramienta: Number(herramienta),  
        cantidad,
    };

    const response = await api.post(API_URL, payload, {
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });

    return response.data;
};

export const useRegistrarBodegaHerramienta = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: registrarBodegaHerramienta,
        onSuccess: () => {
            addToast({ title: "Éxito", description: "Registro guardado con éxito" });
            queryClient.invalidateQueries({ queryKey: ["bodegaHerramienta"] });
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
                description: "Error al registrar",
                timeout: 3000,
              });
            }
          },
        });
      };

const actualizarBodegaHerramienta = async ({ id, bodega, herramienta, cantidad }: BodegaHerramienta) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    const payload = {
        bodega,
        herramienta: Number(herramienta), 
        cantidad,
    };

    const response = await api.put(`${API_URL}${id}/`, payload, {
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });

    return response.data;
};

export const useActualizarBodegaHerramienta = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: actualizarBodegaHerramienta,
        onSuccess: () => {
            addToast({ title: "Éxito", description: "Registro actualizado con éxito" });
            queryClient.invalidateQueries({ queryKey: ["bodegaHerramienta"] });
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
                description: "Error al actualizar",
                timeout: 3000,
              });
            }
          },
        });
      };

const eliminarBodegaHerramienta = async (id: number) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    await api.delete(`${API_URL}${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
    });
};

export const useEliminarBodegaHerramienta = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: eliminarBodegaHerramienta,
        onSuccess: () => {
            addToast({ title: "Éxito", description: "Registro eliminado con éxito" });
            queryClient.invalidateQueries({ queryKey: ["bodegaHerramienta"] });
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
                description: "Error al eliminar el registro",
                timeout: 3000,
              });
            }
          },
        });
      };
