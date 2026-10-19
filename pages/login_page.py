"""Page object for the demo login page (demo_site/login.html)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "login-btn")
    ERROR = (By.ID, "error-msg")

    # Demo credentials for the bundled local demo app (not a real account).
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "password123"

    def open(self, base_url: str) -> "LoginPage":
        super().open(f"{base_url}/login.html")
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.safe_click(self.SUBMIT)
        return self

    def login_as_admin(self) -> "LoginPage":
        return self.login(self.VALID_USERNAME, self.VALID_PASSWORD)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self.ERROR)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR)
