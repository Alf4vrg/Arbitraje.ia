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

            page = browser.new_page()
            page.goto("https://www.mercadolibre.com.mx/", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(5000)

            title = page.title()
            html = page.content()
            page.screenshot(path="ml_home.png", full_page=True)

            browser.close()

            return {
                "ok": True,
                "title": title,
                "html_length": len(html),
                "has_nav_input": "nav-search-input" in html,
                "has_search": "search" in html.lower(),
                "url": "https://www.mercadolibre.com.mx/",
                "html_preview": html[:1200],
            }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
        }

result = test_home()

print("RESULT:", result, flush=True)