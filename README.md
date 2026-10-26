# Brian David Calero Torres
**QA Tester** · Colombia

Hola, soy QA Tester formado en TripleTen. Pruebo software para encontrar los
errores antes de que lleguen al usuario: valido que cada sistema haga lo que
promete, documento lo que falla y automatizo las pruebas para que se puedan
repetir.

En este repositorio presento los servicios que puedo ofrecer como QA y pruebas
reales a tres APIs públicas: **52 casos de prueba y 28 bugs encontrados y
documentados** contra la documentación oficial de cada API.

## Servicios que ofrezco

### 🔌 Pruebas de API
Pruebas funcionales, de validación de datos, de códigos de respuesta y de
contrato frente a la especificación OpenAPI/Swagger.

### 🤖 Automatización de pruebas
Suites en Python con pytest y requests, que se pueden volver a correr en
cualquier momento para confirmar si un bug sigue o ya se corrigió. También
automatizo pruebas web con Selenium WebDriver y Page Object Model.

### 🐞 Diseño de casos y reporte de defectos
Casos de prueba con resultado esperado y obtenido, y reportes de bugs con
severidad, pasos para reproducir, evidencia e impacto. Los gestiono en Jira.

### 🔒 Pruebas de seguridad básica
Control de acceso, manejo de credenciales inválidas, exposición de datos y
validación de la entrada del usuario.

### 🧭 Pruebas manuales
Web, cross-browser, móvil Android y API, con pruebas exploratorias y de
regresión.

## Proyectos: pruebas a APIs públicas

| API | Qué es | Casos | Pasan | Bugs | Hallazgo principal |
|---|---|---|---|---|---|
| [Restful-Booker](./API/RestfulBooker/RestfulBooker.md) | Reservas de hotel | 18 | 8 | 10 | Acepta datos inválidos (fechas que no son fechas, depósito en texto guardado como pagado) y pierde los decimales del precio |
| [Swagger Petstore](./API/Petstore/Petstore.md) | Tienda de mascotas | 17 | 6 | 11 | No valida contra su propia especificación y el login acepta cualquier usuario y clave |
| [Toolshop](./API/Toolshop/Toolshop.md) | Tienda en línea | 17 | 10 | 7 | Facturas con datos de los clientes y reportes de ventas visibles sin iniciar sesión |

Cada carpeta de [`API/`](./API) sigue la misma estructura:

| Carpeta | Contenido |
|---|---|
| `PRUEBAS/` | Suite automatizada: `configuration.py` (URL y rutas), `data.py` (datos de prueba), `sender_stand_request.py` (peticiones HTTP con `requests`) y `*_test.py` (casos positivos y negativos). |
| `DOCUMENTACION/` | `documentacion_*.html`: copia de la página oficial de documentación de la API en un solo archivo (se abre con doble clic). De ahí sale el resultado esperado de cada caso. |
| `RESULTADOS/` | `casos_de_prueba_*.xlsx` (casos, bugs y resumen) e `informe_de_errores_*.docx` (informe de errores en Word). |
| `*.md` | Resumen de la API: alcance, casos, resultados y bugs. |

## Cómo correr las pruebas

En Windows, ejecuta `setup.bat` (doble clic). Crea un entorno virtual en
`API\venv` e instala `requests` y `pytest`. Luego, en una terminal:

```bash
API\venv\Scripts\activate
cd API\Petstore\PRUEBAS
pytest -v
```

Igual con `API\RestfulBooker\PRUEBAS` y `API\Toolshop\PRUEBAS`: cada suite se
corre desde su carpeta `PRUEBAS`. Los casos que cumplen la documentación aparecen como `PASSED` y cada
bug aparece como `FAILED`, con el código de respuesta obtenido frente al
esperado. Si una API corrige un bug, esa prueba pasa a `PASSED`.

## Contacto

📧 portafolio.financiero.info@gmail.com
