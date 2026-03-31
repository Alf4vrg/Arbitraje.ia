import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
}


def search_mercadolibre_prices(query: str) -> dict:
    url = "https://api.mercadolibre.com/sites/MLM/search"

    try:
        response = requests.get(
            url,
            params={"q": query},
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])[:20]
        prices = [item["price"] for item in results if "price" in item and item["price"]]

        if not prices:
            return {
                "min_price": 0,
                "max_price": 0,
                "avg_price": 0,
                "competition": 0,
                "source": "mercadolibre_api_no_prices",
                "debug": "no prices from API",
                "url": response.url,
            }

        return {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": round(sum(prices) / len(prices), 2),
            "competition": len(prices),
            "source": "mercadolibre_api",
            "debug": f"{len(prices)} prices",
            "url": response.url,
        }

    except Exception as e:
        return {
            "min_price": 0,
            "max_price": 0,
            "avg_price": 0,
            "competition": 0,
            "source": "mercadolibre_error",
            "debug": str(e),
            "url": f"{url}?q={query}",
        }