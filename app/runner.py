from config.settings import ESTIMATED_SALE_MULTIPLIER, USD_TO_MXN
from core.filters import is_valid_category, passes_minimum_margin
from core.scoring import (
    calculate_buy_index,
    calculate_demand_score,
    calculate_estimated_sale_price,
    calculate_margin,
    calculate_profit,
    initial_decision,
)
from sources.dummyjson_source import DummyJsonSource


def run_pipeline():
    from sources.aliexpress import obtener_productos_aliexpress

    products = obtener_productos_aliexpress(category_filter="smartphones")

    candidates = []

    for product in products:
        if not is_valid_category(product.category):
            continue

        price_buy_mxn = round(product.price * USD_TO_MXN, 2)
        discount_fraction = product.discount_percent / 100 if product.discount_percent > 0 else 0

        product.price = price_buy_mxn
        product.currency = "MXN"
        product.base_price = round(product.price / (1 - discount_fraction), 2) if 0 < discount_fraction < 1 else product.price
        product.estimated_sale_price = round(calculate_estimated_sale_price(product.price, ESTIMATED_SALE_MULTIPLIER), 2)
        product.estimated_profit = round(calculate_profit(product.price, product.estimated_sale_price), 2)
        product.estimated_margin = calculate_margin(product.price, product.estimated_sale_price)
        product.demand_score = calculate_demand_score(product.rating)
        product.buy_index = calculate_buy_index(product.estimated_margin, product.discount_percent, product.rating)
        product.initial_decision = initial_decision(
            product.estimated_margin,
            product.rating,
            product.price,
            product.discount_percent,
        )

        if not passes_minimum_margin(product.estimated_margin):
            continue

        candidates.append(product)

    candidates.sort(key=lambda x: x.buy_index, reverse=True)

    print(f"\nCandidatos: {len(candidates)}\n")

    for product in candidates:
        print(f"""
    📦 {product.title}
    💰 Compra: {round(product.price, 2)} MXN
    💸 Venta estimada: {round(product.estimated_sale_price, 2)} MXN
    📊 Margen: {round(product.estimated_margin, 2)}%
    🔥 Demanda: {round(product.demand_score, 2)}
    🧠 Índice: {round(product.buy_index, 2)}
    🎯 Decisión: {product.initial_decision}
    🔗 Link: {getattr(product, 'product_url', 'N/A')}
    🖼 Imagen: {getattr(product, 'image_url', 'N/A')}
    --------------------------
    """)
    return candidates