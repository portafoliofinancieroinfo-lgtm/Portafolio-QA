#Headers que pide la documentación: Content-Type y Accept
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

headers_xml = {
    "Content-Type": "application/json",
    "Accept": "application/xml"
}

#Booking - CreateBooking: todos los campos son obligatorios según la documentación
booking_body = {
    "firstname": "Ana",
    "lastname": "Prueba",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-12-01",
        "checkout": "2026-12-05"
    },
    "additionalneeds": "Desayuno"
}

#Auth - CreateToken con credenciales que no existen
bad_credentials = {
    "username": "noexiste",
    "password": "incorrecta"
}

# Token inventado para probar que no da acceso
fake_token = "abc123"

# Id de reserva que no existe
booking_id_not_found = 999999999
