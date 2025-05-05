import ReuModal from "../globales/ReuModal";
import { ReuInput } from "../globales/ReuInput";
import { useRegistrarCultivo } from "@/hooks/cultivo/useCultivo";
import { useEspecies } from "@/hooks/cultivo/useEspecie";
import { useBancales } from "@/hooks/cultivo/usebancal";
import { Cultivo } from "@/types/cultivo/Cultivo";
import { useState } from "react";

interface ModalCultivoProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess?: () => void;
}

export const ModalCultivo = ({ isOpen, onOpenChange, onSuccess }: ModalCultivoProps) => {
  const [nuevoCultivo, setNuevoCultivo] = useState<Cultivo>({
    nombre: "",
    unidad_de_medida: "",
    activo: false,
    fechaSiembra: "",
    Especie: 0,
    Bancal: 0,
  });

  const { data: especies } = useEspecies();
  const { data: bancales } = useBancales();
  const mutation = useRegistrarCultivo();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const checked = type === 'checkbox' ? (e.target as HTMLInputElement).checked : undefined;
    
    setNuevoCultivo(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : 
              (name === 'Especie' || name === 'Bancal') ? Number(value) : value
    }));
  };

  const handleSubmit = () => {
    mutation.mutate(nuevoCultivo, {
      onSuccess: () => {
        onOpenChange(false);
        setNuevoCultivo({
          nombre: "",
          unidad_de_medida: "",
          activo: false,
          fechaSiembra: "",
          Especie: 0,
          Bancal: 0,
        });
        onSuccess?.();
      }
    });
  };

  return (
    <ReuModal
      isOpen={isOpen}
      onOpenChange={onOpenChange}
      title="Registrar Nuevo Cultivo"
      onConfirm={handleSubmit}
      confirmText="Guardar"
      cancelText="Cancelar"
    >
      <div className="space-y-4">
        <ReuInput
          label="Nombre"
          placeholder="Ingrese el nombre"
          type="text"
          value={nuevoCultivo.nombre}
          onChange={(e)=> setNuevoCultivo({...nuevoCultivo, nombre: e.target.value})}
        />

        <ReuInput
          label="Unidad de Medida"
          placeholder="Ej: kg, g, unidades"
          type="text"
          value={nuevoCultivo.unidad_de_medida}
          onChange={(e)=> setNuevoCultivo({...nuevoCultivo, unidad_de_medida: e.target.value})}
        />

        <ReuInput
          label="Fecha de Siembra"
          type="date"
          value={nuevoCultivo.fechaSiembra}
          onChange={(e)=> setNuevoCultivo({...nuevoCultivo, fechaSiembra: e.target.value})}
        />

        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="activo"
            checked={nuevoCultivo.activo}
            onChange={handleChange}
            className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
          />
          <span className="text-sm text-gray-700">Activo</span>
        </label>

        <div>
          <label className="block text-sm font-medium text-gray-700">Especie</label>
          <select
            name="Especie"
            value={nuevoCultivo.Especie || ""}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border"
          >
            <option value="0">Seleccione una especie</option>
            {especies?.map((especie) => (
              <option key={especie.id} value={especie.id}>{especie.nombre}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Bancal</label>
          <select
            name="Bancal"
            value={nuevoCultivo.Bancal || ""}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border"
          >
            <option value="0">Seleccione un bancal</option>
            {bancales?.map((bancal) => (
              <option key={bancal.id} value={bancal.id}>{bancal.nombre}</option>
            ))}
          </select>
        </div>
      </div>
    </ReuModal>
  );
};