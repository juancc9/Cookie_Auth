import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DefaultLayout from '@/layouts/default';
import { useCalcularPago } from '@/hooks/finanzas/usePago';
import { useUsuarios } from '@/hooks/cultivo/useActividad';
import Formulario from '@/components/globales/Formulario';
import { ReuInput } from '@/components/globales/ReuInput';
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import { addToast } from "@heroui/react";

const animatedComponents = makeAnimated();

interface UsuarioOption {
  value: number;
  label: string;
}

const CalcularPagoPage: React.FC = () => {
  const [selectedUsuario, setSelectedUsuario] = useState<UsuarioOption | null>(null);
  const [fechaInicio, setFechaInicio] = useState<string>('');
  const [fechaFin, setFechaFin] = useState<string>('');
  const [searchUsuario, setSearchUsuario] = useState<string>('');
  
  const calcularPagoMutation = useCalcularPago();
  const { data: usuarios } = useUsuarios();
  const navigate = useNavigate();

  const usuarioOptions: UsuarioOption[] = usuarios?.map(u => ({
    value: u.id,
    label: `${u.nombre} ${u.apellido || ''}`.trim()
  })) || [];

  const filteredUsuarios = usuarioOptions.filter(opt => 
    opt.label.toLowerCase().includes(searchUsuario.toLowerCase())
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedUsuario) {
      addToast({
        title: "Usuario no seleccionado",
        description: "Por favor seleccione un usuario antes de calcular el pago.",
        timeout: 3000,
        color:"danger"
      });
      return;
    }
    

    calcularPagoMutation.mutate({
      usuario_id: selectedUsuario.value,
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin,
    }, {
      onSuccess: () => {
        navigate('/finanzas/listarpagos');
      }
    });
      };

  return (
    <DefaultLayout>
      <Formulario
        title="Calcular Nuevo Pago"
        onSubmit={handleSubmit}
        isSubmitting={calcularPagoMutation.isPending}
        buttonText="Calcular"
      >
        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Seleccionar Usuario
          </label>
          <Select
            options={filteredUsuarios}
            value={selectedUsuario}
            onChange={(selected) => setSelectedUsuario(selected as UsuarioOption)}
            onInputChange={setSearchUsuario}
            placeholder="Buscar usuario..."
            components={animatedComponents}
            className="basic-select"
            classNamePrefix="select"
            noOptionsMessage={() => "No hay usuarios disponibles"}
            isClearable
          />
        </div>

        <ReuInput
          label="Fecha Inicio"
          type="date"
          value={fechaInicio}
          onChange={(e) => setFechaInicio(e.target.value)}
        />

        <ReuInput
          label="Fecha Fin"
          type="date"
          value={fechaFin}
          onChange={(e) => setFechaFin(e.target.value)}
        />

        <div className="col-span-1 md:col-span-2 flex justify-center">
          <button
            className="w-full max-w-md px-4 py-3 bg-blue-400 text-white rounded-lg hover:bg-blue-500 transition-all duration-200 shadow-md hover:shadow-lg font-medium text-sm uppercase tracking-wide"
            type="button"
            onClick={() => navigate("/finanzas/listarpagos")}
          >
            Listar Pagos
          </button>
        </div>
      </Formulario>
    </DefaultLayout>
  );
};

export default CalcularPagoPage;