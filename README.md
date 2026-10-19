# Selenium + Python Test Automation Framework

A clean, CI-ready UI test automation framework built with **Selenium WebDriver**,
**pytest**, and the **Page Object Model (POM)** pattern. It ships with a tiny
self-contained demo web app (`demo_site/`) so the whole suite runs locally with
zero external dependencies.

## Architecture

```
selenium-python-automation-framework/
├── config/
│   └── config.py          # Env-var-driven settings (BASE_URL, BROWSER, HEADLESS, TIMEOUT, SCREENSHOT_DIR)
├── pages/
│   ├── base_page.py       # BasePage: explicit-wait helpers (safe_click, type_text, get_text, is_visible)
│   ├── login_page.py      # LoginPage page object
│   └── home_page.py       # HomePage page object
├── demo_site/
│   ├── login.html         # Local demo app: login form (admin / password123)
│   └── index.html         # Local demo app: home page with nav
├── tests/
│   ├── test_login.py      # Login scenarios (marked: browser)
│   ├── test_smoke.py      # Home page smoke tests (marked: browser)
│   └── test_config.py     # Config unit tests — no browser needed
├── conftest.py            # driver fixture, local HTTP server fixture, screenshot-on-failure hook
├── .github/workflows/ci.yml
├── pytest.ini
└── requirements.txt
```

**Design choices**

- **Explicit waits everywhere** — no `time.sleep`; every interaction waits for the
  right condition (visible / clickable), which is the main source of flakiness in
  UI suites.
- **Page Object Model** — locators and page actions live in `pages/`; tests only
  describe behavior.
- **Env-driven config** — the same suite targets the local demo app, staging, or
  prod via `BASE_URL` without code changes.
- **Screenshots on failure** — a pytest hook saves a PNG to `screenshots/` whenever
  a browser test fails.
- **Self-contained demo app** — `conftest.py` spins up `http.server` on an ephemeral
  localhost port, so browser tests never depend on an external site.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Chrome is managed automatically by `webdriver-manager` (no manual driver setup).

## Running the tests

```bash
# Full suite (needs Chrome)
pytest -v

# Only the fast unit tests — no browser required
pytest tests/test_config.py -v

# Skip browser tests explicitly
pytest -m "not browser" -v

# HTML report
pytest --html=reports/report.html --self-contained-html
```

Environment overrides:

```bash
BASE_URL=https://staging.example.com HEADLESS=false TIMEOUT=20 pytest
```

## CI

`.github/workflows/ci.yml` runs on every push/PR: installs Python 3.11 and Chrome
(`browser-actions/setup-chrome`), installs dependencies, runs the full suite, and
uploads the HTML report as an artifact.

## Test status (honest)

| Suite | Tests | Status |
|---|---|---|
| `tests/test_config.py` | 14 | ✅ **Passed locally** (Python 3.x, pytest; no browser needed) |
| `tests/test_login.py` | 3 | ⚠️ Not run locally — no Chrome/browser in this environment. Written for Chrome; runs in CI. |
| `tests/test_smoke.py` | 3 | ⚠️ Not run locally — no Chrome/browser in this environment. Written for Chrome; runs in CI. |

The browser tests were validated by code review against the demo pages' actual
element IDs (`username`, `password`, `login-btn`, `error-msg`, `welcome-heading`,
`logout-link`), but they have **not** been executed here. CI is the source of
truth for them — check the latest workflow run's report artifact.

## Demo credentials

The bundled demo app (`demo_site/`) is a fake local login page for test purposes
only. Credentials `admin` / `password123` exist solely inside that demo and are
not real accounts anywhere.
