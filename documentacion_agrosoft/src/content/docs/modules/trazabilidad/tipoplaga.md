---
title: "Gestión de tipos de plaga"
---

## Estructura de Datos

| Campo           | Tipo            | Descripción |
|-----------------|-----------------|-------------|
| **id**          | `AutoField`     | Identificador único |
| **nombre**      | `CharField(30)` | Nombre del tipo de plaga (único) |
| **descripcion** | `TextField`     | Descripción detallada |
| **img**         | `ImageField`    | Imagen representativa (opcional) |

---

## Ejemplo de API

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipos-plaga/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipos-plaga/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Crea un nuevo tipo de plaga

**Solicitud:**
```json
{
  "nombre": "Hongos",
  "descripcion": "Organismos patógenos que afectan cultivos",
  "img": null
}
```

**Respuesta exitosa (201 Created):**
```json
{
  "id": 1,
  "nombre": "Hongos",
  "descripcion": "Organismos patógenos que afectan cultivos",
  "url_imagen": null
}
```

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipos-plaga/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipos-plaga/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Obtiene los tipos de plaga existente 

**Respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 1,
  "nombre": "Hongos",
  "descripcion": "Organismos patógenos que afectan cultivos",
  "url_imagen": "/media/tipos_plaga_images/hongos.jpg"
}
```


<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipos-plaga/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipos-plaga/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Obtiene un tipo de plaga específico

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Hongos",
  "descripcion": "Organismos patógenos que afectan cultivos",
  "url_imagen": "/media/tipos_plaga_images/hongos.jpg"
}
```

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipos-plaga/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipos-plaga/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |
Resultado: Actualiza un tipo de plaga existente

**Solicitud:**
```json
{
  "descripcion": "Organismos patógenos que afectan cultivos. Se propagan en condiciones de humedad.",
  "img": "nueva_imagen.jpg"
}
```

**Respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 1,
  "message": "Tipo de plaga actualizado correctamente",
  "url_imagen": "/media/tipos_plaga_images/nueva_imagen.jpg"
}
```

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipos-plaga/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipos-plaga/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |
Resultado: Elimina un tipo de plaga

**Respuesta exitosa (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "message": "Tipo de plaga eliminado correctamente",
  "id": 1
}
```

**Error (409 Conflict) - Cuando hay plagas asociadas:**
```json
{
  "error": "No se puede eliminar",
  "detail": "Existen plagas asociadas a este tipo"
}
```

---


---

## ** Ejemplos de Uso**

### **Crear y luego actualizar un tipo de plaga:**
```bash
Metodo: POST 
URL:http://127.0.0.1:8000/cultivo/tipos-plaga/
{
  "nombre": "Hongos",
  "descripcion": "Organismos patógenos que afectan cultivos",
  "url_imagen": "/media/tipos_plaga_images/hongos.jpg"
}

Metodo: PUT 
URL:http://127.0.0.1:8000/cultivo/tipos-plaga/4
{
  "nombre": "Maleza",
}
```

### **Listar tipos de plaga:**
```bash
Metodo: GET 
URL:http://127.0.0.1:8000/cultivo/tipos-plaga/
```

---


## Notas Importantes

1. **Manejo de imágenes:**
   - Se almacenan en `/media/tipos_plaga_images/`
   - Al actualizar, la imagen anterior se elimina automáticamente
   - Proporciona URL completa en las respuestas
