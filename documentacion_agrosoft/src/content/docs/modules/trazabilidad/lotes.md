---
title: Gestion de lotes
--- 
  

## ¿Qué es un Lote?  
Los **lotes** son unidades de cultivo delimitadas dentro de un terreno agrícola, caracterizadas por su ubicación precisa, dimensiones y estado productivo.

## ¿Cómo registrar un lote?  
Para crear un nuevo lote en Agrosoft:  
1. Accede al módulo de Trazabilidad > Lotes  
2. Haz clic en **"Nuevo Lote"**  
3. Completa los campos obligatorios:  
   - **Nombre**: Identificador único (ej: "Lote Norte")  
   - **Dimensiones**: Ancho (X) y Largo (Y) en metros  
   - **Ubicación**: Coordenadas dentro del terreno general  
   - **Estado**: Activo/Inactivo  

## Estructura de Datos  

| Campo           | Tipo de Dato       | Descripción | Validaciones |  
|-----------------|--------------------|-------------|--------------|  
| **ID**         | `AutoField`        | Identificador único | - |  
| **Nombre**     | `CharField`        | Nombre identificador | Único, máx. 15 chars |  
| **Descripción**| `TextField`        | Información adicional | Opcional |  
| **Estado**     | `BooleanField`     | Disponibilidad | True=Activo |  
| **Tam_x**      | `DecimalField`     | Ancho (metros) | > 0, 2 decimales |  
| **Tam_y**      | `DecimalField`     | Largo (metros) | > 0, 2 decimales |  
| **Pos_x**      | `DecimalField`     | Coordenada X | ≥ 0 |  
| **Pos_y**      | `DecimalField`     | Coordenada Y | ≥ 0 |  

## Ejemplo de API para gestión de lotes  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/lotes/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/lotes/"><div></div></button></div></figure></div>  
</section>  

**Encabezados de la solicitud**  
| Encabezado        | Valor                      | Descripción |  
|-------------------|----------------------------|-------------|  
| **Content-Type**  | `application/json`         | Formato de datos |  
| **Authorization** | `Bearer <token_de_acceso>` | Autenticación |  

**Ejemplo de solicitud:**  
```json  
{  
  "nombre": "Lote A",  
  "descripcion": "Lote principal con riego automatizado",  
  "activo": true,  
  "tam_x": 10.50,  
  "tam_y": 15.75,  
  "pos_x": 5.00,  
  "pos_y": 3.50  
}  
```  

**Validaciones:**  
- `nombre` debe ser único en el sistema  
- `tam_x` y `tam_y` deben ser valores positivos  
- Coordenadas no pueden superar dimensiones del terreno general  

**Ejemplo de respuesta exitosa (201 Created):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "nombre": "Lote A",  
  "descripcion": "Lote principal con riego automatizado",  
  "estado": "Activo",  
  "dimensiones": "10.5m × 15.75m",  
  "ubicacion": "(5.0, 3.5)",  
  "area": "165.38 m²",  
  "bancales": 0,  
  "cultivos_activos": 0  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/lotes/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/lotes/"><div></div></button></div></figure></div>  
</section>  

**Filtros disponibles:**  
- `?estado=activo/inactivo`  
- `?area_min=X` (Área mínima en m²)  
- `?cultivos=true` (Solo con cultivos activos)  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
[  
  {  
    "id": 1,  
    "nombre": "Lote A",  
    "estado": "Activo",  
    "dimensiones": "10.5m × 15.75m",  
    "ubicacion": "Sector Norte",  
    "cultivos_activos": 3,  
    "ultima_actividad": "2023-11-15"  
  },  
  {  
    "id": 2,  
    "nombre": "Lote B",  
    "estado": "En descanso",  
    "dimensiones": "8.0m × 12.0m",  
    "ubicacion": "Sector Este",  
    "cultivos_activos": 0,  
    "proximo_cultivo": "2024-02-01"  
  }  
]  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/lotes/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/lotes/{id}/"><div></div></button></div></figure></div>  
</section>  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "nombre": "Lote A",  
  "descripcion": "Lote principal con riego automatizado",  
  "estado": "Activo",  
  "dimensiones": {  
    "ancho": 10.5,  
    "largo": 15.75,  
    "area": "165.38 m²"  
  },  
  "ubicacion": {  
    "x": 5.0,  
    "y": 3.5,  
    "sector": "Noreste"  
  },  
  "bancales": [  
    {  
      "id": 12,  
      "nombre": "B1",  
      "cultivos_activos": 2  
    }  
  ],  
  "historial": {  
    "creacion": "2023-01-10",  
    "ultima_modificacion": "2023-11-01",  
    "actividades_30dias": 5  
  }  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/lotes/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/lotes/{id}/"><div></div></button></div></figure></div>  
</section>  

**Restricciones:**  
- No se puede reducir tamaño si contiene bancales  
- Cambio a `activo=false` requiere confirmación  

**Ejemplo de solicitud:**  
```json  
{  
  "descripcion": "Lote principal - Riego por goteo instalado 2023",  
  "tam_y": 16.0  
}  
```  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "message": "Lote actualizado correctamente",  
  "cambios": {  
    "descripcion": ["Texto anterior", "Nuevo texto"],  
    "tam_y": [15.75, 16.0]  
  },  
  "area_actualizada": "168.0 m²"  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/lotes/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/lotes/{id}/"><div></div></button></div></figure></div>  
</section>  

**Condiciones para eliminación:**  
- Sin bancales asociados  
- Sin historial de actividades  

**Ejemplo de respuesta exitosa (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "message": "Lote eliminado correctamente",  
  "id": 3,  
  "espacio_liberado": "120.25 m²"  
}  
```  

**Error común (409 Conflict):**  
```json  
{  
  "error": "Eliminación restringida",  
  "detail": "El lote contiene 4 bancales activos",  
  "alternativa": "Desactivar el lote en lugar de eliminar"  
}  
```  

---  

## **Relaciones en el Sistema**  
Los **Lotes** se vinculan con:  
- **Bancales** (subdivisiones productivas)  
- **Actividades** (labores realizadas)  
- **Programaciones** (calendario de uso)  
- **Mapas** (georreferenciación)  

## **Buenas Prácticas**  
 **Identificación clara**: Usar nombres que indiquen ubicación (Norte/Sur)  
 **Documentación espacial**: Registrar coordenadas exactas  
 **Rotación planificada**: Alternar estados activo/descanso  
✔️ **Actualización dimensional**: Ajustar medidas después de modificaciones físicas  

## **Ejemplo Completo de Uso**  

```bash  
# 1. Registrar nuevo lote  
POST /cultivo/lotes/  
{  
  "nombre": "Lote Experimental",  
  "descripcion": "Para pruebas de nuevas variedades",  
  "tam_x": 12.5,  
  "tam_y": 8.75,  
  "pos_x": 2.0,  
  "pos_y": 0.0  
}  

# 2. Consultar lotes disponibles  
GET /cultivo/lotes/?estado=activo&area_min=100  

# 3. Expandir dimensión  
PUT /cultivo/lotes/5/  
{  
  "tam_x": 15.0,  
  "descripcion": "Ampliación Este completada"  
}  
```