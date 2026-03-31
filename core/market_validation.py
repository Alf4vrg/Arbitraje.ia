from sources.mercadolibre import search_mercadolibre_prices

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

    # 1. intentar Mercado Libre real
    real_market = search_mercadolibre_prices(title)
    if real_market["avg_price"] > 0:
        real_market["source"] = "mercadolibre_scraper"
        return real_market

    # 2. coincidencia exacta manual
    if title in MARKET_REFERENCE:
        data = MARKET_REFERENCE[title].copy()
        data["source"] = "manual_reference_exact"
        return data

    # 3. coincidencia parcial manual
    for key, data in MARKET_REFERENCE.items():
        if key in title or title in key:
            result = data.copy()
            result["source"] = "manual_reference_partial"
            return result

    # 4. sin datos
    return {
        "min_price": 0,
        "max_price": 0,
        "avg_price": 0,
        "competition": 0,
        "source": "no_data",
    }