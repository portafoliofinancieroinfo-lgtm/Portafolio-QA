"""Pruebas de API: Swagger Petstore v2 (tienda de mascotas).

Las pruebas marcadas con xfail documentan bugs confirmados contra la propia
especificación de la API (https://petstore.swagger.io/v2/swagger.json).
"""
import random

import pytest
import requests

BASE = "https://petstore.swagger.io/v2"
ESTADOS_VALIDOS = {"available", "pending", "sold"}


def bug(codigo, descripcion):
    return pytest.mark.xfail(strict=True, reason=f"{codigo}: {descripcion}")


@pytest.fixture
def pet_id():
    """Id único por prueba; la mascota se borra al terminar para no dejar basura en la API pública."""
    pid = random.randint(10**9, 2 * 10**9)
    yield pid
    requests.delete(f"{BASE}/pet/{pid}", timeout=30)


def crear(pet):
    return requests.post(f"{BASE}/pet", json=pet, timeout=30)


# --- Casos que deben pasar -------------------------------------------------

def test_ps_c01_crear_leer_y_borrar_mascota(pet_id):
    pet = {"id": pet_id, "name": "Firulais", "photoUrls": [], "tags": [], "status": "available"}
    assert crear(pet).ok
    assert requests.get(f"{BASE}/pet/{pet_id}", timeout=30).json() == pet
    assert requests.delete(f"{BASE}/pet/{pet_id}", timeout=30).ok
    assert requests.get(f"{BASE}/pet/{pet_id}", timeout=30).status_code == 404


def test_ps_c02_buscar_por_estado_devuelve_solo_ese_estado():
    mascotas = requests.get(f"{BASE}/pet/findByStatus", params={"status": "sold"}, timeout=30).json()
    assert mascotas and all(m["status"] == "sold" for m in mascotas)


# --- Bugs confirmados ------------------------------------------------------

@bug("PS-01", "crea mascotas sin los campos obligatorios name y photoUrls")
def test_ps_b01_mascota_sin_campos_obligatorios_es_rechazada(pet_id):
    assert crear({"id": pet_id}).status_code == 405


@bug("PS-02", "acepta un estado que no existe en la especificación")
def test_ps_b02_estado_fuera_de_la_lista_es_rechazado(pet_id):
    assert crear({"id": pet_id, "name": "Firulais", "photoUrls": [], "status": "volando"}).status_code == 405


@bug("PS-03", "el inventario está contaminado con estados inválidos (consecuencia de PS-02)")
def test_ps_b03_inventario_solo_tiene_estados_validos():
    inventario = requests.get(f"{BASE}/store/inventory", timeout=30).json()
    assert set(inventario) <= ESTADOS_VALIDOS


@bug("PS-04", "un id de texto provoca error 500 en vez de 405 por entrada inválida")
def test_ps_b04_id_de_texto_es_rechazado_sin_error_500():
    assert crear({"id": "abc", "name": "Firulais", "photoUrls": []}).status_code == 405


@bug("PS-05", "buscar por un estado inválido responde 200 en vez de 400")
def test_ps_b05_buscar_estado_invalido_responde_400():
    r = requests.get(f"{BASE}/pet/findByStatus", params={"status": "volando"}, timeout=30)
    assert r.status_code == 400


@bug("PS-06", "acepta pedidos con cantidad negativa")
def test_ps_b06_pedido_con_cantidad_negativa_es_rechazado(pet_id):
    orden = {"id": pet_id, "petId": pet_id, "quantity": -5, "status": "placed", "complete": False}
    r = requests.post(f"{BASE}/store/order", json=orden, timeout=30)
    requests.delete(f"{BASE}/store/order/{pet_id}", timeout=30)
    assert r.status_code == 400
