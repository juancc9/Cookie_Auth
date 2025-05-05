import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import DefaultLayout from "@/layouts/default";
import {useRegistrarPrecioProducto,useUnidadesMedida,useCrearUnidadMedida,} from "@/hooks/inventario/usePrecio_Producto";
import { useCosechas } from "@/hooks/cultivo/usecosecha";
import { ReuInput } from "@/components/globales/ReuInput";
import Formulario from "@/components/globales/Formulario";
import ReuModal from "@/components/globales/ReuModal";
import { PrecioProducto, UnidadMedida } from "@/types/inventario/Precio_producto";
import { addToast } from "@heroui/react";

const PrecioProductoPage: React.FC = () => {
    const navigate = useNavigate();
    const { data: cosechas } = useCosechas();
    const { data: unidadesMedida, isLoading: isLoadingUnidades } =
        useUnidadesMedida();
    const registrarPrecioProducto = useRegistrarPrecioProducto();
    const crearUnidadMedida = useCrearUnidadMedida();

    const [precioProducto, setPrecioProducto] = useState<
        Omit<PrecioProducto, "id" | "unidad_medida"> & { unidad_medida_id?: number }
    >({
        cosecha: 0,
        precio: 0,
        fecha_registro: new Date().toISOString().slice(0, 10),
        stock: 0,
        fecha_caducidad: null,
        unidad_medida_id: undefined,
    });

    const [nuevaUnidad, setNuevaUnidad] = useState<
        Omit<UnidadMedida, "id" | "fecha_creacion" | "creada_por_usuario">
    >({
        nombre: "",
        descripcion: "",
    });
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleSubmitPrecioProducto = (e: React.FormEvent) => {
        e.preventDefault();
        if (!precioProducto.cosecha) {
            addToast({
                title: "Error",
                description: "Seleccione una cosecha válida",
                timeout: 3000,
            });
            return;
        }
        registrarPrecioProducto.mutate(precioProducto, {
            onSuccess: () => {
                setPrecioProducto({
                    cosecha: 0,
                    precio: 0,
                    fecha_registro: new Date().toISOString().slice(0, 10),
                    stock: 0,
                    fecha_caducidad: null,
                    unidad_medida_id: undefined,
                });
            },
        });
    };

    const handleSubmitUnidadMedida = () => {
        crearUnidadMedida.mutate(nuevaUnidad, {
            onSuccess: () => {
                setIsModalOpen(false);
                setNuevaUnidad({ nombre: "", descripcion: "" });
            },
        });
    };

    const formatDate = (date: string | null) => {
        return date || "";
    };

    return (
        <DefaultLayout>
            <Formulario
                title="Registro de Precio de Producto"
                onSubmit={handleSubmitPrecioProducto}
                buttonText="Guardar"
                isSubmitting={registrarPrecioProducto.isPending}
            >
                <div className="flex items-end gap-2">
                    <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Cosecha
                        </label>
                        <select
                            value={precioProducto.cosecha || ""}
                            onChange={(e) =>
                                setPrecioProducto({
                                    ...precioProducto,
                                    cosecha: Number(e.target.value),
                                })
                            }
                            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="">Seleccione una cosecha</option>
                            {cosechas?.map((cosecha) => (
                                <option key={cosecha.id} value={cosecha.id}>
                                    {`Cosecha ${cosecha.id_cultivo} - ${cosecha.fecha}`}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
                <div className="flex items-end gap-2">
                    <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Unidad de Medida
                        </label>
                        <select
                            value={precioProducto.unidad_medida_id || ""}
                            onChange={(e) =>
                                setPrecioProducto({
                                    ...precioProducto,
                                    unidad_medida_id: e.target.value
                                        ? Number(e.target.value)
                                        : undefined,
                                })
                            }
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
                        onClick={() => setIsModalOpen(true)}
                        className="px-3 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                    >
                        Nueva Unidad
                    </button>
                </div>
                <ReuInput
                    label="Precio"
                    placeholder="Ingrese el precio"
                    type="number"
                    variant="bordered"
                    radius="md"
                    step="0.01"
                    value={precioProducto.precio.toString()}
                    onChange={(e) =>
                        setPrecioProducto({
                            ...precioProducto,
                            precio: Number(e.target.value),
                        })
                    }
                />
                <ReuInput
                    label="Fecha de Registro"
                    type="date"
                    variant="bordered"
                    radius="md"
                    value={precioProducto.fecha_registro}
                    onChange={(e) =>
                        setPrecioProducto({
                            ...precioProducto,
                            fecha_registro: e.target.value,
                        })
                    }
                />
                <ReuInput
                    label="Stock"
                    placeholder="Ingrese el stock inicial"
                    type="number"
                    variant="bordered"
                    radius="md"
                    value={precioProducto.stock.toString()}
                    onChange={(e) =>
                        setPrecioProducto({
                            ...precioProducto,
                            stock: Number(e.target.value),
                        })
                    }
                />
                <ReuInput
                    label="Fecha de Caducidad"
                    type="date"
                    variant="bordered"
                    radius="md"
                    value={formatDate(precioProducto.fecha_caducidad)}
                    onChange={(e) =>
                        setPrecioProducto({
                            ...precioProducto,
                            fecha_caducidad: e.target.value || null,
                        })
                    }
                />
                <div className="col-span-1 md:col-span-2 flex justify-center">
                    <button
                        type="button"
                        className="w-full max-w-md px-4 py-3 bg-blue-400 text-white rounded-md hover:bg-blue-500 transition-all duration-200 shadow-md hover:shadow-lg font-medium text-sm uppercase tracking-wide"
                        onClick={() => navigate("/inventario/listarpreciosproductos/")}
                    >
                        Listar Precios de Productos
                    </button>
                </div>
            </Formulario>

            <ReuModal
                isOpen={isModalOpen}
                onOpenChange={setIsModalOpen}
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
                    onChange={(e) =>
                        setNuevaUnidad({ ...nuevaUnidad, nombre: e.target.value })
                    }
                />
                <ReuInput
                    label="Descripción"
                    placeholder="Descripción de la unidad"
                    type="text"
                    variant="bordered"
                    radius="md"
                    value={nuevaUnidad.descripcion || ""}
                    onChange={(e) =>
                        setNuevaUnidad({
                            ...nuevaUnidad,
                            descripcion: e.target.value,
                        })
                    }
                />
            </ReuModal>
        </DefaultLayout>
    );
};

export default PrecioProductoPage;