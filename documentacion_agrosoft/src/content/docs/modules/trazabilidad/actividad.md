---
title: Gestion de actividades
---


Las **Actividades** son tareas programadas relacionadas con el manejo de cultivos, que involucran recursos, personal y planificación.

## ¿Cómo registrar una actividad?
Para registrar una nueva actividad en Agrosoft:
1. Navega al módulo de Actividades
2. Haz clic en el botón **"Nueva Actividad"**
3. Completa los siguientes campos obligatorios:
   - **Tipo de actividad**: Selecciona de la lista disponible
   - **Programación**: Asocia a una programación existente
   - **Fechas**: Define inicio y fin de la actividad
   - **Usuario responsable**: Asigna un usuario
   - **Cultivo**: Selecciona el cultivo afectado

## Datos de una actividad
Cada actividad tiene la siguiente información:

| Campo               | Tipo                | Descripción |  
|---------------------|---------------------|-------------|  
| **id**              | `AutoField`         | Identificador único |  
| **tipo_actividad**  | `ForeignKey`        | Relación con tabla TipoActividad |  
| **programacion**    | `ForeignKey`        | Relación con tabla Programación |  
| **descripcion**     | `TextField`         | Detalles de la actividad |  
| **fecha_inicio**    | `DateField`         | Fecha de inicio |  
| **fecha_fin**       | `DateField`         | Fecha de finalización |  
| **usuario**         | `ForeignKey`        | Usuario responsable |  
| **cultivo**         | `ForeignKey`        | Cultivo asociado |  
| **insumo**          | `ForeignKey`        | Insumo utilizado |  
| **cantidadUsada**   | `IntegerField`      | Cantidad de insumo utilizada |  

## Ejemplo de API para gestionar actividades

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/actividades/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/actividades/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |

**Ejemplo de solicitud:**
```json
{
  "tipo_actividad": 3,
  "programacion": 5,
  "descripcion": "Aplicación de fertilizante orgánico",
  "fecha_inicio": "2023-11-20",
  "fecha_fin": "2023-11-21",
  "usuario": 12,
  "cultivo": 45,
  "insumo": 8,
  "cantidadUsada": 5
}
```

**Validaciones:**
- `fecha_inicio` no puede ser posterior a `fecha_fin`
- `cultivo` debe estar activo
- `insumo` debe tener suficiente stock disponible
- `cantidadUsada` debe ser mayor que 0

**Ejemplo de respuesta exitosa (201 Created):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{
  "id": 1,
  "tipo_actividad": 3,
  "programacion": 5,
  "descripcion": "Aplicación de fertilizante orgánico",
  "fecha_inicio": "2023-11-20",
  "fecha_fin": "2023-11-21",
  "usuario": 12,
  "cultivo": 45,
  "insumo": 8,
  "cantidadUsada": 5
}
```

**Posibles errores:**
- `400 Bad Request`: Si faltan campos obligatorios
- `409 Conflict`: Si hay solapamiento de fechas con otras actividades

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/actividades/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/actividades/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
[
  {
    "id": 1,
    "tipo_actividad": {
      "id": 3,
      "nombre": "Fertilización"
    },
    "programacion": {
      "id": 5,
      "nombre": "Programación Noviembre"
    },
    "descripcion": "Aplicación de fertilizante orgánico",
    "fecha_inicio": "2023-11-20",
    "fecha_fin": "2023-11-21",
    "usuario": {
      "id": 12,
      "nombre": "Juan Pérez"
    },
    "cultivo": {
      "id": 45,
      "nombre": "Lechuga Romana - B2"
    },
    "insumo": {
      "id": 8,
      "nombre": "Fertilizante Orgánico 5kg"
    },
    "cantidadUsada": 5
  }
]
```

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/actividades/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/actividades/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{
  "id": 1,
  "tipo_actividad": {
    "id": 3,
    "nombre": "Fertilización"
  },
  "programacion": {
    "id": 5,
    "nombre": "Programación Noviembre"
  },
  "descripcion": "Aplicación de fertilizante orgánico",
  "fecha_inicio": "2023-11-20",
  "fecha_fin": "2023-11-21",
  "usuario": {
    "id": 12,
    "nombre": "Juan Pérez"
  },
  "cultivo": {
    "id": 45,
    "nombre": "Lechuga Romana - B2"
  },
  "insumo": {
    "id": 8,
    "nombre": "Fertilizante Orgánico 5kg"
  },
  "cantidadUsada": 5
}
```

**Posibles errores:**
- `404 Not Found`: Si el ID no existe

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/actividades/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/actividades/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |

**Ejemplo de solicitud:**
```json
{
  "descripcion": "Aplicación de fertilizante orgánico (dosis doble)",
  "cantidadUsada": 10,
  "fecha_fin": "2023-11-22"
}
```

**Restricciones:**
- No se puede modificar `cultivo` o `tipo_actividad` después de creado
- `fecha_inicio` solo editable si la actividad no ha comenzado

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{
  "id": 1,
  "message": "Actividad actualizada correctamente"
}
```

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/actividades/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/actividades/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |

**Ejemplo de respuesta exitosa (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{
  "message": "Actividad eliminada correctamente",
  "id": 1
}
```

**Error común (400 Bad Request):**
```json
{
  "error": "No se puede eliminar",
  "detail": "La actividad ya ha comenzado"
}
```

---

## **Ejemplos de Uso**

### **Crear y luego actualizar una actividad:**
```bash
# Crear (POST)
POST /actividades/
{
  "tipo_actividad": 1,
  "programacion": 2,
  "descripcion": "Riego por goteo",
  "fecha_inicio": "2023-11-25",
  "fecha_fin": "2023-11-25",
  "usuario": 15,
  "cultivo": 32,
  "insumo": null,
  "cantidadUsada": 0
}

# Actualizar (PUT)
PUT /actividades/8
{
  "cantidadUsada": 3,
  "descripcion": "Ajuste de cantidad según recomendación técnica"
}
```

### **Filtrar actividades:**
```bash
# Por cultivo
GET /actividades/?cultivo=45

# Por rango de fechas
GET /actividades/?fecha_inicio=2023-11-01&fecha_fin=2023-11-30
```

---

## **Relaciones en el Sistema**
Las **Actividades** se vinculan con:
- **Usuarios** (responsables de ejecución)
- **Cultivos** (afectados por la actividad)
- **Insumos** (recursos utilizados)
- **Programaciones** (calendario de trabajo)

---

## **Buenas Prácticas**
 **Planificación anticipada**: Programar actividades con al menos 3 días de anticipación  
 **Verificación de stock**: Confirmar disponibilidad de insumos antes de crear actividades  
 **Actualización oportuna**: Registrar cambios en fechas o cantidades tan pronto ocurran  
 **Documentación detallada**: Usar el campo descripción para notas relevantes