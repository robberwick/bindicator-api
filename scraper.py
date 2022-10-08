from datetime import datetime
from playwright.async_api import async_playwright
import asyncio

service_date_text_pattern = r"/\d\d\/\d\d\/\d\d\d\d/"
service_name_text_pattern = "/.*Collection Service/"

async def scrape_content():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True  # Show the browser
        )
        page = await browser.new_page()
        await page.goto('https://uhtn-wrp.whitespacews.com/#!')
        # Data Extraction Code Here
        bin_link = page.locator("text=Find my bin collection day")
        await bin_link.click()
        await page.type("input[name=address_name_number]", "88")
        await page.type("input[name=address_street]", "cambridge road")
        await page.type("input[name=address_postcode]", "sg40jh")
        await page.locator("button[type='submit']", has_text='continue').click()
        await page.get_by_text('88, Cambridge road').click()
        # get the list of dates
        service_dates = await page.locator(f"text={service_date_text_pattern}").all_text_contents()

        service_names = await page.locator(f"text={service_name_text_pattern}").all_text_contents()

        zipped = zip(service_dates, service_names)
        services_by_date: dict[str, list[str]] =  {}
        for key, value in zipped:
            if not value.lower().startswith('food'):
                services_by_date.setdefault(key, []).append(value)

        service_date, service_name = list(services_by_date.items())[0]

        next_date = datetime.strptime(service_date, '%d/%m/%Y').date()
        today = datetime.today().date()

        bins_due = (next_date - today).days < 2

        await browser.close()
        return dict(
            service=service_name[0].split()[0],
            date=service_date,
            isDue=bins_due
        )

if __name__ == '__main__':
    asyncio.run(scrape_content())