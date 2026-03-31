MARKET_REFERENCE = {
    "kz edx pro": {
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
    "mini impresora termica": {
        "min_price": 120,
        "max_price": 180,
        "avg_price": 150,
        "competition": 6,
    },
    "smartwatch deportivos": {
        "min_price": 190,
        "max_price": 300,
        "avg_price": 245,
        "competition": 4,
    },
    "sensor de posicion del cigüeñal nissan": {
        "min_price": 197,
        "max_price": 399,
        "avg_price": 315,
        "competition": 3,
    },
    "probador de relé automotriz": {
        "min_price": 111,
        "max_price": 388,
        "avg_price": 224,
        "competition": 10,
    },
}


def normalize_text(text: str) -> str:
    return text.strip().lower()


def estimate_market_price(product_title: str):
    title = normalize_text(product_title)

    # 1. coincidencia exacta
    if title in MARKET_REFERENCE:
        return MARKET_REFERENCE[title]

    # 2. coincidencia parcial
    for key, data in MARKET_REFERENCE.items():
        if key in title or title in key:
            return data

    # 3. sin datos
    return {
        "min_price": 0,
        "max_price": 0,
        "avg_price": 0,
        "competition": 0,
    }