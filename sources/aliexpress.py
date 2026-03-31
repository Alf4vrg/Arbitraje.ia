import re
from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup

from core.models import Product


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def clean_price(text: str) -> float | None:
    if not text:
        return None

    text = text.replace(",", "").strip()

    # busca algo tipo 12.34 o 1234
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    if not match:
        return None

    try:
        return float(match.group(1))
    except ValueError:
        return None


def infer_category(title: str, keyword: str) -> str:
    text = f"{title} {keyword}".lower()

    if any(x in text for x in ["sensor", "relay", "automotive", "car", "auto", "cigüeñal"]):
        return "auto-accessories"
    if any(x in text for x in ["tool", "herramienta", "drill", "repair", "kit"]):
        return "tools"
    if any(x in text for x in ["headphone", "earphone", "audifono", "kz", "bluetooth"]):
        return "mobile-accessories"

    return "mobile-accessories"


def extract_title(card) -> str:
    candidates = [
        card.get("title"),
        card.get("aria-label"),
        card.get_text(" ", strip=True),
    ]

    for c in candidates:
        if c and len(c.strip()) > 8:
            return c.strip()

    return "Producto sin título"


def extract_image(card) -> str:
    img = card.select_one("img")
    if not img:
        return ""

    return (
        img.get("src")
        or img.get("data-src")
        or img.get("data-lazy-src")
        or ""
    )


def extract_price_near(card) -> float | None:
    # intenta sacar precio del texto cercano
    text = card.get_text(" ", strip=True)
    return clean_price(text)


def search_aliexpress_products(keyword: str, limit: int = 8):
    query = quote_plus(keyword.strip())
    url = f"https://www.aliexpress.com/w/wholesale-{query}.html"

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print("❌ Error AliExpress request:", e)
        return []

    html = response.text

    # debug por si luego toca inspeccionar
    with open("aliexpress_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")

    # buscamos links de productos reales
    links = soup.select('a[href*="/item/"]')

    seen = set()
    products = []

    for link in links:
        href = link.get("href", "").strip()
        if not href:
            continue

        full_url = urljoin("https://www.aliexpress.com", href)

        if full_url in seen:
            continue
        seen.add(full_url)

        title = extract_title(link)
        if not title or len(title) < 8:
            continue

        image_url = extract_image(link)
        price = extract_price_near(link)

        # si no encuentra precio, salta
        if price is None or price <= 0:
            continue

        category = infer_category(title, keyword)

        products.append(
            Product(
                source="aliexpress_real",
                title=title,
                category=category,
                price=price,
                currency="USD",
                rating=4.5,  # temporal mientras extraemos rating real
                discount_percent=0.0,
                image_url=image_url,
                product_url=full_url,
            )
        )

        if len(products) >= limit:
            break

    print(f"🔎 AliExpress products found: {len(products)}")
    return products