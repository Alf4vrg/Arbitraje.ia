from core.models import Product
from config.settings import KEYWORDS


def obtener_productos_aliexpress():
    products = []

    for keyword in KEYWORDS:
        query = keyword.replace(" ", "+")

        products.append(
            Product(
                source="aliexpress",
                title=keyword,
                category="smartphones",
                price=150.0,
                currency="USD",
                rating=4.5,
                discount_percent=10.0,
                image_url="https://via.placeholder.com/150",
                product_url=f"https://www.aliexpress.com/wholesale?SearchText={query}",
            )
        )

    return products