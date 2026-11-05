# Test Plan & QA Automation Strategy: Northline Store

**Target Under Test:** [https://ecomcicid.netlify.app/](https://ecomcicid.netlify.app/)  
**Document Version:** 1.0.0  
**Author:** Senior QA Automation Engineer  
**Framework:** Python 3.11+ / Pytest / Playwright (`pytest-playwright`) / GitHub Actions CI/CD  

---

## 1. Executive Summary & Objectives

This Test Plan defines the end-to-end (E2E), integration, and network testing strategy for the **Northline Store** e-commerce application. The primary objectives are:
1. Validate core storefront user journeys: catalog browsing, product inspection, cart operations, financial calculations, multi-stage checkout, and order confirmation.
2. Verify application resilience across both live Netlify hosting conditions (offline/local fallback) and real backend API contracts (mocked via Playwright network routing).
3. Ensure UI consistency across major desktop browsers (Chromium, Firefox, WebKit) and mobile viewports (iPhone / Android dimensions).
4. Establish an automated, repeatable CI/CD test pipeline with artifact generation (HTML test reports, video recordings, and trace archives on failure).

---

## 2. Target Scope & Architecture

### In-Scope
- **Storefront Features:**
  - Homepage navigation, theme toggling (dark/light), hero banners, category highlights, footer links.
  - Product catalog (`/products`): grid layout, sale badges, pricing, stock levels.
  - Filtering & Sorting: category pills, dual-handle price range sliders, rating filters, sort options (`Newest`, `Price: low to high`, `Popularity`), and URL-based search (`?search=`).
  - Product Details Page (`/products/:slug`): image gallery, ratings, quantity selector, tabbed information (Description, Specifications, Reviews), `"Add to cart"`, `"Buy now"`, and `"Save"` (wishlist).
  - Shopping Cart (`/cart` & Cart Drawer): drawer modal, line item cards, quantity increment/decrement, line removal, subtotal calculation, promo code input.
  - Shipping & Financial Calculations: `$75.00` free shipping threshold, `$9.99` standard shipping fee, exact `8%` tax rate formula.
  - Checkout (`/checkout`): Stage 1 address form validation, 2-letter ISO country code validation, Stage 2 review step, and order placement.
  - Order Confirmation (`/orders/:id/confirmed`): order ID generation, estimated delivery date range, summary breakdown, address recap, and cart clearing.
  - Authentication (`/login`): Customer role redirection to `/account`, Admin role redirection to `/admin`.
  - Mobile Responsiveness: viewport scaling, mobile filter sheet toggle, full-width cart drawer.
- **Network / API Resilience:**
  - Fallback state verification when API calls return Netlify 404/405.
  - Mocked REST contract validation (`page.route()`) for 200/201 success and 500 error scenarios.

### Out-of-Scope
- Live third-party credit card gateway transactions (disabled on target with UI disclaimer).
- Production email notifications / SMS delivery (no live SMTP backend configured).
- Storefront search input field testing (verified to not exist in the DOM; covered via URL query parameter tests).

---

## 3. Automation Framework Architecture

```
northline-store-automation/
├── .github/
│   └── workflows/
│       └── e2e-ci.yml           # GitHub Actions CI matrix
├── docs/
│   ├── WEBSITE_DISCOVERY.md     # Comprehensive discovery findings
│   ├── API_INVENTORY.md         # API endpoints & network specs
│   └── TEST_PLAN.md             # Master QA Test Plan
├── framework/
│   ├── config.py                # Environment configs & URL constants
│   ├── pages/                   # Page Object Models (POM)
│   │   ├── base_page.py         # Common base methods & locators
│   │   ├── home_page.py         # Homepage & navigation
│   │   ├── products_page.py     # Catalog, filters, sorting
│   │   ├── product_detail_page.py # PDP interactions
│   │   ├── cart_page.py         # Cart drawer & /cart page
│   │   ├── checkout_page.py     # Multi-step checkout & validations
│   │   ├── order_confirm_page.py# Confirmation & receipt
│   │   ├── login_page.py        # Authentication & account
│   │   └── admin_page.py        # Admin views
│   └── fixtures/
│       └── mock_api.py          # Playwright route interception mocks
├── tests/
│   ├── conftest.py              # Pytest fixtures, browser context setup
│   ├── e2e/
│   │   ├── test_home_navigation.py
│   │   ├── test_catalog_and_pdp.py
│   │   ├── test_filters_and_search.py
│   │   ├── test_cart_management.py
│   │   ├── test_shipping_and_tax.py
│   │   ├── test_checkout_validation.py
│   │   ├── test_order_confirmation.py
│   │   ├── test_auth_and_roles.py
│   │   └── test_mobile_responsive.py
│   └── api/
│       └── test_api_contracts.py # Live & mocked API tests
├── pytest.ini                   # Pytest configuration & markers
└── requirements.txt             # Python dependencies
```

---

## 4. Stable UI Locators Dictionary

All selectors below have been verified against the live DOM on `https://ecomcicid.netlify.app`:

| Component | Target Element | Recommended Stable Locator | Description / Strategy |
| :--- | :--- | :--- | :--- |
| **Header** | Brand Logo | `header a[href="/"]` | Home link with text `"Northline"` |
| **Header** | Products Link | `header a[href="/products"]` | Catalog navigation |
| **Header** | Sign In Link | `header a[href="/login"]` | Auth navigation |
| **Header** | Account Link | `header a[href="/account"]` | Visible when authenticated |
| **Header** | Cart Button | `header button:has-text("Cart")` | Displays count e.g. `Cart (1)` |
| **Header** | Theme Toggle | `button[aria-label="Toggle theme"]` | Dark/Light mode switch |
| **Products**| Product Cards | `a[href^="/products/"]` | Links to individual PDPs |
| **Products**| Category Filter | `button:has-text("Living")` | Category buttons (`Living`, etc.) |
| **Products**| Min Price Range | `input[type="range"][aria-label="Minimum price"]` | Dual price slider min |
| **Products**| Max Price Range | `input[type="range"][aria-label="Maximum price"]` | Dual price slider max |
| **Products**| Rating Filter | `button:has-text("Any rating")` | Rating selector buttons |
| **Products**| Sort Dropdown | `button:has-text("Newest")` | Active sort menu trigger |
| **Products**| Mobile Filters | `button:has-text("Filters")` | Appears on `<1024px` viewports |
| **PDP** | Title Heading | `h1` | Product title |
| **PDP** | Price Tag | `main .font-semibold` | Displayed product price |
| **PDP** | Qty Decrement | `button[aria-label="Decrease quantity"]` | Lowers item count |
| **PDP** | Qty Increment | `button[aria-label="Increase quantity"]` | Increases item count |
| **PDP** | Add to Cart | `button:has-text("Add to cart")` | Primary CTA |
| **PDP** | Buy Now | `button:has-text("Buy now")` | Direct checkout CTA |
| **PDP** | Save / Wishlist | `button:has-text("Save")` | Wishlist toggle |
| **Cart** | Cart Drawer | `[role="dialog"]` | Slide-over drawer modal |
| **Cart** | Qty Decrement | `button[aria-label="Decrease quantity"]` | Decrement inside cart |
| **Cart** | Qty Increment | `button[aria-label="Increase quantity"]` | Increment inside cart |
| **Cart** | Remove Button | `button:has-text("Remove")` | Removes line item |
| **Cart** | Promo Code Input| `input[placeholder*="Promo" i]` | Optional promo code |
| **Cart** | Apply Promo | `button:has-text("Apply")` | Applies promo |
| **Cart** | Subtotal DL | `dt:has-text("Subtotal") + dd` | Subtotal amount display |
| **Cart** | Shipping DL | `dt:has-text("Shipping") + dd` | Displays `"Free"` or `"$9.99"` |
| **Cart** | Tax DL | `dt:has-text("Tax") + dd` | Exactly 8% of subtotal |
| **Cart** | Total DL | `dt:has-text("Total") + dd` | Total payable amount |
| **Cart** | Checkout Button | `button:has-text("Checkout")` | Proceeds to `/checkout` |
| **Checkout**| Address Line 1 | `#line1` or `input[name="line1"]` | Required street address |
| **Checkout**| Address Line 2 | `#line2` or `input[name="line2"]` | Optional suite/apt |
| **Checkout**| City | `#city` or `input[name="city"]` | Required city |
| **Checkout**| State | `#state` or `input[name="state"]` | Required/optional state |
| **Checkout**| Postal Code | `#postalCode` or `input[name="postalCode"]`| Required postal code |
| **Checkout**| Country | `#country` or `input[name="country"]` | Required 2-letter ISO code (`US`) |
| **Checkout**| Phone | `#phone` or `input[name="phone"]` | Optional contact phone |
| **Checkout**| Review Submit | `button[type="submit"]:has-text("Continue to review")` | Stage 1 submission |
| **Checkout**| Error Messages | `form p.text-xs` or `p.text-danger-600` | Validation alert messages |
| **Checkout**| Stage 2 Back | `button:has-text("Back")` | Reverts to Stage 1 |
| **Checkout**| Place Order | `button:has-text("Place order")` | Stage 2 order finalization |
| **Confirm** | Order Heading | `h1` (`Order confirmed`) | Success banner |
| **Confirm** | Order Number | `main :text-matches("ORD-LOCAL-")`| Unique receipt identifier |
| **Confirm** | Keep Shopping | `a:has-text("Keep shopping")` | Link to `/products` |

---

## 5. Detailed Test Suite Specifications

### Test Suite 1: Navigation & Header Controls
- **TC-NAV-001:** Verify homepage loads with correct title and branding.
- **TC-NAV-002:** Verify navigation to `/products` via header link and hero CTA.
- **TC-NAV-003:** Verify Dark/Light theme toggle updates DOM attributes and persists in `localStorage["ecom-ui"]`.
- **TC-NAV-004:** Verify footer links navigate to correct storefront and info routes.

### Test Suite 2: Product Catalog & Product Details
- **TC-CAT-001:** Verify all 6 products from `/catalog.json` render in grid with name, image, and price.
- **TC-CAT-002:** Verify discounted products (`Oak side table`, `Linen lounge chair`) display both current and strike-through compare prices.
- **TC-CAT-003:** Verify clicking product card navigates to `/products/:slug` with matching title and details.
- **TC-CAT-004:** Verify PDP tab navigation switches between Description, Specifications, and Reviews without page reload.
- **TC-CAT-005:** Verify PDP quantity selector increments and decrements quantity (minimum 1).

### Test Suite 3: Search, Filters & Sorting
- **TC-FLT-001:** Verify clicking category filter (`Living`) restricts visible products to 4 items.
- **TC-FLT-002:** Verify clicking `"All products"` resets category filter to 6 items.
- **TC-FLT-003:** Verify sorting by `"Price: low to high"` orders products ascending by price (`$86.00` to `$890.00`).
- **TC-FLT-004:** Verify sorting by `"Newest"` orders products descending by creation date.
- **TC-FLT-005:** Verify navigating to `/products?search=chair` filters catalog to `Linen lounge chair`.
- **TC-FLT-006:** Verify price range slider adjustments filter visible products within min/max bounds.

### Test Suite 4: Shopping Cart & Updates
- **TC-CRT-001:** Verify empty cart state shows `"Your cart is empty"` and link to shop.
- **TC-CRT-002:** Verify clicking `"Add to cart"` adds item, opens Cart Drawer, and increments header cart counter.
- **TC-CRT-003:** Verify incrementing quantity in cart recalculates line total and subtotal.
- **TC-CRT-004:** Verify decrementing quantity updates subtotal; does not drop below 1.
- **TC-CRT-005:** Verify clicking `"Remove"` removes line item and updates cart badge count.
- **TC-CRT-006:** Verify cart state persists across browser page reloads via `localStorage["ecom-cart"]`.

### Test Suite 5: Shipping & Financial Calculations
- **TC-FIN-001:** Verify single item cart ($\ge \$75.00$, e.g. Ceramic set at $\$86.00$) displays `"Free"` shipping.
- **TC-FIN-002:** Verify subtotal $<\$75.00$ calculates standard shipping fee of exactly `$$9.99$`.
- **TC-FIN-003:** Verify Tax calculation equals exactly $8\%$ ($0.08$) of effective subtotal.
- **TC-FIN-004:** Verify Total equals $\text{Effective Subtotal} + \text{Shipping} + \text{Tax}$ to 2 decimal places.

### Test Suite 6: Checkout Form & Validations
- **TC-CHK-001:** Verify submitting empty checkout form prevents progression and triggers required field errors:
  - `"Street address is required"`
  - `"City is required"`
  - `"Postal code is required"`
- **TC-CHK-002:** Verify entering non-2-letter country name triggers `"Use a 2-letter country code"`.
- **TC-CHK-003:** Verify entering valid address with country `"US"` successfully transitions to Stage 2 (`Review`).
- **TC-CHK-004:** Verify clicking `"Back"` from Stage 2 returns to Stage 1 with previously entered data intact.

### Test Suite 7: Order Confirmation & Receipt
- **TC-ORD-001:** Verify clicking `"Place order"` on Stage 2 places order and redirects to `/orders/:id/confirmed`.
- **TC-ORD-002:** Verify confirmation page displays unique order number matching pattern `ORD-LOCAL-YYYYMMDD-[A-Z0-9]+`.
- **TC-ORD-003:** Verify confirmation displays correct shipping address recap and estimated delivery window.
- **TC-ORD-004:** Verify cart is completely cleared after order placement (header badge resets to `"Cart"`).
- **TC-ORD-005:** Verify order is saved in `localStorage["ecom-local-orders"]`.

### Test Suite 8: Authentication & Role-Based Access
- **TC-AUT-001:** Verify customer login (`customer@example.com` / `Password123!`) redirects to `/account`.
- **TC-AUT-002:** Verify admin login (`admin@northline.com` / `Password123!`) redirects to `/admin`.
- **TC-AUT-003:** Verify user sign out clears session and updates header to `"Sign in"`.

### Test Suite 9: Mobile Responsiveness
- **TC-MOB-001:** Verify viewport 375x667 hides desktop filter sidebar and displays mobile `"Filters"` toggle button.
- **TC-MOB-002:** Verify clicking mobile `"Filters"` opens responsive filter sheet.
- **TC-MOB-003:** Verify checkout form stacks inputs vertically in single-column layout on mobile.

### Test Suite 10: API & Network Simulation
- **TC-API-001:** Verify live target offline resilience: app functions when write calls return 404/405.
- **TC-API-002:** Mock `POST /api/orders` returning `201 Created` with server order ID; verify UI handles real server orders.
- **TC-API-003:** Mock `POST /api/orders` returning `500 Server Error`; verify error banner is displayed.

---

## 6. CI/CD Pipeline Design

### GitHub Actions Workflow Matrix
- **Triggers:** Push to `main`, Pull Requests, and Scheduled Nightly runs.
- **Environment:** Ubuntu-latest / Windows-latest with Python 3.11+.
- **Browser Matrix:**
  - Chromium (Desktop 1280x800)
  - Firefox (Desktop 1280x800)
  - WebKit (Safari Desktop 1280x800)
  - Mobile Chrome (Pixel 5 simulation)
  - Mobile Safari (iPhone 13 simulation)
- **Artifacts:**
  - Playwright HTML Report (`playwright-report/`)
  - Trace viewer zip files for failed tests (`test-results/`)
  - Video recordings of test runs.

---

## 7. Entry, Exit, and Suspension Criteria

- **Entry Criteria:**
  - Python 3.11+ environment configured with Playwright and dependencies.
  - Target URL `https://ecomcicid.netlify.app/` accessible with HTTP 200.
  - Page Object Models and test data fixtures initialized.
- **Suspension Criteria:**
  - Target site unreachable (5xx gateway error or DNS failure).
  - Browser engine fails to launch in CI runner.
- **Exit Criteria:**
  - 100% of P0 and P1 test cases executed.
  - All critical user flows pass (catalog -> cart -> checkout -> confirmation).
  - All discovered anomalies documented in test reports.
