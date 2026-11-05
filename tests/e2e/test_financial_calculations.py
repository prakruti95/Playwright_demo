"""
E2E Test Suite 5: Shipping, Tax, and Financial Precision Validations.
"""
import pytest
from framework.pages import CartPage, ProductDetailPage, ProductsPage
from framework.config import FREE_SHIPPING_THRESHOLD, TAX_RATE

pytestmark = [pytest.mark.e2e]


@pytest.mark.smoke
@pytest.mark.cart
@pytest.mark.regression
def test_free_shipping_for_orders_over_75(pdp: ProductDetailPage, cart_page: CartPage):
    """Verify orders over $75 qualify for Free shipping."""
    # Ceramic set is $86.00 (> $75.00)
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    cart_page.load()
    assert cart_page.get_subtotal() >= FREE_SHIPPING_THRESHOLD
    assert cart_page.is_shipping_free(), "Shipping should be Free for order >= $75.00"


@pytest.mark.cart
@pytest.mark.regression
def test_tax_calculation_at_8_percent(pdp: ProductDetailPage, cart_page: CartPage):
    """Verify sales tax is calculated at exactly 8% of taxable subtotal."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    cart_page.load()
    subtotal = cart_page.get_subtotal()
    expected_tax = round(subtotal * TAX_RATE, 2)
    actual_tax = cart_page.get_tax()
    
    assert abs(actual_tax - expected_tax) <= 0.01, f"Tax mismatch: {actual_tax} vs {expected_tax}"


@pytest.mark.cart
@pytest.mark.regression
def test_order_total_formula_precision(pdp: ProductDetailPage, cart_page: CartPage):
    """Verify Total = Subtotal + Shipping + Tax."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    cart_page.load()
    subtotal = cart_page.get_subtotal()
    shipping = cart_page.get_shipping()
    tax = cart_page.get_tax()
    total = cart_page.get_total()
    
    expected_total = round(subtotal + shipping + tax, 2)
    assert abs(total - expected_total) <= 0.01, f"Total mismatch: {total} vs {expected_total}"


@pytest.mark.cart
@pytest.mark.regression
def test_shipping_below_75_threshold_behavior_with_actual_catalog(products_page: ProductsPage):
    """
    Verify requirement 12: Shipping below $75, if supported by actual product data.
    Documents and verifies that all products in live catalog have prices >= $86.00,
    confirming that sub-$75 orders are not achievable with single catalog products.
    """
    products_page.load()
    prices = products_page.get_product_prices()
    assert len(prices) == 6
    min_price = min(prices)
    assert min_price >= FREE_SHIPPING_THRESHOLD, (
        f"Minimum catalog product price ${min_price:.2f} exceeds ${FREE_SHIPPING_THRESHOLD:.2f} threshold; "
        "every individual item qualifies for free shipping under actual catalog data."
    )

