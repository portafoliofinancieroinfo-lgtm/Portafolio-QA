import configuration
import requests
import data

def post_new_booking(body, headers=data.headers):
    return requests.post(configuration.URL_SERVICE + configuration.BOOKING_PATH,
                         json=body,
                         headers=headers,
                         timeout=30)

def get_booking(booking_id):
    return requests.get(configuration.URL_SERVICE + configuration.BOOKING_PATH + "/" + str(booking_id),
                        headers=data.headers,
                        timeout=30)

def get_booking_ids(filters):
    return requests.get(configuration.URL_SERVICE + configuration.BOOKING_PATH,
                        params=filters,
                        headers=data.headers,
                        timeout=30)

def put_booking(booking_id, body, token=None):
    return requests.put(configuration.URL_SERVICE + configuration.BOOKING_PATH + "/" + str(booking_id),
                        json=body,
                        headers=headers_with_token(token),
                        timeout=30)

def patch_booking(booking_id, body, token=None):
    return requests.patch(configuration.URL_SERVICE + configuration.BOOKING_PATH + "/" + str(booking_id),
                          json=body,
                          headers=headers_with_token(token),
                          timeout=30)

def delete_booking(booking_id, token=None):
    return requests.delete(configuration.URL_SERVICE + configuration.BOOKING_PATH + "/" + str(booking_id),
                           headers=headers_with_token(token),
                           timeout=30)

def post_auth(credentials):
    return requests.post(configuration.URL_SERVICE + configuration.AUTH_PATH,
                         json=credentials,
                         headers=data.headers,
                         timeout=30)

def get_ping():
    return requests.get(configuration.URL_SERVICE + configuration.PING_PATH, timeout=30)

# La documentación envía el token en la cookie "token"
def headers_with_token(token):
    header_token = data.headers.copy()
    if token:
        header_token["Cookie"] = "token=" + token
    return header_token
