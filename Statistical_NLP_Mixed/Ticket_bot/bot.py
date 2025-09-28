from playwright.async_api import async_playwright
from notifier import send_telegram
from config import PHONE_NUMBER, PASSWORD
import asyncio

# আপনার Google Chrome এর এক্সিকিউটেবল path (Linux এর উদাহরণ)
CHROME_PATH = "/usr/bin/google-chrome"

async def run_bot():
    max_retries = 5

    for attempt in range(max_retries):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    executable_path=CHROME_PATH,
                    args=["--start-maximized"]
                )
                page = await browser.new_page()

                await page.goto("https://eticket.railway.gov.bd/")
                await page.click("text=Login")
                await page.fill('input[name="email"]', PHONE_NUMBER)
                await page.fill('input[name="password"]', PASSWORD)
                await page.click("button:text('Login')")

                await page.wait_for_timeout(3000)

                # টিকিট সার্চ
                await page.click("text=Purchase Ticket")

                await page.select_option("select[name='from_station']", value="Dhaka")
                await page.select_option("select[name='to_station']", value="Rajshahi")
                await page.fill("input[name='date']", "2025-06-20")  # <-- আপনার কাঙ্ক্ষিত তারিখ দিন
                await page.click("button:text('Search')")

                await page.wait_for_timeout(3000)

                # কিনে ফেলা
                await page.click("text=Buy Now")

                await page.wait_for_timeout(2000)
                await page.click("text=Continue Purchase")

                await send_telegram("✅ টিকিট বুকিং সফল হয়েছে!")

                await browser.close()
                break

        except Exception as e:
            await send_telegram(f"❌ চেষ্টা {attempt+1} বার: {str(e)}")
            await asyncio.sleep(3)
