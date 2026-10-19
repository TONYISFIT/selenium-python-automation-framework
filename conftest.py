"""Shared pytest fixtures and hooks.

- ``base_url``: URL of the app under test (env BASE_URL or the local demo server).
- ``http_server``: serves ``demo_site/`` on 127.0.0.1 with an ephemeral port.
- ``driver``: headless Chrome via webdriver-manager; skips when Chrome is
  unavailable instead of failing the whole run.
- screenshot hook: saves a PNG on any browser-test failure.

Selenium is imported lazily so non-browser tests (e.g. test_config.py) run
even on machines without selenium installed.
"""
import functools
import http.server
import os
import threading

import pytest

from config.config import load_config

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager

    SELENIUM_AVAILABLE = True
except ImportError:  # pragma: no cover - environment without selenium
    SELENIUM_AVAILABLE = False


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture(scope="session")
def http_server():
    """Serve demo_site/ over HTTP on an ephemeral localhost port."""
    demo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_site")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=demo_dir)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    yield f"http://{host}:{port}"
    server.shutdown()
    thread.join()


@pytest.fixture(scope="session")
def base_url(http_server, config):
    # An explicit BASE_URL env var (e.g. staging) wins over the local server.
    if os.environ.get("BASE_URL"):
        return config.base_url
    return http_server


@pytest.fixture()
def driver(config):
    """Headless Chrome driver. Skips the test if no Chrome is available."""
    if not SELENIUM_AVAILABLE:
        pytest.skip("selenium is not installed")
    options = ChromeOptions()
    if config.headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,768")
    try:
        service = ChromeService(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=options)
    except Exception as exc:  # Chrome binary missing, no network, etc.
        pytest.skip(f"Chrome WebDriver could not start: {exc}")
    drv.implicitly_wait(0)  # explicit waits only
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot when a browser test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is None:  # fixture missing or skipped before creating a driver
            return
        try:
            cfg = load_config()
            os.makedirs(cfg.screenshot_dir, exist_ok=True)
            path = os.path.join(cfg.screenshot_dir, f"{item.name}.png")
            drv.save_screenshot(path)
            print(f"\nScreenshot saved to {path}")
        except Exception:
            pass
