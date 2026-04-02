from playwright.sync_api import sync_playwright

def search_mercadolibre_prices_playwright(query: str):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                ],
            )

            page = browser.new_page()
            url = f"https://listado.mercadolibre.com.mx/{query.replace(' ', '-')}"

            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(4000)

            html = page.content()
            browser.close()

            return {
                "ok": True,
                "html_length": len(html),
                "has_results": "ui-search-result" in html,
                "has_price": "$" in html,
                "url": url,
            }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
        }

query = "sensor nissan"
result = search_mercadolibre_prices_playwright(query)

print("QUERY:", query, flush=True)
print("RESULT:", result, flush=True)