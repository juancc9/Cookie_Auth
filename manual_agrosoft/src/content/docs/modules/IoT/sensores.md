---

title: "Módulo de IoT - Gestión de Sensores"  
slug: modules/IoT/sensores  
description: "Cómo administrar sensores en el módulo de IoT de Agrosoft para monitoreo en tiempo real de condiciones meteorológicas en cultivos."  

---


# Módulo de IoT - Gestión de Sensores

Los **Sensores** son dispositivos físicos conectados al sistema que recopilan datos meteorológicos en tiempo real, como temperatura y humedad, en los bancales de cultivo. Estos datos se integran con el módulo de trazabilidad para un control completo del proceso agrícola.

## ¿Cómo registrar un sensor?
Para registrar un nuevo sensor en Agrosoft:  
1. Ve a la sección **IoT → Sensores**.  
2. Hacer clic en el botón **"Registrar Sensor"**.  
3. Completar los siguientes campos:  
   - **Nombre del Sensor:** Nombre único del sensor (por ejemplo, "DHT22_001").  
   - **Tipo de Sensor:** Tipo de sensor (por ejemplo, "DHT22").  
   - **Unidad de Medida:** Unidad de los datos (por ejemplo, "Celsius/%").  
   - **Descripción:** Información adicional sobre el sensor (opcional).  
   - **Medida Mínima:** Valor mínimo que el sensor puede registrar.  
   - **Medida Máxima:** Valor máximo que el sensor puede registrar.  
4. Guardar los cambios.  
   - **Nota:** La asociación del sensor a un bancal se realiza al configurar los datos enviados por el dispositivo.

## Datos de un Sensor
Cada sensor tiene la siguiente información:  
| Campo             | Tipo de Dato    | Descripción                                      |  
|-------------------|-----------------|--------------------------------------------------|  
| **ID**            | `Integer`       | Identificador único del sensor                  |  
| **Nombre**        | `CharField`     | Nombre del sensor (máx. 15 caracteres, único)   |  
| **Tipo**          | `CharField`     | Tipo de sensor (ej. "DHT22")                    |  
| **Unidad**        | `CharField`     | Unidad de medida (ej. "Celsius/%")              |  
| **Descripción**   | `TextField`     | Información opcional sobre el sensor            |  
| **Medida Mínima** | `DecimalField`  | Valor mínimo que el sensor puede registrar      |  
| **Medida Máxima** | `DecimalField`  | Valor máximo que el sensor puede registrar      |

## Ejemplo de API para gestionar sensores

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span> </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/iot/sensores/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/iot/sensores/"><div></div></button></div></figure></div>  </section>  

**Encabezados de la solicitud**  
| Encabezado     | Valor                         | Descripción                                               |  
|----------------|-------------------------------|-----------------------------------------------------------|  
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |  
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |  
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |  
- Crea un nuevo sensor.  

**Ejemplo de solicitud:**  
```json  
{  
  "nombre": "DHT22_001",  
  "tipo": "DHT22",  
  "unidad": "Celsius/%",  
  "descripcion": "Sensor de temperatura y humedad",  
  "medida_minima": -40.00,  
  "medida_maxima": 80.00  
}  
```

**Ejemplo de respuesta exitosa (201 Created):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>  
```json  
{  
  "id": 1,  
  "nombre": "DHT22_001",  
  "tipo": "DHT22",  
  "unidad": "Celsius/%",  
  "descripcion": "Sensor de temperatura y humedad",  
  "medida_minima": -40.00,  
  "medida_maxima": 80.00  
}  
```

**Posibles errores:**  
- `400 Bad Request`: Si faltan campos obligatorios.  
- `409 Conflict`: Si el nombre ya existe.  

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span> </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/iot/sensores/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/iot/sensores/"><div></div></button></div></figure></div>  </section>  

**Encabezados de la solicitud**  
| Encabezado     | Valor                         | Descripción                                               |  
|----------------|-------------------------------|-----------------------------------------------------------|  
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |  
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |  
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |  
- Obtiene todos los sensores registrados.  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>  
```json  
[  
  {  
    "id": 1,  
    "nombre": "DHT22_001",  
    "tipo": "DHT22",  
    "unidad": "Celsius/%",  
    "descripcion": "Sensor de temperatura y humedad",  
    "medida_minima": -40.00,  
    "medida_maxima": 80.00  
  }  
]  
```

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span> </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/iot/sensores/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/iot/sensores/{id}/"><div></div></button></div></figure></div>  </section>  

**Encabezados de la solicitud**  
| Encabezado     | Valor                         | Descripción                                               |  
|----------------|-------------------------------|-----------------------------------------------------------|  
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |  
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |  
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |  
- Obtiene un sensor específico por su ID.  

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>  
```json  
{  
  "id": 1,  
  "nombre": "DHT22_001",  
  "tipo": "DHT22",  
  "unidad": "Celsius/%",  
  "descripcion": "Sensor de temperatura y humedad",  
  "medida_minima": -40.00,  
  "medida_maxima": 80.00  
}  
```

**Posibles errores:**  
- `404 Not Found`: Si el ID no existe.  

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span> </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/iot/sensores/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/iot/sensores/{id}/"><div></div></button></div></figure></div>  </section>  

**Encabezados de la solicitud**  
| Encabezado     | Valor                         | Descripción                                               |  
|----------------|-------------------------------|-----------------------------------------------------------|  
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |  
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |  
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |  
- Actualiza un sensor existente.  

**Ejemplo de solicitud:**  
```json  
{  
  "nombre": "DHT22_001_modificado",  
  "descripcion": "Sensor actualizado"  
}  
```

**Ejemplo de respuesta (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>  
```json  
{  
  "id": 1,  
  "nombre": "DHT22_001_modificado",  
  "tipo": "DHT22",  
  "unidad": "Celsius/%",  
  "descripcion": "Sensor actualizado",  
  "medida_minima": -40.00,  
  "medida_maxima": 80.00  
}  
```

**Posibles errores:**  
- `404 Not Found`: Si el ID no existe.  
- `400 Bad Request`: Si los datos enviados son inválidos.  

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span> </p>  
URL:  
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/iot/sensores/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/iot/sensores/{id}/"><div></div></button></div></figure></div>  </section>  

**Encabezados de la solicitud**  
| Encabezado     | Valor                         | Descripción                                               |  
|----------------|-------------------------------|-----------------------------------------------------------|  
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |  
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |  
| **Accept**       | `application/json`            | Indica que la respuesta debe estar en formato JSON.       |  
- Elimina un sensor (si no está en uso).  

**Ejemplo de respuesta exitosa (200 OK):**  
<span class="sl-badge success small astro-avdet4wd">Success</span>  
```json  
{  
  "message": "Sensor eliminado correctamente"  
}  
```

**Posibles errores:**  
- `404 Not Found`: Si el ID no existe.  
---