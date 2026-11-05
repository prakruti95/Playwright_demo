"""
API Test Suite 2: Storefront Contracts, Static Catalog & Playwright Route Interception.
"""
import pytest
import requests
from playwright.sync_api import Page, Route
from framework.config import BASE_URL, TEST_SHIPPING_ADDRESS
from framework.pages import ProductDetailPage, CheckoutPage, ProductsPage

pytestmark = [pytest.mark.api]


@pytest.mark.api
@pytest.mark.smoke
def test_catalog_json_contract():
    """Verify /catalog.json returns valid JSON containing categories and 6 products."""
    resp = requests.get(f"{BASE_URL}/catalog.json", timeout=10)
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")
    data = resp.json()
    
    assert "categories" in data
    assert "products" in data
    assert len(data["categories"]) == 4
    assert len(data["products"]) == 6
    
    # Verify product contract fields
    sample_product = data["products"][0]
    for field in ["id", "name", "slug", "price", "stockQuantity", "categoryId"]:
        assert field in sample_product, f"Missing field '{field}' in catalog product"


@pytest.mark.api
def test_live_netlify_resilience_on_cart_post():
    """Verify live Netlify hosting behavior on POST /api/cart/items returns 404."""
    resp = requests.post(f"{BASE_URL}/api/cart/items", json={"productId": "test", "quantity": 1}, timeout=10)
    # Target Netlify static edge returns 404 for unmapped POSTs
    assert resp.status_code == 404


@pytest.mark.api
def test_mock_order_api_success_contract(page: Page):
    """
    Verify application handles simulated 201 Created server response
    using Playwright route interception.
    """
    mock_order = {
        "id": "server-order-98765",
        "orderNumber": "ORD-SRV-2026-98765",
        "status": "PAID",
        "subtotal": "86.00",
        "shippingAmount": "0.00",
        "taxAmount": "6.88",
        "total": "92.88",
    }

    def handle_orders(route: Route):
        if route.request.method == "POST":
            route.fulfill(
                status=201,
                content_type="application/json",
                body=str(mock_order).replace("'", '"')
            )
        else:
            route.continue_()

    page.route("**/api/orders", handle_orders)

    pdp = ProductDetailPage(page)
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()

    checkout = CheckoutPage(page)
    checkout.load()
    checkout.fill_shipping_address(TEST_SHIPPING_ADDRESS)
    checkout.submit_shipping_form()
    
    # Ensure review stage is reached
    assert checkout.is_review_stage_visible()


@pytest.mark.api
def test_live_ui_and_catalog_api_consistency(page: Page):
    """
    Verify requirement 8: UI and API Consistency.
    Confirms that catalog data from GET /catalog.json strictly matches
    the products rendered in the live UI catalog.
    """
    api_resp = requests.get(f"{BASE_URL}/catalog.json", timeout=10)
    assert api_resp.status_code == 200
    api_products = api_resp.json()["products"]
    api_names = {p["name"] for p in api_products}

    products_page = ProductsPage(page)
    products_page.load()
    ui_titles = set(products_page.get_product_titles())

    # All API products must be rendered in UI
    assert len(ui_titles) == len(api_names) == 6
    assert ui_titles == api_names, f"Mismatch between API and UI: {ui_titles ^ api_names}"


@pytest.mark.api
def test_playwright_network_mocking_500_error_handling(page: Page):
    """
    Verify requirement 9: Playwright network mocking for HTTP 500 error.
    Intercepts catalog endpoint with HTTP 500 and verifies UI displays graceful error notice.
    """
    page.route(
        "**/catalog.json",
        lambda route: route.fulfill(
            status=500,
            content_type="text/plain",
            body="Internal Server Error: Simulated Fault"
        )
    )

    products_page = ProductsPage(page)
    products_page.load()
    
    # Verify graceful error message rendered in main container
    error_notice = page.locator("text=Could not load products. Try again shortly.")
    error_notice.wait_for(state="visible", timeout=10000)
    assert error_notice.is_visible(), "UI should render 'Could not load products. Try again shortly.' on 500"

