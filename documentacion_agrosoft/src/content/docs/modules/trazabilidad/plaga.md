---
title: Gestion de lotes
--- 
    

## ¿Qué es una Plaga?  
Las **plagas** son organismos que causan daño a los cultivos, incluyendo insectos, hongos, bacterias y otros agentes biológicos que impactan negativamente la producción agrícola.

## ¿Cómo registrar una plaga?  
Para documentar una nueva plaga en el sistema:  
1. Navega a Cultivos > Protección > Plagas  
2. Selecciona **"Registrar Plaga"**  
3. Completa los campos obligatorios:  
   - **Tipo de plaga**: Clasificación principal  
   - **Nombre**: Identificador único  
   - **Descripción**: Síntomas y daños característicos  

## Estructura de Datos  

| Campo               | Tipo                | Descripción | Validaciones |  
|---------------------|---------------------|-------------|--------------|  
| **ID**             | `AutoField`         | Identificador único | - |  
| **Tipo_plaga**     | `ForeignKey`        | Categoría principal | Debe existir |  
| **Nombre**         | `CharField`         | Nombre común | Único, máx. 30 chars |  
| **Descripción**    | `TextField`         | Características | Mín. 20 caracteres |  
| **Imagen**         | `ImageField`        | Foto referencia | Formatos: JPG/PNG/WEBP |  

## Ejemplo de API para gestión de plagas  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/plagas/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/plagas/"><div></div></button></div></figure></div>  
</section>  

**Encabezados de la solicitud**  
| Encabezado        | Valor                      | Descripción |  
|-------------------|----------------------------|-------------|  
| **Content-Type**  | `multipart/form-data`      | Para envío de imágenes |  
| **Authorization** | `Bearer <token_de_acceso>` | Autenticación |  

**Ejemplo de solicitud (form-data):**  
```
fk_tipo_plaga: 2  
nombre: "Mosca blanca"  
descripcion: "Insecto chupador que debilita plantas. Afecta principalmente hojas nuevas."  
img: [archivo.jpg]  
```  

**Validaciones:**  
- `nombre` debe ser único (case-insensitive)  
- `descripcion` mínimo 20 caracteres  
- `img` máximo 2MB  

**Ejemplo de respuesta exitosa (201 Created):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "tipo_plaga": {  
    "id": 2,  
    "nombre": "Insectos",  
    "icono": "insectos.svg"  
  },  
  "nombre": "Mosca blanca",  
  "slug": "mosca-blanca",  
  "descripcion": "Insecto chupador que debilita plantas...",  
  "imagen_url": "/media/plagas/mosca-blanca.jpg",  
  "tratamientos_recomendados": []  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/plagas/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/plagas/"><div></div></button></div></figure></div>  
</section>  

**Filtros disponibles:**  
- `?tipo=ID` (Filtrar por tipo de plaga)  
- `?cultivo=ID` (Plagas asociadas a un cultivo)  
- `?search=texto` (Búsqueda en nombre/descripción)  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
[  
  {  
    "id": 1,  
    "nombre": "Mosca blanca",  
    "tipo_plaga": "Insectos",  
    "imagen_miniatura": "/media/plagas/thumbs/mosca-blanca.jpg",  
    "afecta": ["Solanáceas", "Cucurbitáceas"],  
    "detecciones_30dias": 3  
  },  
  {  
    "id": 2,  
    "nombre": "Oídio",  
    "tipo_plaga": "Hongos",  
    "imagen_miniatura": "/media/plagas/thumbs/oidio.jpg",  
    "afecta": ["Rosáceas", "Vid"],  
    "detecciones_30dias": 7  
  }  
]  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/plagas/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/plagas/{id}/"><div></div></button></div></figure></div>  
</section>  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "nombre": "Mosca blanca",  
  "nombre_cientifico": "Bemisia tabaci",  
  "tipo_plaga": {  
    "id": 2,  
    "nombre": "Insectos",  
    "descripcion": "Plagas de tipo insecto"  
  },  
  "descripcion": "Insecto chupador de 1-2mm que coloniza el envés de las hojas...",  
  "sintomas": [  
    "Amarillamiento hojas",  
    "Fumagina",  
    "Debilitamiento general"  
  ],  
  "imagen_url": "/media/plagas/full/mosca-blanca.jpg",  
  "tratamientos_efectivos": [  
    {  
      "id": 5,  
      "nombre": "Jabón potásico",  
      "tipo": "Biológico"  
    }  
  ],  
  "estadisticas": {  
    "afecta_12_cultivos": true,  
    "detecciones_mes": 3,  
    "epoca_riesgo": "Verano"  
  }  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/plagas/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/plagas/{id}/"><div></div></button></div></figure></div>  
</section>  

**Restricciones:**  
- `tipo_plaga` no editable después de creación  
- Actualización de `nombre` debe mantener unicidad  

**Ejemplo de solicitud:**  
```json  
{  
  "descripcion": "Insecto chupador que transmite virus. Control crítico en tomate y berenjena.",  
  "img": "nueva_imagen.jpg"  
}  
```  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "message": "Plaga actualizada correctamente",  
  "cambios": {  
    "descripcion": ["Texto anterior", "Nuevo texto"],  
    "imagen": ["old.jpg", "new.jpg"]  
  }  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/plagas/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/plagas/{id}/"><div></div></button></div></figure></div>  
</section>  

**Condiciones para eliminación:**  
- Sin tratamientos asociados  
- Sin registros de detección históricos  

**Ejemplo de respuesta exitosa (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "message": "Plaga eliminada correctamente",  
  "id": 15,  
  "imagen_eliminada": true  
}  
```  

**Error común (409 Conflict):**  
```json  
{  
  "error": "Eliminación restringida",  
  "detail": "Existen 8 registros de detección asociados",  
  "alternativa": "Marcar como inactiva en lugar de eliminar"  
}  
```  

---  

## **Relaciones en el Sistema**  
Las **Plagas** se vinculan con:  
- **Tipos de plaga** (clasificación científica)  
- **Tratamientos** (métodos de control)  
- **Detecciones** (registros en cultivos)  
- **Alertas** (sistema de monitoreo)  

## **Buenas Prácticas**  
 **Identificación precisa**: Incluir nombre científico y común  
 **Documentación detallada**: Describir síntomas y condiciones favorables  
 **Imágenes claras**: Mostrar distintos estadios de desarrollo  
 **Actualización constante**: Añadir nuevos tratamientos efectivos  

## **Ejemplo Completo de Uso**  

```bash  
# 1. Registrar nueva plaga con imagen  
POST /cultivo/plagas/  
Content-Type: multipart/form-data  

{  
  "fk_tipo_plaga": 3,  
  "nombre": "Mildiu",  
  "descripcion": "Hongo que causa manchas aceitosas en hojas...",  
  "img": "mildiu.jpg"  
}  

# 2. Consultar plagas por cultivo  
GET /cultivo/plagas/?cultivo=8  

# 3. Actualizar información  
PUT /cultivo/plagas/5/  
{  
  "descripcion": "Nuevas cepas resistentes a fungicidas comunes..."  
}  
```