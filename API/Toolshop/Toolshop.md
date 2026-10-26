# Toolshop — API de tienda en línea

**API probada:** https://api-with-bugs.practicesoftwaretesting.com · [Documentación en línea](https://api-with-bugs.practicesoftwaretesting.com/api/documentation)  
**Referencia (versión sin bugs):** https://api.practicesoftwaretesting.com  
**Documentación guardada:** [`documentacion_toolshop.html`](./DOCUMENTACION/documentacion_toolshop.html) — la página original de Swagger UI con la especificación OpenAPI 3.0 (v5.0.0) completa, en un solo archivo  
**Tipo de prueba:** funcional, seguridad (control de acceso) y contrato  
**Herramientas:** Python · pytest · requests  
**Fecha de ejecución:** 25 de octubre de 2026  
**Resultado:** 17 casos · 10 pasan · 7 fallan por bugs

## Alcance

Catálogo (orden, paginación, filtros, detalle y búsqueda), contrato de la
respuesta de productos, control de acceso a las rutas protegidas y la propia
documentación. El resultado esperado sale de la especificación OpenAPI (las
rutas con `security: apiAuth` exigen login) y de la versión sin bugs de la misma
API. No se inició sesión ni se usaron datos de pago, y las pruebas no guardan
datos de clientes: solo revisan códigos de respuesta y nombres de campos.

## Estructura

| Carpeta | Archivo | Descripción |
|---|---|---|
| `PRUEBAS/` | `configuration.py` | URL base y rutas de los endpoints. |
| | `data.py` | Campos del contrato `ProductResponse`, rutas protegidas, rutas de reportes y credenciales falsas. |
| | `sender_stand_request.py` | Funciones que hacen las peticiones HTTP con `requests`, incluida la descarga de la especificación. |
| | `toolshop_test.py` | 17 casos de prueba (positivos y negativos). |
| `DOCUMENTACION/` | [`documentacion_toolshop.html`](./DOCUMENTACION/documentacion_toolshop.html) | Copia de la página oficial de documentación; se abre con doble clic. |
| `RESULTADOS/` | [`casos_de_prueba_toolshop.xlsx`](./RESULTADOS/casos_de_prueba_toolshop.xlsx) | Casos de prueba con resultado esperado, obtenido y estado; hoja de bugs y resumen. |
| | [`informe_de_errores_toolshop.docx`](./RESULTADOS/informe_de_errores_toolshop.docx) | Informe de errores con severidad, pasos para reproducir e impacto. |

## Ejecución

Con el entorno activado (ver `setup.bat` en la raíz del proyecto):

```bash
cd API/Toolshop/PRUEBAS
pytest -v
```

## Casos de prueba

| # | Caso | Esperado | Obtenido | Resultado |
|---|---|---|---|---|
| 1 | Ordenar por precio ascendente | Precios en orden | En orden | ✅ PASSED |
| 2 | Ordenar por nombre descendente | Nombres en orden | En orden | ✅ PASSED |
| 3 | Recorrer todas las páginas | Cada producto una vez y el total cuadra | Cuadra | ✅ PASSED |
| 4 | Filtrar precio entre 10 y 20 | Solo precios en el rango | En el rango | ✅ PASSED |
| 5 | Consultar un producto existente | 200 con el mismo id | 200 | ✅ PASSED |
| 6 | Consultar un producto que no existe | 404 "Requested item not found" | 404 | ✅ PASSED |
| 7 | Buscar `hammer` | Solo nombres que lo contienen | Correcto | ✅ PASSED |
| 8 | `/users`, `/users/me`, `/favorites`, `/messages`, `/invoices/search` sin token | 401 | 401 | ✅ PASSED |
| 9 | Login con una cuenta que no existe | 401 | 401 | ✅ PASSED |
| 10 | Facturas sin login (referencia) | 401 | 401 | ✅ PASSED |
| 11 | Facturas sin login (versión probada) | 401 | 200 con las facturas | ❌ FAILED · TS-01 |
| 12 | Ordenar por un campo inexistente | 400/422 | 500 | ❌ FAILED · TS-02 |
| 13 | Buscar `%` | Sin resultados | Todo el catálogo (29) | ❌ FAILED · TS-03 |
| 14 | Campos de un producto | Solo los del contrato | Incluye `stock`, `brand_id`… | ❌ FAILED · TS-04 |
| 15 | Los 7 reportes de ventas sin login | 401 | 200 con los datos | ❌ FAILED · TS-05 |
| 16 | Buscar sin el parámetro obligatorio `q` | Sin resultados | Todo el catálogo (29) | ❌ FAILED · TS-06 |
| 17 | Documentación de `GET /products/{productId}` | Describe un producto | Describe una marca | ❌ FAILED · TS-07 |

