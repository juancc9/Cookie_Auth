---
title: "Gestión de Bodega"
slug: modules/inventario/bodega
description: "Documentación de la API para la gestión de bodegas en Agrosoft."
---

# **Gestión de Bodega**

El módulo **Bodega** permite administrar el almacenamiento de herramientas e insumos dentro de la finca. Esta documentación cubre los endpoints RESTful para su gestión.

## **Endpoints de la API**

### **Obtener todas las bodegas**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code">http://127.0.0.1:8000/bodega/</div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/bodega/"><div></div></button></div></figure></div>  </section>

**Parámetros opcionales:**
- `?ubicacion=Sector A`: Filtra por ubicación.
- `?capacidad_min=100`: Filtra bodegas con capacidad mayor o igual.
- `?capacidad_max=1000`: Filtra bodegas con capacidad menor o igual.

**Ejemplo de respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Bodega Central",
    "ubicacion": "Sector A",
    "capacidad": 500,
    "responsable": {"id": 3, "nombre": "Juan Pérez"}
  }
]
```

---

### **Obtener una bodega por ID**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code">http://127.0.0.1:8000/bodega/{id}/</div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/bodega/{id}/"><div></div></button></div></figure></div>  </section>

**Ejemplo de respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Bodega Central",
  "ubicacion": "Sector A",
  "capacidad": 500,
  "responsable": {"id": 3, "nombre": "Juan Pérez"}
}
```

---

### **Registrar una nueva bodega**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code">http://127.0.0.1:8000/bodega/</div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/bodega/"><div></div></button></div></figure></div>  </section>

**Ejemplo de solicitud:**
```json
{
  "nombre": "Bodega Norte",
  "ubicacion": "Sector B",
  "capacidad": 300,
  "responsable": 5
}
```

**Ejemplo de respuesta (201 Created):**
```json
{
  "id": 2,
  "message": "Bodega registrada correctamente"
}
```

---

### **Actualizar una bodega**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code">http://127.0.0.1:8000/bodega/{id}/</div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/bodega/{id}/"><div></div></button></div></figure></div>  </section>

**Ejemplo de solicitud:**
```json
{
  "nombre": "Bodega Principal",
  "capacidad": 600
}
```

**Ejemplo de respuesta (200 OK):**
```json
{
  "id": 1,
  "message": "Bodega actualizada correctamente"
}
```

---

### **Eliminar una bodega**

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code">http://127.0.0.1:8000/bodega/{id}/</div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/bodega/{id}/"><div></div></button></div></figure></div>  </section>

**Ejemplo de respuesta exitosa (200 OK):**
```json
{
  "message": "Bodega eliminada correctamente"
}
```

---

## **Manejo de Errores**

### **Ejemplo de error (bodega con elementos asociados):**
```json
{
  "error": "Conflict",
  "detail": "No se puede eliminar la bodega porque tiene herramientas o insumos asignados."
}
```

---

## **Buenas Prácticas**
✔️ **Registro actualizado**: Mantener la información de las bodegas actualizada.  
✔️ **Verificación de capacidad**: No exceder la capacidad registrada.  
✔️ **Asignación de responsables**: Cada bodega debe tener un responsable asignado.  

---

