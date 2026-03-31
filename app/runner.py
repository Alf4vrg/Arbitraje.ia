from config.settings import ESTIMATED_SALE_MULTIPLIER, USD_TO_MXN
from core.filters import is_valid_category, passes_minimum_margin
from core.scoring import (
    calculate_buy_index,
    calculate_demand_score,
    calculate_estimated_sale_price,
    calculate_margin,
    calculate_profit,
    final_decision,
)
from sources.catalog import get_products_by_keyword
from sources.aliexpress import search_aliexpress_products
from core.market_validation import estimate_market_price, simplify_title_for_market

def run_pipeline(keyword: str = "auto", source_name: str = "catalog"):
    if source_name == "aliexpress":
        products = search_aliexpress_products(keyword)
    else:
        products = get_products_by_keyword(keyword)

    candidates = []

    for product in products:
        if not is_valid_category(product.category):
            continue

        if product.currency == "USD":
            price_buy_mxn = round(product.price * USD_TO_MXN, 2)
        elif product.currency == "MXN":
            price_buy_mxn = round(product.price, 2)
        else:
            continue

        discount_fraction = product.discount_percent / 100 if product.discount_percent > 0 else 0

        product.price = price_buy_mxn
        product.currency = "MXN"

        product.base_price = round(
            product.price / (1 - discount_fraction), 2
        ) if 0 < discount_fraction < 1 else product.price

        if product.rating >= 4.7:
            multiplier = 2.5
        else:
            multiplier = 1.8

        market_data = estimate_market_price(product.title)

        product.market_min_price = market_data["min_price"]
        product.market_max_price = market_data["max_price"]
        product.market_avg_price = market_data["avg_price"]
        product.market_competition = market_data["competition"]
        product.market_source = market_data["source"]
        product.market_debug = market_data.get("debug", "")
        product.market_url = market_data.get("url", "")
        product.market_query = simplify_title_for_market(product.title)


        raw_sale_price = calculate_estimated_sale_price(product.price, multiplier)

        # Ajuste con mercado real
        if product.market_avg_price > 0:
            product.estimated_sale_price = round(
                min(raw_sale_price, product.market_avg_price * 0.95), 2
            )
        else:
            product.estimated_sale_price = round(raw_sale_price, 2)

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

        product.initial_decision = final_decision(
            product.estimated_margin,
            product.market_competition,
            product.market_avg_price,
        )


        if not passes_minimum_margin(product.estimated_margin):
            continue

        candidates.append(product)

    candidates.sort(key=lambda x: x.buy_index, reverse=True)

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
        print("🛒 Mercado MX:", product.market_min_price, "-", product.market_max_price)
        print("📈 Promedio MX:", round(product.market_avg_price, 2))
        print("📊 Competencia:", product.market_competition)
        print("🧭 Fuente mercado:", product.market_source)
        print("🛠 Debug mercado:", product.market_debug)
        print("🔗 URL mercado:", product.market_url)
        print("🔎 Query mercado:", product.market_query)

    return candidates