import argparse
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notification_utils import send_email_via_sendgrid, send_telegram_message
from selenium_utils import SeleniumUtils


def navigate_to_appointment_page(driver):
    utils = SeleniumUtils(driver)
    driver.get("https://termine.staedteregion-aachen.de/auslaenderamt/")

    # Navigation
    utils.reject_cookies_by_id("cookie_msg_btn_no")
    utils.click_element("text", "Aufenthaltsangelegenheiten")
    utils.click_element(
        "xpath", "//h3[contains(text(), 'Aufenthalt')]/ancestor::div[1]"
    )
    utils.click_element(
        "xpath",
        "//button[@title='Erhöhen der Anzahl des Anliegens Erteilung/Verlängerung Aufenthalt - Nachname: A - Z (Team 1)']",
    )
    utils.click_element("id", "WeiterButton")
    utils.click_element("id", "OKButton")
    utils.click_element(
        "xpath",
        "//input[@type='submit'][@value='Ausländeramt Aachen, 2. Etage auswählen']",
    )


async def check_appointment_availability(driver):
    utils = SeleniumUtils(driver)

    while True:
        no_appointment_element = utils.find_element(
            "text", "Kein freier Termin verfügbar"
        )
        if no_appointment_element:
            wait_interval = 30
            print(
                f"No appointment available. Checking again in {wait_interval} seconds..."
            )
            await asyncio.sleep(wait_interval)  # Use asyncio.sleep for async sleep
            driver.refresh()
        else:
            print("Appointment available.")
            await send_telegram_message()
            send_email_via_sendgrid()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Selenium in headless mode.")
    parser.add_argument(
        "--headless", action="store_true", help="Run the script in headless mode"
    )
    args = parser.parse_args()

    chrome_options = Options()

    if args.headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    # Use asyncio event loop to run async functions
    navigate_to_appointment_page(driver)
    asyncio.run(check_appointment_availability(driver))

    send_email_via_sendgrid(
        subject="Script has finished running",
        content="The script has finished running. Please check the output for details.",
    )
    driver.quit()
