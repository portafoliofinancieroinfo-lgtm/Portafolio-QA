# Restful-Booker — API de reservas de hotel

**API:** https://restful-booker.herokuapp.com · [Documentación](https://restful-booker.herokuapp.com/apidoc/index.html)  
**Tipo de prueba:** funcional, validación de datos y códigos de respuesta  
**Herramientas:** Python · pytest · requests  
**Pruebas automatizadas:** [`pruebas/test_restful_booker.py`](../pruebas/test_restful_booker.py)  
**Fecha de ejecución:** octubre 2026  

## Alcance

Crear, consultar y borrar reservas, validar los datos que entran (precio,
fechas, campos obligatorios) y revisar la autenticación. No se usaron las
credenciales de administrador: los casos de seguridad se probaron con
credenciales falsas y sin token.

## Casos de prueba

| ID | Caso | Esperado | Obtenido | Resultado |
|---|---|---|---|---|
| RB-C01 | Crear y leer una reserva válida | Se guarda igual a lo enviado | Igual | ✅ Pasa |
| RB-C02 | Consultar una reserva que no existe | 404 | 404 | ✅ Pasa |
| RB-C03 | Borrar una reserva sin token | Rechazado (401/403) | 403 | ✅ Pasa |
| RB-B01 | Precio con decimales (150.75) | Se guarda 150.75 | Se guarda 150 | ❌ Bug RB-01 |
| RB-B02 | Precio en texto | 400 | 200 y precio `null` | ❌ Bug RB-02 |
| RB-B03 | Precio negativo (-150) | 400 | 200 | ❌ Bug RB-03 |
| RB-B04 | Salida antes de la entrada | 400 | 200 | ❌ Bug RB-04 |
| RB-B05 | Faltan campos obligatorios | 400 | 500 | ❌ Bug RB-05 |
| RB-B06 | Credenciales incorrectas | 401 | 200 | ❌ Bug RB-06 |
| RB-B07 | Código al crear una reserva | 201 Created | 200 | ❌ Bug RB-07 |

## Bugs encontrados

### RB-01 · El precio pierde los decimales
**Severidad:** Alta  
**Pasos:** `POST /booking` con `"totalprice": 150.75`.  
**Esperado:** la reserva guarda `150.75`.  
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
**Esperado:** 401 Unauthorized.  
**Obtenido:** 200 con `{"reason": "Bad credentials"}`.  
**Impacto:** un cliente que revisa solo el código de respuesta cree que inició sesión.  

### RB-07 · Crear responde 200 en vez de 201
**Severidad:** Baja  
**Pasos:** `POST /booking` con una reserva válida.  
**Esperado:** 201 Created.  
**Obtenido:** 200 OK.  
**Impacto:** no sigue el estándar REST; además `GET /ping` responde 201, al revés.  

⬅️ [Volver al inicio](../README.md)
