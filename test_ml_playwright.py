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
            page.wait_for_timeout(5000)

            title = page.title()
            html = page.content()
            page.screenshot(path="ml_test.png", full_page=True)

            browser.close()

            return {
                "ok": True,
                "title": title,
                "html_length": len(html),
                "has_results": "ui-search-layout__item" in html,
                "has_price": "$" in html,
                "url": url,
                "html_preview": html[:1000],
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