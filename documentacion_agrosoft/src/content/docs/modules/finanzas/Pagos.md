---
title: "Módulo de Pagos - Gestión de Pagos"
slug: modules/finanzas/pagos
description: "Cómo administrar pagos a trabajadores en el módulo de Pagos de Agrosoft, calculando el total a pagar basado en horas trabajadas y salario por hora."
---

El módulo de Pagos en Agrosoft permite registrar y calcular los pagos a trabajadores basados en las **horas trabajadas** y el **salario por hora** asociado a cada usuario. Este módulo está vinculado al modelo de `Salario` y `Usuarios`, y calcula automáticamente el **total a pagar** mediante un método integrado en el modelo.

## Características principales
- Registro de **pagos** asociados a usuarios específicos.
- Cálculo automático del **total a pagar** basado en horas trabajadas y salario por hora.
- Almacenamiento de datos históricos de pagos.
- Integración con los módulos de **Salarios** y **Usuarios** para una gestión eficiente.
- Visualización de pagos en la interfaz de Agrosoft.

## ¿Cómo registrar un pago?
Para registrar un nuevo pago en Agrosoft:
1. Ir a la sección **Pagos → Gestión de Pagos**.
2. Hacer clic en el botón **"Registrar Pago"**.
3. Completar los siguientes campos:
   - **Horas Trabajadas:** Cantidad de horas trabajadas por el usuario (por ejemplo, "40").
   - **Salario:** Seleccionar el salario asociado al trabajador desde el módulo de Salarios.
   - **Usuario:** Seleccionar el usuario al que corresponde el pago.
   - **Total a Pagar:** Se calcula automáticamente al guardar (opcional para edición manual).
4. Guardar los cambios.
   - **Nota:** El método `calcular_total()` se ejecuta automáticamente para determinar el total a pagar.

## Datos de un Pago
Cada pago tiene la siguiente información:

| Campo               | Tipo de Dato      | Descripción                                      |
|---------------------|-------------------|--------------------------------------------------|
| **ID**              | `Integer`         | Identificador único del pago                    |
| **Horas Trabajadas**| `IntegerField`    | Cantidad de horas trabajadas por el usuario     |
| **Salario**         | `ForeignKey`      | Relación con el modelo `Salario` (salario/hora) |
| **Total a Pagar**   | `DecimalField`    | Total calculado (máx. 10 dígitos, 2 decimales)  |
| **Usuario**         | `ForeignKey`      | Relación con el modelo `Usuarios`               |

---

## Ejemplos de API para gestionar pagos

A continuación, se presentan los ejemplos de uso de la API para las operaciones CRUD sobre el recurso `/api/pagos`:

### **POST /api/pagos**

Registra un nuevo pago para un trabajador.

**Validaciones:**
- Campos obligatorios: `horas_trabajadas`, `salario`, `usuario`
- `horas_trabajadas` debe ser un número entero mayor o igual a 0
- `salario` y `usuario` deben corresponder a IDs válidos en sus respectivas tablas

---
### **Ejemplos de solicitudes y respuestas post:**

```json
// POST /api/pagos - Ejemplo de solicitud
{
  "horas_trabajadas": 40,
  "salario": 1,
  "usuario": 5
}

// POST /api/pagos - Respuesta exitosa (201 Created)
{
  "id": 1,
  "message": "Pago registrado correctamente"
}
```
---
### **GET /api/pagos**

Obtiene todos los pagos registrados con filtros opcionales.

---

### **Ejemplos de solicitudes y respuestas get:**

```json

// GET /api/pagos - Ejemplo de respuesta (200 OK)
[
  {
    "id": 1,
    "horas_trabajadas": 40,
    "salario": {"id": 1, "valor_por_hora": 20.00},
    "total_a_pagar": 800.00,
    "usuario": {"id": 5, "nombre": "Juan Pérez"}
  }
]
```

---


**Parámetros opcionales:**
- `?usuario=5`: Filtra por ID de usuario
- `?salario=1`: Filtra por ID de salario

---

### **GET /api/pagos/{id}**

Obtiene un pago específico por su ID.

---

### **Ejemplos de solicitudes y respuestas get por ID:**

```json

// GET /api/pagos/{id} - Ejemplo de respuesta (200 OK)
{
  "id": 1,
  "horas_trabajadas": 40,
  "salario": {"id": 1},
  "total_a_pagar": 800.00,
  "usuario": {"id": 5}
}

```

---

### **PUT /api/pagos/{id}**

Actualiza un pago existente.

---

### **Ejemplos de solicitudes y respuestas put por ID:**

```json

// PUT /api/pagos/{id} - Ejemplo de solicitud
{
  "horas_trabajadas": 45,
  "salario": 1
}
```

**Restricciones:**
- No se puede modificar el `usuario` asociado
- `horas_trabajadas` debe ser un número entero mayor o igual a 0

---

### **DELETE /api/pagos/{id}**

Elimina un registro de pago.

**Error común (404 Not Found):**

---

### **Ejemplos de solicitudes y respuestas delete por ID:**
```json

// DELETE /api/pagos/{id} - Respuesta exitosa (200 OK)
{
  "message": "Pago eliminado correctamente"
}

// DELETE /api/pagos/{id} - Error común (404 Not Found)
{
  "error": "No existe el pago especificado"
}
