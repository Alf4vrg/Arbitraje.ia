import random


def estimate_market_price(product_title: str):
    """
    Simula búsqueda en mercado mexicano (después lo conectamos real)
    """

    # ⚠️ por ahora es simulado pero estructurado para lo real
    base_prices = [
        120, 150, 180, 220, 250, 300, 350
    ]

    sampled = random.sample(base_prices, k=3)

    min_price = min(sampled)
    max_price = max(sampled)

    return {
        "min_price": min_price,
        "max_price": max_price,
        "avg_price": sum(sampled) / len(sampled),
        "competition": random.randint(3, 12)
    }