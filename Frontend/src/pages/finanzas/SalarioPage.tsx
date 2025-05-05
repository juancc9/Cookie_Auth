import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import DefaultLayout from "@/layouts/default";
import { Salario } from "@/types/finanzas/Salario";
import { useRegistrarSalario } from "@/hooks/finanzas/useSalario";
import Formulario from "@/components/globales/Formulario";


const SalarioPage: React.FC = () => {

  const [salario, setSalario] = useState<Salario>({
    id: 0,
    fecha_de_implementacion: "",
    valorJornal: 0,
  });

  const [displayValue, setDisplayValue] = useState(""); // Para mostrar el valor formateado
  const mutation = useRegistrarSalario();
  const navigate = useNavigate();

  // Formatear número al estilo colombiano (1.000.000)
  const formatColombianNumber = (value: string): string => {
    const numStr = value.replace(/[^\d]/g, '');
    return numStr.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  };

  // Convertir string formateado a número
  const parseColombianNumber = (value: string): number => {
    return parseFloat(value.replace(/\./g, '')) || 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    if (name === "valorJornal") {
      // Manejo especial para el campo de valor
      const formattedValue = formatColombianNumber(value);
      setDisplayValue(formattedValue);
      setSalario(prev => ({
        ...prev,
        valorJornal: parseColombianNumber(formattedValue)
      }));
    } else {
      setSalario(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(salario, {
      onSuccess: () => {
        setSalario({ id: 0, fecha_de_implementacion: "", valorJornal: 0 });
        setDisplayValue("");
        navigate("/finanzas/listarsalarios/");
      },
    });
  };

  return (
    <DefaultLayout>
      <Formulario
        title="Valor del Jornal "
        onSubmit={handleSubmit}
        buttonText="Guardar"
        isSubmitting={mutation.isPending}
      >
        <input
          type="date"
          name="fecha_de_implementacion"
          value={salario.fecha_de_implementacion}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 transition-all duration-200"
          required
        />
        <input
          type="text"
          name="valorJornal"
          value={displayValue}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 transition-all duration-200"
          placeholder="Ej: 85.500"
          inputMode="numeric"
          pattern="^[\d.]*$"
          required
        />
        <div className="col-span-1 md:col-span-2 flex justify-center">
          <button
            type="button"
            className="w-full max-w-md px-4 py-3 bg-blue-400 text-white rounded-lg hover:bg-blue-500 transition-all duration-200 shadow-md hover:shadow-lg font-medium text-sm uppercase tracking-wide"
            onClick={() => navigate("/finanzas/listarsalarios/")}
          >
            Listar Costo de Jornales
          </button>
        </div>
      </Formulario>
    
    </DefaultLayout>
  );
};

export default SalarioPage;