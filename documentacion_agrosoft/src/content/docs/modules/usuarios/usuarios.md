---
title: Gestion de Usuarios
slug: modules/usuarios/usuarios
description: "Como administrar usuarios en el modulo de usuarios en Agrosoft."
---

#  Gestion de Usuarios

Los **Usuarios** son indivduos que interactúa con el sistema y tienen un rol asignado, lo que define qué permisos y acciones puede realizar.

## ¿Cómo registrar un usuario?
Para registrar un nuevo lote en Agrosoft:
1. Ve a la pagina de Bienvenida o al Incio de sesión principal.
2. Hacer clic en el botón **"Registrar"**.
3. Completar los siguientes campos:
   - **Nombre:** Nombre único del usuario.
   - **Apellido:** Apellido único del usuario.
   - **Contraseña:** cadena de caracteres utilizada para autenticar y verificar la identidad del usuario al acceder a un sistema.
   - **Username:** Nombre corto personalizado único del usuario.
   - **Email:** Dirección de contacto mail única del usuario.


## Datos de un usuario
Cada usuario tiene la siguiente información:
| Campo        | Tipo de Dato  | Descripción |
|-------------|-------------|-------------|
| **ID**       | `AutoField`  | Identificador único del usuario. |
| **Nombre**   | `CharField`  | Nombre del usuario. |
| **Apellido** | `CharField`  | Apellido del usuario. |
| **Contraseña** | `CharField`  | Clave de acceso cifrada del usuario. |
| **Username**   | `CharField`  | Nombre de usuario único y mas personalizado. |
| **Email**    | `EmailField`  | Correo electrónico del usuario. |


## Ejemplo de API para gestionar usuarios
<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">POST</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/usuarios/registro/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/usuarios/registro/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

- Crea un nuevo usuario.

**Ejemplo de solicitud:**

```json

{
    "nombre": "Juan",
    "apellido": "Rojas",
    "email": "juan.rojas@gmail.com",
    "username": "juan123",
    "password": "Segura123!",
    "rol_id": 1
}
```

