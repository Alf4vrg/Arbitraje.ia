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

# 👇 IMPORTAMOS NUEVO SISTEMA DE LINKS
from sources.manual import obtener_links_manual, construir_productos_desde_links


def run_pipeline():
    # 🔹 1. Obtener links manuales
    links = obtener_links_manual()

    # 🔹 2. Convertir links → productos
    products = construir_productos_desde_links(links)

    candidates = []

    for product in products:
        if not is_valid_category(product.category):
            continue

        # 💱 Conversión a MXN
        price_buy_mxn = round(product.price * USD_TO_MXN, 2)
        discount_fraction = product.discount_percent / 100 if product.discount_percent > 0 else 0

        product.price = price_buy_mxn
        product.currency = "MXN"

        # 📊 Cálculos
        product.base_price = round(
            product.price / (1 - discount_fraction), 2
        ) if 0 < discount_fraction < 1 else product.price

        product.estimated_sale_price = round(
            calculate_estimated_sale_price(product.price, ESTIMATED_SALE_MULTIPLIER), 2
        )

        product.estimated_profit = round(
            calculate_profit(product.price, product.estimated_sale_price), 2
        )

        product.estimated_margin = calculate_margin(
            product.price, product.estimated_sale_price
        )

        product.demand_score = calculate_demand_score(product.rating)

        product.buy_index = calculate_buy_index(
            product.estimated_margin,
            product.discount_percent,
            product.rating,
        )

        product.initial_decision = initial_decision(
            product.estimated_margin,
            product.rating,
            product.price,
            product.discount_percent,
        )

        # 🔥 filtro final
        if not passes_minimum_margin(product.estimated_margin):
            continue

        candidates.append(product)

    # 📊 ordenar por mejor oportunidad
    candidates.sort(key=lambda x: x.buy_index, reverse=True)

    # 🖨️ salida
    print(f"Candidatos: {len(candidates)}")

    for product in candidates:
        print("\n📦", product.title)
        print("💰 Compra:", product.price, "MXN")
        print("📈 Venta estimada:", product.estimated_sale_price, "MXN")
        print("📊 Margen:", round(product.estimated_margin, 2), "%")
        print("🔥 Demanda:", product.demand_score)
        print("🧠 Índice:", round(product.buy_index, 2))
        print("🎯 Decisión:", product.initial_decision)
        print("🔗 Link:", product.product_url)
        print("🖼 Imagen:", product.image_url)
        print("-" * 30)

    return candidates