import { useQuery } from "@tanstack/react-query";
import { useDatosMeteorologicosHistoricos } from "@/hooks/iot/useDatosMeteorologicosHistoricos";
import { useCultivos } from "@/hooks/cultivo/useCultivo";
import { addToast } from "@heroui/react";
import { EvapotranspiracionData } from "@/types/iot/type";
import { Cultivo } from "@/types/cultivo/Cultivo";

// Función para calcular la radiación extraterrestre (Ra) basada en latitud y día del año
const calculateRa = (latitude: number, dayOfYear: number): number => {
  const latRad = (latitude * Math.PI) / 180;
  const dr = 1 + 0.033 * Math.cos((2 * Math.PI * dayOfYear) / 365);
  const delta = 0.409 * Math.sin((2 * Math.PI * dayOfYear) / 365 - 1.39);
  const ws = Math.acos(-Math.tan(latRad) * Math.tan(delta));
  const Ra = (24 * 60 / Math.PI) * 0.082 * dr * (ws * Math.sin(latRad) * Math.sin(delta) + Math.cos(latRad) * Math.cos(delta) * Math.sin(ws));
  return Ra;
};

// Función para calcular ET0 usando el método de Hargreaves
const calculateET0 = (
  tMax: number,
  tMin: number,
  ra: number
): number => {
  const tMean = (tMax + tMin) / 2;
  const et0 = 0.0023 * (tMean + 17.8) * Math.sqrt(tMax - tMin) * ra;
  return et0;
};

// Hook principal
export const useEvapotranspiracion = (cultivoId: number) => {
  const { data: datosMeteorologicos = [], isLoading: isLoadingDatos, error: errorDatos } = useDatosMeteorologicosHistoricos();
  const { data: cultivos = [], isLoading: isLoadingCultivos, error: errorCultivos } = useCultivos(false);

  return useQuery<EvapotranspiracionData[], Error>({
    queryKey: ["evapotranspiracion", cultivoId],
    queryFn: async () => {
      if (errorDatos || errorCultivos) {
        addToast({ title: "Error", description: "Error al cargar datos necesarios para el cálculo de evapotranspiración" });
        throw new Error("Error al cargar datos necesarios para el cálculo de evapotranspiración");
      }

      const cultivo = cultivos.find((c: Cultivo) => c.id === cultivoId);
      if (!cultivo) {
        addToast({ title: "Error", description: "Cultivo no encontrado" });
        throw new Error("Cultivo no encontrado");
      }

      const { latitud, bancal } = cultivo;

      const et0Data: EvapotranspiracionData[] = datosMeteorologicos.map((dato) => {
        const fecha = new Date(dato.fecha);
        const dayOfYear = Math.floor(
          (fecha.getTime() - new Date(fecha.getFullYear(), 0, 0).getTime()) / 1000 / 60 / 60 / 24
        );

        const ra = calculateRa(latitud, dayOfYear);
        const tAvg = dato.temperatura;
        const tMax = tAvg + 2;
        const tMin = tAvg - 2;
        const et0 = calculateET0(tMax, tMin, ra);

        return {
          fecha: dato.fecha,
          et0,
          cultivoId,
          bancalId: bancal,
        };
      });

      addToast({ title: "Éxito", description: "Evapotranspiración calculada con éxito" });
      return et0Data;
    },
    enabled: !!datosMeteorologicos.length && !!cultivos.length && !isLoadingDatos && !isLoadingCultivos,
  });
};