**Validaciones:**
- `Email`:
- Debe contener un "@" obligatoriamente.
- Debe tener un dominio válido (ejemplo: gmail.com).
- Puede incluir puntos (.) en el dominio y el nombre de usuario.
- No puede tener espacios 
- Requerido, máximo 255 caracteres, único.
- `Pasword`:
- Debe contenet diferentes tipos de caracteres 
- Mayúsculas (A-Z)
- Minúsculas (a-z)
- Números (0-9)
- Caracteres especiales (@, #, $, %, &, *, !, etc.).

**Ejemplo de respuesta exitosa (201 Created):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 
```json
{

    "id": 1,
    "nombre": "Juan",
    "apellido": "Rojas",
    "email": "juan.rojas@gmail.com",
    "username": "juan123",
    "rol": 1

}
```

**Posibles errores:**
- `400 Bad Request`: Si faltan campos obligatorios.
- `409 Conflict`: Si el nombre ya existe.

---

<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/usuarios/usuarios/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/usuarios/usuarios/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

- Obtiene todos los usuarios registrados.

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
[
{

    "id": 1,
    "nombre": "Juan",
    "apellido": "Rojas",
    "email": "juan.rojas@gmail.com",
    "username": "juan123",
    "rol": {
            "id": 1,
            "rol": "Aprendiz"
        }
}
,{

    "id": 2,
    "nombre": "Alex",
    "apellido": "perez",
    "email": "alex.@gmail.com",
    "username": "alex01",
    "rol": {
            "id": 1,
            "rol": "Aprendiz"
        }
}
]
```


---
<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">GET</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/usuarios/usuarios/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/usuarios/usuarios/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

- Obtiene un usuario específico por su ID.

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{

    "id": 1,
    "nombre": "Juan",
    "apellido": "Rojas",
    "email": "juan.rojas@gmail.com",
    "username": "juan123",
    "rol": {
            "id": 1,
            "rol": "Aprendiz"
        }
}
```

**Posibles errores:**
- `404 Not Found`: Si el ID no existe.

---
<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">PUT</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/usuarios/usuarios/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/usuarios/usuarios/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

- Actualiza un usuario existente.

**Ejemplo de solicitud:**
```json
{
    "nombre": "andres",
    "apellido": "perez",
    "email": "sic@gmail.com",
    "username": "andres9",
    "rol":4
}
```

**Ejemplo de respuesta (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
   "id": 1,
    "nombre": "andres",
    "apellido": "perez",
    "email": "andres@gmail.com",
    "username": "andres9",
    "rol":{
            "id": 4,
            "rol": "Administrador"
        }
}
```
**Posibles errores:**
- `404 Bad Request`: Si el ID no existe.

**Notas:**
- Se pueden actualizar campos individualmente.
- El `nombre`,`email`,`username` debe seguir siendo único.

---
<p> <strong>Método:</strong> <span class="sl-badge success small astro-avdet4wd">DELETE</span>  </p>
URL:
<section id="tab-panel-58" aria-labelledby="tab-58" role="tabpanel">  <div class="expressive-code"><figure class="frame not-content"><figcaption class="header"></figcaption><pre data-language="http" tabindex="0"><code><div class="ec-line"><div class="code"><span style="--0:#D6DEEB;--1:#403F53">http://127.0.0.1:8000/usuarios/usuarios/{id}/</span></div></div></code></pre><div class="copy"><button title="Copiar al portapapeles" data-copied="¡Copiado!" data-code="http://127.0.0.1:8000/usuarios/usuarios/{id}/"><div></div></button></div></figure></div>  </section>

**Encabezados de la solicitud**
| Encabezado     | Valor                         | Descripción                                               |
|----------------|-------------------------------|-----------------------------------------------------------|
| **Content-Type** | `application/json`            | Indica que los datos se envían en formato JSON.           |
| **Authorization** | `Bearer <token_de_acceso>`    | Token de autenticación necesario para acceder al recurso. |

- Elimina un usuario (si no está en uso).

**Ejemplo de respuesta exitosa (200 OK):**
<span class="sl-badge success small astro-avdet4wd">Success</span> 

```json
{
  "message": "Usuario eliminado correctamente"
}
```

**Posibles errores:**
- `404 Not Found`: Si el ID no existe.
- `409 Conflict`: Si el usuario está asociado a actividades pendientes.

---
## ** Ejemplos de Uso**

### **Crear y luego actualizar un usuario:**
```bash
# Crear (POST)
Metodo: POST http://127.0.0.1:8000/usuarios/registro/
{
    "nombre": "Juan",
    "apellido": "Rojas",
    "email": "juan.rojas@gmail.com",
    "username": "juan123",
    "password": "Segura123!",
    "rol_id": 1
}

# Actualizar (PUT)
Metodo: PUT http://127.0.0.1:8000/usuarios/usuarios/1/
{
  "username": "juan054"
}
```

### **Listar usuarios:**
```bash
# Obtener (GET)
Metodo: GET http://127.0.0.1:8000/usuarios/usuarios/
{
    "id": 1 ,
    "nombre": "Juan",
    "apellido": "Rojas",
    "email": "juan.rojas@gmail.com",
    "username": "juan054",
    "password": "Segura123!",
    "rol_id": 1
}

```


---

## **Manejo de Errores**

### **Ejemplo de error (nombre duplicado):**
```json
{
  "error": "ValidationError",
  "detail": {
    "nombre": ["Ya existe un usuario con este nombre."]
  },
  "status": 400
}
```

### **Códigos de estado comunes:**
| Código | Descripción |
|--------|-------------|
| `200` | OK (GET, PUT, DELETE exitoso) |
| `201` | Created (POST exitoso) |
| `400` | Bad Request (datos inválidos) |
| `404` | Not Found (recurso no existe) |
| `409` | Conflict (restricción de integridad) |

---

## **Relaciones en el Sistema**
Los **Usuarios** se vinculan con:
- **Roles** (ejemplo: "Juan rojas" → "Juan rojas-> rol_id: 4 (Adminstrador)").
- **Asignación de labores** (para asignar actividades a otros usuarios recurrentes).
- **Registros sobre economia** (para administrar ventas y producciones).


---



### **Buenas Prácticas**
✔️ **Contraseñas de seguridad efectiva**: (" Usar contraseñas de más de 8 caracteres con variedad de los mismos").  
