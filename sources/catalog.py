from core.models import Product


CATALOG = {
    "audio": [
        Product(
            source="catalog",
            title="Audifonos KZ EDX PRO IEMcableados",
            category="mobile-accessories",
            price=86.59,
            currency="MXN",
            rating=4.9,
            discount_percent=0.0,
            image_url="https://ae01.alicdn.com/kf/placeholder2.jpg",
            product_url="https://www.aliexpress.com/ssr/300000512/BundleDeals2",
        ),
        Product(
            source="catalog",
            title="audifonos bluetooth gaming",
            category="mobile-accessories",
            price=273.26,
            currency="MXN",
            rating=4.9,
            discount_percent=0.0,
            image_url="https://ae01.alicdn.com/kf/placeholder2.jpg",
            product_url="https://es.aliexpress.com/item/1005010653195874.html",
        ),
    ],
    "herramientas": [
        Product(
            source="catalog",
            title="Mini impresora térmica HPRT bluetooth MT53",
            category="mobile-accessories",
            price=152.63,
            currency="MXN",
            rating=3.9,
            discount_percent=0.0,
            image_url="https://ae01.alicdn.com/kf/placeholder2.jpg",
            product_url="https://es.aliexpress.com/item/1005011595270902.html",
        ),
        Product(
            source="catalog",
            title="Herramienta de roscado de tuberías",
            category="tools",
            price=60.00,
            currency="MXN",
            rating=4.7,
            discount_percent=0.0,
            image_url="https://ae01.alicdn.com/kf/placeholder-tools.jpg",
            product_url="https://es.aliexpress.com/item/1005010141362315.html",
        ),
    ],
    "auto": [
        Product(
            source="catalog",
            title="Sensor de posicion del cigüeñal Nissan",
            category="auto-accessories",
            price=210.36,
            currency="MXN",
            rating=4.7,
            discount_percent=0.0,
            image_url="https://ae01.alicdn.com/kf/placeholder-sensor.jpg",
            product_url="https://es.aliexpress.com/item/1005008641253338.html",
        ),
        Product(
            source="catalog",
            title="Probador de relé automotriz 12V",
            category="auto-accessories",
            price=136.59,
            currency="MXN",
            rating=4.9,
            discount_percent=0.0,
            image_url="https://ae01.alicdn.com/kf/placeholder-relay.jpg",
            product_url="https://es.aliexpress.com/ssr/300000512/BundleDeals2",
        ),
    ],
}


def get_products_by_keyword(keyword: str):
    keyword = keyword.strip().lower()

    results = []

    for group_name, products in CATALOG.items():
        if keyword in group_name:
            results.extend(products)
            continue

        for product in products:
            title = product.title.lower()
            category = product.category.lower()

            if keyword in title or keyword in category:
                results.append(product)

    return results