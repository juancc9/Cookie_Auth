import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/components/utils/axios";
import { addToast } from "@heroui/react";
import { Afeccion, AfeccionDetalle } from "@/types/cultivo/Afeccion";

const API_URL = "http://127.0.0.1:8000/cultivo/afecciones/";

const fetchAfecciones = async (): Promise<AfeccionDetalle[]> => {
  const token = localStorage.getItem("access_token");
  const response = await api.get(API_URL, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

const fetchAfeccion = async (id: number): Promise<AfeccionDetalle> => {
  const token = localStorage.getItem("access_token");
  const response = await api.get(`${API_URL}${id}/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

const crearAfeccion = async (afeccion: Omit<Afeccion, 'id' | 'estado'>) => {
  const token = localStorage.getItem("access_token");
  return api.post(API_URL, afeccion, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

const actualizarAfeccion = async (id: number, afeccion: Partial<Afeccion>) => {
  const token = localStorage.getItem("access_token");
  return api.patch(`${API_URL}${id}/`, afeccion, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

const cambiarEstadoAfeccion = async (id: number, estado: 'ST' | 'EC' | 'EL') => {
  const token = localStorage.getItem("access_token");
  return api.post(`${API_URL}${id}/cambiar_estado/`, { estado }, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const useAfecciones = () => {
  return useQuery<AfeccionDetalle[], Error>({
    queryKey: ["afecciones"],
    queryFn: fetchAfecciones,
  });
};

export const useAfeccion = (id: number) => {
  return useQuery<AfeccionDetalle, Error>({
    queryKey: ["afeccion", id],
    queryFn: () => fetchAfeccion(id),
    enabled: !!id,
  });
};

export const useCrearAfeccion = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: crearAfeccion,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["afecciones"] });
      addToast({
        title: "Éxito",
        description: "Afección registrada correctamente",
        timeout: 3000,
      });
    },
  });
};

export const useActualizarAfeccion = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, afeccion }: { id: number; afeccion: Partial<Afeccion> }) => 
      actualizarAfeccion(id, afeccion),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["afecciones"] });
      addToast({
        title: "Éxito",
        description: "Afección actualizada correctamente",
        timeout: 3000,
      });
    },
  });
};

export const useCambiarEstadoAfeccion = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, estado }: { id: number; estado: 'ST' | 'EC' | 'EL' }) => 
      cambiarEstadoAfeccion(id, estado),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["afecciones"] });
      addToast({
        title: "Éxito",
        description: "Estado de afección actualizado",
        timeout: 3000,
      });
    },
  });
};