MARKET_REFERENCE = {
    "Audifonos KZ EDX PRO IEMcableados": {
        "min_price": 140,
        "max_price": 180,
        "avg_price": 155,
        "competition": 9,
    },
    "audifonos bluetooth gaming": {
        "min_price": 190,
        "max_price": 300,
        "avg_price": 240,
        "competition": 8,
    },
    "Mini impresora térmica HPRT bluetooth MT53": {
        "min_price": 120,
        "max_price": 180,
        "avg_price": 150,
        "competition": 6,
    },
    "smartwach deportivos": {
        "min_price": 190,
        "max_price": 300,
        "avg_price": 245,
        "competition": 4,
    },
}


def estimate_market_price(product_title: str):
    data = MARKET_REFERENCE.get(product_title)

    if data:
        return data

    return {
        "min_price": 0,
        "max_price": 0,
        "avg_price": 0,
        "competition": 0,
    }