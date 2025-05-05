---
title: "Módulo de Salarios - Gestión de Salarios"
slug: modules/finanzas/salarios
description: "Cómo administrar salarios de trabajadores en el módulo de Salarios de Agrosoft, gestionando el salario base y el valor por hora."
---

El módulo de Salarios en Agrosoft permite registrar y gestionar los salarios de los trabajadores, incluyendo el **salario base** y el **valor por hora** para calcular pagos. Este módulo está vinculado al modelo de `Pago` y se utiliza para determinar el costo laboral de los usuarios.

## Características principales
- Registro de **salarios** con salario base y valor por hora.
- Almacenamiento de datos históricos de salarios.
- Integración con el módulo de **Pagos** para calcular el total a pagar.
- Visualización de salarios en la interfaz de Agrosoft.

## ¿Cómo registrar un salario?
Para registrar un nuevo salario en Agrosoft:
1. Ir a la sección **Salarios → Gestión de Salarios**.
2. Hacer clic en el botón **"Registrar Salario"**.
3. Completar los siguientes campos:
   - **Salario Base:** Monto base del salario (por ejemplo, "1500.00").
   - **Valor por Hora:** Valor por hora trabajada (por ejemplo, "20.00").
4. Guardar los cambios.

## Datos de un Salario
Cada salario tiene la siguiente información:

| Campo             | Tipo de Dato      | Descripción                                      |
|-------------------|-------------------|--------------------------------------------------|
| **ID**            | `Integer`         | Identificador único del salario                 |
| **Salario Base**  | `DecimalField`    | Salario base del trabajador (máx. 10 dígitos, 2 decimales) |
| **Valor por Hora**| `DecimalField`    | Valor por hora trabajada (máx. 10 dígitos, 2 decimales) |

---

## Ejemplos de API para gestionar salarios

A continuación, se presentan los ejemplos de uso de la API para las operaciones CRUD sobre el recurso `/api/salarios`:

### **POST /api/salarios**

Registra un nuevo salario para un trabajador.

**Validaciones:**
- Campos obligatorios: `salario_base`, `valor_por_hora`
- `salario_base` debe ser un número decimal mayor o igual a 0
- `valor_por_hora` debe ser un número decimal mayor o igual a 0

---
### **Ejemplos de solicitudes y respuestas post:**

```json

// POST /api/salarios - Ejemplo de solicitud
{
  "salario_base": 1500.00,
  "valor_por_hora": 20.00
}

// POST /api/salarios - Respuesta exitosa (201 Created)
{
  "id": 1,
  "message": "Salario registrado correctamente"
}

```
---
### **GET /api/salarios**

Obtiene todos los salarios registrados con filtros opcionales.

---

### **Ejemplos de solicitudes y respuestas get:**

```json

// GET /api/salarios - Ejemplo de respuesta (200 OK)
[
  {
    "id": 1,
    "salario_base": 1500.00,
    "valor_por_hora": 20.00
  }
]

```

---

**Parámetros opcionales:**
- `?salario_base_min=1000.00`: Filtra por salario base mínimo
- `?valor_por_hora_min=15.00`: Filtra por valor por hora mínimo

---

### **GET /api/salarios/{id}**

Obtiene un salario específico por su ID.

---

### **Ejemplos de solicitudes y respuestas get por ID:**

```json

// GET /api/salarios/{id} - Ejemplo de respuesta (200 OK)
{
  "id": 1,
  "salario_base": 1500.00,
  "valor_por_hora": 20.00
}

```

---

### **PUT /api/salarios/{id}**

Actualiza un salario existente.

---

### **Ejemplos de solicitudes y respuestas put por ID:**

```json

// PUT /api/salarios/{id} - Ejemplo de solicitud
{
  "salario_base": 1600.00,
  "valor_por_hora": 22.00
}

```

---

**Restricciones:**
- `salario_base` debe ser un número decimal mayor o igual a 0
- `valor_por_hora` debe ser un número decimal mayor o igual a 0

---

### **DELETE /api/salarios/{id}**

Elimina un registro de salario.

**Error común (404 Not Found):**

---

### **Ejemplos de solicitudes y respuestas delete por ID:**
```json

// DELETE /api/salarios/{id} - Respuesta exitosa (200 OK)
{
  "message": "Salario eliminado correctamente"
}

// DELETE /api/salarios/{id} - Error común (404 Not Found)
{
  "error": "No existe el salario especificado"
}