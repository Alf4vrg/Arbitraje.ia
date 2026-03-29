from core.models import Product


def obtener_productos_aliexpress():
    seeds = [
        {
            "title": "Auriculares Bluetooth TWS",
            "category": "mobile-accessories",
            "price": 12.5,
            "rating": 4.7,
            "discount_percent": 18.0,
        },
        {
            "title": "Smartphone Android 8GB 256GB",
            "category": "smartphones",
            "price": 145.0,
            "rating": 4.5,
            "discount_percent": 12.0,
        },
        {
            "title": "Smartwatch AMOLED",
            "category": "mobile-accessories",
            "price": 35.0,
            "rating": 4.6,
            "discount_percent": 15.0,
        },
    ]

    products = []

    for item in seeds:
        query = item["title"].replace(" ", "+")
        products.append(
            Product(
                source="aliexpress",
                title=item["title"],
                category=item["category"],
                price=item["price"],
                currency="USD",
                rating=item["rating"],
                discount_percent=item["discount_percent"],
                image_url="https://via.placeholder.com/150",
                product_url=f"https://www.aliexpress.com/wholesale?SearchText={query}",
            )
        )

    return products