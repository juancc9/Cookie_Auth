export const opcionesModulos = [
    { nombre: "Cultivo", modulo: "cultivo" },
    { nombre: "Inventario", modulo: "inventario" },
    { nombre: "Usuarios", modulo: "usuarios" },
    { nombre: "IoT", modulo: "iot" },
    { nombre: "Finanzas", modulo: "finanzas" },

];

export const reportesPorModulo: Record<string, { nombre: string; reporte: string }[]> = {
    cultivo: [
        { nombre: "Reporte de Cosechas", reporte: "cosechas" },
        { nombre: "Reporte de lotes", reporte: "lote" },
        { nombre: "Reporte de actividades", reporte: "actividades"},
        { nombre: "Reporte de actividades", reporte: "Bancal"},
    ],
    inventario: [
        { nombre: "Insumos", reporte: "insumo" },
        { nombre: "Herramientas", reporte: "herramientas" },
        { nombre: "Productos", reporte: "precio-producto" },
    ],
    usuarios: [
        { nombre: "Reporte de Usuarios Activos", reporte: "usuarios" },
    ],
    iot: [
        { nombre: "Reporte de Sensores", reporte: "datosmetereologicos" },
    ],
    finanzas: [
        { nombre: "Reporte de Ingresos", reporte: "venta" },
        { nombre: "Reporte de Gastos", reporte: "gastos" },
        { nombre: "Reporte de Egresos", reporte: "pago" },

    ],
};
