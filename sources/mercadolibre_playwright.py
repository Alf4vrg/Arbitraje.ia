from playwright.sync_api import sync_playwright


def search_mercadolibre_prices_playwright(query: str) -> dict:
    url = f"https://listado.mercadolibre.com.mx/{query.strip().replace(' ', '-')}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(5000)

            content = page.content()

            # debug html
            with open("ml_playwright_debug.html", "w", encoding="utf-8") as f:
                f.write(content)

            texts = page.locator("span.andes-money-amount__fraction").all_text_contents()

            browser.close()

        prices = []
        for txt in texts[:20]:
            txt = txt.replace(".", "").replace(",", "").strip()
            if txt.isdigit():
                prices.append(float(txt))

        if not prices:
            return {
                "min_price": 0,
                "max_price": 0,
                "avg_price": 0,
                "competition": 0,
                "source": "mercadolibre_playwright_no_prices",
                "debug": f"no prices found, texts={texts[:10]}",
                "url": url,
            }

        return {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": round(sum(prices) / len(prices), 2),
            "competition": len(prices),
            "source": "mercadolibre_playwright",
            "debug": f"{len(prices)} prices found",
            "url": url,
        }

    except Exception as e:
        return {
            "min_price": 0,
            "max_price": 0,
            "avg_price": 0,
            "competition": 0,
            "source": "mercadolibre_playwright_error",
            "debug": str(e),
            "url": url,
        }