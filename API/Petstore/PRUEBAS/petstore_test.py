import data
import sender_stand_request

# El resultado esperado de cada prueba sale de la especificación oficial
# (documentacion_petstore.html). Las pruebas que fallan son bugs: ver Petstore.md.

# Funcion que me permite generar el cuerpo de una mascota con un id único
def get_pet_body(pet_id, **cambios):
    pet_body = data.pet_body.copy()
    pet_body["id"] = pet_id
    pet_body.update(cambios)
    return pet_body

# Funcion que me permite generar el cuerpo de un pedido con un id único
def get_order_body(order_id, **cambios):
    order_body = data.order_body.copy()
    order_body["id"] = order_id
    order_body.update(cambios)
    return order_body

# Funcion para las pruebas negativas de mascotas: la especificación responde 405 "Invalid input"
def negative_assert_pet_code_405(pet_body):
    response = sender_stand_request.post_new_pet(pet_body)
    sender_stand_request.delete_pet(pet_body["id"])  # limpieza: no dejar datos en la API pública
    assert response.status_code == 405

# Funcion para las pruebas negativas de pedidos: la especificación responde 400 "Invalid Order"
def negative_assert_order_code_400(order_body):
    response = sender_stand_request.post_new_order(order_body)
    sender_stand_request.delete_order(order_body["id"])
    assert response.status_code == 400

#Pruebas
# Prueba 1: Crear una mascota válida y leerla igual a lo enviado
def test_create_pet_valid_body_get_success_response():
    pet_body = get_pet_body(data.new_id())
    try:
        response = sender_stand_request.post_new_pet(pet_body)
        assert response.status_code == 200
        assert sender_stand_request.get_pet(pet_body["id"]).json() == pet_body
    finally:
        sender_stand_request.delete_pet(pet_body["id"])

# Prueba 2: Una mascota borrada ya no se encuentra (404 "Pet not found")
def test_delete_pet_then_get_not_found_response():
    pet_body = get_pet_body(data.new_id())
    sender_stand_request.post_new_pet(pet_body)
    assert sender_stand_request.delete_pet(pet_body["id"]).status_code == 200
    response = sender_stand_request.get_pet(pet_body["id"])
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"

# Prueba 3: Buscar por estado devuelve solo mascotas en ese estado
def test_find_by_status_sold_get_only_sold_pets():
    response = sender_stand_request.get_pets_by_status("sold")
    assert response.status_code == 200
    assert response.json() and all(pet["status"] == "sold" for pet in response.json())

# Prueba 4: Consultar una mascota que no existe responde 404
def test_get_pet_not_found_get_404_response():
    assert sender_stand_request.get_pet(data.new_id()).status_code == 404

# Prueba 5: Crear un pedido válido y leerlo
def test_create_order_valid_body_get_success_response():
    order_body = get_order_body(data.new_id())
    try:
        response = sender_stand_request.post_new_order(order_body)
        assert response.status_code == 200
        assert sender_stand_request.get_order(order_body["id"]).json()["quantity"] == 1
    finally:
        sender_stand_request.delete_order(order_body["id"])

# Prueba 6: Consultar un usuario que no existe responde 404 "User not found"
def test_get_user_not_found_get_404_response():
    response = sender_stand_request.get_user(data.bad_login["username"])
    assert response.status_code == 404

# Prueba 7 (PS-01): Mascota sin los campos obligatorios name y photoUrls
def test_create_pet_without_required_fields_get_error_response():
    negative_assert_pet_code_405({"id": data.new_id()}) #Failed: 200

# Prueba 8 (PS-02): Estado de mascota que no existe en la lista permitida
def test_create_pet_invalid_status_get_error_response():
    negative_assert_pet_code_405(get_pet_body(data.new_id(), status="volando")) #Failed: 200

# Prueba 9 (PS-03): El inventario solo debe tener los estados válidos
def test_inventory_has_only_valid_status():
    inventory = sender_stand_request.get_inventory().json()
    assert set(inventory) <= data.pet_status_validos #Failed: estados basura

# Prueba 10 (PS-04): Id de texto en lugar de número
def test_create_pet_text_id_get_error_response():
    response = sender_stand_request.post_new_pet(get_pet_body("abc"))
    assert response.status_code == 405 #Failed: 500

# Prueba 11 (PS-05): Buscar por un estado inválido responde 400 "Invalid status value"
def test_find_by_invalid_status_get_error_response():
    assert sender_stand_request.get_pets_by_status("volando").status_code == 400 #Failed: 200

# Prueba 12 (PS-06): Pedido con cantidad negativa
def test_create_order_negative_quantity_get_error_response():
    negative_assert_order_code_400(get_order_body(data.new_id(), quantity=-5)) #Failed: 200

# Prueba 13 (PS-07): Consultar una mascota con id de texto responde 400 "Invalid ID supplied"
def test_get_pet_text_id_get_error_response():
    response = sender_stand_request.get_pet("abc")
    assert response.status_code == 400 #Failed: 404 con excepción de Java
    assert "Exception" not in response.text

# Prueba 14 (PS-08): Actualizar una mascota que no existe responde 404 "Pet not found"
def test_update_pet_not_found_get_404_response():
    pet_body = get_pet_body(data.new_id())
    response = sender_stand_request.put_pet(pet_body)
    sender_stand_request.delete_pet(pet_body["id"])
    assert response.status_code == 404 #Failed: 200 y la crea

# Prueba 15 (PS-09): Pedido con estado que no existe en la lista permitida
def test_create_order_invalid_status_get_error_response():
    negative_assert_order_code_400(get_order_body(data.new_id(), status="perdido")) #Failed: 200

# Prueba 16 (PS-10): Pedido con fecha de envío que no es fecha
def test_create_order_invalid_ship_date_get_error_response():
    negative_assert_order_code_400(get_order_body(data.new_id(), shipDate="ayer")) #Failed: 500

# Prueba 17 (PS-11): Login con un usuario que no existe responde 400 "Invalid username/password supplied"
def test_login_bad_credentials_get_error_response():
    response = sender_stand_request.get_login(data.bad_login)
    assert response.status_code == 400 #Failed: 200 con sesión iniciada
