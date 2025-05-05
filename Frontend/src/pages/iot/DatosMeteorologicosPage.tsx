import { useState, useMemo } from "react";
import DefaultLayout from "@/layouts/default";
import { useDatosMeteorologicosHistoricos } from "@/hooks/iot/useDatosMeteorologicosHistoricos";
import { useSensoresRegistrados } from "@/hooks/iot/useSensoresRegistrados";
import { useNavigate } from "react-router-dom";
import Tabla from "@/components/globales/Tabla";
import { Sensor, SensorData } from "@/types/iot/type";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";
import { ArrowLeft } from "lucide-react";
import {
  FaTemperatureHigh,
  FaTint,
  FaSun,
  FaCloudRain,
  FaWind,
  FaCompass,
  FaVial,
} from "react-icons/fa";

// Registrar los componentes de Chart.js
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function DatosMeteorologicosPage() {
  const [selectedDataType, setSelectedDataType] = useState<string | null>(null);
  const { data: historicos = [], isLoading, error } = useDatosMeteorologicosHistoricos(); // Eliminado 0, ""
  const { sensores = [], isLoading: sensoresLoading, error: sensoresError } = useSensoresRegistrados();
  const navigate = useNavigate();

  // Definir los tipos de datos que se pueden filtrar, con íconos
  const dataTypes = [
    { label: "Temperatura (°C)", key: "temperatura", icon: <FaTemperatureHigh className="text-red-500" /> },
    { label: "Humedad (%)", key: "humedad_ambiente", icon: <FaTint className="text-blue-500" /> },
    { label: "Humedad Suelo (%)", key: "humedad_suelo", icon: <FaTint className="text-blue-700" /> },
    { label: "Luminosidad (lux)", key: "luminosidad", icon: <FaSun className="text-yellow-500" /> },
    { label: "Lluvia (mm)", key: "lluvia", icon: <FaCloudRain className="text-gray-500" /> },
    { label: "Velocidad Viento (m/s)", key: "velocidad_viento", icon: <FaWind className="text-teal-500" /> },
    { label: "Dirección Viento (grados)", key: "direccion_viento", icon: <FaCompass className="text-green-500" /> },
    { label: "pH Suelo", key: "ph_suelo", icon: <FaVial className="text-purple-500" /> },
  ];

  // Columnas para la tabla
  const columns = [
    { name: "ID", uid: "id" },
    { name: "Sensor", uid: "sensor" },
    { name: selectedDataType ? dataTypes.find(dt => dt.key === selectedDataType)?.label || "Dato" : "Dato", uid: "value" },
    { name: "Fecha de Medición", uid: "fecha_medicion" },
  ];

  // Filtrar los datos históricos según el tipo de dato seleccionado
  const filteredHistoricos = useMemo(() => {
    let filtered = historicos;

    // Filtrar por tipo de dato seleccionado
    if (selectedDataType) {
      filtered = filtered.filter((dato: SensorData) => {
        const value = dato[selectedDataType as keyof SensorData];
        return value !== null && value !== undefined;
      });
    }

    return filtered;
  }, [historicos, selectedDataType]);

  // Formatear los datos para la tabla
  const formattedData = useMemo(() => {
    return filteredHistoricos.map((dato: SensorData) => ({
      id: dato.id || "N/A",
      sensor: sensores.find((s: Sensor) => s.id === dato.sensor)?.nombre || dato.sensor || "N/A", // Cambiado fk_sensor por sensor
      value: selectedDataType ? dato[selectedDataType as keyof SensorData] ?? "N/A" : "N/A",
      fecha_medicion: dato.fecha_medicion ? new Date(dato.fecha_medicion).toLocaleString() : "N/A",
    }));
  }, [filteredHistoricos, sensores, selectedDataType]);

  // Preparar datos para la gráfica histórica
  const chartData = useMemo(() => {
    if (!selectedDataType) return null;

    const labels = filteredHistoricos.map((dato: SensorData) =>
      dato.fecha_medicion ? new Date(dato.fecha_medicion).toLocaleString() : "N/A"
    );
    const dataValues = filteredHistoricos.map((dato: SensorData) => dato[selectedDataType as keyof SensorData] ?? 0);

    return {
      labels,
      datasets: [
        {
          label: dataTypes.find(dt => dt.key === selectedDataType)?.label || "Dato",
          data: dataValues,
          borderColor: "rgba(75, 192, 192, 1)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          fill: true,
          tension: 0.4,
        },
      ],
    };
  }, [filteredHistoricos, selectedDataType]);

  // Mostrar error en la consola y en la UI
  if (error || sensoresError) {
    console.error("Error en DatosMeteorologicosPage:", error || sensoresError);
  }

  return (
    <DefaultLayout>
      <div className="w-full flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-5xl">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Datos Meteorológicos Históricos</h2>

          {/* Botón de navegación */}
          <div className="mb-4 flex justify-start items-center gap-2">
            <button
              className="px-3 py-2 bg-green-600 text-white text-sm font-semibold rounded-lg hover:bg-green-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
              onClick={() => navigate("/iot/sensores")}
            >
              Volver a Tiempo Real
            </button>
          </div>

          {/* Botones de tipos de datos o vista detallada */}
          {selectedDataType ? (
            <div className="mb-4">
              {/* Botón de regreso */}
              <button
                className="flex items-center px-3 py-2 bg-gray-600 text-white text-sm font-semibold rounded-lg hover:bg-gray-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105 mb-4"
                onClick={() => setSelectedDataType(null)}
              >
                <ArrowLeft className="mr-2" size={16} />
                Volver a Tipos de Datos
              </button>

              {/* Lista de datos filtrados */}
              {formattedData.length === 0 ? (
                <p className="text-gray-600 text-center">
                  No hay datos disponibles para {dataTypes.find(dt => dt.key === selectedDataType)?.label}
                </p>
              ) : (
                <Tabla columns={columns} data={formattedData} />
              )}

              {/* Gráfica historica */}
              {chartData && (
                <div className="mt-6">
                  <h3 className="text-lg font-semibold text-gray-700 mb-4">
                    Gráfica Histórica - {dataTypes.find(dt => dt.key === selectedDataType)?.label}
                  </h3>
                  <Line
                    data={chartData}
                    options={{
                      responsive: true,
                      plugins: {
                        legend: { position: "top" },
                        title: { display: true, text: "Histórico de Datos" },
                      },
                      scales: {
                        x: { title: { display: true, text: "Fecha de Medición" } },
                        y: { title: { display: true, text: "Valor" } },
                      },
                    }}
                  />
                </div>
              )}
            </div>
          ) : (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-4">Seleccionar Tipo de Dato</h3>
              <div className="bg-white rounded-lg shadow-md p-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {dataTypes.map((type) => (
                  <button
                    key={type.key}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white text-sm font-semibold rounded-lg hover:bg-blue-600 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
                    onClick={() => setSelectedDataType(type.key)}
                  >
                    {type.icon}
                    <span>{type.label}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Mostrar mensaje de carga o error si no hay tipo de dato seleccionado */}
          {!selectedDataType && (
            <>
              {isLoading || sensoresLoading ? (
                <p className="text-gray-600 text-center">Cargando datos históricos...</p>
              ) : error || sensoresError ? (
                <p className="text-red-500 text-center">
                  Error al cargar datos: {(error || sensoresError)?.message} {/* Ajustado a .message */}
                </p>
              ) : null}
            </>
          )}
        </div>
      </div>
    </DefaultLayout>
  );
}