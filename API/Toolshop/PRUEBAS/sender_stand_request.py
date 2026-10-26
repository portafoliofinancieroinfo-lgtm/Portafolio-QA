import configuration
import requests
import data

def get_products(params=None, base=configuration.URL_SERVICE):
    return requests.get(base + configuration.PRODUCTS_PATH,
                        params=params,
                        headers=data.headers,
                        timeout=30)

def get_product(product_id):
    return requests.get(configuration.URL_SERVICE + configuration.PRODUCTS_PATH + "/" + str(product_id),
                        headers=data.headers,
                        timeout=30)

def get_products_search(params, base=configuration.URL_SERVICE):
    return requests.get(base + configuration.PRODUCTS_SEARCH_PATH,
                        params=params,
                        headers=data.headers,
                        timeout=30)

def get_invoices(base=configuration.URL_SERVICE):
    return requests.get(base + configuration.INVOICES_PATH,
                        headers=data.headers,
                        timeout=30)

# Petición sin token a cualquier ruta
def get_path(path, base=configuration.URL_SERVICE):
    return requests.get(base + path,
                        headers=data.headers,
                        timeout=30)

def post_login(credentials):
    return requests.post(configuration.URL_SERVICE + configuration.LOGIN_PATH,
                         json=credentials,
                         headers=data.headers,
                         timeout=30)

# Descarga la especificación OpenAPI oficial de la API
def get_spec():
    return requests.get(configuration.URL_SERVICE + configuration.SPEC_PATH,
                        headers=data.headers,
                        timeout=30).json()
