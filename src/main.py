import argparse
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notification_utils import send_email_via_sendgrid, send_telegram_message
from selenium_utils import SeleniumUtils
import time


def navigate_to_appointment_page(driver, team):
    utils = SeleniumUtils(driver)
    driver.get("https://termine.staedteregion-aachen.de/auslaenderamt/")

    # Navigation
    utils.reject_cookies_by_id("cookie_msg_btn_no")
    utils.click_element("text", "Aufenthaltsangelegenheiten")
    utils.click_element(
        "xpath", "//h3[contains(text(), 'Aufenthalt')]/ancestor::div[1]"
    )

    button_text = f"Erhöhen der Anzahl des Anliegens Erteilung/Verlängerung Aufenthalt - Nachname: A - Z ({team})"
    utils.click_element(
        "xpath",
        f"//button[normalize-space(@title)='{button_text}']",
    )
    utils.click_element("id", "WeiterButton")
    utils.click_element("id", "OKButton")
    utils.click_element(
        "xpath",
        "//input[@type='submit'][@value='Ausländeramt Aachen, 2. Etage auswählen']",
    )


async def check_appointment_availability(driver, team):
    utils = SeleniumUtils(driver)

    message = f"An appointment is available at the Ausländeramt Aachen {team}. Book now! https://termine.staedteregion-aachen.de/auslaenderamt/"

    no_appointment_element = utils.find_element(
        "text", "Kein freier Termin verfügbar", timeout=5
    )
    if no_appointment_element:
        print(f"No appointment available on {team}.")
    else:
        print(f"Appointment available on {team}.")
        await send_telegram_message(message)
        send_email_via_sendgrid(message)


def setup_chrome_options(headless=False):
    """Configure Chrome options."""
    options = Options()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
    return options


async def process_team(driver, team):
    """Process each team by navigating and checking appointment availability."""
    start_time = time.time()
    navigate_to_appointment_page(driver, team)
    await check_appointment_availability(driver, team)


def ensure_duration(start_time, target_duration):
    """Ensure each loop iteration takes at least a specified number of seconds."""
    duration = time.time() - start_time
    remaining_time = target_duration - duration
    if remaining_time > 0:
        time.sleep(remaining_time)


async def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Run Selenium in headless mode.")
    parser.add_argument(
        "--headless", action="store_true", help="Run the script in headless mode"
    )
    args = parser.parse_args()

    options = setup_chrome_options(args.headless)
    driver = webdriver.Chrome(options=options)

    try:
        while True:
            teams = ["Team 1", "Team 2", "Team 3"]
            for team in teams:
                await process_team(driver, team)
    except Exception as e:
        print(f"Script ended due to an error: {e}")
    finally:
        send_email_via_sendgrid(
            subject="Script has finished running",
            content="The script has finished running. Please check the output for details.",
        )
        driver.quit()


if __name__ == "__main__":
    asyncio.run(main())