## Bugs encontrados

### TS-01 · Las facturas se ven sin iniciar sesión
**Severidad:** Crítica  
**Pasos:** `GET /invoices` sin token.  
**Esperado:** 401, como responde la versión de referencia. La especificación de la referencia marca esta ruta con `security: apiAuth`.  
**Obtenido:** 200 con el listado de facturas, que incluye la dirección de los clientes y los datos de su cuenta de pago.  
**Impacto:** cualquiera en internet puede leer datos personales de los clientes. Es una falla de control de acceso: `GET /invoices/search` sí exige login, así que la protección es inconsistente entre rutas del mismo recurso. En la especificación de la versión probada a esta ruta le falta `security`.  

### TS-02 · Error 500 al ordenar por un campo inexistente
**Severidad:** Media  
**Pasos:** `GET /products?sort=precio,asc`.  
**Esperado:** 400 o 422 indicando el campo inválido. La documentación solo admite `name` y `price`.  
**Obtenido:** `500 "Something went wrong"`.  
**Impacto:** el parámetro llega sin validar a la base de datos. La versión de referencia tiene el mismo comportamiento.  

### TS-03 · Buscar `%` devuelve todo el catálogo
**Severidad:** Media  
**Pasos:** `GET /products/search?q=%`.  
**Esperado:** ningún resultado, porque ningún producto contiene `%`.  
**Obtenido:** los 29 productos. La versión de referencia devuelve 0.  
**Impacto:** el texto se pasa a la consulta SQL sin escapar los comodines. Hoy solo afecta la búsqueda, pero indica que la entrada del usuario no se limpia antes de llegar a la base de datos.  

### TS-04 · Los productos exponen campos internos
**Severidad:** Baja  
**Pasos:** `GET /products` y revisar los campos de un producto.  
**Esperado:** solo los campos del contrato `ProductResponse`.  
**Obtenido:** además trae `stock` (cantidad exacta en bodega), `brand_id`, `category_id` y `product_image_id`.  
**Impacto:** se publica el inventario exacto a la competencia y la respuesta no cumple el contrato que usan los clientes de la API.  

### TS-05 · Los reportes de ventas se ven sin iniciar sesión
**Severidad:** Alta  
**Pasos:** `GET` sin token a cada ruta de `/reports`: `total-sales-per-country`, `top10-purchased-products`, `top10-best-selling-categories`, `total-sales-of-years`, `average-sales-per-month`, `average-sales-per-week` y `customers-by-country`.  
**Esperado:** 401. La especificación marca las 7 rutas con `security: apiAuth`, y la versión de referencia responde 401 en todas.  
**Obtenido:** 200 en las 7, con ventas por país, productos más vendidos, ingresos por categoría y clientes por país.  
**Impacto:** la información comercial del negocio, que solo debería ver el administrador, queda pública.  

### TS-06 · Buscar sin texto devuelve todo el catálogo
**Severidad:** Baja  
**Pasos:** `GET /products/search` sin el parámetro `q`.  
**Esperado:** la especificación marca `q` como obligatorio; la versión de referencia responde sin resultados.  
**Obtenido:** los 29 productos.  
**Impacto:** el parámetro obligatorio no se valida, y una búsqueda vacía termina en una consulta de todo el catálogo.  

### TS-07 · La documentación describe mal la respuesta de un producto
**Severidad:** Baja (defecto de documentación)  
**Pasos:** abrir `GET /products/{productId}` en la documentación y comparar con la respuesta real.  
**Esperado:** que la respuesta 200 use el esquema `ProductResponse`.  
**Obtenido:** la documentación dice `BrandResponse` (`id`, `name`, `slug`), pero la API devuelve un producto completo con precio, categoría e imagen.  
**Impacto:** quien genere un cliente a partir de la especificación obtiene un modelo equivocado y pierde los datos del producto.  

⬅️ [Volver al inicio](../../README.md)
