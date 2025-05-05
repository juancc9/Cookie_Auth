---
title: "Gestión de productos control"
---
## Estructura de Datos

| Campo               | Tipo                | Descripción |
|---------------------|---------------------|-------------|
| **id**              | `AutoField`         | Identificador único |
| **precio**          | `IntegerField`      | Valor en pesos (COP) |
| **nombre**          | `CharField(30)`     | Nombre comercial (único) |
| **compuestoActivo** | `CharField(50)`     | Principio activo |
| **fichaTecnica**    | `TextField`         | Especificaciones técnicas |
| **Contenido**       | `IntegerField`      | Cantidad contenida |
| **tipoContenido**   | `CharField(10)`     | Unidad de medida (ml, gr, kg, etc.) |
| **unidades**        | `IntegerField`      | Número de unidades por empaque |

---


<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/productos-control/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/productos-control/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Crea un nuevo producto de control

**Request:**
```json
{
  "precio": 85000,
  "nombre": "Fungicida XT-200",
  "compuestoActivo": "Azoxistrobina 25%",
  "fichaTecnica": "Fungicida sistémico para control de hongos...",
  "Contenido": 500,
  "tipoContenido": "ml",
  "unidades": 1
}
```

**Response (201 Created):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 1,
  "precio": 85000,
  "nombre": "Fungicida XT-200",
  "compuestoActivo": "Azoxistrobina 25%",
  "fichaTecnica": "Fungicida sistémico para control de hongos...",
  "Contenido": 500,
  "tipoContenido": "ml",
  "unidades": 1,
  "precioUnitario": 170.0
}
```
<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/productos-control/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/productos-control/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Obtiene los productos existentes 

**Response (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 1,
  "precio": 85000,
  "nombre": "Fungicida XT-200",
  "compuestoActivo": "Azoxistrobina 25%",
  "fichaTecnica": "Fungicida sistémico para control de hongos...",
  "Contenido": 500,
  "tipoContenido": "ml",
  "unidades": 1,
}
{
  "id": 2,
  "precio": 120000,
  "nombre": "Herbicida GreenKill",
  "compuestoActivo": "Glifosato 48%",
  "fichaTecnica": "Herbicida no selectivo para control de malezas...",
  "Contenido": 1000,
  "tipoContenido": "ml",
  "unidades": 1
}

```


<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/productos-control/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/productos-control/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Obtiene un producto específico

**Response (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 1,
  "precio": 85000,
  "nombre": "Fungicida XT-200",
  "compuestoActivo": "Azoxistrobina 25%",
  "fichaTecnica": "Fungicida sistémico para control de hongos...",
  "Contenido": 500,
  "tipoContenido": "ml",
  "unidades": 1,
}
```

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/productos-control/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/productos-control/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Actualiza un producto existente

**Request:**
```json
{
  "precio": 90000,
  "unidades": 2
}
```

**Response (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 1,
  "message": "Producto actualizado correctamente",
  "nuevoPrecioUnitario": 90.0
}
```

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/productos-control/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/productos-control/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Elimina un producto

**Response (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "message": "Producto eliminado correctamente",
  "id": 1
}
```

**Error (409 Conflict):**
```json
{
  "error": "No se puede eliminar",
  "detail": "Existen registros de aplicación asociados a este producto"
}
```

---
---

## ** Ejemplos de Uso**

### **Crear y luego actualizar un producto:**
```bash
Metodo: POST 
URL:http://127.0.0.1:8000/cultivo/productos-control/
{
  "precio": 85000,
  "nombre": "Fungicida XT-200",
  "compuestoActivo": "Azoxistrobina 25%",
  "fichaTecnica": "Fungicida sistémico para control de hongos...",
  "Contenido": 500,
  "tipoContenido": "ml",
  "unidades": 1,
}

Metodo: PUT 
URL:http://127.0.0.1:8000/cultivo/productos-control/4
{
  "Contenido": 600,
}
```

### **Listar productos:**
```bash
Metodo: GET 
URL:http://127.0.0.1:8000/cultivo/productos-control/
```

---


## Validaciones

1. **Campos requeridos:**
   ```python
   ["precio", "nombre", "compuestoActivo", "Contenido", "tipoContenido"]
   ```

2. **Restricciones:**
   - `precio`: Valor positivo (min. $1,000)
   - `Contenido`: Entero positivo
   - `unidades`: Entero positivo (default=1)
   - `tipoContenido`: Valores permitidos: ["ml", "gr", "kg", "lt", "un"]

3. **Unicidad:**
   - `nombre` debe ser único (case-insensitive)

---


