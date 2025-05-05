import React, { useState } from "react";
import DefaultLayout from "@/layouts/default";
import { ReuInput } from "@/components/globales/ReuInput";
import { useRegistrarActividad, useInsumos, useUsuarios } from "@/hooks/cultivo/useActividad";
import { useHerramientas } from "@/hooks/inventario/useHerramientas";
import { useTipoActividad, useRegistrarTipoActividad } from "@/hooks/cultivo/usetipoactividad";
import { useCultivos } from "@/hooks/cultivo/useCultivo";
import { useNavigate } from "react-router-dom";
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import Formulario from "@/components/globales/Formulario";
import ReuModal from "@/components/globales/ReuModal";
import { Plus } from 'lucide-react';
import { ModalCultivo } from "@/components/cultivo/ModalCultivo";
import { ModalHerramienta } from "@/components/cultivo/ModalHerramienta";
const animatedComponents = makeAnimated();

interface SelectedOption {
  value: number;
  label: string;
  cantidad?: number;
  devuelta?: boolean;
}

const ActividadPage: React.FC = () => {
    const navigate = useNavigate();

    const [actividad, setActividad] = useState({
        descripcion: "",
        fecha_inicio: "",
        fecha_fin: "",
        tipo_actividad: 0,
        cultivo: 0,
        estado: "PENDIENTE",
        prioridad: "MEDIA",
        instrucciones_adicionales: "",
        usuarios: [] as SelectedOption[],
        insumos: [] as SelectedOption[],
        herramientas: [] as SelectedOption[]
    });

    const [searchUsuario, setSearchUsuario] = useState("");
    const [searchInsumo, setSearchInsumo] = useState("");
    const [searchHerramienta, setSearchHerramienta] = useState("");

    const mutation = useRegistrarActividad();
    const registrarTipoActividad = useRegistrarTipoActividad()
    const { data: tiposActividad } = useTipoActividad();
    const { data: usuarios } = useUsuarios();
    const { data: cultivos } = useCultivos();
    const { data: insumos } = useInsumos();
    const { data: herramientas } = useHerramientas();
    const [openTipoActividadModal, setOpenTipoActividadModal] = useState(false);
    const [openCultivoModal, setOpenCultivoModal] = useState(false);
    const [openHerramientaModal, setOpenHerramientaModal] = useState(false);


    const [nuevoTipoActividad, setNuevoTipoActividad] = useState({
        nombre: "",
        descripcion: ""
    });
    const handleSubmitTipoActividad = () => {
        registrarTipoActividad.mutate(nuevoTipoActividad, {
            onSuccess: () => {
                setOpenTipoActividadModal(false);
                setNuevoTipoActividad({ nombre: "", descripcion: "" });
            }
        });
    };
    

    const usuarioOptions = usuarios?.map(u => ({ value: u.id, label: u.nombre })) || [];
    const insumoOptions = insumos?.map(i => ({ 
        value: i.id, 
        label: `${i.nombre} (Disponible: ${i.cantidad})`,
        cantidad: 0 
    })) || [];
    const herramientaOptions = herramientas?.map(h => ({ 
        value: h.id, 
        label: h.nombre,
        devuelta: false
    })) || [];

    const filteredUsuarios = usuarioOptions.filter(opt => 
        opt.label.toLowerCase().includes(searchUsuario.toLowerCase())
    );
    const filteredInsumos = insumoOptions.filter(opt => 
        opt.label.toLowerCase().includes(searchInsumo.toLowerCase())
    );
    const filteredHerramientas = herramientaOptions.filter(opt => 
        opt.label.toLowerCase().includes(searchHerramienta.toLowerCase())
    );

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        
        const payload = {
            ...actividad,
            usuarios: actividad.usuarios.map(u => u.value),
            insumos: actividad.insumos.map(i => ({
                insumo: i.value,
                cantidad_usada: i.cantidad || 0
            })),
            herramientas: actividad.herramientas.map(h => ({
                herramienta: h.value,
                entregada: true,
                devuelta: false
            }))
        };

        mutation.mutate(payload)
    };

    const handleInsumoCantidadChange = (value: number, index: number) => {
        const updatedInsumos = [...actividad.insumos];
        updatedInsumos[index] = { ...updatedInsumos[index], cantidad: value };
        setActividad({ ...actividad, insumos: updatedInsumos });
    };

    return (
        <DefaultLayout>
            <ModalHerramienta 
                isOpen={openHerramientaModal}
                onOpenChange={setOpenHerramientaModal}
            />
             <ModalCultivo 
                    isOpen={openCultivoModal}
                    onOpenChange={setOpenCultivoModal}
             />
             <ReuModal
                isOpen={openTipoActividadModal}
                onOpenChange={setOpenTipoActividadModal}
                title="Registrar Nuevo Tipo de Actividad"
                onConfirm={handleSubmitTipoActividad}
                confirmText="Guardar"
                cancelText="Cancelar"
            >
                <ReuInput
                    label="Nombre"
                    placeholder="Ingrese el nombre"
                    type="text"
                    value={nuevoTipoActividad.nombre}
                    onChange={(e) => setNuevoTipoActividad({...nuevoTipoActividad, nombre: e.target.value})}
                />
                <ReuInput
                    label="Descripción"
                    placeholder="Ingrese la descripción"
                    type="text"
                    value={nuevoTipoActividad.descripcion}
                    onChange={(e) => setNuevoTipoActividad({...nuevoTipoActividad, descripcion: e.target.value})}
                />
            </ReuModal>
                <Formulario 
                    title="Asignar actividad" 
                    onSubmit={handleSubmit}
                    buttonText="Guardar Actividad"
                    isSubmitting={mutation.isPending}
                    className="bg-gray-50"
                >
                    <div className="space-y-4">
                        <ReuInput
                            label="Descripción"
                            placeholder="Ingrese la descripción"
                            type="text"
                            value={actividad.descripcion}
                            onChange={(e) => setActividad({ ...actividad, descripcion: e.target.value })}
                        />

                        <ReuInput
                            label="Fecha de Inicio"
                            type="datetime-local"
                            value={actividad.fecha_inicio}
                            onChange={(e) => setActividad({ ...actividad, fecha_inicio: e.target.value })}
                        />

                        <ReuInput
                            label="Fecha de Fin"
                            type="datetime-local"
                            value={actividad.fecha_fin}
                            onChange={(e) => setActividad({ ...actividad, fecha_fin: e.target.value })}
                        />

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Estado</label>
                                <select 
                                    name="estado" 
                                    value={actividad.estado} 
                                    onChange={(e) => setActividad({ ...actividad, estado: e.target.value })}
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border"
                                >
                                    <option value="PENDIENTE">Pendiente</option>
                                    <option value="EN_PROCESO">En proceso</option>
                                    <option value="COMPLETADA">Completada</option>
                                    <option value="CANCELADA">Cancelada</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700">Prioridad</label>
                                <select 
                                    name="prioridad" 
                                    value={actividad.prioridad} 
                                    onChange={(e) => setActividad({ ...actividad, prioridad: e.target.value })}
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border"
                                >
                                    <option value="ALTA">Alta</option>
                                    <option value="MEDIA">Media</option>
                                    <option value="BAJA">Baja</option>
                                </select>
                            </div>
                        </div>

                        <div>
                        <div className="flex items-center gap-2 mb-1">
                        <label className="block text-sm font-medium text-gray-700">Tipo de Actividad</label>
                        <button 
                            className="p-1 h-6 w-6 flex items-center justify-center rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500"
                            onClick={() => setOpenTipoActividadModal(true)}
                            type="button"
                        >
                            <Plus className="h-4 w-4" />
                        </button>
                        </div>
                    <select 
                        name="tipo_actividad" 
                        value={actividad.tipo_actividad || ""} 
                        onChange={(e) => setActividad({ ...actividad, tipo_actividad: Number(e.target.value) })}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border"
                    >
                        <option value="">Seleccione un tipo de actividad</option>
                        {tiposActividad?.map((tipo) => (
                            <option key={tipo.id} value={tipo.id}>{tipo.nombre}</option>
                        ))}
                    </select>
                </div>

                        <div>
                        <div className="flex items-center gap-2 mb-1">
                            <label className="block text-sm font-medium text-gray-700">Cultivo</label>
                            <button 
                                className="p-1 h-6 w-6 flex items-center justify-center rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500"
                                onClick={() => setOpenCultivoModal(true)}
                                type="button"
                            >
                                <Plus className="h-4 w-4" />
                            </button>
                        </div>
                            <select 
                                name="cultivo" 
                                value={actividad.cultivo || ""} 
                                onChange={(e) => setActividad({ ...actividad, cultivo: Number(e.target.value) })}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border"
                            >
                                <option value="">Seleccione un cultivo</option>
                                {cultivos?.map((cultivo) => (
                                    <option key={cultivo.id} value={cultivo.id}>{cultivo.nombre}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Asignar a Usuarios</label>
                            <Select
                                isMulti
                                options={filteredUsuarios}
                                value={actividad.usuarios}
                                onChange={(selected) => setActividad({ ...actividad, usuarios: selected as SelectedOption[] })}
                                onInputChange={setSearchUsuario}
                                placeholder="Buscar usuarios..."
                                components={animatedComponents}
                                className="basic-multi-select"
                                classNamePrefix="select"
                                noOptionsMessage={() => "No hay usuarios disponibles"}
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Insumos Requeridos</label>
                            <Select
                                isMulti
                                options={filteredInsumos}
                                value={actividad.insumos}
                                onChange={(selected) => setActividad({ ...actividad, insumos: selected as SelectedOption[] })}
                                onInputChange={setSearchInsumo}
                                placeholder="Buscar insumos..."
                                components={animatedComponents}
                                className="basic-multi-select"
                                classNamePrefix="select"
                                noOptionsMessage={() => "No hay insumos disponibles"}
                            />

                            {actividad.insumos.length > 0 && (
                                <div className="mt-2 space-y-2">
                                    {actividad.insumos.map((insumo, index) => (
                                        <div key={insumo.value} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                                            <span className="text-sm">{insumo.label.split('(')[0]}</span>
                                            <input
                                                type="number"
                                                min="0"
                                                value={insumo.cantidad || 0}
                                                onChange={(e) => handleInsumoCantidadChange(Number(e.target.value), index)}
                                                className="w-20 px-2 py-1 border rounded text-sm"
                                                placeholder="Cantidad"
                                            />
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        <div>
                        <div className="flex items-center gap-2 mb-1">
                        <label className="block text-sm font-medium text-gray-700">Herramientas</label>
                            <button 
                                className="p-1 h-6 w-6 flex items-center justify-center rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500"
                                onClick={() => setOpenHerramientaModal(true)}
                                type="button"
                            >
                                <Plus className="h-4 w-4" />
                            </button>
                        </div>
                            <Select
                                isMulti
                                options={filteredHerramientas}
                                value={actividad.herramientas}
                                onChange={(selected) => setActividad({ ...actividad, herramientas: selected as SelectedOption[] })}
                                onInputChange={setSearchHerramienta}
                                placeholder="Buscar herramientas..."
                                components={animatedComponents}
                                className="basic-multi-select"
                                classNamePrefix="select"
                                noOptionsMessage={() => "No hay herramientas disponibles"}
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Instrucciones Adicionales</label>
                            <textarea
                                name="instrucciones_adicionales"
                                value={actividad.instrucciones_adicionales}
                                onChange={(e) => setActividad({ ...actividad, instrucciones_adicionales: e.target.value })}
                                rows={3}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border"
                                placeholder="Ingrese instrucciones adicionales para la actividad"
                            />
                        </div>
                        
                    </div>
                    <div className="col-span-1 md:col-span-2 flex justify-center">
                    <button
                        className="w-full max-w-md px-4 py-3 bg-blue-400 text-white rounded-lg hover:bg-blue-500 transition-all duration-200 shadow-md hover:shadow-lg font-medium text-sm uppercase tracking-wide"
                        onClick={() => navigate("/cultivo/listaractividad/")}
                    >
                        Listar actividades
                    </button>
                </div>
                </Formulario>
                </DefaultLayout>
    );
};

export default ActividadPage;