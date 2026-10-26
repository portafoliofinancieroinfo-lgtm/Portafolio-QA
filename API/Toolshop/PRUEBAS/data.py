headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

#Products - Campos del contrato ProductResponse (components.schemas.ProductResponse)
product_fields = {"id", "name", "description", "price", "is_location_offer", "is_rental",
                  "co2_rating", "is_eco_friendly", "brand", "category", "product_image"}

#Rutas que la documentación marca con seguridad (apiAuth) y responden 401 sin token
protected_paths = [
    "/users",
    "/users/me",
    "/favorites",
    "/messages",
    "/invoices/search?q=a",
]

#Reports - Reportes de ventas del administrador, todos con seguridad en la documentación
report_paths = [
    "/reports/total-sales-per-country",
    "/reports/top10-purchased-products",
    "/reports/top10-best-selling-categories",
    "/reports/total-sales-of-years",
    "/reports/average-sales-per-month",
    "/reports/average-sales-per-week",
    "/reports/customers-by-country",
]

#Users - Login con una cuenta que no existe
bad_login = {
    "email": "noexiste@example.com",
    "password": "Incorrecta123!"
}

# Id de producto que no existe
product_id_not_found = 99999999
