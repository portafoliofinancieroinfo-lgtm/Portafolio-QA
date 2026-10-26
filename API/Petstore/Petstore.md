# Swagger Petstore — API de tienda de mascotas

**API:** https://petstore.swagger.io/v2 · [Documentación en línea](https://petstore.swagger.io/)  
**Documentación guardada:** [`documentacion_petstore.html`](./DOCUMENTACION/documentacion_petstore.html) — la página original de Swagger UI con la especificación completa, en un solo archivo  
**Tipo de prueba:** funcional y de contrato (respuesta frente a la especificación OpenAPI 2.0)  
**Herramientas:** Python · pytest · requests  
**Fecha de ejecución:** 25 de octubre de 2026  
**Resultado:** 17 casos · 6 pasan · 11 fallan por bugs

## Alcance

Ciclo de vida de una mascota (crear, leer, actualizar, borrar), búsqueda por
estado, pedidos, inventario y login de usuarios. El resultado esperado sale de
la propia especificación de la API:

- `Pet`: `name` y `photoUrls` son obligatorios; `status` solo puede ser `available`, `pending` o `sold`.
- `Order`: `status` solo puede ser `placed`, `approved` o `delivered`; `shipDate` es `date-time`.
- Cada ruta documenta sus códigos de error: `405 Invalid input`, `400 Invalid ID supplied`, `404 Pet not found`, `400 Invalid Order`, `400 Invalid username/password supplied`.

Cada prueba borra la mascota o el pedido que crea, para no dejar datos en la API pública.

## Estructura

| Carpeta | Archivo | Descripción |
|---|---|---|
| `PRUEBAS/` | `configuration.py` | URL base y rutas de los endpoints. |
| | `data.py` | Cuerpos de mascota y pedido, estados válidos y credenciales falsas. |
| | `sender_stand_request.py` | Funciones que hacen las peticiones HTTP con `requests`. |
| | `petstore_test.py` | 17 casos de prueba (positivos y negativos). |
| `DOCUMENTACION/` | [`documentacion_petstore.html`](./DOCUMENTACION/documentacion_petstore.html) | Copia de la página oficial de documentación; se abre con doble clic. |
| `RESULTADOS/` | [`casos_de_prueba_petstore.xlsx`](./RESULTADOS/casos_de_prueba_petstore.xlsx) | Casos de prueba con resultado esperado, obtenido y estado; hoja de bugs y resumen. |
| | [`informe_de_errores_petstore.docx`](./RESULTADOS/informe_de_errores_petstore.docx) | Informe de errores con severidad, pasos para reproducir e impacto. |

## Ejecución

Con el entorno activado (ver `setup.bat` en la raíz del proyecto):

```bash
cd API/Petstore/PRUEBAS
pytest -v
```

## Casos de prueba

| # | Caso | Esperado (según la especificación) | Obtenido | Resultado |
|---|---|---|---|---|
| 1 | Crear una mascota válida y leerla | 200 y se lee igual | Igual | ✅ PASSED |
| 2 | Borrar una mascota y volver a consultarla | 404 "Pet not found" | 404 | ✅ PASSED |
| 3 | Buscar por estado `sold` | Solo mascotas vendidas | Solo vendidas | ✅ PASSED |
| 4 | Consultar una mascota que no existe | 404 | 404 | ✅ PASSED |
| 5 | Crear un pedido válido y leerlo | 200 | 200 | ✅ PASSED |
| 6 | Consultar un usuario que no existe | 404 "User not found" | 404 | ✅ PASSED |
| 7 | Mascota sin `name` ni `photoUrls` | 405 | 200 | ❌ FAILED · PS-01 |
| 8 | Mascota con estado `volando` | 405 | 200 | ❌ FAILED · PS-02 |
| 9 | Inventario por estado | Solo estados válidos | Decenas de estados basura | ❌ FAILED · PS-03 |
| 10 | Mascota con id `"abc"` | 405 | 500 | ❌ FAILED · PS-04 |
| 11 | Buscar por estado inválido | 400 "Invalid status value" | 200 con lista vacía | ❌ FAILED · PS-05 |
| 12 | Pedido con cantidad -5 | 400 "Invalid Order" | 200 | ❌ FAILED · PS-06 |
| 13 | `GET /pet/abc` | 400 "Invalid ID supplied" | 404 con excepción de Java | ❌ FAILED · PS-07 |
| 14 | Actualizar una mascota que no existe | 404 "Pet not found" | 200 y la crea | ❌ FAILED · PS-08 |
| 15 | Pedido con estado `perdido` | 400 "Invalid Order" | 200 | ❌ FAILED · PS-09 |
| 16 | Pedido con `shipDate: "ayer"` | 400 "Invalid Order" | 500 | ❌ FAILED · PS-10 |
| 17 | Login con un usuario que no existe | 400 "Invalid username/password supplied" | 200 con sesión | ❌ FAILED · PS-11 |

