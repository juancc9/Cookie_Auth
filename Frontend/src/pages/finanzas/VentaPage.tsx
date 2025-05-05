import React, { useState, ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import DefaultLayout from "@/layouts/default";
import { useVenta } from "@/hooks/finanzas/useVenta";
import { ReuInput } from "@/components/globales/ReuInput";
import { Venta } from "@/types/finanzas/Venta";
import { usePreciosProductos } from "@/hooks/inventario/usePrecio_Producto";
import Tabla from "@/components/globales/Tabla";
import {Trash2 } from 'lucide-react';

const VentaPage: React.FC = () => {
  const [venta, setVenta] = useState<Venta>({
    producto: 0,
    cantidad: 0,
    precio: 0,
    total: 0,
    fecha: '',
  });

  const [productosAgregados, setProductosAgregados] = useState<Venta[]>([]);
  const [editIndex, setEditIndex] = useState<number | null>(null);

  const { registrarVenta, isRegistrando } = useVenta();
  const { data: precio_producto, isLoading: precioProductoLoading } = usePreciosProductos();
  const navigate = useNavigate();
  
  const handleChange = (field: keyof Venta) => (e: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { value } = e.target;
    setVenta((prev) => ({
      ...prev,
      [field]: field === "cantidad" || field === "precio" || field === "producto" ? Number(value) : value,
    }));
  };

  const agregarProducto = () => {
    const productoSeleccionado = precio_producto?.find(p => p.id === venta.producto);
    if (!productoSeleccionado) return;

    const nuevoProducto = {
      ...venta,
      precio: productoSeleccionado.precio,
      total: venta.cantidad * productoSeleccionado.precio,
    };

    if (editIndex !== null) {
      const nuevosProductos = [...productosAgregados];
      nuevosProductos[editIndex] = nuevoProducto;
      setProductosAgregados(nuevosProductos);
      setEditIndex(null);
    } else {
      setProductosAgregados([...productosAgregados, nuevoProducto]);
    }

    setVenta({
      producto: 0,
      cantidad: 0,
      precio: 0,
      total: 0,
      fecha: venta.fecha,
    });
  };

  

  const handleDelete = (index: number) => {
    const nuevosProductos = productosAgregados.filter((_, i) => i !== index);
    setProductosAgregados(nuevosProductos);
  };

  const columns = [
    { name: "Producto", uid: "producto" },
    { name: "Cantidad", uid: "cantidad" },
    { name: "Precio Unitario", uid: "precio" },
    { name: "Total", uid: "total" },
    { name: "Quitar", uid: "acciones" },
  ];
  const transformedData = productosAgregados.map((venta, index) => {
    const productoNombre = precio_producto?.find(p => p.id === venta.producto)?.cultivo || "Desconocido";
    const precio = Number(venta.precio) || 0;
    const total = Number(venta.total) || 0;
    
    return {
      id: index.toString(),
      producto: productoNombre,
      cantidad: venta.cantidad,
      precio: `${precio.toFixed(2)}`,
      total: `${total.toFixed(2)}`,
      acciones: (
        <>
          <button
            className="text-red-500 hover:underline"
            onClick={() => handleDelete(index)}
          >
            <Trash2 size={22} color='red'/>
          </button>
        </>
      ),
    };
  });

  const calcularTotalVenta = () => {
    return productosAgregados.reduce((sum, item) => sum + item.total, 0);
  };

  return (
    <DefaultLayout>
      <div className="w-full flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-4xl bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Registro de Venta</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Producto</label>
              <select
                name="producto"
                value={venta.producto || ""}
                onChange={handleChange("producto")}
                className="w-full mb-4 p-2 border rounded"
                disabled={precioProductoLoading}
              >
                <option value="0">Seleccione un producto</option>
                {precio_producto?.map((precioProducto) => (
                  <option key={precioProducto.id} value={precioProducto.id}>
                    {precioProducto.cultivo}
                  </option>
                ))}
              </select>

              <ReuInput
                label="Cantidad"
                placeholder="Ingrese la cantidad"
                type="number"
                value={String(venta.cantidad)}
                onChange={handleChange("cantidad")}
              />
            </div>

            <div>
              <ReuInput
                label="Fecha"
                placeholder="Seleccione la fecha"
                type="date"
                value={venta.fecha}
                onChange={handleChange("fecha")}
              />

              <div className="mt-6">
                <button
                  className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
                  onClick={(e) => {
                    e.preventDefault();
                    agregarProducto();
                  }}
                  disabled={venta.producto === 0 || venta.cantidad <= 0}
                >
                  {editIndex !== null ? "Actualizar Producto" : "Agregar Producto"}
                </button>
              </div>
            </div>
          </div>

          {productosAgregados.length > 0 && (
            <>
              <div className="mb-4">
                <Tabla columns={columns} data={transformedData} />
              </div>

              <div className="flex justify-between items-center mt-4">
                <div className="text-lg font-semibold">
                  Total Venta: {calcularTotalVenta().toFixed(2)}
                </div>

                <button
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
                  disabled={isRegistrando || productosAgregados.length === 0}
                  onClick={(e) => {
                    e.preventDefault();
                    productosAgregados.forEach(producto => {
                      registrarVenta(
                        { ...producto, fecha: venta.fecha },
                        {
                          onSuccess: () => {
                            setProductosAgregados([]);
                            setVenta({
                              producto: 0,
                              cantidad: 0,
                              precio: 0,
                              total: 0,
                              fecha: new Date().toISOString().split("T")[0],
                            });
                          },
                        }
                      );
                    });
                  }}
                >
                  {isRegistrando ? "Registrando..." : "Finalizar Venta"}
                </button>
              </div>
            </>
          )}

          <button
            className="w-full px-4 py-2 bg-green-600 text-white rounded-lg mt-4 hover:bg-green-700 transition-all duration-300 ease-in-out shadow-md hover:shadow-lg transform hover:scale-105"
            onClick={() => navigate("/finanzas/listarventas/")}
          >
            Listar Ventas
          </button>
        </div>
      </div>
    </DefaultLayout>
  );
};

export default VentaPage;