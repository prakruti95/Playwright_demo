"""
E2E Test Suite 4: Shopping Cart, Drawer, Quantity Updates, and Item Removal.
"""
import pytest
from framework.pages import CartPage, ProductDetailPage

pytestmark = [pytest.mark.e2e]


@pytest.mark.cart
@pytest.mark.regression
def test_cart_empty_state(cart_page: CartPage):
    """Verify empty cart displays notice and link to shop."""
    cart_page.navigate("/cart")
    cart_page.clear_local_storage()
    cart_page.load()
    cart_page.empty_cart_msg.wait_for(state="visible", timeout=5000)
    assert cart_page.is_empty(), "Cart should display empty state"
    assert cart_page.continue_shopping_link.is_visible()


@pytest.mark.smoke
@pytest.mark.cart
@pytest.mark.regression
def test_add_product_to_cart_and_drawer(pdp: ProductDetailPage, cart_page: CartPage):
    """Verify adding product opens drawer and updates header count."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    # Drawer modal should appear
    assert pdp.cart_drawer.is_visible(), "Cart drawer should open on add to cart"
    assert pdp.get_cart_badge_count() >= 1, "Header cart counter should be >= 1"


@pytest.mark.cart
@pytest.mark.regression
def test_cart_quantity_increment(cart_page: CartPage, pdp: ProductDetailPage):
    """Verify incrementing item quantity updates subtotal."""
    # Add ceramic set ($86.00)
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    cart_page.load()
    initial_subtotal = cart_page.get_subtotal()
    
    cart_page.increment_item(0)
    new_subtotal = cart_page.get_subtotal()
    
    assert new_subtotal > initial_subtotal, f"Subtotal should increase: {new_subtotal} > {initial_subtotal}"


@pytest.mark.cart
@pytest.mark.regression
def test_cart_remove_line_item(cart_page: CartPage, pdp: ProductDetailPage):
    """Verify removing item removes line from cart."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    
    cart_page.load()
    count_before = cart_page.get_items_count()
    assert count_before >= 1
    
    cart_page.remove_item(0)
    count_after = cart_page.get_items_count()
    assert count_after == count_before - 1


@pytest.mark.smoke
@pytest.mark.cart
@pytest.mark.regression
def test_cart_persistence_across_page_reload(pdp: ProductDetailPage, cart_page: CartPage):
    """Verify requirement 17: Cart items and quantities persist across browser page reload via localStorage."""
    pdp.load("ceramic-pour-over-set")
    pdp.add_to_cart()
    assert pdp.get_cart_badge_count() >= 1

    cart_page.load()
    items_before = cart_page.get_items_count()
    subtotal_before = cart_page.get_subtotal()
    assert items_before >= 1

    # Reload page and verify state persistence
    cart_page.page.reload()
    cart_page.page.wait_for_load_state("networkidle")

    items_after = cart_page.get_items_count()
    subtotal_after = cart_page.get_subtotal()
    assert items_after == items_before, f"Item count mismatch after reload: {items_after} vs {items_before}"
    assert subtotal_after == subtotal_before, f"Subtotal mismatch after reload: {subtotal_after} vs {subtotal_before}"

