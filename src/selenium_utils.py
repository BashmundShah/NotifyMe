from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SeleniumUtils:
    def __init__(self, driver):
        self.driver = driver

    def click_element(self, locator, value, timeout=20):
        """
        Clicks an element identified by a locator and value.
        Locator can be 'xpath', 'id', or 'text' (for buttons).
        """
        try:
            if locator == "xpath":
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, value))
                )
            elif locator == "id":
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.ID, value))
                )
            elif locator == "text":
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//button[contains(text(), '{value}')]")
                    )
                )
            else:
                raise ValueError("Unsupported locator")
            element.click()
        except TimeoutException:
            print(f"Element with locator '{locator}' and value '{value}' not found.")

    def find_element(self, locator, value, timeout=20):
        """
        Finds an element by xpath or text containing.
        """
        try:
            if locator == "xpath":
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, value))
                )
            elif locator == "text":
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//*[contains(text(), '{value}')]")
                    )
                )
            elif locator == "id":
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.ID, value))
                )
            else:
                raise ValueError("Unsupported locator")
        except TimeoutException:
            print(f"Element with locator '{locator}' and value '{value}' not found.")
            return None

    def reject_cookies_by_id(self, cookie_id):
        """
        Specialized method for rejecting cookies by ID, only if the cookie element exists.
        """
        try:
            cookie_element = self.find_element("id", cookie_id)
            if cookie_element.is_displayed():
                cookie_element.click()
        except TimeoutException:
            print(f"Cookie element with ID '{cookie_id}' not found.")
