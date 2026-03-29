from core.models import Product
from config.settings import ALIEXPRESS_KEYWORDS


def obtener_productos_aliexpress():
    products = []

    for item in ALIEXPRESS_KEYWORDS:
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