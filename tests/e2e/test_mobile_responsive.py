"""
E2E Test Suite 9: Mobile Responsive Viewport Testing (390x844 - iPhone / Android).
"""
import pytest
from playwright.sync_api import Page
from framework.pages import HomePage, ProductsPage, ProductDetailPage, CartPage

pytestmark = [pytest.mark.e2e]


@pytest.mark.mobile
@pytest.mark.regression
def test_mobile_header_layout(mobile_page: Page):
    """Verify essential navigation controls fit on mobile screen."""
    home = HomePage(mobile_page)
    home.load()
    
    assert home.logo.is_visible()
    assert home.cart_button.is_visible()
    assert home.theme_toggle_btn.is_visible()


@pytest.mark.mobile
@pytest.mark.regression
def test_mobile_filters_toggle_button(mobile_page: Page):
    """Verify mobile view exposes 'Filters' toggle button for sidebar drawer."""
    products = ProductsPage(mobile_page)
    products.load()
    
    assert products.mobile_filters_btn.is_visible(), "Mobile 'Filters' button should be visible"


@pytest.mark.mobile
@pytest.mark.regression
def test_mobile_cart_drawer_interaction(mobile_page: Page):
    """Verify adding item opens cart drawer covering mobile viewport."""
    pdp = ProductDetailPage(mobile_page)
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    assert pdp.cart_drawer.is_visible(), "Cart drawer should open on mobile"
    drawer_box = pdp.cart_drawer.bounding_box()
    assert drawer_box is not None
    assert drawer_box["width"] > 300, "Drawer should occupy full mobile width"
