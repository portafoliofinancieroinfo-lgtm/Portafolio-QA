# Brian David Calero Torres
**QA Tester** · Colombia

Hola, soy QA Tester formado en TripleTen. Pruebo software para encontrar los
errores antes de que lleguen al usuario: valido que cada sistema haga lo que
promete, documento lo que falla y automatizo las pruebas para que se puedan
repetir.

En este repositorio presento los servicios que puedo ofrecer como QA y pruebas
reales a tres APIs públicas, con **17 bugs encontrados y documentados**.

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

| API | Qué es | Casos | Bugs | Hallazgo principal |
|---|---|---|---|---|
| [Restful-Booker](./detalles/RestfulBooker.md) | Reservas de hotel | 10 | 7 | Acepta datos inválidos (precios negativos o en texto, fechas imposibles) y pierde los decimales del precio |
| [Swagger Petstore](./detalles/Petstore.md) | Tienda de mascotas | 8 | 6 | No valida contra su propia especificación: estados inválidos que ya contaminaron el inventario |
| [Toolshop](./detalles/Toolshop.md) | Tienda en línea | 8 | 4 | Datos personales de los clientes visibles sin iniciar sesión |

## Cómo correr las pruebas

```bash
pip install -r requirements.txt
pytest -rxX pruebas
```

Los casos que deben funcionar aparecen como `passed`, y cada bug confirmado
aparece como `xfailed` con su código, por ejemplo `RB-01`. Si alguna API
corrige un bug, la prueba aparece como `XPASS` y la suite falla para que se
revise ese caso.

## Contacto

📧 portafolio.financiero.info@gmail.com
