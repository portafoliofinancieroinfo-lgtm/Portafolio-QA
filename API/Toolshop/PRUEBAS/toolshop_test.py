import configuration
import data
import sender_stand_request

# El resultado esperado sale de la documentación oficial (documentacion_toolshop.html)
# y de la versión sin bugs de la misma API. Las pruebas que fallan son bugs: ver Toolshop.md.
# No se inicia sesión y no se imprimen datos de clientes: solo se revisan códigos y campos.

# Funcion que devuelve los precios de la primera página de productos
def get_prices(params):
    return [product["price"] for product in sender_stand_request.get_products(params).json()["data"]]

# Funcion para las rutas protegidas: sin token deben responder 401
def assert_requires_login(paths):
    open_paths = [path for path in paths if sender_stand_request.get_path(path).status_code != 401]
    assert open_paths == []

#Pruebas
# Prueba 1: Ordenar por precio ascendente
def test_products_sort_price_asc_get_sorted_prices():
    prices = get_prices({"sort": "price,asc"})
    assert prices == sorted(prices)

# Prueba 2: Ordenar por nombre descendente
def test_products_sort_name_desc_get_sorted_names():
    names = [product["name"] for product in sender_stand_request.get_products({"sort": "name,desc"}).json()["data"]]
    assert names == sorted(names, reverse=True)

# Prueba 3: Recorrer todas las páginas trae cada producto una vez y el total cuadra
def test_products_pagination_get_every_product_once():
    first_page = sender_stand_request.get_products({"page": 1}).json()
    ids = [product["id"]
           for page in range(1, first_page["last_page"] + 1)
           for product in sender_stand_request.get_products({"page": page}).json()["data"]]
    assert len(ids) == len(set(ids)) == first_page["total"]

# Prueba 4: Filtrar por precio entre 10 y 20
def test_products_between_price_get_prices_in_range():
    prices = get_prices({"between": "price,10,20"})
    assert prices and all(10 <= price <= 20 for price in prices)

# Prueba 5: Consultar un producto existente
def test_get_product_existing_get_success_response():
    product_id = sender_stand_request.get_products().json()["data"][0]["id"]
    response = sender_stand_request.get_product(product_id)
    assert response.status_code == 200
    assert response.json()["id"] == product_id

# Prueba 6: Consultar un producto que no existe responde 404
def test_get_product_not_found_get_404_response():
    response = sender_stand_request.get_product(data.product_id_not_found)
    assert response.status_code == 404
    assert response.json()["message"] == "Requested item not found"

# Prueba 7: La búsqueda se hace sobre el nombre del producto
def test_products_search_hammer_get_only_matching_names():
    products = sender_stand_request.get_products_search({"q": "hammer"}).json()["data"]
    assert products and all("hammer" in product["name"].lower() for product in products)

# Prueba 8: Las rutas protegidas exigen login
def test_protected_paths_without_token_get_401_response():
    assert_requires_login(data.protected_paths)

# Prueba 9: Login con una cuenta que no existe responde 401
def test_login_bad_credentials_get_401_response():
    assert sender_stand_request.post_login(data.bad_login).status_code == 401

# Prueba 10: En la versión de referencia las facturas exigen login
def test_reference_invoices_without_token_get_401_response():
    assert sender_stand_request.get_invoices(configuration.URL_REFERENCE).status_code == 401

# Prueba 11 (TS-01): Las facturas exigen login
def test_invoices_without_token_get_401_response():
    assert sender_stand_request.get_invoices().status_code == 401 #Failed: 200 con las facturas

# Prueba 12 (TS-02): Ordenar por un campo que no existe no debe romper el servidor
def test_products_sort_invalid_field_get_no_server_error():
    assert sender_stand_request.get_products({"sort": "precio,asc"}).status_code < 500 #Failed: 500

# Prueba 13 (TS-03): Buscar "%" no debe devolver todo el catálogo
def test_products_search_percent_get_no_results():
    assert sender_stand_request.get_products_search({"q": "%"}).json()["total"] == 0 #Failed: todo el catálogo

# Prueba 14 (TS-04): Un producto solo trae los campos del contrato ProductResponse
def test_product_fields_match_contract():
    product = sender_stand_request.get_products().json()["data"][0]
    assert set(product) <= data.product_fields #Failed: stock, brand_id...

# Prueba 15 (TS-05): Los reportes de ventas exigen login
def test_reports_without_token_get_401_response():
    assert_requires_login(data.report_paths) #Failed: los 7 reportes responden 200

# Prueba 16 (TS-06): Buscar sin el parámetro obligatorio q no debe devolver todo el catálogo
def test_products_search_without_query_get_no_results():
    assert sender_stand_request.get_products_search({}).json()["total"] == 0 #Failed: todo el catálogo

# Prueba 17 (TS-07): La documentación de GET /products/{productId} debe describir un producto
def test_spec_get_product_response_is_product_schema():
    spec = sender_stand_request.get_spec()
    response_200 = spec["paths"]["/products/{productId}"]["get"]["responses"]["200"]
    schema = response_200["content"]["application/json"]["schema"]["$ref"]
    assert schema == "#/components/schemas/ProductResponse" #Failed: documenta BrandResponse
