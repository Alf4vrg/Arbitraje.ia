from core.models import Product


def obtener_productos_manual():
    return [
        Product(
            source="manual",
            title="Auriculares Bluetooth TWS gaming baja latencia",
            category="mobile-accessories",
            price=8.5,   # USD realista (barato → margen)
            currency="USD",
            rating=4.6,
            discount_percent=20.0,
            image_url="https://ae01.alicdn.com/kf/placeholder.jpg",
            product_url="https://www.aliexpress.com/wholesale?SearchText=Auriculares+Bluetooth+TWS+gaming"
        ),

        Product(
            source="manual",
            title="Mini impresora térmica portátil bluetooth",
            category="mobile-accessories",
            price=12.0,
            currency="USD",
            rating=4.7,
            discount_percent=25.0,
            image_url="https://ae01.alicdn.com/kf/placeholder.jpg",
            product_url="https://www.aliexpress.com/wholesale?SearchText=Mini+impresora+termica+bluetooth"
        ),
    ]