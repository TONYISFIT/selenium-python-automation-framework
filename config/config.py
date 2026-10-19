"""Central configuration for the framework.

All settings are driven by environment variables so the same suite can run
locally and in CI without code changes. Nothing in this module requires a
browser, which keeps it unit-testable.
"""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    base_url: str = "http://127.0.0.1:8000"
    browser: str = "chrome"
    headless: bool = True
    timeout: int = 10
    screenshot_dir: str = "screenshots"


def _get_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "y", "on")


def _get_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except (TypeError, ValueError):
        return default


def load_config() -> Config:
    """Build a Config from the current environment."""
    return Config(
        base_url=os.environ.get("BASE_URL", Config.base_url),
        browser=os.environ.get("BROWSER", Config.browser).lower(),
        headless=_get_bool("HEADLESS", Config.headless),
        timeout=_get_int("TIMEOUT", Config.timeout),
        screenshot_dir=os.environ.get("SCREENSHOT_DIR", Config.screenshot_dir),
    )
