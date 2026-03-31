def calculate_estimated_sale_price(price_buy: float, multiplier: float = 1.8) -> float:
    return price_buy * multiplier


def calculate_profit(price_buy: float, sale_price: float) -> float:
    return sale_price - price_buy


def calculate_margin(price_buy: float, sale_price: float) -> float:
    if price_buy <= 0:
        return 0.0
    return round((sale_price - price_buy) / price_buy * 100, 2)


def calculate_demand_score(rating: float) -> float:
    return round(rating * 20, 2)


def calculate_buy_index(margin: float, discount: float, rating: float) -> float:
    return round(margin * 0.4 + discount * 0.3 + (rating * 10) * 0.3, 2)

def initial_decision(margin: float, rating: float, price_buy: float, discount: float) -> str:
    if (
        (margin >= 35 and rating >= 4.4 and price_buy <= 12000 and discount >= 8)
        or
        (margin >= 80 and rating >= 4.7 and price_buy <= 500)
    ):
        return "🔥 OPORTUNIDAD"

    if margin >= 20 and rating >= 4.0 and price_buy <= 18000:
        return "⚠️ MEDIA"

    return "❌ DESCARTAR"




def final_decision(estimated_margin: float, market_competition: int, market_avg_price: float) -> str:
    if market_avg_price == 0:
        return "❌ DESCARTAR"

    if market_competition <= 4 and estimated_margin >= 80:
        return "🔥 OPORTUNIDAD"

    if market_competition >= 8 and estimated_margin < 80:
        return "⚠️ MEDIA"

    if estimated_margin >= 50:
        return "⚠️ MEDIA"

    return "❌ DESCARTAR"