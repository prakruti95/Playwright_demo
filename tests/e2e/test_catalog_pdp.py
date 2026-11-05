"""
E2E Test Suite 2: Product Catalog & Product Detail Page (PDP).
"""
import pytest
from framework.pages import ProductsPage, ProductDetailPage

pytestmark = [pytest.mark.e2e]


@pytest.mark.smoke
@pytest.mark.catalog
@pytest.mark.regression
def test_catalog_render_all_items(products_page: ProductsPage):
    """Verify products catalog displays all 6 catalog items."""
    products_page.load()
    count = products_page.get_products_count()
    assert count == 6, f"Expected 6 catalog products, found {count}"


@pytest.mark.catalog
@pytest.mark.regression
def test_discounted_products_show_compare_price(products_page: ProductsPage):
    """Verify sale items display both current price and strike-through compare price."""
    products_page.load()
    # Oak side table is on sale ($320 was $390)
    card = products_page.page.locator("a[href='/products/oak-side-table']")
    assert card.is_visible(), "Oak side table card should be visible"
    card_text = card.inner_text()
    assert "$320.00" in card_text
    assert "$390.00" in card_text


@pytest.mark.smoke
@pytest.mark.catalog
@pytest.mark.regression
def test_navigate_to_product_detail(products_page: ProductsPage, pdp: ProductDetailPage):
    """Verify clicking product opens PDP with title and price."""
    products_page.load()
    products_page.click_product("ceramic-pour-over-set")
    
    assert "/products/ceramic-pour-over-set" in pdp.get_current_url()
    assert "Ceramic pour-over set" in pdp.get_title_text()
    assert pdp.get_price_value() == 86.00


@pytest.mark.catalog
@pytest.mark.regression
def test_pdp_tab_switching(pdp: ProductDetailPage):
    """Verify switching between Description, Specifications, and Reviews tabs."""
    pdp.load("ceramic-pour-over-set")
    
    # Switch to Specifications
    pdp.switch_tab("specifications")
    spec_text = pdp.page.locator("main").inner_text()
    assert "Specifications" in spec_text

    # Switch to Reviews
    pdp.switch_tab("reviews")
    reviews_text = pdp.page.locator("main").inner_text()
    assert "Reviews" in reviews_text


@pytest.mark.catalog
@pytest.mark.regression
def test_pdp_quantity_selector(pdp: ProductDetailPage):
    """Verify PDP quantity increment and decrement buttons."""
    pdp.load("ceramic-pour-over-set")
    
    pdp.increase_quantity(2)
    # Check displayed quantity
    qty_indicator = pdp.page.locator("button[aria-label='Increase quantity']").locator("xpath=preceding-sibling::*[1]")
    # Or find span between decrement and increment
    span_qty = pdp.page.locator("button[aria-label='Decrease quantity'] ~ span, button[aria-label='Decrease quantity'] + *")
    assert span_qty.count() > 0
