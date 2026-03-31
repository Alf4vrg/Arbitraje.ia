import requests


def search_mercadolibre_prices(query: str) -> dict:
    url = f"https://api.mercadolibre.com/sites/MLM/search?q={query}"

    try:
        response = requests.get(url, timeout=15)
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
                "url": url,
            }

        return {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": round(sum(prices) / len(prices), 2),
            "competition": len(prices),
            "source": "mercadolibre_api",
            "debug": f"{len(prices)} prices",
            "url": url,
        }

    except Exception as e:
        return {
            "min_price": 0,
            "max_price": 0,
            "avg_price": 0,
            "competition": 0,
            "source": "mercadolibre_error",
            "debug": str(e),
            "url": url,
        }