import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/components/utils/axios"; // Este archivo debería estar configurado para usar withCredentials: true
import { addToast } from "@heroui/react";

const API_URL = "http://127.0.0.1:8000/usuarios/";

export interface Rol {
  id: number;
  rol: string;
}

export interface Usuario {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  username?: string;
  rol: Rol | null;
}

export interface UsuarioUpdate {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  username?: string;
  rol_id: number | null;
}

export const useUsuarios = () => {
  const queryClient = useQueryClient();

  // Fetch usuarios, asegurando que las cookies sean enviadas automáticamente
  const fetchUsuarios = async (): Promise<Usuario[]> => {
    const response = await api.get(`${API_URL}usuarios/`, { withCredentials: true });
    if (!Array.isArray(response.data)) {
      throw new Error("La API no devolvió un array de usuarios.");
    }
    return response.data;
  };

  const fetchRoles = async (): Promise<Rol[]> => {
    const response = await api.get(`${API_URL}roles/`, { withCredentials: true });
    if (!Array.isArray(response.data)) {
      throw new Error("La API no devolvió un array de roles.");
    }
    return response.data;
  };

  const updateUsuario = async (usuario: UsuarioUpdate): Promise<Usuario> => {
    const response = await api.put(`${API_URL}usuarios/${usuario.id}/`, usuario, { withCredentials: true });
    return response.data;
  };

  const deleteUsuario = async (id: number): Promise<void> => {
    await api.delete(`${API_URL}usuarios/${id}/`, { withCredentials: true });
  };

  // Consultas con react-query
  const usuariosQuery = useQuery<Usuario[], Error>({
    queryKey: ["usuarios"],
    queryFn: fetchUsuarios,
    retry: 1,
  });

  const rolesQuery = useQuery<Rol[], Error>({
    queryKey: ["roles"],
    queryFn: fetchRoles,
    retry: 1,
  });

  // Mutaciones para actualizar y eliminar usuarios
  const updateMutation = useMutation<Usuario, Error, UsuarioUpdate>({
    mutationFn: updateUsuario,
    onSuccess: (updatedUsuario) => {
      queryClient.setQueryData<Usuario[]>(["usuarios"], (oldData) =>
        oldData ? oldData.map((u) => (u.id === updatedUsuario.id ? updatedUsuario : u)) : [updatedUsuario]
      );
      queryClient.invalidateQueries({ queryKey: ["usuarios"] });
      addToast({ title: "Éxito", description: "Usuario actualizado con éxito", timeout: 3000, color: "success" });
    },
    onError: (error) => {
      addToast({ title: "Error", description: error.message || "Error al actualizar el usuario", timeout: 3000, color: "danger" });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteUsuario,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["usuarios"] });
      addToast({ title: "Éxito", description: "Usuario eliminado con éxito", timeout: 3000, color: "success" });
    },
    onError: () => {
      addToast({ title: "Error", description: "Error al eliminar el usuario", timeout: 3000, color: "danger" });
    },
  });

  return {
    ...usuariosQuery,
    roles: rolesQuery.data,
    isLoadingRoles: rolesQuery.isLoading,
    updateUsuario: updateMutation.mutateAsync,
    deleteUsuario: deleteMutation.mutate,
  };
};
