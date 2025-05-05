---
title: "Gestión de tipos de especie"
---
Los **Tipos de Especie** son clasificaciones que permiten organizar y categorizar las diferentes especies vegetales o animales manejadas en el sistema Agrosoft.


## Datos de un Tipo de Especie
Cada tipo de especie tiene la siguiente información:

| Campo           | Tipo de Dato  | Descripción |
|---------------|-------------|-------------|
| **ID**       | `Integer`    | Identificador único automático |
| **Nombre**   | `CharField`  | Nombre del tipo (máx. 30 caracteres, único) |
| **Descripción** | `TextField` | Información detallada sobre el tipo |

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_especie/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_especie/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Crea un nuevo tipo de especie
```json
{
  "nombre": "Frutales de Clima Templado",
  "descripcion": "Árboles frutales que requieren inviernos fríos para su correcto desarrollo",
}
```

**Ejemplo de respuesta (201 Created):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 7,
  "nombre": "Frutales de Clima Templado",
  "descripcion": "Árboles frutales que requieren inviernos fríos para su correcto desarrollo",
}
```

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_especie/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_especie/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Obtiene los tipos de especie existentes.

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 7,
  "nombre": "Frutales de Clima Templado",
  "descripcion": "Árboles frutales que requieren inviernos fríos para su correcto desarrollo",
}
```


<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_especie/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_especie/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Resultado: Obtiene un tipo de especie específico por su ID.

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 7,
  "nombre": "Frutales de Clima Templado",
  "descripcion": "Árboles frutales que requieren inviernos fríos para su correcto desarrollo",
}
```

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_especie/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_especie/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Actualiza un tipo de especie existente.

**Ejemplo de solicitud:**
```json
{
  "descripcion": "Árboles frutales que requieren entre 600-1200 horas de frío invernal",
}
```

**Respuesta exitosa (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "id": 7,
  "message": "Tipo de especie actualizado correctamente",
}
```

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/cultivo/tipo_especie/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/cultivo/tipo_especie/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

Desactiva un tipo de especie (eliminación lógica).

**Respuesta exitosa (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "message": "Tipo de especie eliminado correctamente",
}
```

---

---

## ** Ejemplos de Uso**

### **Crear y luego actualizar un tipo de especie:**
```bash
Metodo: POST 
URL:http://127.0.0.1:8000/cultivo/tipo_especie/
{
  "nombre": "Frutales de Clima Templado",
  "descripcion": "Árboles frutales que requieren inviernos fríos para su correcto desarrollo",
}

Metodo: PUT 
URL:http://127.0.0.1:8000/cultivo/tipo_especie/4
{
  "nombre": "Cultivo legumbre",
}
```

### **Listar tipos de especie:**
```bash
Metodo: GET 
URL:http://127.0.0.1:8000/cultivo/tipo_especie/
```

---

## **Validaciones Adicionales**

1. **Nombre único**:
   - No puede repetirse en el sistema (case-insensitive)
   - Máximo 30 caracteres
   - No permite caracteres especiales excepto guiones


## Características importantes
- **Nombres únicos:** No puede haber duplicados en los tipos de especie
- **Descripción detallada:** Permite documentar características comunes del grupo



## Consideraciones
1. Usar nombres descriptivos pero concisos
2. Proporcionar descripciones completas que ayuden a identificar el grupo
4. Mantener una estructura jerárquica lógica (ej: "Hortalizas" > "Hortalizas de Fruto")