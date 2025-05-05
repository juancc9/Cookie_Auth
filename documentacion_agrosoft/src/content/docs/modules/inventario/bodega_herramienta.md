---
title: "Gestión de Bodega Herramienta"
slug: modules/inventario/bodega_herramienta
description: "Documentación de la API para la gestión de bodega herramienta en Agrosoft."
---

# **Gestión de Bodega Herramienta**

Los **registros de Bodega Herramienta** documentan la relación entre herramientas y bodegas, incluyendo la cantidad disponible de cada herramienta en una bodega específica. Esta documentación cubre los endpoints RESTful y las conexiones WebSocket para su gestión.

## **Endpoints de la API**

### **Obtener todas las relaciones entre bodegas y herramientas**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
```http
http://127.0.0.1:8000/inventario/bodega_herramienta/
```

**Parámetros opcionales:**
- `?bodega=1`: Filtra por ID de bodega.
- `?herramienta=2`: Filtra por ID de herramienta.

**Ejemplo de respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "bodega": 1,
    "herramienta": 2,
    "cantidad": 5
  }
]
```

---

### **Obtener una relación específica por ID**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
```http
http://127.0.0.1:8000/inventario/bodega_herramienta/{id}/
```

**Ejemplo de respuesta (200 OK):**
```json
{
  "id": 1,
  "bodega": 1,
  "herramienta": 2,
  "cantidad": 5
}
```

---

### **Registrar una nueva relación entre bodega y herramienta**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>
URL:
```http
http://127.0.0.1:8000/inventario/bodega_herramienta/
```

**Ejemplo de solicitud:**
```json
{
  "bodega": 1,
  "herramienta": 2,
  "cantidad": 3
}
```

**Validaciones:**
- Campos obligatorios: `bodega`, `herramienta`
- `cantidad` debe ser un entero positivo (≥ 1)

**Ejemplo de respuesta (201 Created):**
```json
{
  "id": 2,
  "bodega": 1,
  "herramienta": 2,
  "cantidad": 3
}
```

---

### **Actualizar una relación entre bodega y herramienta**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>
URL:
```http
http://127.0.0.1:8000/inventario/bodega_herramienta/{id}/
```

**Ejemplo de solicitud:**
```json
{
  "cantidad": 4
}
```

**Restricciones:**
- Solo se puede modificar `cantidad`

**Ejemplo de respuesta (200 OK):**
```json
{
  "id": 1,
  "bodega": 1,
  "herramienta": 2,
  "cantidad": 4
}
```

---

### **Eliminar una relación entre bodega y herramienta**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>
URL:
```http
http://127.0.0.1:8000/inventario/bodega_herramienta/{id}/
```

**Ejemplo de respuesta exitosa (204 No Content):**
```json
{}
```

---

## **WebSocket**

**Conexión:**
```http
ws://127.0.0.1:8000/inventario/bodega_herramienta/
```

Permite actualizaciones en tiempo real de las relaciones entre bodegas y herramientas.

### **Estado inicial:**
```json
{
  "action": "initial_state",
  "data": [
    {
      "id": 1,
      "bodega": "Bodega Central",
      "herramienta": "Martillo",
      "cantidad": 5
    }
  ],
  "message_id": "uuid-aqui"
}
```

### **Eventos en tiempo real:**

#### **Creación/Actualización:**
```json
{
  "id": 1,
  "bodega": "Bodega Central",
  "herramienta": "Martillo",
  "cantidad": 5,
  "accion": "create"
}
```

#### **Eliminación:**
```json
{
  "id": 1,
  "accion": "delete"
}
```

---

## **Manejo de Errores**

### **Ejemplo de error (404 Not Found):**
```json
{
  "detail": "No encontrado."
}
```

### **Ejemplo de error (400 Bad Request):**
```json
{
  "error": "Bad Request",
  "detail": "El campo 'cantidad' debe ser un entero positivo."
}
```

---

## **Buenas Prácticas**
✔️ **Registro inmediato:** Actualizar la cantidad tras cada movimiento de herramientas.  
✔️ **Detalles específicos:** Verificar que la cantidad coincida con el inventario físico.  
✔️ **Sincronización:** Usar WebSocket para reflejar cambios en tiempo real en el frontend.  

---

## **Integraciones Comunes**
▸ **Notificaciones:** Alertas cuando la cantidad de herramientas cae por debajo de un umbral.  
▸ **Inventario:** Actualización automática del stock en `Herramienta` al modificar `BodegaHerramienta`.  
▸ **Reportes:**  
  - Disponibilidad por bodega  
  - Histórico de movimientos de herramientas  

---

## **Relaciones en el Sistema**
```mermaid
graph TD
    A[Bodega] --> B[BodegaHerramienta]
    C[Herramienta] --> B
```

