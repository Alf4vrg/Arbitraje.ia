from core.models import Product


def obtener_productos_manual():
    return [
        Product(
            source="manual",
            title="iPhone 11 128GB",
            category="smartphones",
            price=213.82,  # USD aprox si lo quieres seguir manejando así
            currency="USD",
            rating=4.8,
            discount_percent=0.0,
            image_url="https://ae01.alicdn.com/kf/placeholder.jpg",
            product_url="https://www.aliexpress.com/wholesale?SearchText=iPhone+11+128GB",
        ),
        Product(
            source="manual",
            title="Samsung Galaxy A51",
            category="smartphones",
            price=208.82,
            currency="USD",
            rating=4.6,
            discount_percent=0.0,
            image_url="https://ae01.alicdn.com/kf/placeholder2.jpg",
            product_url="https://www.aliexpress.com/wholesale?SearchText=Samsung+Galaxy+A51",
        ),
    ]