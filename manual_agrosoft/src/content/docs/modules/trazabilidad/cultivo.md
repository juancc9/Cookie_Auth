---
title: Gestion de cultivos
--- 

## ¿Qué es un Cultivo?  
Los **Cultivos** representan instancias específicas de siembra de una especie en un bancal particular, con seguimiento completo de su ciclo productivo desde siembra hasta cosecha.

## ¿Cómo registrar un cultivo?  
Para crear un nuevo cultivo en Agrosoft:  
1. Navega a Cultivos > Registro  
2. Selecciona **"Nuevo Cultivo"**  
3. Completa los campos obligatorios:  
   - **Especie**: Selecciona del catálogo  
   - **Bancal**: Ubicación física asignada  
   - **Nombre**: Identificador único descriptivo  
   - **Fecha de siembra**: Establece inicio del ciclo  

## Estructura de Datos  

| Campo               | Tipo                | Descripción | Validaciones |  
|---------------------|---------------------|-------------|--------------|  
| **ID**             | `AutoField`         | Identificador único | - |  
| **Especie**        | `ForeignKey`        | Tipo de planta | Debe existir en catálogo |  
| **Bancal**         | `ForeignKey`        | Ubicación física | Debe estar activo |  
| **Nombre**         | `CharField`         | Identificador único | Máx 50 chars, único |  
| **Unidad_medida**  | `CharField`         | Unidad para cosecha | Valores predefinidos |  
| **Activo**         | `BooleanField`      | Estado del cultivo | - |  
| **FechaSiembra**   | `DateField`         | Inicio del ciclo | No futura |  

## Ejemplo de API para gestión de cultivos  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cultivos/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cultivos/"><div></div></button></div></figure></div>  
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
  "Especie": 45,  
  "Bancal": 12,  
  "nombre": "Lechuga Romana - B2",  
  "unidad_de_medida": "kg",  
  "activo": true,  
  "fechaSiembra": "2023-11-15"  
}  
```  

**Validaciones:**  
- `Nombre` debe ser único en el sistema  
- `Bancal` no puede tener cultivos activos superpuestos  
- `Unidad_medida` debe ser: `['kg', 'g', 'lb', 'unidades', 'cajas']`  
- `fechaSiembra` no puede ser futura  

**Ejemplo de respuesta exitosa (201 Created):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "Especie": {  
    "id": 45,  
    "nombre": "Lechuga Romana",  
    "ciclo_dias": 60  
  },  
  "Bancal": {  
    "id": 12,  
    "nombre": "B2",  
    "lote": "Norte"  
  },  
  "nombre": "Lechuga Romana - B2",  
  "unidad_de_medida": "kg",  
  "activo": true,  
  "fechaSiembra": "2023-11-15",  
  "fechaEstimadaCosecha": "2024-01-14"  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cultivos/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cultivos/"><div></div></button></div></figure></div>  
</section>  

**Filtros disponibles:**  
- `?activo=true/false`  
- `?bancal=ID`  
- `?especie=ID`  
- `?fecha_inicio=YYYY-MM-DD`  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
[  
  {  
    "id": 1,  
    "nombre": "Lechuga Romana - B2",  
    "Especie": "Lechuga Romana",  
    "Bancal": "B2 (Lote Norte)",  
    "estado": "Activo",  
    "fechaSiembra": "2023-11-15",  
    "dias_transcurridos": 25,  
    "progreso": "42%"  
  },  
  {  
    "id": 2,  
    "nombre": "Zanahoria Nantes - S3",  
    "Especie": "Zanahoria Nantes",  
    "Bancal": "S3 (Lote Sur)",  
    "estado": "Inactivo",  
    "fechaSiembra": "2023-09-10",  
    "fechaFinalizacion": "2023-11-20",  
    "produccion_total": "85 kg"  
  }  
]  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cultivos/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cultivos/{id}/"><div></div></button></div></figure></div>  
</section>  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "nombre": "Lechuga Romana - B2",  
  "Especie": {  
    "id": 45,  
    "nombre": "Lechuga Romana",  
    "familia": "Asteraceae",  
    "ciclo_dias": 60,  
    "requerimientos": "Riego frecuente"  
  },  
  "Bancal": {  
    "id": 12,  
    "nombre": "B2",  
    "dimensiones": "2.5m x 1.8m",  
    "lote": "Norte"  
  },  
  "unidad_medida": "kg",  
  "estado": "Activo",  
  "fechaSiembra": "2023-11-15",  
  "fechaEstimadaCosecha": "2024-01-14",  
  "actividades": [  
    {  
      "id": 101,  
      "tipo": "Fertilización",  
      "fecha": "2023-11-25",  
      "completado": true  
    }  
  ],  
  "cosechas": [],  
  "observaciones": "Variedad resistente a plagas"  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cultivos/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cultivos/{id}/"><div></div></button></div></figure></div>  
</section>  

**Restricciones:**  
- `Especie` y `Bancal` no editables después de creación  
- Cambio a `activo=false` requiere motivo  

**Ejemplo de solicitud:**  
```json  
{  
  "activo": false,  
  "observaciones": "Cosecha completa realizada 2023-12-10",  
  "unidad_medida": "g"  
}  
```  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "message": "Cultivo actualizado correctamente",  
  "cambios": {  
    "estado": ["Activo", "Inactivo"],  
    "unidad_medida": ["kg", "g"]  
  },  
  "bancal_liberado": true  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cultivos/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cultivos/{id}/"><div></div></button></div></figure></div>  
</section>  

**Condiciones para eliminación:**  
- Sin cosechas registradas  
- Sin actividades realizadas  
- Creado en los últimos 7 días  

**Ejemplo de respuesta exitosa (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "message": "Cultivo eliminado correctamente",  
  "id": 15,  
  "bancal_liberado": true  
}  
```  

**Error común (409 Conflict):**  
```json  
{  
  "error": "Eliminación restringida",  
  "detail": "El cultivo tiene 3 cosechas registradas",  
  "alternativa": "Actualice el estado a 'inactivo' en lugar de eliminar"  
}  
```  

---  

## **Relaciones en el Sistema**  
Los **Cultivos** se vinculan con:  
- **Especies** (catálogo de plantas)  
- **Bancales** (ubicación física)  
- **Actividades** (labores realizadas)  
- **Cosechas** (producción obtenida)  
- **Inventario** (seguimiento de insumos)  

## **Buenas Prácticas**  
 **Nomenclatura clara**: Usar formato "Especie-Ubicación-Temporada"  
 **Actualización oportuna**: Cambiar estado al finalizar ciclo  
 **Documentación**: Registrar observaciones relevantes  
 **Liberación de bancales**: Inactivar cultivos terminados  

## **Ejemplo Completo de Uso**  

```bash  
# 1. Registrar nuevo cultivo  
POST /cultivo/cultivos/  
{  
  "Especie": 78,  
  "Bancal": 15,  
  "nombre": "Tomate Cherry - E3-2024",  
  "unidad_medida": "kg",  
  "fechaSiembra": "2024-01-10",  
  "observaciones": "Variedad resistente"  
}  

# 2. Consultar cultivos activos en bancal  
GET /cultivo/cultivos/?bancal=15&activo=true  

# 3. Finalizar cultivo  
PUT /cultivo/cultivos/22/  
{  
  "activo": false,  
  "observaciones": "Cosecha final completada 2024-03-15"  
}  
```