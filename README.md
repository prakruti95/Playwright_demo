# Northline Store Automation Testing Framework

[![CI/CD Pipeline](https://github.com/prakruti95/Playwright_demo/actions/workflows/tests.yml/badge.svg)](https://github.com/prakruti95/Playwright_demo/actions)
![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.14-blue)
![Playwright](https://img.shields.io/badge/playwright-1.64.1-green)
![Pytest](https://img.shields.io/badge/pytest-9.2.0-orange)
![Tests Passing](https://img.shields.io/badge/tests-58%2F58%20passed-brightgreen)

An enterprise-grade, end-to-end (E2E) and REST API test automation framework for the **Northline Store** e-commerce application, built with **Python**, **Playwright**, **Pytest**, and **GitHub Actions**.

---

## 1. Project Overview & Deliverables

- **Target Web Application:** [https://ecomcicid.netlify.app/](https://ecomcicid.netlify.app/)
- **Supplied Mock API:** [https://681444af225ff1af16285b31.mockapi.io/electronicapi](https://681444af225ff1af16285b31.mockapi.io/electronicapi)
- **GitHub Repository:** [https://github.com/prakruti95/Playwright_demo.git](https://github.com/prakruti95/Playwright_demo.git)
- **Author:** Senior QA Automation Engineer (`prakruti95`)

### Primary Documentation Artifacts
- **[REQUIREMENTS.md](REQUIREMENTS.md):** Formal audit of all 24 project requirements.
- **[TEST_SUMMARY.md](TEST_SUMMARY.md):** Test suite breakdown, multi-browser matrix results, and diagnostic outputs.
- **[docs/REQUIREMENT_TRACEABILITY.md](docs/REQUIREMENT_TRACEABILITY.md):** Traceability matrix linking requirements to code and test markers.
- **[docs/WEBSITE_DISCOVERY.md](docs/WEBSITE_DISCOVERY.md):** Deep architectural audit of DOM, navigation, PDP, and checkout.
- **[docs/API_INVENTORY.md](docs/API_INVENTORY.md):** Comprehensive REST endpoint inventory and schema contracts.
- **[docs/TEST_PLAN.md](docs/TEST_PLAN.md):** Master QA Test Plan with risk matrix and stable locator dictionary.

---

## 2. Key Architecture & Discovered Behaviors

1. **Target Architecture & Resilience Layer:**
   - The frontend is a modern React SPA hosted on Netlify Edge with client-side routing.
   - The target Netlify hosting environment serves static assets with SPA fallbacks. Unmapped write requests (`POST /api/cart/items`, `POST /api/orders`) return HTTP 404/405.
   - The application incorporates an offline resilience layer (`isOfflineOrNetworkError` handler): failed write calls gracefully fall back to `localStorage` (`ecom-cart`, `ecom-local-orders`, `ecom-auth`), creating deterministic local orders (`ORD-LOCAL-YYYYMMDD-XXXXXX`).
2. **Search Discovery:**
   - Storefront catalog search is driven by the URL parameter `?search=<term>` rather than a visible input element. A dedicated text search input is present in the Admin catalog view (`/admin/products`).
3. **Financial Formulas:**
   - Free shipping threshold: **$\ge \$75.00$** (orders under $\$75.00$ charge a standard **$\$9.99$** fee).
   - Sales tax: exactly **$8\%$** (`0.08`) applied on taxable subtotal.
   - Catalog floor: All 6 active products in `/catalog.json` have unit prices $\ge \$86.00$. Any single product purchase automatically qualifies for free shipping.
4. **Checkout Validation:**
   - Strict 2-letter ISO uppercase country code requirement (e.g. `US`; entering `United States` triggers `"Use a 2-letter country code"`).
   - Card payment is intentionally bypassed with a banner confirming test mode.
5. **Supplied MockAPI Behavior:**
   - MockAPI stores `price` as string attributes (`"19200"`), resulting in lexicographical rather than numerical sort orders.
   - Malformed non-JSON payloads sent with `Content-Type: application/json` trigger HTTP 400 Bad Request.

---

## 3. Framework Architecture (Page Object Model)

The framework follows the **Page Object Model (POM)** pattern, separating element locators and page interactions from test assertions:

```
northline-store-automation/
├── .github/
│   └── workflows/
│       └── tests.yml                # CI/CD pipeline (API, smoke, and full regression matrix)
├── docs/
│   ├── WEBSITE_DISCOVERY.md         # Comprehensive DOM & network findings
│   ├── API_INVENTORY.md             # REST endpoints & schema contracts
│   ├── TEST_PLAN.md                 # Master QA Test Plan
│   └── REQUIREMENT_TRACEABILITY.md  # Requirement Traceability Matrix (RTM)
├── framework/
│   ├── __init__.py
│   ├── config.py                    # Decoupled URLs, thresholds, synthetic test data
│   └── pages/                       # Page Object Models
│       ├── __init__.py
│       ├── base_page.py             # Global header, footer, drawer & storage
│       ├── home_page.py             # Hero banners, brand links & categories
│       ├── products_page.py         # Catalog grid, filters, sorting & search
│       ├── product_detail_page.py   # PDP gallery, quantities, tabs & CTAs
│       ├── cart_page.py             # Cart drawer, quantities & line items
│       ├── checkout_page.py         # Multi-stage checkout form & validation
│       ├── order_confirmation_page.py # Receipt, order number & delivery range
│       ├── login_page.py            # Customer & admin authentication
│       ├── account_page.py          # Customer profile & sign out
│       └── admin_page.py            # Admin dashboard & management
├── tests/
│   ├── conftest.py                  # Pytest fixtures, multi-browser contexts & hooks
│   ├── e2e/                         # 39 End-to-End Test Cases
│   │   ├── test_home_navigation.py  # Homepage, navigation, theme toggle, 404 route
│   │   ├── test_catalog_pdp.py      # Product listing, compare prices, PDP tabs
│   │   ├── test_filters_sorting.py  # Category filters, sorting, search, no results
│   │   ├── test_cart_operations.py  # Cart empty state, add, increment, remove, reload
│   │   ├── test_financial_calculations.py # Free shipping, 8% tax, formula precision
│   │   ├── test_checkout_validations.py # Empty form errors, ISO country code
│   │   ├── test_order_confirmation.py   # Receipt validation, cart reset
│   │   ├── test_auth_roles.py       # Customer -> /account, Admin -> /admin, email validity
│   │   └── test_mobile_responsive.py# 390x844 viewport, mobile filter sheet
│   └── api/                         # 19 REST API Test Cases
│       ├── test_electronic_api.py   # 14 CRUD, schema, SLA, and 400 error tests on MockAPI
│       └── test_storefront_contracts.py # 5 static, mocked 201, UI consistency, 500 fault tests
├── REQUIREMENTS.md                  # Comprehensive requirements specification & audit
├── TEST_SUMMARY.md                  # Detailed test execution summary & diagnostics
├── pytest.ini                       # Pytest configuration & markers
├── requirements.txt                 # Pinned dependencies
└── README.md                        # Documentation
```

---

## 4. Test Coverage Summary

| Suite | File | Tests | Coverage Scope | Status |
| :--- | :--- | :---: | :--- | :---: |
| **API (Supplied)** | `test_electronic_api.py` | 14 | GET, POST, PUT, DELETE, schema, pagination, search, sort, headers, SLA, 400 fault | **PASS** |
| **API (Contracts)** | `test_storefront_contracts.py`| 5 | `/catalog.json`, Netlify 404 resilience, mocked 201 orders, UI consistency, 500 fault | **PASS** |
| **E2E Home** | `test_home_navigation.py` | 5 | Title, brand link, header navigation, dark/light theme, unknown 404 route | **PASS** |
| **E2E Catalog** | `test_catalog_pdp.py` | 5 | 6 catalog items, compare prices, PDP tabs, quantities | **PASS** |
| **E2E Filters** | `test_filters_sorting.py` | 6 | Category filter, reset filter, price sort, newest, search term, no-match empty state | **PASS** |
| **E2E Cart** | `test_cart_operations.py` | 5 | Empty cart, add to cart, drawer slide-over, increment, remove, reload persistence | **PASS** |
| **E2E Financial** | `test_financial_calculations.py`| 4 | Free shipping threshold, 8% sales tax, total formula precision, catalog price floor | **PASS** |
| **E2E Checkout** | `test_checkout_validations.py` | 4 | Required fields, strict 2-letter ISO country, review stage navigation, back button | **PASS** |
| **E2E Order** | `test_order_confirmation.py` | 3 | Order placement, receipt format (`ORD-LOCAL-`), badge counter reset | **PASS** |
| **E2E Auth** | `test_auth_roles.py` | 4 | Customer login, admin dashboard redirection, sign out session clear, email validity | **PASS** |
| **E2E Mobile** | `test_mobile_responsive.py` | 3 | Viewport $390\times844$, mobile header controls, mobile filter drawer | **PASS** |
| **Total Suite** | **11 Modules** | **58** | **Full Functional & Non-Functional E2E + API Coverage** | **PASS** |

---

## 5. Local Execution Guide

### Prerequisites
- Python 3.11+
- Git

### Installation
```powershell
# Clone the repository
git clone https://github.com/prakruti95/Playwright_demo.git
cd Playwright_demo

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install --with-deps
```

### Running Test Suites
```powershell
# Run smoke tests across default browser (Chromium)
pytest -m "smoke"

# Run smoke tests on specific browser engines
pytest -m "smoke" --browser firefox
pytest -m "smoke" --browser webkit

# Run all E2E tests
pytest -m "e2e"

# Run all REST API tests
pytest -m "api"

# Run the complete test suite with self-contained HTML report
pytest --html=test-results/report.html --self-contained-html
```

---

## 6. GitHub Actions CI/CD Pipeline

The `.github/workflows/tests.yml` pipeline runs automatically on:
- Every push to `main`
- Every pull request targeting `main`
- Manual invocation via `workflow_dispatch`
- Nightly scheduled run at 02:00 UTC (`0 2 * * *`)

### Pipeline Stages
1. **`api-tests`:** Executes all 19 REST API and contract tests in isolation.
2. **`smoke-tests`:** Matrix execution across **Chromium**, **Firefox**, and **WebKit**.
3. **`e2e-regression-tests`:** Full 39-test E2E regression across all 3 browsers (gated on smoke test success).
4. **Artifacts:** Uploads pytest HTML reports, Playwright traces, failure screenshots, and execution videos.
