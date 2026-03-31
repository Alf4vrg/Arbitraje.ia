import re
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def clean_price(text: str) -> float | None:
    if not text:
        return None

    text = text.replace("$", "").replace("MXN", "").replace(",", "").strip()

    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None


def search_mercadolibre_prices(query: str) -> dict:
    """
    Búsqueda básica en Mercado Libre México.
    Devuelve min, max, avg, competition y debug.
    """
    url_query = query.strip().replace(" ", "-")
    url = f"https://listado.mercadolibre.com.mx/{url_query}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
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

    soup = BeautifulSoup(response.text, "html.parser")

    prices = []

    selectors = [
        "span.andes-money-amount__fraction",
        "span.poly-price__current span.andes-money-amount__fraction",
        "div.poly-price__current span.andes-money-amount__fraction",
        "div.ui-search-price__second-line span.andes-money-amount__fraction",
        "span.price-tag-fraction",
    ]

    found_texts = []
    for selector in selectors:
        elements = soup.select(selector)
        for el in elements:
            txt = el.get_text(strip=True)
            if txt:
                found_texts = found_texts[:30]

    for txt in found_texts:
        price = clean_price(txt)
        if price and price > 0:
            prices.append(price)

    prices = prices[:20]

    if not prices:
        with open("ml_debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        return {
            "min_price": 0,
            "max_price": 0,
            "avg_price": 0,
            "competition": 0,
            "source": "mercadolibre_no_prices",
            "debug": f"no prices found, html length={len(response.text)}, sample_texts={found_texts[:10]}",
            "url": url,
        }

    return {
        "min_price": min(prices),
        "max_price": max(prices),
        "avg_price": round(sum(prices) / len(prices), 2),
        "competition": len(prices),
        "source": "mercadolibre_scraper",
        "debug": f"found {len(prices)} prices",
        "url": url,
    }