---
title: Gestion de cosechas
---

## ¿Qué es un Registro de Cosecha?  
Los registros de **Cosecha** documentan la producción obtenida de cada cultivo, permitiendo llevar un historial preciso de rendimientos y productividad.

## ¿Cómo registrar una cosecha?  
Para documentar una nueva cosecha:  
1. Accede al módulo de Cultivos > Cosechas  
2. Selecciona **"Registrar Cosecha"**  
3. Completa los campos obligatorios:  
   - **Cultivo**: Selecciona de la lista activa  
   - **Cantidad**: Valor numérico positivo  
   - **Unidad**: Selecciona la medida adecuada  
   - **Fecha**: Establece la fecha de cosecha  

## Estructura de Datos  

| Campo               | Tipo de Dato        | Descripción | Validaciones |  
|---------------------|---------------------|-------------|--------------|  
| **ID**             | `AutoField`         | Identificador único | - |  
| **id_cultivo**     | `ForeignKey`        | Cultivo asociado | Debe existir |  
| **cantidad**       | `IntegerField`      | Producción obtenida | > 0 |  
| **unidades_de_medida** | `CharField`  | Unidad de medida | Valores predefinidos |  
| **fecha**          | `DateField`         | Fecha de registro | ≤ fecha actual |  

## Ejemplo de API para gestión de cosechas  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cosechas/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cosechas/"><div></div></button></div></figure></div>  
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
  "id_cultivo": 45,  
  "cantidad": 120,  
  "unidades_de_medida": "kg",  
  "fecha": "2023-11-20"  
}  
```  

**Validaciones:**  
- `id_cultivo` debe corresponder a un cultivo activo  
- `cantidad` debe ser entero positivo  
- `unidades_de_medida` debe ser uno de: `['kg', 'g', 'lb', 'ton', 'cajas', 'unidades']`  
- `fecha` no puede ser futura  

**Ejemplo de respuesta exitosa (201 Created):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "id_cultivo": 45,  
  "cultivo_nombre": "Lechuga Romana - B2",  
  "cantidad": 120,  
  "unidades_de_medida": "kg",  
  "fecha": "2023-11-20",  
  "message": "Cosecha registrada exitosamente"  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cosechas/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cosechas/"><div></div></button></div></figure></div>  
</section>  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
[  
  {  
    "id": 1,  
    "fecha": "2023-11-20",  
    "cultivo": {  
      "id": 45,  
      "nombre": "Lechuga Romana",  
      "variedad": "B2"  
    },  
    "cantidad": 120,  
    "unidades_de_medida": "kg",  
    "valor_estimado": 360000  
  },  
  {  
    "id": 2,  
    "fecha": "2023-11-18",  
    "cultivo": {  
      "id": 32,  
      "nombre": "Zanahoria",  
      "variedad": "Nantes"  
    },  
    "cantidad": 85,  
    "unidades_de_medida": "kg",  
    "valor_estimado": 212500  
  }  
]  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cosechas/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cosechas/{id}/"><div></div></button></div></figure></div>  
</section>  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "fecha": "2023-11-20",  
  "cultivo": {  
    "id": 45,  
    "nombre": "Lechuga Romana",  
    "variedad": "B2",  
    "bancal": "N1",  
    "lote": "Norte"  
  },  
  "cantidad": 120,  
  "unidades_de_medida": "kg",  
  "registrado_por": {  
    "id": 12,  
    "nombre": "Juan Pérez"  
  },  
  "valor_estimado": 360000,  
  "observaciones": "Cosecha primera temporada"  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cosechas/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cosechas/{id}/"><div></div></button></div></figure></div>  
</section>  

**Restricciones:**  
- No se puede modificar `id_cultivo` después de creado  
- `fecha` solo editable por administradores  

**Ejemplo de solicitud:**  
```json  
{  
  "cantidad": 125,  
  "observaciones": "Ajuste por merma inicial"  
}  
```  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "id": 1,  
  "message": "Registro de cosecha actualizado",  
  "changes": {  
    "cantidad": ["120", "125"],  
    "observaciones": ["", "Ajuste por merma inicial"]  
  }  
}  
```  

---  

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  
  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/cosechas/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/cosechas/{id}/"><div></div></button></div></figure></div>  
</section>  

**Ejemplo de respuesta exitosa (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>   
```json  
{  
  "message": "Registro de cosecha eliminado",  
  "id": 2,  
  "cultivo": "Zanahoria Nantes",  
  "cantidad": "85 kg"  
}  
```  

**Error común (403 Forbidden):**  
```json  
{  
  "error": "Acción restringida",  
  "detail": "Solo administradores pueden eliminar registros antiguos"  
}  
```  

---  

## **Relaciones en el Sistema**  
Los **Registros de Cosecha** se vinculan con:  
- **Cultivos** (origen de la producción)  
- **Usuarios** (responsable del registro)  
- **Inventario** (actualización automática de existencias)  
- **Ventas** (asignación de productos vendidos)  

## **Buenas Prácticas**  
 **Registro inmediato**: Documentar cosechas el mismo día de recolección  
 **Unidades consistentes**: Usar preferiblemente unidades métricas (kg, g)  
 **Verificación cruzada**: Contrastar con registros de actividades previas  
 **Documentación**: Incluir observaciones sobre calidad o condiciones especiales  

## **Ejemplo Completo de Uso**  

```bash  
# 1. Registrar nueva cosecha  
POST /cultivo/cosechas/  
{  
  "id_cultivo": 78,  
  "cantidad": 200,  
  "unidades_de_medida": "kg",  
  "fecha": "2023-11-25",  
  "observaciones": "Cosecha orgánica certificada"  
}  

# 2. Filtrar por cultivo  
GET /cultivo/cosechas/?cultivo=78  

# 3. Actualizar por error de pesaje  
PUT /cultivo/cosechas/15/  
{  
  "cantidad": 195  
}  
```