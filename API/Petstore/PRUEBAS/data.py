import random

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Estados permitidos por la especificación (definitions.Pet.status y definitions.Order.status)
pet_status_validos = {"available", "pending", "sold"}
order_status_validos = {"placed", "approved", "delivered"}

#Pet - Mascota válida: name y photoUrls son obligatorios según la especificación
pet_body = {
    "name": "Firulais",
    "photoUrls": ["https://example.com/firulais.jpg"],
    "tags": [],
    "status": "available"
}

#Store - Pedido válido
order_body = {
    "petId": 1,
    "quantity": 1,
    "shipDate": "2026-12-01T10:00:00.000+0000",
    "status": "placed",
    "complete": False
}

#User - Credenciales que no existen en el sistema
bad_login = {
    "username": "usuario_que_no_existe_qa",
    "password": "clave_incorrecta"
}


# Id único por prueba para no chocar con los datos de otros usuarios de la API pública
def new_id():
    return random.randint(10**9, 2 * 10**9)