## Bugs encontrados

### PS-01 · Crea mascotas sin los campos obligatorios
**Severidad:** Media  
**Pasos:** `POST /pet` con solo `{"id": 123}`.  
**Esperado:** 405 "Invalid input"; la especificación marca `name` y `photoUrls` como obligatorios.  
**Obtenido:** 200 y se crea una mascota sin nombre.  
**Impacto:** quedan registros incompletos que luego fallan en otras pantallas.  

### PS-02 · Acepta estados de mascota que no existen
**Severidad:** Media  
**Pasos:** `POST /pet` con `"status": "volando"`.  
**Esperado:** 405, porque el estado debe ser `available`, `pending` o `sold`.  
**Obtenido:** 200 y se guarda `volando`.  
**Impacto:** el estado deja de ser confiable para filtrar o reportar.  

### PS-03 · El inventario ya está contaminado
**Severidad:** Alta  
**Pasos:** `GET /store/inventory`.  
**Esperado:** solo los tres estados válidos.  
**Obtenido:** decenas de estados basura, como `string`, `sdf`, `3000`, `INVALID_VALUE` o `invalid`.  
**Impacto:** es la consecuencia real de PS-02: como la API deja entrar datos inválidos, el inventario ya no es confiable.  

### PS-04 · Error 500 al crear una mascota con id en texto
**Severidad:** Media  
**Pasos:** `POST /pet` con `"id": "abc"`.  
**Esperado:** 405 "Invalid input".  
**Obtenido:** `500 "something bad happened"`.  
**Impacto:** el servidor no valida tipos de dato antes de procesar.  

### PS-05 · Buscar por un estado inválido no avisa
**Severidad:** Baja  
**Pasos:** `GET /pet/findByStatus?status=volando`.  
**Esperado:** 400 "Invalid status value".  
**Obtenido:** 200 con lista vacía.  
**Impacto:** el cliente no distingue entre "no hay resultados" y "pedí mal".  

### PS-06 · Pedidos con cantidad negativa
**Severidad:** Alta  
**Pasos:** `POST /store/order` con `"quantity": -5`.  
**Esperado:** 400 "Invalid Order".  
**Obtenido:** 200 y el pedido se guarda con `-5`.  
**Impacto:** quedan pedidos con cantidades imposibles que alteran el inventario.  

### PS-07 · Un id inválido expone una excepción interna
**Severidad:** Media  
**Pasos:** `GET /pet/abc` (también pasa con `GET /store/order/abc`).  
**Esperado:** 400 "Invalid ID supplied".  
**Obtenido:** 404 con el mensaje `java.lang.NumberFormatException: For input string: "abc"`.  
**Impacto:** responde con un código que no corresponde y deja ver el lenguaje y la excepción del servidor, información útil para un atacante.  

### PS-08 · Actualizar una mascota que no existe la crea
**Severidad:** Media  
**Pasos:** `PUT /pet` con un `id` que no existe.  
**Esperado:** 404 "Pet not found".  
**Obtenido:** 200 y la mascota queda creada.  
**Impacto:** un error de id en una actualización crea registros nuevos sin que el cliente se entere.  

### PS-09 · Acepta estados de pedido que no existen
**Severidad:** Media  
**Pasos:** `POST /store/order` con `"status": "perdido"`.  
**Esperado:** 400, porque el estado debe ser `placed`, `approved` o `delivered`.  
**Obtenido:** 200 y se guarda `perdido`.  
**Impacto:** el mismo problema de PS-02, ahora en los pedidos.  

### PS-10 · Error 500 con una fecha de envío inválida
**Severidad:** Media  
**Pasos:** `POST /store/order` con `"shipDate": "ayer"`.  
**Esperado:** 400 "Invalid Order".  
**Obtenido:** `500 "something bad happened"`.  
**Impacto:** el servidor falla en lugar de rechazar el dato, y el cliente no sabe qué corregir.  

### PS-11 · El login acepta cualquier usuario y clave
**Severidad:** Alta  
**Pasos:** `GET /user/login?username=usuario_que_no_existe_qa&password=clave_incorrecta`.  
**Esperado:** 400 "Invalid username/password supplied".  
**Obtenido:** 200 con `"logged in user session:..."`.  
**Impacto:** el login no comprueba las credenciales: cualquiera obtiene una sesión.  

⬅️ [Volver al inicio](../../README.md)
