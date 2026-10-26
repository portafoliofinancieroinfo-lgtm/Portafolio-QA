import random

import data
import sender_stand_request

# El resultado esperado de cada prueba sale de la documentación oficial
# (documentacion_restfulbooker.html). Las pruebas que fallan son bugs: ver RestfulBooker.md.
# No se usan las credenciales de administrador: los casos de seguridad van sin token
# o con un token inventado.

# Funcion que me permite generar el cuerpo de una reserva con un campo cambiado
def get_booking_body(**cambios):
    booking_body = data.booking_body.copy()
    booking_body.update(cambios)
    return booking_body

# Funcion para las pruebas positivas: la reserva se crea y se guarda igual a lo enviado
def positive_assert(booking_body):
    response = sender_stand_request.post_new_booking(booking_body)
    assert response.status_code == 200
    assert response.json()["booking"] == booking_body
    booking_id = response.json()["bookingid"]
    assert sender_stand_request.get_booking(booking_id).json() == booking_body

# Funcion para las pruebas negativas: la reserva no se debe crear
def negative_assert_code_400(booking_body):
    response = sender_stand_request.post_new_booking(booking_body)
    assert response.status_code == 400

#Pruebas
# Prueba 1: Crear una reserva válida responde 200 (así lo indica la documentación) y se lee igual
def test_create_booking_valid_body_get_success_response():
    positive_assert(get_booking_body())

# Prueba 2: Consultar una reserva que no existe responde 404
def test_get_booking_not_found_get_404_response():
    assert sender_stand_request.get_booking(data.booking_id_not_found).status_code == 404

# Prueba 3: Borrar una reserva sin token es rechazado
def test_delete_booking_without_token_get_error_response():
    booking_id = sender_stand_request.post_new_booking(data.booking_body).json()["bookingid"]
    assert sender_stand_request.delete_booking(booking_id).status_code == 403

# Prueba 4: Actualizar (PUT) una reserva sin token es rechazado
def test_update_booking_without_token_get_error_response():
    booking_id = sender_stand_request.post_new_booking(data.booking_body).json()["bookingid"]
    response = sender_stand_request.put_booking(booking_id, get_booking_body(firstname="Otra"))
    assert response.status_code == 403
    assert sender_stand_request.get_booking(booking_id).json()["firstname"] == "Ana"

# Prueba 5: Actualizar parcialmente (PATCH) con un token inventado es rechazado
def test_partial_update_booking_fake_token_get_error_response():
    booking_id = sender_stand_request.post_new_booking(data.booking_body).json()["bookingid"]
    response = sender_stand_request.patch_booking(booking_id, {"firstname": "Otra"}, data.fake_token)
    assert response.status_code == 403
    assert sender_stand_request.get_booking(booking_id).json()["firstname"] == "Ana"

# Prueba 6: Filtrar por nombre y apellido devuelve la reserva creada
def test_get_booking_ids_filter_by_name_get_created_booking():
    booking_body = get_booking_body(firstname="Filtro", lastname="QA" + str(random.randint(10**6, 10**7)))
    booking_id = sender_stand_request.post_new_booking(booking_body).json()["bookingid"]
    filters = {"firstname": booking_body["firstname"], "lastname": booking_body["lastname"]}
    assert sender_stand_request.get_booking_ids(filters).json() == [{"bookingid": booking_id}]

# Prueba 7: HealthCheck responde 201 Created, como dice la documentación
def test_ping_get_201_response():
    assert sender_stand_request.get_ping().status_code == 201

# Prueba 8: Con Accept application/xml la respuesta llega en XML
def test_create_booking_accept_xml_get_xml_response():
    response = sender_stand_request.post_new_booking(data.booking_body, data.headers_xml)
    assert response.status_code == 200
    assert response.text.startswith("<?xml")
    assert "<created-booking>" in response.text

# Prueba 9 (RB-01): Un precio con decimales se debe guardar completo
def test_create_booking_decimal_price_keeps_decimals():
    response = sender_stand_request.post_new_booking(get_booking_body(totalprice=150.75))
    assert response.json()["booking"]["totalprice"] == 150.75 #Failed: se guarda 150

# Prueba 10 (RB-02): Precio en texto en lugar de número
def test_create_booking_text_price_get_error_response():
    negative_assert_code_400(get_booking_body(totalprice="ciento cincuenta")) #Failed: 200 y precio null

# Prueba 11 (RB-03): Precio negativo
def test_create_booking_negative_price_get_error_response():
    negative_assert_code_400(get_booking_body(totalprice=-150)) #Failed: 200

# Prueba 12 (RB-04): Fecha de salida anterior a la de entrada
def test_create_booking_checkout_before_checkin_get_error_response():
    dates = {"checkin": "2026-12-10", "checkout": "2026-12-01"}
    negative_assert_code_400(get_booking_body(bookingdates=dates)) #Failed: 200

# Prueba 13 (RB-05): Faltan campos obligatorios
def test_create_booking_missing_fields_get_error_response():
    negative_assert_code_400({"firstname": "Ana"}) #Failed: 500

# Prueba 14 (RB-06): Credenciales incorrectas
def test_auth_bad_credentials_get_error_response():
    response = sender_stand_request.post_auth(data.bad_credentials)
    assert response.status_code == 401 #Failed: 200 con "Bad credentials"

# Prueba 15 (RB-07): Fechas que no son fechas
def test_create_booking_invalid_dates_get_error_response():
    dates = {"checkin": "no-es-fecha", "checkout": "2026-13-45"}
    negative_assert_code_400(get_booking_body(bookingdates=dates)) #Failed: 200 con "0NaN-aN-aN"

# Prueba 16 (RB-08): depositpaid debe ser Boolean
def test_create_booking_text_depositpaid_get_error_response():
    negative_assert_code_400(get_booking_body(depositpaid="tal vez")) #Failed: 200 y se guarda true

# Prueba 17 (RB-09): firstname debe ser String
def test_create_booking_number_firstname_get_error_response():
    negative_assert_code_400(get_booking_body(firstname=123)) #Failed: 500

# Prueba 18 (RB-10): firstname es obligatorio, no puede ir vacío
def test_create_booking_empty_firstname_get_error_response():
    negative_assert_code_400(get_booking_body(firstname="")) #Failed: 200
