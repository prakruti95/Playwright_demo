# Northline Store Automation Testing Framework

[![E2E & API Tests](https://github.com/prakruti95/Playwright_demo/actions/workflows/e2e-ci.yml/badge.svg)](https://github.com/prakruti95/Playwright_demo/actions)
![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.14-blue)
![Playwright](https://img.shields.io/badge/playwright-1.64.1-green)
![Pytest](https://img.shields.io/badge/pytest-9.2.0-orange)
![Tests Passing](https://img.shields.io/badge/tests-47%20passed-brightgreen)

An enterprise-grade, end-to-end (E2E) and REST API test automation framework for the **Northline Store** e-commerce application, built with **Python**, **Playwright**, **Pytest**, and **GitHub Actions**.

---

## 1. Project Overview & Scope

- **Target Web Application:** [https://ecomcicid.netlify.app/](https://ecomcicid.netlify.app/)
- **Supplied Mock API:** [https://681444af225ff1af16285b31.mockapi.io/electronicapi](https://681444af225ff1af16285b31.mockapi.io/electronicapi)
- **GitHub Repository:** [https://github.com/prakruti95/Playwright_demo.git](https://github.com/prakruti95/Playwright_demo.git)
- **Author:** Senior QA Automation Engineer (`prakruti95`)

---

## 2. Key Architecture & Discovery Highlights

During autonomous discovery, deep browser inspection, and bundle source auditing, key architectural characteristics were uncovered:

1. **Target Architecture & Resilience Layer:**
   - The frontend is a modern React SPA hosted on Netlify Edge with client-side routing.
   - The target Netlify hosting environment serves static assets with SPA fallbacks. Unmapped write requests (`POST /api/cart/items`, `POST /api/orders`) return HTTP 404/405.
   - The application incorporates an offline resilience layer (`isOfflineOrNetworkError` handler): failed write calls gracefully fall back to `localStorage` (`ecom-cart`, `ecom-local-orders`, `ecom-auth`), creating deterministic local orders (`ORD-LOCAL-YYYYMMDD-XXXXXX`).
2. **Search Discovery:**
   - Storefront catalog search is driven by the URL parameter `?search=<term>` rather than a visible input element. A dedicated text search input is present in the Admin catalog view (`/admin/products`).
3. **Financial Formulas:**
   - Free shipping threshold: **$\ge \$75.00$** (orders under $\$75.00$ charge a standard **$\$9.99$** fee).
   - Sales tax: exactly **$8\%$** (`0.08`) applied on taxable subtotal.
4. **Checkout Validation:**
   - Strict 2-letter ISO uppercase country code requirement (e.g. `US`; entering `United States` triggers `"Use a 2-letter country code"`).
   - Card payment is intentionally bypassed with a banner confirming test mode.

---

## 3. Framework Architecture (Page Object Model)

The framework follows the **Page Object Model (POM)** pattern, separating element locators and page interactions from test assertions:

```
northline-store-automation/
├── .github/
│   └── workflows/
│       └── e2e-ci.yml               # GitHub Actions CI matrix (Chromium, Firefox, WebKit)
├── docs/
│   ├── WEBSITE_DISCOVERY.md         # Comprehensive DOM & network findings
│   ├── API_INVENTORY.md             # REST endpoints & schema contracts
│   └── TEST_PLAN.md                 # Master QA Test Plan
├── framework/
│   ├── __init__.py
│   ├── config.py                    # Environment URLs, thresholds, test data
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
│   ├── e2e/                         # 33 End-to-End Test Cases
│   │   ├── test_home_navigation.py  # Homepage, navigation, theme toggle
│   │   ├── test_catalog_pdp.py      # Product listing, compare prices, PDP tabs
│   │   ├── test_filters_sorting.py  # Category filters, sorting, ?search= param
│   │   ├── test_cart_operations.py  # Cart empty state, add, increment, remove
│   │   ├── test_financial_calculations.py # Free shipping threshold, 8% tax formula
│   │   ├── test_checkout_validations.py # Empty form errors, ISO country code
│   │   ├── test_order_confirmation.py   # Receipt validation, cart reset
│   │   ├── test_auth_roles.py       # Customer -> /account, Admin -> /admin
│   │   └── test_mobile_responsive.py# 390x844 viewport, mobile filter sheet
│   └── api/                         # 14 REST API Test Cases
│       ├── test_electronic_api.py   # 10 CRUD & schema tests on supplied MockAPI
│       └── test_storefront_contracts.py # 4 static & mocked route contract tests
├── pytest.ini                       # Pytest configuration & markers
├── requirements.txt                 # Pinned dependencies
└── README.md                        # Documentation
```

---

## 4. Test Coverage Summary

| Suite | File | Tests | Coverage Scope | Status |
| :--- | :--- | :---: | :--- | :---: |
| **API (Supplied)** | `test_electronic_api.py` | 10 | GET, POST, PUT, DELETE, schema, pagination, search, filter, 404 | **PASS** |
| **API (Contracts)** | `test_storefront_contracts.py`| 4 | `/catalog.json`, Netlify 404 resilience, mocked 201 orders | **PASS** |
| **E2E Home** | `test_home_navigation.py` | 4 | Title, brand link, header navigation, dark/light theme | **PASS** |
| **E2E Catalog** | `test_catalog_pdp.py` | 5 | 6 catalog items, compare prices, PDP tabs, quantities | **PASS** |
| **E2E Filters** | `test_filters_sorting.py` | 5 | Category filter, reset filter, price sort, newest, `?search=` | **PASS** |
| **E2E Cart** | `test_cart_operations.py` | 4 | Empty cart, add to cart, drawer slide-over, increment, remove | **PASS** |
| **E2E Financial** | `test_financial_calculations.py`| 3 | $75 free shipping rule, 8% tax precision, total sum formula | **PASS** |
| **E2E Checkout** | `test_checkout_validations.py` | 4 | Empty form validation, 2-letter ISO country code, Stage 2 review | **PASS** |
| **E2E Confirm** | `test_order_confirmation.py`| 3 | Order placement, `ORD-LOCAL-` number format, cart clear | **PASS** |
| **E2E Auth** | `test_auth_roles.py` | 3 | Customer login -> `/account`, Admin login -> `/admin`, sign out | **PASS** |
| **E2E Mobile** | `test_mobile_responsive.py` | 2 | Mobile header, mobile filter sheet, full-width cart drawer | **PASS** |
| **Total** | **All Suites** | **47** | **Full E2E + API Automation Matrix** | **100% PASS** |

---

## 5. Local Setup & Execution Guide

### Prerequisites
- Python 3.11+
- Git

### 1. Clone Repository & Install Dependencies
```bash
git clone https://github.com/prakruti95/Playwright_demo.git
cd Playwright_demo
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install --with-deps
```

### 2. Run All Tests
```bash
# Run full suite (47 tests) with HTML report
python -m pytest tests/ --html=test-results/report.html --self-contained-html -v
```

### 3. Run Specific Test Suites
```bash
# Run API tests only (14 tests)
python -m pytest tests/api -v

# Run E2E tests only (33 tests)
python -m pytest tests/e2e -v

# Run smoke tests only
python -m pytest -m smoke -v

# Run against specific browser engine
python -m pytest tests/e2e --browser chromium -v
python -m pytest tests/e2e --browser firefox -v
python -m pytest tests/e2e --browser webkit -v
```

---

## 6. CI/CD Pipeline (GitHub Actions)

The workflow file [`.github/workflows/e2e-ci.yml`](.github/workflows/e2e-ci.yml) executes automatically on:
- Every push to `main` or `master`.
- Every pull request to `main` or `master`.
- Manual trigger via `workflow_dispatch`.

### CI Matrix Configuration:
- **Matrix Strategy:** Parallel execution across **Chromium**, **Firefox**, and **WebKit**.
- **Runner OS:** `ubuntu-latest` with Python 3.11.
- **Artifacts Uploaded:**
  - Standalone HTML Reports (`test-results/report-<browser>.html`).
  - Failure screenshots (`test-results/screenshots/`).
  - Video recordings of test execution (`test-results/videos/`).
  - Playwright Traces (`test-results/traces/trace.zip`).
