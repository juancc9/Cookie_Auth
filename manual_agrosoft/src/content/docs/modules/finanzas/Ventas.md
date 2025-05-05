---
title: "Módulo de Ventas - Gestión de Ventas"
slug: modules/finanzas/ventas
description: "Cómo administrar ventas de productos agrícolas en el módulo de Ventas de Agrosoft, gestionando productos, cantidades, precios y totales."
---


El módulo de Ventas en Agrosoft permite registrar y gestionar las ventas de productos agrícolas, incluyendo el **producto**, la **cantidad**, el **precio** y el **total** calculado automáticamente. Este módulo está vinculado al modelo de `Cultivo` y registra la fecha de cada venta de forma automática.

## Características principales
- Registro de **ventas** asociadas a productos agrícolas.
- Cálculo automático del **total** basado en la cantidad y el precio.
- Almacenamiento de datos históricos de ventas con fecha automática.
- Integración con el módulo de **Cultivos** para asociar productos.
- Visualización de ventas en la interfaz de Agrosoft.

## ¿Cómo registrar una venta?
Para registrar una nueva venta en Agrosoft:
1. Ir a la sección **Ventas → Gestión de Ventas**.
2. Hacer clic en el botón **"Registrar Venta"**.
3. Completar los siguientes campos:
   - **Producto:** Seleccionar el producto agrícola desde el módulo de Cultivos.
   - **Cantidad:** Cantidad de unidades vendidas (por ejemplo, "100").
   - **Precio:** Precio por unidad (por ejemplo, "2.50").
4. Guardar los cambios.
   - **Nota:** El campo `total` se calcula automáticamente como `precio * cantidad`, y la `fecha` se registra con la fecha y hora actuales.

## Datos de una Venta
Cada venta tiene la siguiente información:

| Campo        | Tipo de Dato         | Descripción                                      |
|--------------|----------------------|--------------------------------------------------|
| **ID**       | `Integer`            | Identificador único de la venta                 |
| **Producto** | `ForeignKey`         | Relación con el modelo `Cultivo` (producto vendido) |
| **Cantidad** | `PositiveIntegerField` | Cantidad de unidades vendidas                  |
| **Total**    | `DecimalField`       | Total calculado (máx. 10 dígitos, 2 decimales, no editable) |
| **Fecha**    | `DateTimeField`      | Fecha y hora de la venta (automática)           |
| **Precio**   | `DecimalField`       | Precio por unidad (máx. 10 dígitos, 2 decimales) |

---

## Ejemplos de API para gestionar ventas

A continuación, se presentan los ejemplos de uso de la API para las operaciones CRUD sobre el recurso `/api/ventas`:

### **POST /api/ventas**

Registra una nueva venta de un producto agrícola.

**Validaciones:**
- Campos obligatorios: `producto`, `cantidad`, `precio`
- `cantidad` debe ser un número entero mayor o igual a 1
- `precio` debe ser un número decimal mayor o igual a 0
- `producto` debe corresponder a un ID válido en la tabla `Cultivo`

---

### **Ejemplos de solicitudes y respuestas post:**

```json

// POST /api/ventas - Ejemplo de solicitud
{
  "producto": 1,
  "cantidad": 100,
  "precio": 2.50
}

// POST /api/ventas - Respuesta exitosa (201 Created)
{
  "id": 1,
  "message": "Venta registrada correctamente"
}

```

---

### **GET /api/ventas**

Obtiene todas las ventas registradas con filtros opcionales.

**Parámetros opcionales:**
- `?producto=1`: Filtra por ID de producto
- `?fecha_desde=2023-01-01`: Ventas después de esta fecha
- `?fecha_hasta=2023-12-31`: Ventas antes de esta fecha

---

### **Ejemplos de solicitudes y respuestas get:**

```json

// GET /api/ventas - Ejemplo de respuesta (200 OK)
[
  {
    "id": 1,
    "producto": {"id": 1, "nombre": "Tomate Bancal 1"},
    "cantidad": 100,
    "total": 250.00,
    "fecha": "2023-01-15T10:30:00Z",
    "precio": 2.50
  }
]

```

---

### **GET /api/ventas/{id}**

Obtiene una venta específica por su ID.

---

### **Ejemplos de solicitudes y respuestas get por ID:**

```json

// GET /api/ventas/{id} - Ejemplo de respuesta (200 OK)
{
  "id": 1,
  "producto": {"id": 1},
  "cantidad": 100,
  "total": 250.00,
  "fecha": "2023-01-15T10:30:00Z",
  "precio": 2.50
}

```

---

### **PUT /api/ventas/{id}**

Actualiza una venta existente.

---

### **Ejemplos de solicitudes y respuestas put por ID:**

```json

// PUT /api/ventas/{id} - Ejemplo de solicitud
{
  "cantidad": 120,
  "precio": 2.75
}

```

---

**Restricciones:**
- No se puede modificar el `producto` asociado
- `cantidad` debe ser un número entero mayor o igual a 1
- `precio` debe ser un número decimal mayor o igual a 0

---

### **DELETE /api/ventas/{id}**

Elimina un registro de venta.

**Error común (404 Not Found):**

---

### **Ejemplos de solicitudes y respuestas delete por ID:**

```json

// PUT /api/ventas/{id} - Ejemplo de solicitud
{
  "cantidad": 120,
  "precio": 2.75
}

// DELETE /api/ventas/{id} - Respuesta exitosa (200 OK)
{
  "message": "Venta eliminada correctamente"
}

// DELETE /api/ventas/{id} - Error común (404 Not Found)
{
  "error": "No existe la venta especificada"
}