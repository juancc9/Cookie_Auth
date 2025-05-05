import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import DefaultLayout from "@/layouts/default";
import { useRegistrarInsumo, useUnidadesMedida, useCrearUnidadMedida, useTiposInsumo, useCrearTipoInsumo, useInsumos, useActualizarInsumo } from "@/hooks/inventario/useInsumo";
import { ReuInput } from "@/components/globales/ReuInput";
import Formulario from "@/components/globales/Formulario";
import ReuModal from "@/components/globales/ReuModal";
import { Insumo, UnidadMedida, TipoInsumo } from "@/types/inventario/Insumo";
import InsumoNotifications from "@/components/inventario/InsumoNotifications";
import { useAuth } from "@/context/AuthContext";
import { addToast } from "@heroui/react";

const InsumoPage: React.FC = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const { data: unidadesMedida, isLoading: isLoadingUnidades } = useUnidadesMedida();
    const { data: tiposInsumo, isLoading: isLoadingTipos } = useTiposInsumo();
    const { data: insumos, isLoading: isLoadingInsumos } = useInsumos();
    const registrarInsumo = useRegistrarInsumo();
    const crearUnidadMedida = useCrearUnidadMedida();
    const crearTipoInsumo = useCrearTipoInsumo();
    const actualizarInsumo = useActualizarInsumo();

    const [insumo, setInsumo] = useState<Omit<Insumo, "id" | "unidad_medida" | "tipo_insumo" | "componentes"> & { unidad_medida_id?: number; tipo_insumo_id?: number; componentes_data?: { insumo_componente: number; cantidad: number }[] }>({
        nombre: "",
        descripcion: "",
        cantidad: 0,
        activo: true,
        tipo_empacado: null,
        fecha_registro: new Date().toISOString(),
        fecha_caducidad: null,
        precio_insumo: 0,
        es_compuesto: false,
        unidad_medida_id: undefined,
        tipo_insumo_id: undefined,
        componentes_data: [],
    });

    const [nuevaUnidad, setNuevaUnidad] = useState<Omit<UnidadMedida, "id" | "fecha_creacion" | "creada_por_usuario">>({
        nombre: "",
        descripcion: "",
    });

    const [nuevoTipo, setNuevoTipo] = useState<Omit<TipoInsumo, "id" | "fecha_creacion" | "creada_por_usuario">>({
        nombre: "",
        descripcion: "",
    });

    const [isUnidadModalOpen, setIsUnidadModalOpen] = useState(false);
    const [isTipoModalOpen, setIsTipoModalOpen] = useState(false);
    const [nuevoComponente, setNuevoComponente] = useState<{ insumo_componente: number; cantidad: number }>({ insumo_componente: 0, cantidad: 0 });

    const handleSubmitInsumo = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (insumo.es_compuesto && insumo.componentes_data && insumo.cantidad > 0) {
            for (const componente of insumo.componentes_data) {
                const insumoComponente = insumos?.find((i) => i.id === componente.insumo_componente);
                if (!insumoComponente) {
                    addToast({ 
                        title: "Error en componentes",
                        description: `Componente con ID ${componente.insumo_componente} no encontrado`
                    });
                    return;
                }
                const cantidadRequerida = componente.cantidad * insumo.cantidad;
                if (insumoComponente.cantidad < cantidadRequerida) {
                    addToast({ 
                        title: "Stock insuficiente",
                        description: `Stock insuficiente para ${insumoComponente.nombre}. Disponible: ${insumoComponente.cantidad}, Requerido: ${cantidadRequerida}`
                    });
                    return;
                }
            }

            
            for (const componente of insumo.componentes_data) {
                const insumoComponente = insumos?.find((i) => i.id === componente.insumo_componente);
                if (insumoComponente && insumoComponente.id !== undefined) {
                    const cantidadRequerida = componente.cantidad * insumo.cantidad;
                    await actualizarInsumo.mutateAsync({
                        id: insumoComponente.id,
                        insumo: {
                            ...insumoComponente,
                            cantidad: insumoComponente.cantidad - cantidadRequerida,
                            unidad_medida_id: insumoComponente.unidad_medida?.id,
                            tipo_insumo_id: insumoComponente.tipo_insumo?.id,
                            componentes_data: insumoComponente.componentes,
                        },
                    });
                }
            }
        }

        
        registrarInsumo.mutate(insumo, {
            onSuccess: () => {
                setInsumo({
                    nombre: "",
                    descripcion: "",
                    cantidad: 0,
                    activo: true,
                    tipo_empacado: null,
                    fecha_registro: new Date().toISOString(),
                    fecha_caducidad: null,
                    precio_insumo: 0,
                    es_compuesto: false,
                    unidad_medida_id: undefined,
                    tipo_insumo_id: undefined,
                    componentes_data: [],
                });
                addToast({ 
                    title: "Éxito",
                    description: "Insumo registrado exitosamente"
                });
            },
            onError: () => {
                addToast({ 
                    title: "Error",
                    description: "Error al registrar el insumo"
                });
            },
        });
    };

    const handleSubmitUnidadMedida = () => {
        crearUnidadMedida.mutate(nuevaUnidad, {
            onSuccess: () => {
                setIsUnidadModalOpen(false);
                setNuevaUnidad({ nombre: "", descripcion: "" });
                addToast({ 
                    title: "Éxito",
                    description: "Unidad de medida creada exitosamente"
                });
            },
            onError: () => {
                addToast({ 
                    title: "Error",
                    description: "Error al crear la unidad de medida"
                });
            },
        });
    };

    const handleSubmitTipoInsumo = () => {
        crearTipoInsumo.mutate(nuevoTipo, {
            onSuccess: () => {
                setIsTipoModalOpen(false);
                setNuevoTipo({ nombre: "", descripcion: "" });
                addToast({ 
                    title: "Éxito",
                    description: "Tipo de insumo creado exitosamente"
                });
            },
            onError: () => {
                addToast({ 
                    title: "Error",
                    description: "Error al crear el tipo de insumo"
                });
            },
        });
    };

    const handleAddComponente = () => {
        if (nuevoComponente.insumo_componente && nuevoComponente.cantidad > 0) {
            setInsumo({
                ...insumo,
                componentes_data: [...(insumo.componentes_data || []), nuevoComponente],
            });
            setNuevoComponente({ insumo_componente: 0, cantidad: 0 });
        }
    };

    const handleRemoveComponente = (index: number) => {
        setInsumo({
            ...insumo,
            componentes_data: (insumo.componentes_data || []).filter((_, i) => i !== index),
        });
    };

    const formatDateTimeLocal = (isoString: string) => {
        return isoString.slice(0, 16);
    };

    const formatDate = (date: string | null) => {
        return date || "";
    };

    return (
        <DefaultLayout>
            <Formulario
                title="Registro de Insumo"
                onSubmit={handleSubmitInsumo}
                buttonText="Guardar"
                isSubmitting={registrarInsumo.isPending}
            >
                <ReuInput
                    label="Nombre"
                    placeholder="Ingrese el nombre"
                    type="text"
                    variant="bordered"
                    radius="md"
                    value={insumo.nombre}
                    onChange={(e) => setInsumo({ ...insumo, nombre: e.target.value })}
                />
                <ReuInput
                    label="Descripción"
                    placeholder="Ingrese la descripción"
                    type="text"
                    variant="bordered"
                    radius="md"
                    value={insumo.descripcion}
                    onChange={(e) => setInsumo({ ...insumo, descripcion: e.target.value })}
                />
                <ReuInput
                    label="Cantidad"
                    placeholder="Ingrese la cantidad"
                    type="number"
                    variant="bordered"
                    radius="md"
                    value={insumo.cantidad}
                    onChange={(e) => setInsumo({ ...insumo, cantidad: Number(e.target.value) })}
                />
                <div className="flex items-end gap-2">
                    <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700 mb-1">Unidad de Medida</label>
                        <select
                            value={insumo.unidad_medida_id || ""}
                            onChange={(e) => setInsumo({ ...insumo, unidad_medida_id: e.target.value ? Number(e.target.value) : undefined })}
                            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
                            disabled={isLoadingUnidades}
                        >
                            <option value="">Seleccione una unidad</option>
                            {unidadesMedida?.map((unidad) => (
                                <option key={unidad.id} value={unidad.id}>
                                    {unidad.nombre}
                                </option>
                            ))}
                        </select>
                    </div>
                    <button
                        type="button"
                        onClick={() => setIsUnidadModalOpen(true)}
                        className="px-3 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                    >
                        Nueva Unidad
                    </button>
                </div>
                <div className="flex items-end gap-2">
                    <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700 mb-1">Tipo de Insumo</label>
                        <select
                            value={insumo.tipo_insumo_id || ""}
                            onChange={(e) => setInsumo({ ...insumo, tipo_insumo_id: e.target.value ? Number(e.target.value) : undefined })}
                            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
                            disabled={isLoadingTipos}
                        >
                            <option value="">Seleccione un tipo</option>
                            {tiposInsumo?.map((tipo) => (
                                <option key={tipo.id} value={tipo.id}>
                                    {tipo.nombre}
                                </option>
                            ))}
                        </select>
                    </div>
                    <button
                        type="button"
                        onClick={() => setIsTipoModalOpen(true)}
                        className="px-3 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                    >
                        Nuevo Tipo
                    </button>
                </div>
                <div className="flex items-center">
                    <input
                        type="checkbox"
                        checked={insumo.activo}
                        onChange={(e) => setInsumo({ ...insumo, activo: e.target.checked })}
                        className="w-4 h-4 text-blue-500 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <label className="ml-2 text-sm font-medium text-gray-700">Activo</label>
                </div>
                <div className="flex items-center">
                    <input
                        type="checkbox"
                        checked={insumo.es_compuesto}
                        onChange={(e) => setInsumo({ ...insumo, es_compuesto: e.target.checked, componentes_data: e.target.checked ? insumo.componentes_data : [] })}
                        className="w-4 h-4 text-blue-500 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <label className="ml-2 text-sm font-medium text-gray-700">Es Compuesto</label>
                </div>
                {insumo.es_compuesto && (
                    <div className="col-span-1 sm:col-span-2">
                        <label className="block text-sm font-medium text-gray-700 mb-2">Componentes</label>
                        <div className="flex flex-col sm:flex-row gap-4 mb-4 items-end">
                            <div className="flex-1">
                                <label className="block text-sm font-medium text-gray-700 mb-1">Insumo</label>
                                <select
                                    value={nuevoComponente.insumo_componente}
                                    onChange={(e) => setNuevoComponente({ ...nuevoComponente, insumo_componente: Number(e.target.value) })}
                                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
                                    disabled={isLoadingInsumos}
                                >
                                    <option value="0">Seleccione un insumo</option>
                                    {insumos?.map((insumoItem) => (
                                        <option key={insumoItem.id} value={insumoItem.id}>
                                            {insumoItem.nombre}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div className="w-1/3 sm:w-1/4">
                                <ReuInput
                                    label="Cantidad"
                                    type="number"
                                    variant="bordered"
                                    radius="md"
                                    value={nuevoComponente.cantidad}
                                    onChange={(e) => setNuevoComponente({ ...nuevoComponente, cantidad: Number(e.target.value) })}
                                />
                            </div>
                            <div className="flex items-end">
                                <button
                                    type="button"
                                    onClick={handleAddComponente}
                                    className="px-3 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
                                >
                                    Agregar
                                </button>
                            </div>
                        </div>
                        <div className="space-y-2">
                            {insumo.componentes_data?.map((comp, index) => (
                                <div key={index} className="flex justify-between items-center">
                                    <span className="text-gray-700">
                                        {insumos?.find(i => i.id === comp.insumo_componente)?.nombre || `ID: ${comp.insumo_componente}`} ({comp.cantidad})
                                    </span>
                                    <button
                                        type="button"
                                        onClick={() => handleRemoveComponente(index)}
                                        className="px-2 py-1 bg-red-500 text-white rounded-md hover:bg-red-600"
                                    >
                                        Eliminar
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                <ReuInput
                    label="Tipo de Empacado"
                    placeholder="Ingrese el tipo de empacado"
                    type="text"
                    variant="bordered"
                    radius="md"
                    value={insumo.tipo_empacado || ""}
                    onChange={(e) => setInsumo({ ...insumo, tipo_empacado: e.target.value || null })}
                />
                <ReuInput
                    label="Fecha de Registro"
                    type="datetime-local"
                    variant="bordered"
                    radius="md"
                    value={formatDateTimeLocal(insumo.fecha_registro)}
                    onChange={(e) => setInsumo({ ...insumo, fecha_registro: new Date(e.target.value).toISOString() })}
                />
                <ReuInput
                    label="Fecha de Caducidad"
                    type="date"
                    variant="bordered"
                    radius="md"
                    value={formatDate(insumo.fecha_caducidad)}
                    onChange={(e) => setInsumo({ ...insumo, fecha_caducidad: e.target.value || null })}
                />
                <ReuInput
                    label="Precio del Insumo"
                    placeholder="Ingrese el precio del insumo"
                    type="number"
                    variant="bordered"
                    radius="md"
                    step="0.01"
                    value={insumo.precio_insumo}
                    onChange={(e) => setInsumo({ ...insumo, precio_insumo: Number(e.target.value) })}
                />
                <div className="col-span-1 sm:col-span-2 flex justify-center">
                    <button
                        type="button"
                        onClick={() => navigate("/inventario/listarinsumos/")}
                        className="px-4 py-2 bg-blue-400 text-white rounded-md hover:bg-blue-500"
                    >
                        Listar Insumos
                    </button>
                </div>
            </Formulario>

            <ReuModal
                isOpen={isUnidadModalOpen}
                onOpenChange={setIsUnidadModalOpen}
                title="Crear Nueva Unidad de Medida"
                onConfirm={handleSubmitUnidadMedida}
            >
                <ReuInput
                    label="Nombre"
                    placeholder="Ej. kg, L"
                    type="text"
                    variant="bordered"
                    radius="md"
                    value={nuevaUnidad.nombre}
                    onChange={(e) => setNuevaUnidad({ ...nuevaUnidad, nombre: e.target.value })}
                />
                <ReuInput
                    label="Descripción"
                    placeholder="Descripción de la unidad"
                    type="text"
                    variant="bordered"
                    radius="md"
                    value={nuevaUnidad.descripcion || ""}
                    onChange={(e) => setNuevaUnidad({ ...nuevaUnidad, descripcion: e.target.value })}
                />
            </ReuModal>

            <ReuModal
                isOpen={isTipoModalOpen}
                onOpenChange={setIsTipoModalOpen}
                title="Crear Nuevo Tipo de Insumo"
                onConfirm={handleSubmitTipoInsumo}
            >
                <ReuInput
                    label="Nombre"
                    placeholder="Ej. Fertilizante"
                    type="text"
                    variant="bordered"
                    radius="md"
                    value={nuevoTipo.nombre}
                    onChange={(e) => setNuevoTipo({ ...nuevoTipo, nombre: e.target.value })}
                />
                <ReuInput
                    label="Descripción"
                    placeholder="Descripción del tipo"
                    type="text"
                    variant="bordered"
                    radius="md"
                    value={nuevoTipo.descripcion || ""}
                    onChange={(e) => setNuevoTipo({ ...nuevoTipo, descripcion: e.target.value })}
                />
            </ReuModal>

            {user && <InsumoNotifications userId1={user.id} />}
        </DefaultLayout>
    );
};

export default InsumoPage;