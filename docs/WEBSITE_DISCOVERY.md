# Website Discovery Report: Northline Store

**Target URL:** [https://ecomcicid.netlify.app/](https://ecomcicid.netlify.app/)  
**Date of Discovery:** November 5, 2026  
**Auditor:** Senior QA Automation Engineer  
**Technology Stack Discovered:**
- **Frontend:** React SPA (Vite bundle), React Router, Tailwind CSS, Lucide icons, Zustand state management with `localStorage` persistence (`ecom-cart`, `ecom-local-orders`, `ecom-ui`, `ecom-auth`).
- **Hosting / CDN:** Netlify Edge (Static hosting with 200 rewrite SPA fallback).
- **Static Assets:** `/catalog.json` (6 products, 4 categories), Unsplash CDN images, Google Fonts (Inter).
- **Backend / API Behavior:** The SPA issues REST requests to `/api/*` endpoints. Because the Netlify deployment lacks active serverless functions for write routes (`POST`, `PATCH`, `DELETE`), Netlify returns `200 text/html` (SPA fallback) on GETs, `404 text/html` on unmapped POSTs, and `405 text/plain` on PATCH/DELETE. The frontend implements an offline/resilient fallback architecture (`isOfflineOrNetworkError` handler) that seamlessly persists cart operations, checkouts, and local orders (`ORD-LOCAL-YYYYMMDD-XXXXXX`) in browser `localStorage`.

---

## 1. Homepage & Navigation

### URL & Structure
- **URL:** `https://ecomcicid.netlify.app/`
- **Page Title:** `Quiet luxury for winter living · Northline`

### Navigation Header
- **Logo / Brand Link:** Anchor link to `/` with text `"Northline"`.
- **Products Link:** Anchor link to `/products` with text `"Products"`.
- **Sign In Link:** Anchor link to `/login` with text `"Sign in"` (changes to `"Account"` link to `/account` upon authentication).
- **Cart Button:** Header button with dynamic item count badge (e.g. `"Cart"` or `"Cart (1)"`). Clicking triggers the Cart Drawer modal (`role="dialog"`).
- **Theme Toggle Button:** Button with `aria-label="Toggle theme"` switching between dark and light themes (persisted in `localStorage["ecom-ui"]`).

### Hero & Banner Sections
- **Hero Title:** `"Quiet luxury, designed for modern homes."`
- **Hero CTAs:**
  - `"Shop the collection"` -> Link to `/products`
  - `"View new arrivals"` -> Link to `/products?sort=createdAt`
- **Editor's Pick Card:** Displays featured product `"Atelier daybed · from $890"`.
- **Featured Pieces Grid:** Displays 4 featured products with sale/compare prices and direct links to `/products/:slug`:
  - `Linen lounge chair` (`$640.00`, was `$780.00`)
  - `Ceramic pour-over set` (`$86.00`)
  - `Wool throw blanket` (`$128.00`)
  - `Oak side table` (`$320.00`, was `$390.00`)
- **Category Navigation Cards ("Shop by room"):**
  - Living (`/products?category=living`)
  - Apparel (`/products?category=apparel`)
  - Objects (`/products?category=objects`)
  - Wellness (`/products?category=wellness`)
- **Social Proof / Testimonials:** 3 quote cards from interior designers/studios.
- **Newsletter Subscription:** Input field with `aria-label="Email address"` and `"Subscribe"` button.

### Footer
- **Shop Links:** `"All products"`, `"New arrivals"`, `"Cart"`.
- **Company Links:** `"About"`, `"Design system"` (`/styleguide`), `"Account"`.
- **Support Links:** `"Sign in"` (`/login`), `"Create account"` (`/register`), `"Reset password"` (`/reset-password`).
- **Payment Method Badges:** VISA, MASTERCARD, AMEX, PAYPAL indicators.
- **Copyright:** `© 2026 Northline Commerce. All rights reserved.`

---

## 2. Product Listing & Product Details

### Product Catalog (`/products`)
- **URL:** `https://ecomcicid.netlify.app/products`
- **Page Title:** `Products · Northline`
- **Product Count:** Exactly 6 active items in `/catalog.json`:
  1. `Organic cotton overshirt` (`/products/organic-cotton-overshirt`) — Category: Apparel, Price: `$165.00`, Stock: 22.
  2. `Atelier daybed` (`/products/atelier-daybed`) — Category: Living, Price: `$890.00`, Stock: 4.
  3. `Oak side table` (`/products/oak-side-table`) — Category: Living, Price: `$320.00` (was `$390.00`), Stock: 9.
  4. `Wool throw blanket` (`/products/wool-throw-blanket`) — Category: Living, Price: `$128.00`, Stock: 28.
  5. `Ceramic pour-over set` (`/products/ceramic-pour-over-set`) — Category: Objects, Price: `$86.00`, Stock: 40.
  6. `Linen lounge chair` (`/products/linen-lounge-chair`) — Category: Living, Price: `$640.00` (was `$780.00`), Stock: 12.
- **Product Card Elements:**
  - Product Image (`img` with optimized CDN URL).
  - Category tag pill (e.g., `Living`, `Apparel`, `Objects`).
  - Product Name (clickable anchor).
  - Current Price & Strike-through Compare-At Price (when discounted).

### Product Details Page (`/products/:slug`)
- **URL Pattern:** `https://ecomcicid.netlify.app/products/<product-slug>`
- **Page Title:** `<Product Name> · Northline`
- **Main Heading:** `h1` with exact product name.
- **Gallery:** Large featured image with thumbnail preview buttons.
- **Rating Display:** 5 star buttons (`aria-label="1 star"` through `"5 stars"`).
- **Price Display:** Prominent formatted currency (e.g. `$86.00`).
- **Quantity Selector:**
  - Decrement button: `button[aria-label="Decrease quantity"]`
  - Current quantity indicator text
  - Increment button: `button[aria-label="Increase quantity"]`
- **Action Buttons:**
  - `"Add to cart"`: Adds item to cart, increments header badge count, and triggers the Cart Drawer.
  - `"Buy now"`: Adds item to cart and immediately navigates to `/checkout`.
  - `"Save"`: Adds product to wishlist (persisted in `localStorage["ecom-wishlist"]`).
- **Tabbed Information:**
  - `"Description"` (Active tab with product overview).
  - `"Specifications"` (Dimensions, materials, care instructions).
  - `"Reviews"` (Customer reviews and ratings list).

---

## 3. Search, Filter, and Sorting

### Search Functionality
- **Storefront Findings:** There is **no visible text input field for search** in the storefront header or `/products` main view.
- **URL Parameter Search:** The storefront controller (`Products-Oqk6aOGQ.js`) explicitly checks for `a.get("search")`.
  - Navigating to `/products?search=chair` executes in-memory filtering against product names and descriptions, reducing the visible list to `Linen lounge chair` (1 item).
  - Passing `?search=ceramic` displays `Ceramic pour-over set`.
- **Admin Search:** The Admin Product view (`/admin/products`) includes a dedicated search input: `input[name="product-search"][placeholder="Search name or description"]`.

### Category Filters
- Filter options available on `/products`:
  - `"All products"` (resets category filter).
  - `"Living"` (filters to 4 living products: daybed, side table, blanket, chair).
  - `"Apparel"` (filters to 1 apparel product: overshirt).
  - `"Objects"` (filters to 1 object: pour-over set).
  - `"Wellness"` (0 items currently in catalog).
- UI Elements: Plain buttons inside sidebar; active category receives `bg-neutral-100 font-medium`.

### Price Range Filters
- Dual slider range inputs:
  - Minimum price: `input[type="range"][aria-label="Minimum price"]` (min: 0, max: 2000).
  - Maximum price: `input[type="range"][aria-label="Maximum price"]` (min: 0, max: 2000).
- Slider changes trigger real-time filtering of visible products.

### Rating Filters
- Buttons:
  - `"Any rating"` (default).
  - Star ratings: `4 & up`, `3 & up`, `2 & up`.

### Sorting
- Sort trigger button displaying current sort (default: `"Newest"`).
- Clicking opens a dropdown menu with 3 options:
  1. `"Newest"` (`sort=createdAt`, `order=desc`)
  2. `"Price: low to high"` (`sort=price`, `order=asc`)
  3. `"Popularity"` (`sort=popularity`, `order=desc`)
- Selecting an option re-orders the product grid and updates the query parameters.

---

## 4. Shopping Cart & Quantity Updates

### Cart Drawer & Cart Page
- **Cart Drawer:** Triggered by clicking header `"Cart"` button or clicking `"Add to cart"` on PDP. Rendered in a fixed overlay modal (`role="dialog"`).
- **Dedicated Cart Page:** Accessible at `/cart`.
- **Empty State:** When no items exist, shows `"Your cart is empty. Continue shopping"` with link to `/products`.

### Cart Line Item Controls
- **Item Details:** Thumbnail image, product name (linked to PDP), unit price.
- **Quantity Increment:** `button[aria-label="Increase quantity"]`.
- **Quantity Decrement:** `button[aria-label="Decrease quantity"]`. Prevents decrements below 1.
- **Remove Button:** Button labeled `"Remove"`. Completely deletes the line item from cart.
- **Live Calculations:**
  - Line Total = `unitPrice * quantity`
  - Subtotal = Sum of all line totals.

### Promo Code Field
- Text input inside cart summary.
- `"Apply"` button: Stores code in `cart.promoCode` state.
- Discovered promo message: `"Free shipping over $75.00. Promo codes apply at checkout."`

---

## 5. Shipping & Financial Calculations

### Calculation Rules (Discovered from bundle source `xA(subtotal, discount)`):
- **Free Shipping Threshold (`jy`):** `$75.00`
- **Standard Shipping Rate (`EA`):** `$9.99` (applies if `subtotal - discount < $75.00`)
- **Tax Rate (`SA`):** Exactly `8%` (`0.08`) applied on taxable amount `(subtotal - discount)`.
- **Formulas:**
  $$\text{Effective Subtotal} = \max(\text{Subtotal} - \text{Discount}, 0)$$
  $$\text{Shipping} = \begin{cases} \$0.00 & \text{if Effective Subtotal} \ge \$75.00 \\ \$9.99 & \text{if Effective Subtotal} < \$75.00 \end{cases}$$
  $$\text{Tax} = \text{Effective Subtotal} \times 0.08$$
  $$\text{Total} = \text{Effective Subtotal} + \text{Shipping} + \text{Tax}$$

*Note:* All 6 products in `/catalog.json` have unit prices $> \$75.00$, qualifying any single-item cart for free shipping. If a future item is $<\$75.00$ or discount drops subtotal $<\$75.00$, the $\$9.99$ shipping fee applies automatically.

---

## 6. Checkout & Form Validation

### Multi-Step Checkout Flow (`/checkout`)
The checkout flow consists of 2 stages indicated by breadcrumbs `1 Shipping / 2 Review`:

#### Stage 1: Shipping Address Form
- **Form Inputs:**
  - `Address`: `#line1` / `input[name="line1"]`
  - `Apartment, suite (optional)`: `#line2` / `input[name="line2"]`
  - `City`: `#city` / `input[name="city"]`
  - `State`: `#state` / `input[name="state"]`
  - `Postal code`: `#postalCode` / `input[name="postalCode"]`
  - `Country`: `#country` / `input[name="country"]` (Helper caption: `"ISO code, e.g. US"`)
  - `Phone (optional)`: `#phone` / `input[name="phone"]`
- **Submit Button:** `button[type="submit"]:has-text("Continue to review")`.

#### Validation Rules (Verified by form submission):
- Submitting empty form yields inline error messages:
  - `"Street address is required"`
  - `"City is required"`
  - `"Postal code is required"`
- Submitting Country with full name (e.g. `"United States"`) triggers:
  - `"Use a 2-letter country code"` (Strict 2-letter uppercase requirement, e.g. `US`, `CA`, `GB`).

#### Stage 2: Review & Confirmation
- Upon valid Stage 1 submission, UI switches to Step 2.
- Displays summary of shipping address:
  - Address, City, State, Postal Code, Country.
- Notice: `"Card checkout is not enabled. Confirm the address and place the order — nothing will be charged."`
- Navigation Buttons:
  - `"Back"`: Returns to Stage 1 to edit address details.
  - `"Place order · $<Total>"`: Triggers order finalization.

---

## 7. Order Confirmation

### Order Finalization Behavior
- Clicking `"Place order · $<Total>"`:
  - Dispatches `POST /api/orders`.
  - Fallback handler creates a unique local order record in `localStorage["ecom-local-orders"]`.
  - Generates unique ID `local-<UUID>` and formatted Order Number: `ORD-LOCAL-YYYYMMDD-<SHORTID>` (e.g. `ORD-LOCAL-20261105-35BE0C`).
  - Clears shopping cart (`ecom-cart` resets to `items: []`, `itemCount: 0`).
  - Redirects browser to `/orders/:orderId/confirmed`.

### Confirmation Page Details (`/orders/:orderId/confirmed`)
- **Main Heading:** `"Order confirmed"` / `"Thank you"`.
- **Status Subtext:** `"Order ORD-LOCAL-YYYYMMDD-XXXXXX is paid. Estimated delivery Tue, Nov 10 – Fri, Nov 13."`
- **Summary Breakdown:**
  - Items list with unit prices and quantities.
  - Subtotal, Shipping (`Free` or `$9.99`), Tax (8%), and Total.
- **Shipping Address Recap:** Ships to address entered during checkout.
- **CTAs:**
  - `"View orders"` -> Navigates to `/account/orders` (or local order history).
  - `"Keep shopping"` -> Navigates to `/products`.

---

## 8. Mobile Responsive Behaviour

### Viewport Observations (Tested at 375x667, 390x844):
- **Header:**
  - Brand Logo, Cart Button, and Theme Toggle remain visible and accessible in the mobile top bar.
  - Nav links wrap or collapse gracefully into the responsive header bar.
- **Products Catalog:**
  - Desktop sidebar filter panel is hidden.
  - Mobile filter toggle button appears: `button:has-text("Filters")` (`lg:hidden`).
  - Clicking `"Filters"` displays a responsive drawer/sheet with all category, price, and rating controls.
- **Cart Drawer:**
  - Drawer width expands to full mobile viewport width (`100vw`), maintaining 44px+ tap targets for quantity increment/decrement and remove buttons.
- **Checkout & Confirmation:**
  - Form fields transition from 2-column grid (`sm:grid-cols-2`) to single-column layout for easy touch input.

---

## 9. Customer & Admin Authentication

### Authentication System (`/login`)
- **Inputs:** `input[type="email"]`, `input[type="password"]`.
- **Submit Button:** `button[type="submit"]:has-text("Sign in")`.
- **Authentication Roles:**
  - **Admin Login:** Using any email containing `"admin"` (e.g. `admin@northline.com` / `Password123!`) redirects to `/admin` dashboard.
  - **Customer Login:** Any other valid email (e.g. `customer@example.com` / `Password123!`) logs in with `CUSTOMER` role and redirects to `/account`.
- **Account Pages:**
  - `/account` (Profile management)
  - `/account/orders` (Order history)
  - `/account/addresses` (Saved addresses)
  - `/account/wishlist` (Saved products)
- **Admin Pages:**
  - `/admin` (Metrics & KPI summary)
  - `/admin/products` (Catalog management with dedicated search bar)
  - `/admin/orders` (Store order management)
  - `/admin/customers` (Customer list)
  - `/admin/categories` (Category management)
  - `/admin/settings` (Store configuration)

---

## 10. Summary of Features That Cannot Be Inspected on Live Target

1. **Live Stripe / Gateway Card Processing:** Live payment capture cannot be tested because card checkout is intentionally disabled by the application with notice `"Card checkout is not enabled. Confirm the address and place the order — nothing will be charged."`
2. **Server-Side Order Webhooks / Notifications:** No external webhooks or email delivery mechanisms fire because Netlify serves static assets without serverless database integrations.
3. **Storefront Search Input Element:** Cannot inspect a search box on `/products` because none exists in the DOM; search functionality is strictly URL parameter-driven (`?search=...`).
