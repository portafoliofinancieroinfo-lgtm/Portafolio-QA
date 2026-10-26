# Restful-Booker — API de reservas de hotel

**API:** https://restful-booker.herokuapp.com · [Documentación en línea](https://restful-booker.herokuapp.com/apidoc/index.html)  
**Documentación guardada:** [`documentacion_restfulbooker.html`](./DOCUMENTACION/documentacion_restfulbooker.html) — la página original de apiDoc completa, en un solo archivo  
**Tipo de prueba:** funcional, validación de datos, seguridad y códigos de respuesta  
**Herramientas:** Python · pytest · requests  
**Fecha de ejecución:** 25 de octubre de 2026  
**Resultado:** 18 casos · 8 pasan · 10 fallan por bugs

## Alcance

Crear, consultar, filtrar, actualizar y borrar reservas; validar los datos que
entran y revisar la autenticación. El resultado esperado sale de la
documentación oficial:

- `CreateBooking`: todos los campos son obligatorios; `totalprice` es `Number`, `depositpaid` es `Boolean`, `firstname` es `String` y las fechas son `Date`. Responde `200 OK`.
- `UpdateBooking`, `PartialUpdateBooking` y `DeleteBooking` exigen un token o autenticación básica.
- `HealthCheck` (`GET /ping`) responde `201 Created`.

La documentación publica las credenciales de administrador, pero no se usaron:
los casos de seguridad se probaron sin token y con un token inventado. Por eso
las reservas de prueba no se pueden borrar; la API pública se reinicia sola cada
cierto tiempo.

## Estructura

| Carpeta | Archivo | Descripción |
|---|---|---|
| `PRUEBAS/` | `configuration.py` | URL base y rutas de los endpoints. |
| | `data.py` | Cuerpo de la reserva, headers JSON/XML, credenciales y token falsos. |
| | `sender_stand_request.py` | Funciones que hacen las peticiones HTTP con `requests`. |
| | `restful_booker_test.py` | 18 casos de prueba (positivos y negativos). |
| `DOCUMENTACION/` | [`documentacion_restfulbooker.html`](./DOCUMENTACION/documentacion_restfulbooker.html) | Copia de la página oficial de documentación; se abre con doble clic. |
| `RESULTADOS/` | [`casos_de_prueba_restfulbooker.xlsx`](./RESULTADOS/casos_de_prueba_restfulbooker.xlsx) | Casos de prueba con resultado esperado, obtenido y estado; hoja de bugs y resumen. |
| | [`informe_de_errores_restfulbooker.docx`](./RESULTADOS/informe_de_errores_restfulbooker.docx) | Informe de errores con severidad, pasos para reproducir e impacto. |

## Ejecución

Con el entorno activado (ver `setup.bat` en la raíz del proyecto):

```bash
cd API/RestfulBooker/PRUEBAS
pytest -v
```

## Casos de prueba

| # | Caso | Esperado (según la documentación) | Obtenido | Resultado |
|---|---|---|---|---|
| 1 | Crear una reserva válida y leerla | 200 y se guarda igual | Igual | ✅ PASSED |
| 2 | Consultar una reserva que no existe | 404 | 404 | ✅ PASSED |
| 3 | Borrar sin token | Rechazado | 403 | ✅ PASSED |
| 4 | Actualizar (PUT) sin token | Rechazado y sin cambios | 403, sin cambios | ✅ PASSED |
| 5 | Actualizar (PATCH) con token inventado | Rechazado y sin cambios | 403, sin cambios | ✅ PASSED |
| 6 | Filtrar por nombre y apellido | Devuelve la reserva creada | La devuelve | ✅ PASSED |
| 7 | HealthCheck `GET /ping` | 201 Created | 201 | ✅ PASSED |
| 8 | Crear con `Accept: application/xml` | Respuesta en XML | XML | ✅ PASSED |
| 9 | Precio con decimales (150.75) | Se guarda 150.75 | Se guarda 150 | ❌ FAILED · RB-01 |
| 10 | Precio en texto | 400 | 200 y precio `null` | ❌ FAILED · RB-02 |
| 11 | Precio negativo (-150) | 400 | 200 | ❌ FAILED · RB-03 |
| 12 | Salida antes de la entrada | 400 | 200 | ❌ FAILED · RB-04 |
| 13 | Faltan campos obligatorios | 400 | 500 | ❌ FAILED · RB-05 |
| 14 | Credenciales incorrectas | 401 | 200 | ❌ FAILED · RB-06 |
| 15 | Fechas que no son fechas | 400 | 200 con `0NaN-aN-aN` | ❌ FAILED · RB-07 |
| 16 | `depositpaid: "tal vez"` | 400 | 200 y se guarda `true` | ❌ FAILED · RB-08 |
| 17 | `firstname` numérico | 400 | 500 | ❌ FAILED · RB-09 |
| 18 | `firstname` vacío | 400 | 200 | ❌ FAILED · RB-10 |

