---
title: "Gestión de tipo de actividad"
---
Los **Tipos de Actividad** permiten clasificar las diferentes labores agrícolas realizadas en el sistema (siembra, riego, fertilización, poda, cosecha, etc.). Esta documentación cubre los endpoints RESTful para su gestión.

---

## **Endpoints de la API**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_actividad/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_actividad/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |


Resultado: Obtiene todos los tipos de actividad registrados.

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
[
  {
    "id": 1,
    "nombre": "Riego",
    "descripcion": "Aplicación controlada de agua a los cultivos"
  },
  {
    "id": 2,
    "nombre": "Fertilización",
    "descripcion": "Aporte de nutrientes al suelo"
  }
]
```

**Parámetros opcionales:**
- `?search=riego`: Busca tipos por nombre (búsqueda insensible a mayúsculas).

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_actividad/{id}</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_actividad/{id}"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |


Resultado: Obtiene un tipo de actividad específico por su ID.

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 1,
  "nombre": "Riego",
  "descripcion": "Aplicación controlada de agua a los cultivos"
}
```

**Posibles errores:**
- `404 Not Found`: Si el ID no existe.

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_actividad/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_actividad/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |


Resultado: Crea un nuevo tipo de actividad.

**Ejemplo de solicitud:**
```json
{
  "nombre": "Poda",
  "descripcion": "Corte de ramas para mejorar el crecimiento"
}
```

**Validaciones:**
- `nombre`: Requerido, máximo 255 caracteres, único.
- `descripcion`: Opcional.

**Ejemplo de respuesta exitosa (201 Created):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "message": "tipo de actividad registrado con exito"
}
```

**Posibles errores:**
- `400 Bad Request`: Si faltan campos obligatorios.
- `409 Conflict`: Si el nombre ya existe.

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_actividad/{id}</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_actividad/{id}"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |


Resultado: Actualiza un tipo de actividad existente.

**Ejemplo de solicitud:**
```json
{
  "nombre": "Poda de formación",
  "descripcion": "Poda para guiar la estructura de la planta"
}
```

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{
  "message": "tipo de actividad actualizado con exito"
}
```

**Notas:**
- Se pueden actualizar campos individualmente.
- El `nombre` debe seguir siendo único.

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_actividad/{id}</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_actividad/{id}"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |


Resultado: Elimina un tipo de actividad (si no está en uso).

**Ejemplo de respuesta exitosa (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "message": "Tipo de actividad eliminado correctamente"
}
```

**Posibles errores:**
- `404 Not Found`: Si el ID no existe.
- `409 Conflict`: Si el tipo está asociado a actividades registradas.

---

## ** Ejemplos de Uso**

### **Crear y luego actualizar un tipo:**
```bash
Metodo: POST 
URL:http://127.0.0.1:8000/cultivo/tipo_actividad/
{
  "nombre": "Deshierbe",
  "descripcion": "Eliminación de malezas"
}

Metodo: PUT 
URL:http://127.0.0.1:8000/cultivo/tipo_actividad/4
{
  "descripcion": "Eliminación manual o química de malezas"
}
```

### **Listar tipos de actividad:**
```bash
Metodo: GET 
URL:http://127.0.0.1:8000/cultivo/tipo_actividad/
```

---

## **Manejo de Errores**

### **Ejemplo de error (nombre duplicado):**
```json
{
   "message": "Ya existe un tipo de actividad con este nombre"
}
```

### **Buenas Prácticas**
**Nomenclatura clara**: Usar nombres descriptivos (ej: "Fertilización foliar" en lugar de "Aplicación 1").  
**Descripciones útiles**: Incluir detalles como métodos comunes o precauciones.  
**Evitar duplicados**: Revisar tipos existentes antes de crear nuevos.