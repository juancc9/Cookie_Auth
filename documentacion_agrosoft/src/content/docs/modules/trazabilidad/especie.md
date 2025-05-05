---
title: Gestion de especies
--- 


## ¿Qué es una Especie?  
Las **Especies** representan las variedades vegetales o animales específicas que se cultivan o crían en el sistema, asociadas a un tipo general y con características propias definidas.

## ¿Cómo registrar una especie?  
Para agregar una nueva especie al catálogo:  
1. Navega a Cultivos > Catálogo > Especies  
2. Selecciona **"Nueva Especie"**  
3. Completa los campos obligatorios:  
   - **Tipo de especie**: Categoría principal  
   - **Nombre**: Identificador único  
   - **Días de crecimiento**: Duración estimada del ciclo  

## Estructura de Datos  

| Campo               | Tipo de Dato        | Descripción | Validaciones |  
|---------------------|---------------------|-------------|--------------|  
| **ID**             | `AutoField`         | Identificador único | - |  
| **Tipo_especie**   | `ForeignKey`        | Categoría general | Debe existir |  
| **Nombre**         | `CharField`         | Variedad específica | Único, máx. 30 chars |  
| **Descripción**    | `TextField`         | Características | Opcional |  
| **Días_crecimiento** | `IntegerField`    | Ciclo vegetativo | ≥ 1 |  
| **Imagen**         | `ImageField`        | Foto referencia | Formatos: JPG/PNG |  

## Ejemplo de API para gestión de especies  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/especies/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/especies/"><div></div></button></div></figure></div>  
</section>  

**Encabezados de la solicitud**  
| Encabezado        | Valor                      | Descripción |  
|-------------------|----------------------------|-------------|  
| **Content-Type**  | `multipart/form-data`      | Para imágenes |  
| **Authorization** | `Bearer <token_de_acceso>` | Autenticación |  

**Ejemplo de solicitud (form-data):**  
```
fk_tipo_especie: 3  
nombre: "Tomate Cherry"  
descripcion: "Variedad de tomate pequeño y dulce"  
largoCrecimiento: 75  
img: [archivo.jpg]  
```  

**Validaciones:**  
- `nombre` debe ser único en el sistema  
- `largoCrecimiento` mínimo 1 día  
- `img` máxima resolución 2000x2000px  

**Ejemplo de respuesta exitosa (201 Created):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "tipo_especie": {  
    "id": 3,  
    "nombre": "Solanáceas"  
  },  
  "nombre": "Tomate Cherry",  
  "slug": "tomate-cherry",  
  "descripcion": "Variedad de tomate pequeño y dulce",  
  "largoCrecimiento": 75,  
  "imagen_url": "/media/especies/tomate-cherry.jpg",  
  "requerimientos": []  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/especies/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/especies/"><div></div></button></div></figure></div>  
</section>  

**Filtros disponibles:**  
- `?tipo=ID` (Filtrar por tipo de especie)  
- `?search=texto` (Búsqueda en nombre/descripción)  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
[  
  {  
    "id": 1,  
    "nombre": "Tomate Cherry",  
    "tipo_especie": "Solanáceas",  
    "dias_crecimiento": 75,  
    "imagen_miniatura": "/media/especies/thumbs/tomate-cherry.jpg",  
    "total_cultivos": 12  
  },  
  {  
    "id": 2,  
    "nombre": "Lechuga Romana",  
    "tipo_especie": "Asteráceas",  
    "dias_crecimiento": 60,  
    "imagen_miniatura": "/media/especies/thumbs/lechuga-romana.jpg",  
    "total_cultivos": 23  
  }  
]  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/especies/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/especies/{id}/"><div></div></button></div></figure></div>  
</section>  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "nombre": "Tomate Cherry",  
  "slug": "tomate-cherry",  
  "tipo_especie": {  
    "id": 3,  
    "nombre": "Solanáceas",  
    "icono": "solanaceas.svg"  
  },  
  "descripcion": "Variedad de tomate pequeño (1-3cm), dulce y productivo. Ideal para ensaladas y snacks.",  
  "dias_crecimiento": 75,  
  "imagen_url": "/media/especies/full/tomate-cherry.jpg",  
  "requerimientos": [  
    {  
      "tipo": "Clima",  
      "descripcion": "Temperaturas entre 18-28°C"  
    },  
    {  
      "tipo": "Riego",  
      "descripcion": "Frecuente sin encharcamiento"  
    }  
  ],  
  "estadisticas": {  
    "cultivos_activos": 5,  
    "cultivos_historicos": 42,  
    "rendimiento_promedio": "3.2 kg/planta"  
  }  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/especies/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/especies/{id}/"><div></div></button></div></figure></div>  
</section>  

**Restricciones:**  
- `tipo_especie` no editable después de creación  
- Cambios en `nombre` deben mantener unicidad  

**Ejemplo de solicitud:**  
```json  
{  
  "descripcion": "Variedad mejorada - Mayor resistencia a plagas",  
  "largoCrecimiento": 70,  
  "img": "nueva_imagen.jpg"  
}  
```  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "message": "Especie actualizada correctamente",  
  "changes": {  
    "descripcion": ["Texto anterior", "Nuevo texto"],  
    "largoCrecimiento": [75, 70],  
    "imagen": ["old.jpg", "new.jpg"]  
  }  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/especies/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/especies/{id}/"><div></div></button></div></figure></div>  
</section>  

**Condiciones para eliminación:**  
- Sin cultivos históricos asociados  
- No ser referencia en programaciones  

**Ejemplo de respuesta exitosa (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "message": "Especie eliminada correctamente",  
  "id": 15,  
  "imagen_eliminada": true  
}  
```  

**Error común (409 Conflict):**  
```json  
{  
  "error": "Eliminación restringida",  
  "detail": "Existen 8 cultivos históricos asociados",  
  "alternativa": "Marcar como inactiva en lugar de eliminar"  
}  
```  

---  

## **Relaciones en el Sistema**  
Las **Especies** se vinculan con:  
- **Tipos de especie** (clasificación botánica/zootécnica)  
- **Cultivos** (instancias de producción)  
- **Programaciones** (planificación de siembras)  
- **Actividades** (labores específicas por especie)  

## **Buenas Prácticas**  
 **Nomenclatura estandarizada**: Usar nombres científicos o comerciales reconocidos  
 **Documentación completa**: Incluir requerimientos específicos  
 **Actualización progresiva**: Mejorar datos con aprendizajes productivos  
 **Imágenes de calidad**: Usar fotos que muestren características distintivas  

## **Ejemplo Completo de Uso**  

```bash  
# 1. Registrar nueva especie  
POST /cultivo/especies/  
Content-Type: multipart/form-data  

{  
  "fk_tipo_especie": 3,  
  "nombre": "Pimiento California",  
  "descripcion": "Variedad gruesa para ensaladas",  
  "largoCrecimiento": 90,  
  "img": "pimiento-california.jpg"  
}  

# 2. Consultar especies por tipo  
GET /cultivo/especies/?tipo=3  

# 3. Actualizar información agronómica  
PUT /cultivo/especies/8/  
{  
  "largoCrecimiento": 85,  
  "descripcion": "Nuevos datos: Resistencia media a X enfermedad"  
}  
```