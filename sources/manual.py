from core.models import Product


def obtener_links_manual():
    return [
        "https://www.aliexpress.com/wholesale?SearchText=Samsung+Galaxy+A51",
        "https://www.aliexpress.com/wholesale?SearchText=iPhone+11+128GB",
    ]

def construir_productos_desde_links(links):
    products = []

    for link in links:
        products.append(
            Product(
                source="manual",
                title="Producto desde link",
                category="smartphones",
                price=150.0,
                currency="USD",
                rating=4.5,
                discount_percent=10.0,
                image_url="https://via.placeholder.com/150",
                product_url=link,
            )
        )

    return products