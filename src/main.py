import time
from selenium import webdriver
from notification_utils import send_email_via_sendgrid
from selenium_utils import SeleniumUtils


def navigate_to_appointment_page(driver):
    utils = SeleniumUtils(driver)
    driver.get("https://termine.staedteregion-aachen.de/auslaenderamt/")

    # Navigation
    utils.click_element("text", "Aufenthaltsangelegenheiten")
    utils.reject_cookies_by_id("cookie_msg_btn_no")
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


def check_appointment_availability(driver):
    utils = SeleniumUtils(driver)
    while True:
        # Assuming find_element returns None if no element is found
        no_appointment_element = utils.find_element(
            "text", "Kein freier Termin verfügbar"
        )
        if no_appointment_element:
            print("No appointment available. Checking again in 5 seconds...")
            time.sleep(5)
            driver.refresh()

        else:
            print("Appointment available.")
            send_email_via_sendgrid()


# Main execution
driver = webdriver.Chrome()
try:
    navigate_to_appointment_page(driver)
    check_appointment_availability(driver)

finally:
    driver.quit()
