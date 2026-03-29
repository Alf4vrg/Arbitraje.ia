from core.models import Product


def obtener_productos_aliexpress():
    return [
        Product(
            source="aliexpress",
            title="Auriculares Bluetooth TWS",
            category="mobile-accessories",
            price=12.5,
            currency="USD",
            rating=4.7,
            discount_percent=18.0,
            image_url="https://example.com/image1.jpg",
            
        product_url=f"https://www.aliexpress.com/wholesale?SearchText={'Auriculares+Bluetooth+TWS'}"
        ),
        Product(
            source="aliexpress",
            title="Smartphone Android 8GB 256GB",
            category="smartphones",
            price=145.0,
            currency="USD",
            rating=4.5,
            discount_percent=12.0,
            image_url="https://example.com/image2.jpg",
            
        product_url=f"https://www.aliexpress.com/wholesale?SearchText={'Smartphone+Android+8GB+256GB'}"
        ),
    ]