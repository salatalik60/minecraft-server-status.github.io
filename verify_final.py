import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Serve the file
        import subprocess
        process = subprocess.Popen(["python3", "-m", "http.server", "8080"])
        await asyncio.sleep(2)

        try:
            await page.goto("http://localhost:8080/index.html")
            print("Page loaded")

            # Check Title
            title = await page.title()
            print(f"Title: {title}")

            # Test Search
            await page.fill("#ip", "mc.hypixel.net")
            await page.click("button:has-text('Durumu Kontrol Et')")

            # Wait for result
            await page.wait_for_selector("#result", timeout=10000)
            result_text = await page.inner_text("#result")
            print(f"Result: {result_text}")

            # Test Favorite
            await page.click("#favBtn")
            is_active = await page.eval_on_selector("#favBtn", "el => el.classList.contains('active')")
            print(f"Favorite active: {is_active}")

            # Take screenshot
            await page.screenshot(path="final_verification.png")
            print("Screenshot saved to final_verification.png")

        finally:
            process.terminate()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
