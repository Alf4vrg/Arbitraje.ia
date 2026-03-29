from core.models import Product


CATEGORY_SEEDS = {
    "smartphones": [
        {"title": "Smartphone Android 8GB 256GB", "price": 145.0, "rating": 4.5, "discount_percent": 12.0},
        {"title": "Smartphone 5G 12GB 512GB", "price": 220.0, "rating": 4.6, "discount_percent": 10.0},
    ],
    "mobile-accessories": [
        {"title": "Auriculares Bluetooth TWS", "price": 12.5, "rating": 4.7, "discount_percent": 18.0},
        {"title": "Smartwatch AMOLED", "price": 35.0, "rating": 4.6, "discount_percent": 15.0},
        {"title": "Cargador USB-C 65W", "price": 14.0, "rating": 4.5, "discount_percent": 20.0},
    ],
}


def obtener_productos_aliexpress():
    products = []

    for category, items in CATEGORY_SEEDS.items():
        for item in items:
            query = item["title"].replace(" ", "+")
            products.append(
                Product(
                    source="aliexpress",
                    title=item["title"],
                    category=category,
                    price=item["price"],
                    currency="USD",
                    rating=item["rating"],
                    discount_percent=item["discount_percent"],
                    image_url="https://via.placeholder.com/150",
                    product_url=f"https://www.aliexpress.com/wholesale?SearchText={query}",
                )
            )

    return products