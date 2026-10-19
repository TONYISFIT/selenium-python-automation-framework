"""Page object for the demo home page (demo_site/index.html)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    WELCOME_HEADING = (By.ID, "welcome-heading")
    NAV_LINKS = (By.CSS_SELECTOR, "nav a")
    LOGOUT_LINK = (By.ID, "logout-link")

    def open(self, base_url: str) -> "HomePage":
        super().open(f"{base_url}/index.html")
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.WELCOME_HEADING)

    def get_welcome_text(self) -> str:
        return self.get_text(self.WELCOME_HEADING)

    def nav_link_texts(self):
        return [link.text for link in self.driver.find_elements(*self.NAV_LINKS)]

    def logout(self):
        self.safe_click(self.LOGOUT_LINK)
