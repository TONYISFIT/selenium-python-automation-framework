"""Base page object with explicit-wait helpers.

Every interaction waits for the right condition first (visible / clickable),
which removes the flakiness of bare ``find_element`` + ``time.sleep`` code.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # -- navigation ------------------------------------------------------
    def open(self, url: str) -> "BasePage":
        self.driver.get(url)
        return self

    # -- element helpers --------------------------------------------------
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def safe_click(self, locator):
        """Click only after the element is clickable."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text: str):
        """Type only after the element is visible; clears first."""
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find_visible(locator).text

    def is_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    # -- page-level helpers ----------------------------------------------
    @property
    def title(self) -> str:
        return self.driver.title

    def wait_for_url_contains(self, fragment: str):
        self.wait.until(EC.url_contains(fragment))
