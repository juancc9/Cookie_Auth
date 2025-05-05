import { useState, useEffect } from "react";
import DefaultLayout from "@/layouts/default";
import { useSensoresRegistrados } from "@/hooks/iot/useSensoresRegistrados";
import { useNavigate } from "react-router-dom";
import Tabla from "@/components/globales/Tabla";
import { Sensor, SensorData } from "@/types/iot/type";
import {
  FaTemperatureHigh,
  FaTint,
  FaSun,
  FaCloudRain,
  FaWind,
  FaCompass,
  FaVial,
} from "react-icons/fa";
import { ArrowLeft } from "lucide-react";

export default function SensoresPage() {
  const [selectedDataType, setSelectedDataType] = useState<string | null>(null);
  const [realTimeData, setRealTimeData] = useState<SensorData[]>([]);
  const { sensores = [] } = useSensoresRegistrados(); // Eliminado sensoresLoading y sensoresError
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

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/realtime/");

    ws.onopen = () => {
      console.log("Conexión WebSocket establecida");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("Datos en tiempo real recibidos:", message);
      if (message.type === "sensor_data") {
        setRealTimeData((prevData) => {
          const newData = [...prevData, message.data];
          return newData.slice(-50); 
        });
      }
    };

    ws.onerror = (error) => {
      console.error("Error en WebSocket:", error);
    };

    ws.onclose = () => {
      console.log("Conexión WebSocket cerrada");
    };

    return () => {
      ws.close();
    };
  }, []);

  const columns = [
    { name: "ID", uid: "id" },
    { name: "Sensor", uid: "sensor" },
    { name: selectedDataType ? dataTypes.find(dt => dt.key === selectedDataType)?.label || "Dato" : "Dato", uid: "value" },
    { name: "Fecha de Medición", uid: "fecha_medicion" },
  ];

  const filteredData = selectedDataType
    ? realTimeData.filter((dato: SensorData) => {
        const value = dato[selectedDataType as keyof SensorData];
        return value !== null && value !== undefined;
      })
    : realTimeData;

  const formattedData = filteredData.map((dato: SensorData) => ({
    id: dato.id || "N/A",
    sensor: sensores.find((s: Sensor) => s.id === dato.sensor)?.nombre || dato.sensor || "N/A",
    value: selectedDataType ? dato[selectedDataType as keyof SensorData] ?? "N/A" : "N/A",
    fecha_medicion: dato.fecha_medicion ? new Date(dato.fecha_medicion).toLocaleString() : "N/A",
  }));

  return (
    <DefaultLayout>
      <div className="w-full flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-5xl">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Datos Meteorológicos en Tiempo Real</h2>

          {/* Botón de navegación */}
          <div className="mb-4 flex justify-start items-center gap-2">
            <button
              className="px-3 py-2 bg-green-600 text-white text-sm font-semibold rounded-lg hover:bg-green-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
              onClick={() => navigate("/iot/datosmeteorologicos")}
            >
              Ver Datos Históricos
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
              {realTimeData.length === 0 ? (
                <p className="text-gray-600 text-center">Esperando datos en tiempo real...</p>
              ) : null}
            </>
          )}
        </div>
      </div>
    </DefaultLayout>
  );
}