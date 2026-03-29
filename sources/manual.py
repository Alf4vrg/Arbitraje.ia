from core.models import Product


def obtener_productos_manual():
    return [
    Product(
        source="manual",
        title="Auriculares Bluetooth TWS gaming baja latencia",
        category="mobile-accessories",
        price=8.5,
        currency="USD",
        rating=4.6,
        discount_percent=20.0,
        image_url="https://ae01.alicdn.com/kf/placeholder.jpg",
        product_url="https://www.aliexpress.com/wholesale?SearchText=Auriculares+Bluetooth+TWS+gaming+baja+latencia",
    ),
    Product(
        source="manual",
        title="Mini impresora térmica portátil bluetooth",
        category="mobile-accessories",
        price=12.0,
        currency="USD",
        rating=4.7,
        discount_percent=25.0,
        image_url="https://ae01.alicdn.com/kf/placeholder2.jpg",
        product_url="https://www.aliexpress.com/wholesale?SearchText=Mini+impresora+termica+portatil+bluetooth",
    ),
    Product(
        source="manual",
        title="Smartwatch deportivo AMOLED resistente agua",
        category="mobile-accessories",
        price=18.0,
        currency="USD",
        rating=4.5,
        discount_percent=18.0,
        image_url="https://ae01.alicdn.com/kf/placeholder3.jpg",
        product_url="https://www.aliexpress.com/wholesale?SearchText=Smartwatch+deportivo+AMOLED+resistente+agua",
    ),
]