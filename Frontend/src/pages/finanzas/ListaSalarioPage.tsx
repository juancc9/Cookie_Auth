import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import DefaultLayout from "@/layouts/default";
import { Salario } from "@/types/finanzas/Salario";
import { useSalarios, useActualizarSalario, useEliminarSalario } from "@/hooks/finanzas/useSalario";
import ReuModal from "@/components/globales/ReuModal";
import Tabla from "@/components/globales/Tabla";
import { EditIcon, Trash2 } from 'lucide-react';


// Componente para inputs de salario con formato colombiano
const SalarioInput = ({
  label,
  value,
  onChange,
  placeholder
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value.replace(/[^\d]/g, '');
    const formattedValue = inputValue.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    onChange(formattedValue);
  };

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <input
        type="text"
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 transition-all duration-200"
        inputMode="numeric"
      />
    </div>
  );
};

const ListaSalarioPage: React.FC = () => {
  const [selectedSalario, setSelectedSalario] = useState<Salario | null>(null);
  const [displayValue, setDisplayValue] = useState("");
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  const { data: salarios, isLoading, refetch } = useSalarios();
  const updateMutation = useActualizarSalario();
  const deleteMutation = useEliminarSalario();
  const navigate = useNavigate();

  // Formateador de números colombianos
  const formatColombianNumber = (value: number): string => {
    return new Intl.NumberFormat('es-CO').format(value);
  };

  // Manejadores de eventos
  const handleEdit = (salario: Salario) => {
    setSelectedSalario(salario);
    setDisplayValue(formatColombianNumber(salario.valorJornal));
    setIsEditModalOpen(true);
  };

  const handleDelete = (salario: Salario) => {
    setSelectedSalario(salario);
    setIsDeleteModalOpen(true);
  };

  const handleConfirmDelete = () => {
    if (selectedSalario?.id) {
      deleteMutation.mutate(selectedSalario.id, {
        onSuccess: () => {
          setIsDeleteModalOpen(false);
          refetch();
        }
      });
    }
  };

  // Transformación de datos para la tabla
  const transformedData = salarios?.map((salario) => ({
    id: salario.id.toString(),
    fecha_de_implementacion: new Date(salario.fecha_de_implementacion).toLocaleDateString(),
    valorJornal: `$${formatColombianNumber(salario.valorJornal)}`,
    acciones: (
      <div className="flex space-x-2">
        <button 
          onClick={() => handleEdit(salario)} 
          className="text-blue-600 hover:text-blue-800"
          aria-label="Editar salario"
        >
          <EditIcon size={20} />
        </button>
        <button 
          onClick={() => handleDelete(salario)} 
          className="text-red-600 hover:text-red-800"
          aria-label="Eliminar salario"
        >
          <Trash2 size={20} />
        </button>
      </div>
    )
  })) || [];

  return (
    <DefaultLayout>
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Listado del valor del Jornal</h1>
          <button
            onClick={() => navigate("/finanzas/salario/")}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            aria-label="Registrar nuevo salario"
          >
            + Registrar
          </button>
        </div>

        {isLoading ? (
          <div className="text-center py-8">Cargando salarios...</div>
        ) : (
          <Tabla
            columns={[
              { name: "Fecha Implementación", uid: "fecha_de_implementacion" },
              { name: "Valor Jornal", uid: "valorJornal" },
              { name: "Acciones", uid: "acciones" }
            ]}
            data={transformedData}
          />
        )}

        {/* Modal de Edición */}
        <ReuModal
          isOpen={isEditModalOpen}
          onOpenChange={setIsEditModalOpen}
          title="Editar Salario"
          onConfirm={() => {
            if (selectedSalario) {
              updateMutation.mutate(selectedSalario, {
                onSuccess: () => {
                  setIsEditModalOpen(false);
                  refetch();
                }
              });
            }
          }}
          confirmText="Guardar Cambios"
          isConfirming={updateMutation.isPending}
        >
          {selectedSalario && (
            <>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Fecha de Implementación
                </label>
                <input
                  type="date"
                  value={selectedSalario.fecha_de_implementacion}
                  onChange={(e) => setSelectedSalario({
                    ...selectedSalario,
                    fecha_de_implementacion: e.target.value
                  })}
                  className="w-full p-2 border rounded"
                />
              </div>
              <SalarioInput
                label="Valor del Jornal"
                value={displayValue}
                onChange={(value) => {
                  setDisplayValue(value);
                  setSelectedSalario({
                    ...selectedSalario,
                    valorJornal: Number(value.replace(/\./g, ''))
                  });
                }}
                placeholder="Ej: 1.400.500"
              />
            </>
          )}
        </ReuModal>

        {/* Modal de Eliminación */}
        <ReuModal
          isOpen={isDeleteModalOpen}
          onOpenChange={setIsDeleteModalOpen}
          title="Confirmar Eliminación"
          onConfirm={handleConfirmDelete}
          confirmText="Eliminar"
          isConfirming={deleteMutation.isPending}
          
        >
          <p>¿Estás seguro de eliminar este registro de salario?</p>
          {selectedSalario && (
            <div className="mt-4 p-3 bg-gray-100 rounded">
              <p><strong>Fecha:</strong> {new Date(selectedSalario.fecha_de_implementacion).toLocaleDateString()}</p>
              <p><strong>Valor:</strong> ${formatColombianNumber(selectedSalario.valorJornal)}</p>
            </div>
          )}
        </ReuModal>
      </div>
    </DefaultLayout>
  );
};

export default ListaSalarioPage;