> **Corrección frente a la versión anterior:** antes se reportaba como bug que
> crear una reserva responde 200 en vez de 201. La documentación oficial indica
> `HTTP/1.1 200 OK` para `CreateBooking`, así que la API cumple su contrato y
> ese caso pasó a ser una prueba positiva (caso 1).

## Bugs encontrados

### RB-01 · El precio pierde los decimales
**Severidad:** Alta  
**Pasos:** `POST /booking` con `"totalprice": 150.75`.  
**Esperado:** la reserva guarda `150.75`; la documentación define `totalprice` como `Number`.  
**Obtenido:** responde 200 y guarda `"totalprice": 150`.  
**Impacto:** la API guarda un valor distinto al que recibió, sin avisar. Cualquier sistema que use ese dato trabaja con información equivocada.  

### RB-02 · Un precio en texto deja la reserva sin precio
**Severidad:** Alta  
**Pasos:** `POST /booking` con `"totalprice": "ciento cincuenta"`.  
**Esperado:** 400, el precio debe ser numérico.  
**Obtenido:** 200 y la reserva queda con `"totalprice": null`.  
**Impacto:** quedan reservas con un campo obligatorio vacío.  

### RB-03 · Acepta precios negativos
**Severidad:** Media  
**Pasos:** `POST /booking` con `"totalprice": -150`.  
**Esperado:** 400.  
**Obtenido:** 200 y la reserva se guarda con `-150`.  
**Impacto:** se guardan valores sin sentido que afectan cualquier cálculo que use el precio.  

### RB-04 · La salida puede ser anterior a la entrada
**Severidad:** Media  
**Pasos:** `POST /booking` con `checkin: 2026-12-10` y `checkout: 2026-12-01`.  
**Esperado:** 400.  
**Obtenido:** 200 y la reserva se guarda con fechas imposibles.  
**Impacto:** la estadía da un número de noches negativo.  

### RB-05 · Error 500 cuando faltan campos
**Severidad:** Media  
**Pasos:** `POST /booking` solo con `{"firstname": "Ana"}`.  
**Esperado:** 400 con el detalle de los campos faltantes.  
**Obtenido:** `500 Internal Server Error`.  
**Impacto:** el servidor no valida la entrada; quien integra la API no sabe qué corregir.  

### RB-06 · Credenciales incorrectas responden 200
**Severidad:** Baja  
**Pasos:** `POST /auth` con usuario y clave falsos.  
**Esperado:** 401 Unauthorized. La documentación solo define la respuesta 200 con un `token`.  
**Obtenido:** 200 con `{"reason": "Bad credentials"}`.  
**Impacto:** un cliente que revisa solo el código de respuesta cree que inició sesión.  

### RB-07 · Acepta fechas que no son fechas
**Severidad:** Alta  
**Pasos:** `POST /booking` con `checkin: "no-es-fecha"` y `checkout: "2026-13-45"`.  
**Esperado:** 400; la documentación define las fechas como `Date`.  
**Obtenido:** 200 y las dos fechas se guardan como `"0NaN-aN-aN"`.  
**Impacto:** la reserva queda sin fechas válidas y no se puede saber cuándo llega ni cuándo se va el huésped.  

### RB-08 · Un depósito en texto se guarda como pagado
**Severidad:** Alta  
**Pasos:** `POST /booking` con `"depositpaid": "tal vez"`.  
**Esperado:** 400; la documentación define `depositpaid` como `Boolean`.  
**Obtenido:** 200 y se guarda `"depositpaid": true`.  
**Impacto:** la reserva queda marcada con el depósito pagado sin que nadie lo haya confirmado: es un dato de dinero.  

### RB-09 · Error 500 con un nombre numérico
**Severidad:** Media  
**Pasos:** `POST /booking` con `"firstname": 123`.  
**Esperado:** 400; `firstname` es `String`.  
**Obtenido:** `500 Internal Server Error`.  
**Impacto:** un error de tipo de dato tumba la petición en lugar de devolver un mensaje útil.  

### RB-10 · Acepta un nombre vacío
**Severidad:** Baja  
**Pasos:** `POST /booking` con `"firstname": ""`.  
**Esperado:** 400; `firstname` es obligatorio.  
**Obtenido:** 200 y la reserva se guarda sin nombre.  
**Impacto:** quedan reservas que no se pueden asociar a un huésped.  

⬅️ [Volver al inicio](../../README.md)
