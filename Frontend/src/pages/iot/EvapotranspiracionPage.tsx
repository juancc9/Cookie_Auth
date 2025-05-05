import { useState, useEffect } from "react";
import DefaultLayout from "@/layouts/default";
import { useNavigate } from "react-router-dom";
import { ReuInput } from "@/components/globales/ReuInput";
import Tabla from "@/components/globales/Tabla";

interface Bancal {
  id: number;
  nombre: string;
  posX: number | null;
  posY: number | null;
}

interface EvapotranspiracionData {
  id: number;
  fk_bancal: number;
  fecha: string;
  valor: number;
  creado: string;
}

export default function EvapotranspiracionPage() {
  const [formData, setFormData] = useState({
    fk_bancal_id: "",
    fecha: "",
    latitud: "",
    altitud: "",
  });
  const [bancales, setBancales] = useState<Bancal[]>([]);
  const [resultados, setResultados] = useState<EvapotranspiracionData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  // Obtener bancales al cargar la página
  useEffect(() => {
    const fetchBancales = async () => {
      const token = localStorage.getItem("access_token") || "";
      try {
        const response = await fetch("http://127.0.0.1:8000/cultivo/Bancal/", {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) throw new Error("Error al obtener los bancales");
        const data = await response.json();
        setBancales(data);
      } catch (err) {
        setError("Error al cargar los bancales");
        console.error(err);
      }
    };

    fetchBancales();
  }, []);

  // Autocompletar latitud y altitud cuando se selecciona un bancal
  const handleBancalChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const bancalId = e.target.value;
    const selectedBancal = bancales.find((bancal) => bancal.id === Number(bancalId));
    setFormData((prev) => ({
      ...prev,
      fk_bancal_id: bancalId,
      latitud: selectedBancal?.posY ? selectedBancal.posY.toString() : "0",
      altitud: selectedBancal?.posX ? selectedBancal.posX.toString() : "0",
    }));
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const token = localStorage.getItem("access_token") || "";
    try {
      const response = await fetch("http://127.0.0.1:8000/iot/evapotranspiracion/calcular/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          fk_bancal_id: Number(formData.fk_bancal_id),
          fecha: formData.fecha,
          latitud: Number(formData.latitud),
          altitud: Number(formData.altitud),
        }),
      });
      if (!response.ok) throw new Error("Error al calcular la evapotranspiración");
      const data = await response.json();
      setResultados((prev) => [...prev, data]);
    } catch (err: any) {
      setError(err.message || "Error al calcular la evapotranspiración");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { name: "ID", uid: "id" },
    { name: "Bancal", uid: "fk_bancal" },
    { name: "Fecha", uid: "fecha" },
    { name: "Valor (mm/día)", uid: "valor" },
    { name: "Creado", uid: "creado" },
  ];

  const formattedData = resultados.map((dato: EvapotranspiracionData) => ({
    id: dato.id,
    fk_bancal: bancales.find((b) => b.id === dato.fk_bancal)?.nombre || dato.fk_bancal,
    fecha: dato.fecha,
    valor: dato.valor,
    creado: new Date(dato.creado).toLocaleString(),
  }));

  return (
    <DefaultLayout>
      <div className="w-full flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-5xl">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
            Cálculo de Evapotranspiración
          </h2>

          <div className="mb-4 flex justify-start items-center gap-2">
            <button
              className="px-3 py-2 bg-green-600 text-white text-sm font-semibold rounded-lg hover:bg-green-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
              onClick={() => navigate("/iot/sensores")}
            >
              Volver a Sensores
            </button>
          </div>

          <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-md mb-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">
              Calcular Evapotranspiración
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700">Bancal</label>
                <select
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  name="fk_bancal_id"
                  value={formData.fk_bancal_id}
                  onChange={handleBancalChange}
                  required
                >
                  <option value="">Seleccione un bancal</option>
                  {bancales.map((bancal) => (
                    <option key={bancal.id} value={bancal.id}>
                      {bancal.nombre}
                    </option>
                  ))}
                </select>
              </div>

              <ReuInput
                label="Fecha"
                type="date"
                value={formData.fecha}
                onChange={handleChange}
                required
              />
              <ReuInput
                label="Latitud"
                type="number"
                step="0.01"
                value={formData.latitud}
                onChange={handleChange}
                placeholder="Ej: 4.61"
              />
              <ReuInput
                label="Altitud (metros)"
                type="number"
                value={formData.altitud}
                onChange={handleChange}
                placeholder="Ej: 2600"
              />
              <button
                type="submit"
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
                disabled={loading}
              >
                {loading ? "Calculando..." : "Calcular"}
              </button>
            </form>
            {error && <p className="text-red-500 text-center mt-4">{error}</p>}
          </div>

          {resultados.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-4">
                Resultados de Evapotranspiración
              </h3>
              <Tabla columns={columns} data={formattedData} />
            </div>
          )}
        </div>
      </div>
    </DefaultLayout>
  );
}