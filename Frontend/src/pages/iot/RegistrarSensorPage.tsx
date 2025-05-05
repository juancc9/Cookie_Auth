import { useState } from "react";
import DefaultLayout from "@/layouts/default";
import { ReuInput } from "@/components/globales/ReuInput";
import { useNavigate } from "react-router-dom";
import { Sensor } from "@/types/iot/type";

const sensorTypes = [
  { value: "temperatura", label: "Temperatura (°C)" },
  { value: "ambient_humidity", label: "Humedad Ambiente (%)" },
  { value: "soil_humidity", label: "Humedad Suelo (%)" },
  { value: "luminosidad", label: "Luminosidad (lux)" },
  { value: "lluvia", label: "Lluvia (mm/h)" },
  { value: "velocidad_viento", label: "Velocidad Viento (m/s)" },
  { value: "direccion_viento", label: "Dirección Viento (grados)" },
  { value: "ph_suelo", label: "pH Suelo (pH)" },
];

const sensorConfigurations: { [key: string]: { unidad_medida: string; medida_minima: number; medida_maxima: number } } = {
  temperatura: { unidad_medida: "°C", medida_minima: -40, medida_maxima: 85 },
  ambient_humidity: { unidad_medida: "%", medida_minima: 0, medida_maxima: 100 },
  soil_humidity: { unidad_medida: "%", medida_minima: 0, medida_maxima: 100 },
  luminosidad: { unidad_medida: "lux", medida_minima: 0, medida_maxima: 100000 },
  lluvia: { unidad_medida: "mm/h", medida_minima: 0, medida_maxima: 50 },
  velocidad_viento: { unidad_medida: "m/s", medida_minima: 0, medida_maxima: 60 },
  direccion_viento: { unidad_medida: "grados", medida_minima: 0, medida_maxima: 360 },
  ph_suelo: { unidad_medida: "pH", medida_minima: 0, medida_maxima: 14 },
};

const RegistrarSensorPage: React.FC = () => {
  const [sensor, setSensor] = useState<Partial<Sensor>>({
    nombre: "",
    tipo_sensor: "",
    unidad_medida: "",
    descripcion: "",
    medida_minima: 0,
    medida_maxima: 0,
  });

  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    if (name === "tipo_sensor") {
      const config = sensorConfigurations[value] || { unidad_medida: "", medida_minima: 0, medida_maxima: 0 };
      setSensor((prev) => ({
        ...prev,
        tipo_sensor: value,
        unidad_medida: config.unidad_medida,
        medida_minima: config.medida_minima,
        medida_maxima: config.medida_maxima,
      }));
    } else {
      setSensor((prev) => ({
        ...prev,
        [name]: name === "medida_minima" || name === "medida_maxima" ? Number(value) : value,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token") || "";
    try {
      const response = await fetch("http://127.0.0.1:8000/iot/sensores/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(sensor),
      });
      if (!response.ok) throw new Error("Error al registrar el sensor");
      navigate("/iot/listar-sensores");
    } catch (error) {
      console.error("Error:", error);
      alert("Error al registrar el sensor");
    }
  };

  return (
    <DefaultLayout>
      <div className="w-full flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-xl font-semibold text-gray-700 mb-4 text-center">Registro de Sensor</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <ReuInput
              label="Nombre"
              placeholder="Ingrese el nombre del sensor"
              type="text"
              value={sensor.nombre || ""}
              onChange={(e) => setSensor({ ...sensor, nombre: e.target.value })}
            />

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700">Tipo de Sensor</label>
              <select
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                name="tipo_sensor"
                value={sensor.tipo_sensor || ""}
                onChange={handleChange}
              >
                <option value="">Seleccione un tipo de sensor</option>
                {sensorTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            <ReuInput
              label="Unidad de Medida"
              placeholder="Ej: °C, %, lux"
              type="text"
              value={sensor.unidad_medida || ""}
              onChange={(e) => setSensor({ ...sensor, unidad_medida: e.target.value })}
              // readOnly eliminado
            />

            <ReuInput
              label="Descripción"
              placeholder="Descripción del sensor"
              type="text"
              value={sensor.descripcion || ""}
              onChange={(e) => setSensor({ ...sensor, descripcion: e.target.value })}
            />

            <div className="grid grid-cols-2 gap-4">
              <ReuInput
                label="Medida Mínima"
                placeholder="Valor mínimo"
                type="number"
                value={sensor.medida_minima?.toString() || "0"}
                onChange={(e) => setSensor({ ...sensor, medida_minima: Number(e.target.value) })}
              />

              <ReuInput
                label="Medida Máxima"
                placeholder="Valor máximo"
                type="number"
                value={sensor.medida_maxima?.toString() || "0"}
                onChange={(e) => setSensor({ ...sensor, medida_maxima: Number(e.target.value) })}
              />
            </div>

            <button
              className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
              type="submit"
            >
              Guardar
            </button>
            <button
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg mt-4 hover:bg-blue-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
              type="button"
              onClick={() => navigate("/iot/listar-sensores")}
            >
              Ir a Lista de Sensores
            </button>
          </form>
        </div>
      </div>
    </DefaultLayout>
  );
};

export default RegistrarSensorPage;