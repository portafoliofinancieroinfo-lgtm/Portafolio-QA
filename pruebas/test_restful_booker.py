"""Pruebas de API: Restful-Booker (reservas de hotel).

Las pruebas marcadas con xfail documentan bugs confirmados: afirman el
comportamiento correcto y fallan mientras el bug exista. Si un bug se corrige,
pytest lo reporta como XPASS y la suite falla, para revisar el caso.
"""
import pytest
import requests

BASE = "https://restful-booker.herokuapp.com"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
RESERVA = {
    "firstname": "Ana",
    "lastname": "Prueba",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-05"},
    "additionalneeds": "Desayuno",
}


def bug(codigo, descripcion):
    return pytest.mark.xfail(strict=True, reason=f"{codigo}: {descripcion}")


def crear(**cambios):
    return requests.post(f"{BASE}/booking", json={**RESERVA, **cambios}, headers=HEADERS, timeout=30)


# --- Casos que deben pasar -------------------------------------------------

def test_rb_c01_crear_y_leer_reserva_valida():
    r = crear()
    assert r.ok
    reserva = requests.get(f"{BASE}/booking/{r.json()['bookingid']}", headers=HEADERS, timeout=30).json()
    assert reserva == RESERVA


def test_rb_c02_reserva_inexistente_responde_404():
    assert requests.get(f"{BASE}/booking/999999999", headers=HEADERS, timeout=30).status_code == 404


def test_rb_c03_borrar_sin_token_es_rechazado():
    bid = crear().json()["bookingid"]
    assert requests.delete(f"{BASE}/booking/{bid}", timeout=30).status_code in (401, 403)


# --- Bugs confirmados ------------------------------------------------------

@bug("RB-01", "un precio con decimales se guarda sin los decimales (150.75 -> 150)")
def test_rb_b01_precio_con_decimales_se_conserva():
    assert crear(totalprice=150.75).json()["booking"]["totalprice"] == 150.75


@bug("RB-02", "un precio no numérico crea la reserva con precio null")
def test_rb_b02_precio_no_numerico_es_rechazado():
    assert crear(totalprice="ciento cincuenta").status_code == 400


@bug("RB-03", "acepta reservas con precio negativo")
def test_rb_b03_precio_negativo_es_rechazado():
    assert crear(totalprice=-150).status_code == 400


@bug("RB-04", "acepta una fecha de salida anterior a la de entrada")
def test_rb_b04_salida_antes_de_entrada_es_rechazada():
    assert crear(bookingdates={"checkin": "2026-12-10", "checkout": "2026-12-01"}).status_code == 400


@bug("RB-05", "si faltan campos obligatorios responde 500 en vez de 400")
def test_rb_b05_campos_faltantes_responde_400():
    r = requests.post(f"{BASE}/booking", json={"firstname": "Ana"}, headers=HEADERS, timeout=30)
    assert r.status_code == 400


@bug("RB-06", "con credenciales incorrectas responde 200 en vez de 401")
def test_rb_b06_credenciales_incorrectas_responde_401():
    r = requests.post(f"{BASE}/auth", json={"username": "noexiste", "password": "incorrecta"},
                      headers=HEADERS, timeout=30)
    assert r.status_code == 401


@bug("RB-07", "crear una reserva responde 200 en vez de 201 Created")
def test_rb_b07_crear_reserva_responde_201():
    assert crear().status_code == 201
