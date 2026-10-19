"""Login tests against the bundled local demo site. Requires a browser."""
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage

pytestmark = pytest.mark.browser


def test_valid_login_lands_on_home(driver, base_url):
    login = LoginPage(driver).open(base_url)
    login.login_as_admin()

    home = HomePage(driver)
    assert home.is_loaded()
    assert "admin" in home.get_welcome_text().lower()


def test_invalid_login_shows_error(driver, base_url):
    login = LoginPage(driver).open(base_url)
    login.login("admin", "wrong-password")

    assert login.is_error_displayed()
    assert "invalid" in login.get_error_message().lower()


def test_empty_fields_show_required_error(driver, base_url):
    login = LoginPage(driver).open(base_url)
    login.login("", "")

    assert login.is_error_displayed()
    assert "required" in login.get_error_message().lower()
