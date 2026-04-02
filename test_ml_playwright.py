from playwright.sync_api import sync_playwright

def test_home():
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

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                locale="es-MX",
                viewport={"width": 1366, "height": 900},
                extra_http_headers={
                    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
                },
            )

            page = context.new_page()

            url = "https://www.mercadolibre.com.mx/"
            page.goto(url, wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(6000)

            title = page.title()
            html = page.content()
            current_url = page.url

            with open("ml_home.html", "w", encoding="utf-8") as f:
                f.write(html)

            page.screenshot(path="ml_home.png", full_page=True)

            browser.close()

            return {
                "ok": True,
                "title": title,
                "html_length": len(html),
                "has_nav_input": "nav-search-input" in html,
                "has_search": "search" in html.lower(),
                "has_results": "ui-search-layout__item" in html,
                "url": current_url,
                "html_preview": html[:1200],
            }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
        }

result = test_home()
print("RESULT:", result, flush=True)