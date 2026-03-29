from core.models import Product


def obtener_productos_manual():
    return [
        Product(
            source="manual",
            title="iPhone 11 128GB",
            category="smartphones",
            price=180.0,
            currency="USD",
            rating=4.6,
            discount_percent=5.0,
            image_url="https://via.placeholder.com/150",
            product_url="https://www.aliexpress.com/item/example1",
        ),
        Product(
            source="manual",
            title="Samsung Galaxy A51",
            category="smartphones",
            price=150.0,
            currency="USD",
            rating=4.5,
            discount_percent=8.0,
            image_url="https://via.placeholder.com/150",
            product_url="https://www.aliexpress.com/item/example2",
        ),
    ]