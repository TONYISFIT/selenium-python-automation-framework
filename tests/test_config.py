"""Unit tests for config parsing. These do NOT need a browser or selenium."""
import os

import pytest

from config.config import Config, _get_bool, _get_int, load_config


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for key in ("BASE_URL", "BROWSER", "HEADLESS", "TIMEOUT", "SCREENSHOT_DIR"):
        monkeypatch.delenv(key, raising=False)


def test_defaults():
    cfg = load_config()
    assert cfg == Config(
        base_url="http://127.0.0.1:8000",
        browser="chrome",
        headless=True,
        timeout=10,
        screenshot_dir="screenshots",
    )


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://staging.example.com")
    monkeypatch.setenv("BROWSER", "Firefox")
    monkeypatch.setenv("HEADLESS", "false")
    monkeypatch.setenv("TIMEOUT", "25")
    monkeypatch.setenv("SCREENSHOT_DIR", "artifacts/shots")
    cfg = load_config()
    assert cfg.base_url == "https://staging.example.com"
    assert cfg.browser == "firefox"  # normalized to lowercase
    assert cfg.headless is False
    assert cfg.timeout == 25
    assert cfg.screenshot_dir == "artifacts/shots"


@pytest.mark.parametrize("raw,expected", [
    ("1", True), ("true", True), ("TRUE", True), ("yes", True), ("on", True),
    ("0", False), ("false", False), ("no", False), ("", False),
])
def test_bool_parsing(monkeypatch, raw, expected):
    monkeypatch.setenv("HEADLESS", raw)
    assert _get_bool("HEADLESS", not expected) is expected


def test_bool_default_when_unset():
    assert _get_bool("HEADLESS", True) is True
    assert _get_bool("HEADLESS", False) is False


def test_int_parsing_and_invalid_fallback(monkeypatch):
    monkeypatch.setenv("TIMEOUT", "30")
    assert _get_int("TIMEOUT", 10) == 30
    monkeypatch.setenv("TIMEOUT", "not-a-number")
    assert _get_int("TIMEOUT", 10) == 10
    monkeypatch.delenv("TIMEOUT")
    assert _get_int("TIMEOUT", 10) == 10


def test_config_is_immutable():
    cfg = load_config()
    with pytest.raises(Exception):
        cfg.timeout = 99
