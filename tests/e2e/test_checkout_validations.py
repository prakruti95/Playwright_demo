"""
E2E Test Suite 6: Multi-Stage Checkout & Input Validations.
"""
import pytest
from framework.pages import CheckoutPage, ProductDetailPage
from framework.config import TEST_SHIPPING_ADDRESS


@pytest.mark.checkout
@pytest.mark.regression
def test_empty_checkout_validation_errors(pdp: ProductDetailPage, checkout_page: CheckoutPage):
    """Verify submitting empty shipping form displays required field errors."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    checkout_page.load()
    checkout_page.submit_shipping_form()
    
    errors = checkout_page.get_validation_errors()
    assert any("address is required" in e.lower() for e in errors), "Expected address required error"
    assert any("city is required" in e.lower() for e in errors), "Expected city required error"
    assert any("postal code is required" in e.lower() for e in errors), "Expected postal code required error"


@pytest.mark.checkout
@pytest.mark.regression
def test_invalid_country_code_validation(pdp: ProductDetailPage, checkout_page: CheckoutPage):
    """Verify entering full country name instead of 2-letter ISO triggers validation error."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    checkout_page.load()
    invalid_address = TEST_SHIPPING_ADDRESS.copy()
    invalid_address["country"] = "United States"  # Full name instead of US
    
    checkout_page.fill_shipping_address(invalid_address)
    checkout_page.submit_shipping_form()
    
    errors = checkout_page.get_validation_errors()
    assert any("2-letter" in e.lower() for e in errors), "Expected 'Use a 2-letter country code' error"


@pytest.mark.smoke
@pytest.mark.checkout
@pytest.mark.regression
def test_valid_shipping_submission_advances_to_review(pdp: ProductDetailPage, checkout_page: CheckoutPage):
    """Verify submitting valid shipping address advances to Stage 2 Review."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    checkout_page.load()
    checkout_page.fill_shipping_address(TEST_SHIPPING_ADDRESS)
    checkout_page.submit_shipping_form()
    
    assert checkout_page.is_review_stage_visible(), "Review stage (Place order button) should be visible"


@pytest.mark.checkout
@pytest.mark.regression
def test_back_button_returns_to_shipping_step(pdp: ProductDetailPage, checkout_page: CheckoutPage):
    """Verify Back button in Stage 2 returns to Stage 1 with values preserved."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    checkout_page.load()
    checkout_page.fill_shipping_address(TEST_SHIPPING_ADDRESS)
    checkout_page.submit_shipping_form()
    
    assert checkout_page.is_review_stage_visible()
    checkout_page.go_back_to_shipping()
    
    # Verify inputs are visible and retain values
    assert checkout_page.address_line1_input.is_visible()
    assert checkout_page.address_line1_input.input_value() == TEST_SHIPPING_ADDRESS["line1"]
