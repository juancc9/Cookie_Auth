import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import DefaultLayout from "@/layouts/default";
import { ReuInput } from "@/components/globales/ReuInput";
import { useCrearReportePlaga } from "@/hooks/cultivo/useReportePlaga";
import Formulario from "@/components/globales/Formulario";
import { useBancales } from "@/hooks/cultivo/usebancal";
import { usePlagas } from "@/hooks/cultivo/useplaga";
import { ReportePlaga } from "@/types/cultivo/ReportePlaga";

const RegistroReportePlaga: React.FC = () => {
  const [reporte, setReporte] = useState<Omit<ReportePlaga, 'id' | 'estado' | 'fecha_reporte'>>({
    plaga_id: 0,
    bancal_id: 0,
    observaciones: ""
  });

  const { data: bancales, isLoading: loadingBancales } = useBancales();
  const { data: plagas, isLoading: loadingPlagas } = usePlagas();
  const mutation = useCrearReportePlaga();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setReporte((prevReporte) => ({
      ...prevReporte,
      [name]: value, 
    }));
  };
  

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (reporte.plaga_id && reporte.bancal_id) {
      mutation.mutate(reporte);
    }
  };

  if (loadingBancales || loadingPlagas) {
    return <div>Cargando datos...</div>;
  }

  return (
    <DefaultLayout>
     <Formulario
        title="Registro de Afección"
        onSubmit={handleSubmit}
        isSubmitting={mutation.isPending}
        buttonText="Guardar"
        >

     <label className="block text-sm font-medium text-gray-700 mt-4">Bancal</label>
                        <select
                            name="bancal_id"
                            value={reporte.bancal_id || ""}
                            onChange={handleChange}
                            className="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:text-sm"
                        >
                            <option value="">Seleccione un bancal</option>
                            {bancales?.map((bancal) => (
                                <option key={bancal.id} value={bancal.id}>
                                    {bancal.nombre}
                                </option>
                            ))}
                        </select>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700">Plaga</label>
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              name="plaga_id"
              value={reporte.plaga_id}
              onChange={handleChange}
            >
              <option value="">Seleccione una plaga</option>
              {plagas?.map((plaga) => (
                <option key={plaga.id} value={plaga.id}>{plaga.nombre}</option>
              ))}
            </select>
          </div>

        <ReuInput
          label="Observaciones"
          placeholder="Describa la plaga encontrada"
          type="textarea"
          value={reporte.observaciones}
          onChange={(e) => setReporte({...reporte, observaciones: e.target.value})}
        />

        <div className="col-span-1 md:col-span-2 flex justify-center">
          <button
            className="w-full max-w-md px-4 py-3 bg-blue-400 text-white rounded-lg hover:bg-blue-500 transition-all duration-200 shadow-md hover:shadow-lg font-medium text-sm uppercase tracking-wide"
            type="button"
            onClick={() => navigate("/cultivo/listareporteplaga/")}
          >
            Listar reportes
          </button>
        </div>
      </Formulario>
    </DefaultLayout>
  );
};

export default RegistroReportePlaga;