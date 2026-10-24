"""Pruebas de API: Toolshop (practicesoftwaretesting.com), versión con bugs.

Cada bug se compara contra la versión sin bugs de la misma API, que sirve de
referencia del comportamiento esperado. Las pruebas no imprimen ni guardan
datos de clientes: solo revisan códigos de respuesta y nombres de campos.
"""
import pytest
import requests

BASE = "https://api-with-bugs.practicesoftwaretesting.com"
REFERENCIA = "https://api.practicesoftwaretesting.com"
CAMPOS_PRODUCTO = {"id", "name", "description", "price", "is_location_offer", "is_rental",
                   "co2_rating", "is_eco_friendly", "brand", "category", "product_image"}


def bug(codigo, descripcion):
    return pytest.mark.xfail(strict=True, reason=f"{codigo}: {descripcion}")


def get(ruta, base=BASE, **kw):
    return requests.get(base + ruta, timeout=30, **kw)


# --- Casos que deben pasar -------------------------------------------------

def test_ts_c01_ordenar_por_precio_ascendente():
    precios = [p["price"] for p in get("/products", params={"sort": "price,asc"}).json()["data"]]
    assert precios == sorted(precios)


def test_ts_c02_paginacion_recorre_todo_el_catalogo_sin_repetir():
    primera = get("/products", params={"page": 1}).json()
    ids = [p["id"] for pagina in range(1, primera["last_page"] + 1)
           for p in get("/products", params={"page": pagina}).json()["data"]]
    assert len(ids) == len(set(ids)) == primera["total"]


def test_ts_c03_filtro_de_precio_respeta_el_rango():
    precios = [p["price"] for p in get("/products", params={"between": "price,10,20"}).json()["data"]]
    assert precios and all(10 <= p <= 20 for p in precios)


def test_ts_c04_referencia_exige_login_para_ver_facturas():
    assert get("/invoices", base=REFERENCIA).status_code == 401


# --- Bugs confirmados ------------------------------------------------------

@bug("TS-01", "el listado de facturas se ve sin iniciar sesión, con dirección y cuenta de pago")
def test_ts_b01_facturas_exigen_login():
    assert get("/invoices").status_code == 401


@bug("TS-02", "ordenar por un campo inexistente provoca error 500")
def test_ts_b02_orden_invalido_no_provoca_error_500():
    assert get("/products", params={"sort": "precio,asc"}).status_code < 500


@bug("TS-03", "buscar '%' devuelve todo el catálogo: el comodín SQL no se escapa")
def test_ts_b03_busqueda_con_comodin_no_devuelve_todo():
    assert get("/products/search", params={"q": "%"}).json()["total"] == 0


@bug("TS-04", "los productos exponen campos internos (como el stock) que no están en el contrato")
def test_ts_b04_producto_cumple_el_contrato():
    producto = get("/products").json()["data"][0]
    assert set(producto) <= CAMPOS_PRODUCTO
