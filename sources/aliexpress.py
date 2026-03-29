from core.models import Product
from config.settings import ALIEXPRESS_CATEGORY_SEEDS


def obtener_productos_aliexpress():
    products = []


    from config.settings import ALIEXPRESS_CATEGORY_SEEDS, ACTIVE_CATEGORIES

    for category, items in ALIEXPRESS_CATEGORY_SEEDS.items():
        if category not in ACTIVE_CATEGORIES:
            continue
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