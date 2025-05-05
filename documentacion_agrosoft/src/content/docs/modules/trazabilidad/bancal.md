---
title: Gestion de bancales
---

## ¿Qué es un Bancal?  
Los **bancales** son subdivisiones de los lotes que permiten una gestión más detallada del cultivo. Cada bancal tiene dimensiones y ubicación específica dentro de un lote.

## ¿Cómo registrar un bancal?
Para crear un nuevo bancal en Agrosoft:
1. Accede al módulo de Cultivos > Bancales
2. Haz clic en **"Nuevo Bancal"**
3. Completa los campos obligatorios:
   - **Nombre**: Identificador único (ej: "Bancal N1")
   - **Dimensiones**: Ancho (X) y Largo (Y) en metros
   - **Posición**: Coordenadas dentro del lote
   - **Lote**: Selecciona el lote contenedor

## Estructura de Datos

| Campo           | Tipo de Dato       | Descripción | Validaciones |
|-----------------|--------------------|-------------|--------------|
| **ID**         | `AutoField`        | Identificador único | - |
| **Nombre**     | `CharField`        | Nombre identificador | Único, máx. 15 chars |
| **TamX**       | `DecimalField`     | Ancho (metros) | Máx 3 enteros, 2 decimales |
| **TamY**       | `DecimalField`     | Largo (metros) | Máx 3 enteros, 2 decimales |
| **posX**       | `DecimalField`     | Posición horizontal | 2 decimales |
| **posY**       | `DecimalField`     | Posición vertical | 2 decimales |
| **Lote**       | `ForeignKey`       | Lote contenedor | Requerido |

## Ejemplo de API para gestionar bancales

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/bancales/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/bancales/"><div></div></button></div></figure></div>  
</section>

**Encabezados de la solicitud**
| Encabezado        | Valor                      | Descripción |
|-------------------|----------------------------|-------------|
| **Content-Type**  | `application/json`         | Formato de datos |
| **Authorization** | `Bearer <token_de_acceso>` | Autenticación |
| **Accept**        | `application/json`         | Formato de respuesta |

**Ejemplo de solicitud:**
```json
{
  "nombre": "Bancal 1",
  "TamX": 2.50,
  "TamY": 1.75,
  "posX": 0.50,
  "posY": 0.25,
  "lote": 1
}
```

**Validaciones:**
- `nombre` debe ser único en el sistema
- `TamX/TamY` no pueden ser ≤ 0
- `lote` debe existir y estar activo

**Ejemplo de respuesta exitosa (201 Created):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{
  "id": 1,
  "nombre": "Bancal 1",
  "TamX": 2.50,
  "TamY": 1.75,
  "posX": 0.50,
  "posY": 0.25,
  "lote": 1,
  "message": "Bancal creado exitosamente"
}
```

**Errores comunes:**
- `400 Bad Request`: Datos faltantes o inválidos
- `409 Conflict`: Nombre de bancal ya existe

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/bancales/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/bancales/"><div></div></button></div></figure></div>  
</section>

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
[
  {
    "id": 1,
    "nombre": "Bancal 1",
    "TamX": 2.5,
    "TamY": 1.75,
    "posX": 0.5,
    "posY": 0.25,
    "lote": {
      "id": 1,
      "nombre": "Lote Norte"
    },
    "cultivos_activos": 2
  },
  {
    "id": 2,
    "nombre": "Bancal 2",
    "TamX": 3.0,
    "TamY": 2.0,
    "posX": 3.5,
    "posY": 0.25,
    "lote": {
      "id": 1,
      "nombre": "Lote Norte"
    },
    "cultivos_activos": 0
  }
]
```

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/bancales/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/bancales/{id}/"><div></div></button></div></figure></div>  
</section>

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{
  "id": 1,
  "nombre": "Bancal 1",
  "TamX": 2.50,
  "TamY": 1.75,
  "posX": 0.50,
  "posY": 0.25,
  "lote": {
    "id": 1,
    "nombre": "Lote Norte",
    "hectareas": 1.5
  },
  "cultivos_activos": [
    {
      "id": 45,
      "nombre": "Lechuga Romana",
      "fecha_siembra": "2023-10-15"
    }
  ]
}
```

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/bancales/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/bancales/{id}/"><div></div></button></div></figure></div>  
</section>

**Ejemplo de solicitud:**
```json
{
  "TamX": 3.20,
  "TamY": 2.10,
  "nombre": "Bancal 1A"
}
```

**Restricciones:**
- No se puede modificar el campo `lote`
- No se puede reducir tamaño si hay cultivos activos
- El nuevo nombre debe ser único

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{
  "id": 1,
  "nombre": "Bancal 1A",
  "TamX": 3.20,
  "TamY": 2.10,
  "message": "Bancal actualizado correctamente"
}
```

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/bancales/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/bancales/{id}/"><div></div></button></div></figure></div>  
</section>

**Ejemplo de respuesta exitosa (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{
  "message": "Bancal eliminado correctamente",
  "id": 2
}
```

**Error común (409 Conflict):**
```json
{
  "error": "No se puede eliminar",
  "detail": "Existen cultivos asociados a este bancal"
}
```

---

## **Relaciones en el Sistema**
Los **Bancales** se vinculan con:
- **Lotes** (contenedor principal)
- **Cultivos** (asignaciones productivas)
- **Actividades** (tareas realizadas en el bancal)

## **Ejemplos de Uso**

### **Crear y actualizar bancal:**
```bash
# Creación
POST /cultivo/bancales/
{
  "nombre": "Bancal Experimental",
  "TamX": 4.25,
  "TamY": 3.50,
  "posX": 2.0,
  "posY": 1.5,
  "lote": 3
}

# Actualización parcial
PUT /cultivo/bancales/5/
{
  "TamY": 4.0
}
```

### **Filtrar bancales:**
```bash
# Por lote
GET /cultivo/bancales/?lote=3

# Con cultivos activos
GET /cultivo/bancales/?activos=true
```

---

## **Buenas Prácticas**
 **Nomenclatura clara**: Usar nombres que indiquen ubicación (ej: "Bancal Noreste")  
 **Planificación espacial**: Registrar coordenadas precisas para mapeo  
 **Verificación previa**: Confirmar disponibilidad en lote antes de crear  
 **Documentación**: Registrar observaciones en nombre o descripción