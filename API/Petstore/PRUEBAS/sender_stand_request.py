import configuration
import requests
import data

def post_new_pet(body):
    return requests.post(configuration.URL_SERVICE + configuration.PET_PATH,
                         json=body,
                         headers=data.headers,
                         timeout=30)

def put_pet(body):
    return requests.put(configuration.URL_SERVICE + configuration.PET_PATH,
                        json=body,
                        headers=data.headers,
                        timeout=30)

def get_pet(pet_id):
    return requests.get(configuration.URL_SERVICE + configuration.PET_PATH + "/" + str(pet_id),
                        headers=data.headers,
                        timeout=30)

def delete_pet(pet_id):
    return requests.delete(configuration.URL_SERVICE + configuration.PET_PATH + "/" + str(pet_id),
                           headers=data.headers,
                           timeout=30)

def get_pets_by_status(status):
    return requests.get(configuration.URL_SERVICE + configuration.FIND_BY_STATUS_PATH,
                        params={"status": status},
                        headers=data.headers,
                        timeout=30)

def get_inventory():
    return requests.get(configuration.URL_SERVICE + configuration.INVENTORY_PATH,
                        headers=data.headers,
                        timeout=30)

def post_new_order(body):
    return requests.post(configuration.URL_SERVICE + configuration.ORDER_PATH,
                         json=body,
                         headers=data.headers,
                         timeout=30)

def get_order(order_id):
    return requests.get(configuration.URL_SERVICE + configuration.ORDER_PATH + "/" + str(order_id),
                        headers=data.headers,
                        timeout=30)

def delete_order(order_id):
    return requests.delete(configuration.URL_SERVICE + configuration.ORDER_PATH + "/" + str(order_id),
                           headers=data.headers,
                           timeout=30)

def get_user(username):
    return requests.get(configuration.URL_SERVICE + configuration.USER_PATH + "/" + username,
                        headers=data.headers,
                        timeout=30)

def get_login(credentials):
    return requests.get(configuration.URL_SERVICE + configuration.LOGIN_PATH,
                        params=credentials,
                        headers=data.headers,
                        timeout=30)
