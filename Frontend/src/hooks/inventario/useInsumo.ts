import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api from "@/components/utils/axios"; 
import { addToast } from "@heroui/react";
import { Insumo, UnidadMedida, TipoInsumo } from "@/types/inventario/Insumo";

const API_URL = "http://127.0.0.1:8000/inventario/insumo/";

const fetchInsumos = async (): Promise<Insumo[]> => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    const response = await api.get(API_URL, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

export const useInsumos = () => {
    return useQuery({
        queryKey: ["insumos"],
        queryFn: fetchInsumos,
        staleTime: 1000 * 60,
    });
};

const fetchUnidadesMedida = async (): Promise<UnidadMedida[]> => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    const response = await api.get(`${API_URL}unidades_medida/`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

export const useUnidadesMedida = () => {
    return useQuery({
        queryKey: ["unidadesMedida"],
        queryFn: fetchUnidadesMedida,
        staleTime: 1000 * 60,
    });
};

const fetchTiposInsumo = async (): Promise<TipoInsumo[]> => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    const response = await api.get(`${API_URL}tipos_insumo/`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

export const useTiposInsumo = () => {
    return useQuery({
        queryKey: ["tiposInsumo"],
        queryFn: fetchTiposInsumo,
        staleTime: 1000 * 60,
    });
};

const registrarInsumo = async (insumo: Omit<Insumo, "id" | "unidad_medida" | "tipo_insumo" | "componentes"> & { unidad_medida_id?: number; tipo_insumo_id?: number; componentes_data?: { insumo_componente: number; cantidad: number }[] }) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    try {
        const response = await api.post(API_URL, insumo, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error: any) {
        console.error("Error en la API:", error.response?.data);
        throw error;
    }
};

export const useRegistrarInsumo = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (insumo: Omit<Insumo, "id" | "unidad_medida" | "tipo_insumo" | "componentes"> & { unidad_medida_id?: number; tipo_insumo_id?: number; componentes_data?: { insumo_componente: number; cantidad: number }[] }) => registrarInsumo(insumo),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["insumos"] });
            addToast({ title: "Éxito", description: "Insumo registrado con éxito", timeout: 3000 });
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
                description: "Error al registrar el insumo",
                timeout: 3000,
              });
            }
          },
        });
      };
  
interface ActualizarInsumoParams {
    id: number;
    insumo: Omit<Insumo, "unidad_medida" | "tipo_insumo" | "componentes"> & {
        unidad_medida_id?: number;
        tipo_insumo_id?: number;
        componentes_data?: { insumo_componente: number; cantidad: number }[];
    };
}

const actualizarInsumo = async (id: number, insumo: ActualizarInsumoParams["insumo"]) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    try {
        const response = await api.put(`${API_URL}${id}/`, insumo, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error: any) {
        console.error("Error en la API:", error.response?.data);
        throw error;
    }
};

export const useActualizarInsumo = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: ({ id, insumo }: ActualizarInsumoParams) => actualizarInsumo(id, insumo),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["insumos"] });
            addToast({ title: "Éxito", description: "Insumo actualizado con éxito", timeout: 3000 });
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
              description: "Error al actualizar el insumo",
              timeout: 3000,
            });
          }
        },
      });
    };



const eliminarInsumo = async (id: number) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    try {
        const response = await api.delete(`${API_URL}${id}/`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error: any) {
        console.error("Error en la API:", error.response?.data);
        throw error;
    }
};

export const useEliminarInsumo = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (id: number) => eliminarInsumo(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["insumos"] });
            addToast({ title: "Éxito", description: "Insumo eliminado con éxito", timeout: 3000 });
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
                description: "Error al eliminar el insumo",
                timeout: 3000,
              });
            }
          },
        });
      };
  
const crearUnidadMedida = async (unidad: Omit<UnidadMedida, "id" | "fecha_creacion" | "creada_por_usuario">) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    try {
        const response = await api.post(`${API_URL}crear_unidad_medida/`, unidad, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error: any) {
        console.error("Error en la API:", error.response?.data);
        throw error;
    }
};

export const useCrearUnidadMedida = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (unidad: Omit<UnidadMedida, "id" | "fecha_creacion" | "creada_por_usuario">) => crearUnidadMedida(unidad),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["unidadesMedida"] });
            addToast({ title: "Éxito", description: "Unidad de medida creada con éxito", timeout: 3000 });
        },
        onError: (error: any) => {
            addToast({
                title: "Error",
                description: error.response?.data?.message || "Error al crear la unidad de medida",
                timeout: 3000,
            });
        },
    });
};

const crearTipoInsumo = async (tipo: Omit<TipoInsumo, "id" | "fecha_creacion" | "creada_por_usuario">) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    try {
        const response = await api.post(`${API_URL}crear_tipo_insumo/`, tipo, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error: any) {
        console.error("Error en la API:", error.response?.data);
        throw error;
    }
};

export const useCrearTipoInsumo = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (tipo: Omit<TipoInsumo, "id" | "fecha_creacion" | "creada_por_usuario">) => crearTipoInsumo(tipo),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["tiposInsumo"] });
            addToast({ title: "Éxito", description: "Tipo de insumo creado con éxito", timeout: 3000 });
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
                description: "Error al crear el insumo",
                timeout: 3000,
              });
            }
          },
        });
      };
  
const usarEnActividad = async (id: number, data: { cantidad_usada: number; actividad_id?: number }) => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    try {
        const response = await api.post(`${API_URL}${id}/usar_en_actividad/`, data, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error: any) {
        console.error("Error en la API:", error.response?.data);
        throw error;
    }
};

export const useUsarEnActividad = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: { cantidad_usada: number; actividad_id?: number } }) => usarEnActividad(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["insumos"] });
            addToast({ title: "Éxito", description: "Insumo usado en actividad con éxito", timeout: 3000 });
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
                description: "Error al usar el insumo en la actividad",
                timeout: 3000,
              });
            }
          },
        });
      };
  
const descargarReportePDF = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No se encontró el token de autenticación.");

    try {
        const response = await api.get(`${API_URL}reporte_pdf/`, {
            headers: { Authorization: `Bearer ${token}` },
            responseType: 'blob',
        });
        return response.data;
    } catch (error: any) {
        console.error("Error en la API:", error.response?.data);
        throw error;
    }
};

export const useReportePDF = () => {
    return useMutation({
        mutationFn: descargarReportePDF,
        onSuccess: (data) => {
            const url = window.URL.createObjectURL(new Blob([data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'reporte_insumos.pdf');
            document.body.appendChild(link);
            link.click();
            link.remove();
            addToast({ title: "Éxito", description: "Reporte PDF descargado con éxito", timeout: 3000 });
        },
        onError: (error: any) => {
            addToast({
                title: "Error",
                description: error.response?.data?.message || "Error al descargar el reporte PDF",
                timeout: 3000,
            });
        },
    });
};