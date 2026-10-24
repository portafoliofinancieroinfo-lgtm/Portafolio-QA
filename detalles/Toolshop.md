# Toolshop — API de tienda en línea

**API probada:** https://api-with-bugs.practicesoftwaretesting.com · [Documentación](https://api-with-bugs.practicesoftwaretesting.com/api/documentation)  
**Referencia (versión sin bugs):** https://api.practicesoftwaretesting.com  
**Tipo de prueba:** funcional, seguridad (control de acceso) y contrato  
**Herramientas:** Python · pytest · requests  
**Pruebas automatizadas:** [`pruebas/test_toolshop.py`](../pruebas/test_toolshop.py)  
**Fecha de ejecución:** octubre 2026  

## Alcance

Catálogo (orden, paginación, filtros y búsqueda), contrato de la respuesta de
productos y control de acceso a facturas. El resultado esperado sale de la
versión sin bugs de la misma API. No se inició sesión ni se usaron datos de
pago, y las pruebas no guardan datos de clientes: solo revisan códigos de
respuesta y nombres de campos.

## Casos de prueba

| ID | Caso | Esperado | Obtenido | Resultado |
|---|---|---|---|---|
| TS-C01 | Ordenar por precio ascendente | Precios en orden | En orden | ✅ Pasa |
| TS-C02 | Recorrer todas las páginas | Cada producto una vez y el total cuadra | Cuadra | ✅ Pasa |
| TS-C03 | Filtrar precio entre 10 y 20 | Solo precios en el rango | En el rango | ✅ Pasa |
| TS-C04 | Facturas sin login (referencia) | 401 | 401 | ✅ Pasa |
| TS-B01 | Facturas sin login (versión probada) | 401 | 200 con las facturas | ❌ Bug TS-01 |
| TS-B02 | Ordenar por un campo inexistente | 400/422 | 500 | ❌ Bug TS-02 |
| TS-B03 | Buscar `%` | Sin resultados | Todo el catálogo | ❌ Bug TS-03 |
| TS-B04 | Campos de un producto | Solo los del contrato | Incluye `stock`, `brand_id`… | ❌ Bug TS-04 |

## Bugs encontrados

### TS-01 · Las facturas se ven sin iniciar sesión
**Severidad:** Crítica  
**Pasos:** `GET /invoices` sin token.  
**Esperado:** 401, como responde la versión de referencia.  
**Obtenido:** 200 con el listado de facturas, que incluye la dirección de los clientes y los datos de su cuenta de pago.  
**Impacto:** cualquiera en internet puede leer datos personales de los clientes. Es una falla de control de acceso: `GET /invoices/search` sí exige login, así que la protección es inconsistente entre rutas del mismo recurso.  

### TS-02 · Error 500 al ordenar por un campo inexistente
**Severidad:** Media  
**Pasos:** `GET /products?sort=precio,asc`.  
**Esperado:** 400 o 422 indicando el campo inválido.  
**Obtenido:** `500 "Something went wrong"`.  
**Impacto:** el parámetro llega sin validar a la base de datos. La versión de referencia tiene el mismo comportamiento.  

### TS-03 · Buscar `%` devuelve todo el catálogo
**Severidad:** Media  
**Pasos:** `GET /products/search?q=%`.  
**Esperado:** ningún resultado, porque ningún producto contiene `%`.  
**Obtenido:** los 26 productos. La versión de referencia devuelve 0.  
**Impacto:** el texto se pasa a la consulta SQL sin escapar los comodines. Hoy solo afecta la búsqueda, pero indica que la entrada del usuario no se limpia antes de llegar a la base de datos.  

### TS-04 · Los productos exponen campos internos
**Severidad:** Baja  
**Pasos:** `GET /products` y revisar los campos de un producto.  
**Esperado:** solo los campos del contrato `ProductResponse`.  
**Obtenido:** además trae `stock` (cantidad exacta en bodega), `brand_id`, `category_id` y `product_image_id`.  
**Impacto:** se publica el inventario exacto a la competencia y la respuesta no cumple el contrato que usan los clientes de la API.  

⬅️ [Volver al inicio](../README.md)
