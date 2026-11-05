"""
E2E Test Suite 7: Order Confirmation & Receipt Verification.
"""
import pytest
from framework.pages import CheckoutPage, ProductDetailPage, OrderConfirmationPage
from framework.config import TEST_SHIPPING_ADDRESS


@pytest.mark.smoke
@pytest.mark.checkout
@pytest.mark.regression
def test_place_order_creates_order_and_redirects(
    pdp: ProductDetailPage, 
    checkout_page: CheckoutPage, 
    order_confirm_page: OrderConfirmationPage
):
    """Verify placing order navigates to confirmation page."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    checkout_page.load()
    checkout_page.fill_shipping_address(TEST_SHIPPING_ADDRESS)
    checkout_page.submit_shipping_form()
    checkout_page.place_order()
    
    assert "/orders/" in order_confirm_page.get_current_url()
    assert "/confirmed" in order_confirm_page.get_current_url()
    assert order_confirm_page.is_confirmed()


@pytest.mark.checkout
@pytest.mark.regression
def test_order_confirmation_number_format(
    pdp: ProductDetailPage, 
    checkout_page: CheckoutPage, 
    order_confirm_page: OrderConfirmationPage
):
    """Verify order number matches ORD-LOCAL-YYYYMMDD-[A-Z0-9]+ format."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    checkout_page.load()
    checkout_page.fill_shipping_address(TEST_SHIPPING_ADDRESS)
    checkout_page.submit_shipping_form()
    checkout_page.place_order()
    
    order_num = order_confirm_page.get_order_number()
    assert order_num is not None, "Order number must be present"
    assert order_num.startswith("ORD-LOCAL-"), f"Unexpected order number format: {order_num}"


@pytest.mark.checkout
@pytest.mark.regression
def test_cart_is_cleared_after_order_placement(
    pdp: ProductDetailPage, 
    checkout_page: CheckoutPage, 
    order_confirm_page: OrderConfirmationPage
):
    """Verify shopping cart badge resets to 0 items after placing order."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    checkout_page.load()
    checkout_page.fill_shipping_address(TEST_SHIPPING_ADDRESS)
    checkout_page.submit_shipping_form()
    checkout_page.place_order()
    
    # Header cart counter should reset
    assert order_confirm_page.get_cart_badge_count() == 0, "Cart badge should be empty after order"
