# Swagger Petstore — API de tienda de mascotas

**API:** https://petstore.swagger.io/v2 · [Documentación](https://petstore.swagger.io/)  
**Tipo de prueba:** funcional y de contrato (respuesta frente a la especificación OpenAPI)  
**Herramientas:** Python · pytest · requests  
**Pruebas automatizadas:** [`pruebas/test_petstore.py`](../pruebas/test_petstore.py)  
**Fecha de ejecución:** octubre 2026  

## Alcance

Ciclo de vida de una mascota (crear, leer, borrar), búsqueda por estado,
pedidos e inventario. El resultado esperado sale de la propia especificación de
la API: `name` y `photoUrls` son obligatorios, y el estado solo puede ser
`available`, `pending` o `sold`. Cada prueba borra lo que crea para no dejar
datos en la API pública.

## Casos de prueba

| ID | Caso | Esperado | Obtenido | Resultado |
|---|---|---|---|---|
| PS-C01 | Crear, leer y borrar una mascota | Se guarda, se lee igual y luego da 404 | Igual | ✅ Pasa |
| PS-C02 | Buscar por estado `sold` | Solo mascotas vendidas | Solo vendidas | ✅ Pasa |
| PS-B01 | Mascota sin `name` ni `photoUrls` | 405 entrada inválida | 200 | ❌ Bug PS-01 |
| PS-B02 | Estado `volando` (no existe) | 405 | 200 | ❌ Bug PS-02 |
| PS-B03 | Inventario por estado | Solo estados válidos | Incluye `string`, `sdf`, `INVALID_VALUE`… | ❌ Bug PS-03 |
| PS-B04 | Id en texto (`"abc"`) | 405 | 500 | ❌ Bug PS-04 |
| PS-B05 | Buscar por estado inválido | 400 | 200 con lista vacía | ❌ Bug PS-05 |
| PS-B06 | Pedido con cantidad -5 | 400 | 200 | ❌ Bug PS-06 |

## Bugs encontrados

### PS-01 · Crea mascotas sin los campos obligatorios
**Severidad:** Media  
**Pasos:** `POST /pet` con solo `{"id": 123}`.  
**Esperado:** 405 "Invalid input", según la especificación.  
**Obtenido:** 200 y se crea una mascota sin nombre.  
**Impacto:** quedan registros incompletos que luego fallan en otras pantallas.  

### PS-02 · Acepta estados que no existen
**Severidad:** Media  
**Pasos:** `POST /pet` con `"status": "volando"`.  
**Esperado:** 405, porque el estado debe ser `available`, `pending` o `sold`.  
**Obtenido:** 200 y se guarda `volando`.  
**Impacto:** el estado deja de ser confiable para filtrar o reportar.  

### PS-03 · El inventario ya está contaminado
**Severidad:** Alta  
**Pasos:** `GET /store/inventory`.  
**Esperado:** solo los tres estados válidos.  
**Obtenido:** decenas de estados basura, como `string`, `sdf`, `test`, `INVALID_VALUE` o `invalid`.  
**Impacto:** es la consecuencia real de PS-02: como la API deja entrar datos inválidos, el inventario ya no es confiable.  

### PS-04 · Error 500 con un id en texto
**Severidad:** Media  
**Pasos:** `POST /pet` con `"id": "abc"`.  
**Esperado:** 405 entrada inválida.  
**Obtenido:** `500 "something bad happened"`.  
**Impacto:** el servidor no valida tipos de dato antes de procesar.  

### PS-05 · Buscar por un estado inválido no avisa
**Severidad:** Baja  
**Pasos:** `GET /pet/findByStatus?status=volando`.  
**Esperado:** 400 "Invalid status value", según la especificación.  
**Obtenido:** 200 con lista vacía.  
**Impacto:** el cliente no distingue entre "no hay resultados" y "pedí mal".  

### PS-06 · Pedidos con cantidad negativa
**Severidad:** Alta  
**Pasos:** `POST /store/order` con `"quantity": -5`.  
**Esperado:** 400.  
**Obtenido:** 200 y el pedido se guarda con `-5`.  
**Impacto:** quedan pedidos con cantidades imposibles que alteran el inventario.  

⬅️ [Volver al inicio](../README.md)
