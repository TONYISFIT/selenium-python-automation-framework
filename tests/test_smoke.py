"""Smoke tests for the demo home page. Requires a browser."""
import pytest

from pages.home_page import HomePage

pytestmark = pytest.mark.browser


def test_home_page_title(driver, base_url):
    home = HomePage(driver).open(base_url)
    assert "demo shop" in home.title.lower()


def test_nav_links_present(driver, base_url):
    home = HomePage(driver).open(base_url)
    links = home.nav_link_texts()
    for expected in ("Home", "Products", "Cart", "Contact"):
        assert expected in links, f"missing nav link: {expected}"


def test_logout_returns_to_login(driver, base_url):
    home = HomePage(driver).open(base_url)
    home.logout()
    assert "login" in driver.current_url.lower()
