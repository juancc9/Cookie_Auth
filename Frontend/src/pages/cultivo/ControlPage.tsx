import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import DefaultLayout from "@/layouts/default";
import { ReuInput } from "@/components/globales/ReuInput";
import Formulario from "@/components/globales/Formulario";
import { useCrearControl } from "@/hooks/cultivo/useControl";
import { useAfecciones } from "@/hooks/cultivo/useAfecciones";
import { useTipoControl } from "@/hooks/cultivo/usetipocontrol";
import { useProductoControl } from "@/hooks/cultivo/useproductoscontrol";
import { useUsuarios } from "@/hooks/usuarios/useUsuarios";
import { Control } from "@/types/cultivo/Control";

const ControlPage: React.FC = () => {
  const [control, setControl] = useState<Omit<Control, 'id'>>({
    afeccion_id: 0,
    tipo_control_id: 0,
    producto_id: 0,
    descripcion: "",
    fecha_control: new Date().toISOString().slice(0, 10),
    responsable_id: 0,
    efectividad: 50,
    observaciones: ""
  });

  const { data: afecciones } = useAfecciones();
  const { data: tipoControles } = useTipoControl();
  const { data: productos } = useProductoControl();
  const { data: usuarios } = useUsuarios();
  const mutation = useCrearControl();
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(control);
  };

  const efectividadOptions = Array.from({ length: 11 }, (_, i) => i * 10)
    .map(value => ({ value, label: `${value}%` }));

  return (
    <DefaultLayout>
      <Formulario
        title="Registrar Control"
        onSubmit={handleSubmit}
        isSubmitting={mutation.isPending}
        buttonText="Guardar"
      >
        <div className="col-span-1 sm:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Afección</label>
          <select
            name="afeccion_id"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={control.afeccion_id}
            onChange={(e) => setControl({...control, afeccion_id: Number(e.target.value)})}
            required
          >
            <option value="">Seleccione una afección</option>
            {afecciones?.map(a => (
              <option key={a.id} value={a.id}>{`${a.nombre} (${a.plaga.nombre})`}</option>
            ))}
          </select>
        </div>

        <div className="col-span-1 sm:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Tipo de Control</label>
          <select
            name="tipo_control_id"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={control.tipo_control_id}
            onChange={(e) => setControl({...control, tipo_control_id: Number(e.target.value)})}
            required
          >
            <option value="">Seleccione un tipo de control</option>
            {tipoControles?.map(t => (
              <option key={t.id} value={t.id}>{t.nombre}</option>
            ))}
          </select>
        </div>

        <div className="col-span-1 sm:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Producto</label>
          <select
            name="producto_id"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={control.producto_id}
            onChange={(e) => setControl({...control, producto_id: Number(e.target.value)})}
            required
          >
            <option value="">Seleccione un producto</option>
            {productos?.map(p => (
              <option key={p.id} value={p.id}>{p.nombre}</option>
            ))}
          </select>
        </div>

        <ReuInput
          label="Descripción"
          placeholder="Descripción del control aplicado"
          type="textarea"
          value={control.descripcion}
          onChange={(e) => setControl({...control, descripcion: e.target.value})}
        />

        <ReuInput
          label="Fecha de Control"
          type="date"
          value={control.fecha_control}
          onChange={(e) => setControl({...control, fecha_control: e.target.value})}
        />

        <div className="col-span-1 sm:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Responsable</label>
          <select
            name="responsable_id"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={control.responsable_id}
            onChange={(e) => setControl({...control, responsable_id: Number(e.target.value)})}
            required
          >
            <option value="">Seleccione un responsable</option>
            {usuarios?.map(u => (
              <option key={u.id} value={u.id}>{u.nombre}</option>
            ))}
          </select>
        </div>

        <div className="col-span-1 sm:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Efectividad</label>
          <select
            name="efectividad"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={control.efectividad}
            onChange={(e) => setControl({...control, efectividad: Number(e.target.value)})}
            required
          >
            {efectividadOptions.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>

        <ReuInput
          label="Observaciones"
          placeholder="Observaciones adicionales"
          type="textarea"
          value={control.observaciones}
          onChange={(e) => setControl({...control, observaciones: e.target.value})}
        />

        <div className="col-span-1 md:col-span-2 flex justify-center">
          <button
            className="w-full max-w-md px-4 py-3 bg-blue-400 text-white rounded-lg hover:bg-blue-500 transition-all duration-200 shadow-md hover:shadow-lg font-medium text-sm uppercase tracking-wide"
            type="button"
            onClick={() => navigate("/cultivo/listacontrol")}
          >
            Listar Controles
          </button>
        </div>
      </Formulario>
    </DefaultLayout>
  );
};

export default ControlPage;