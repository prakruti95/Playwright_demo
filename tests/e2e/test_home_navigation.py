"""
E2E Test Suite 1: Homepage, Navigation, Branding, and Theme Toggle.
"""
import pytest
from framework.pages import HomePage

pytestmark = [pytest.mark.e2e]


@pytest.mark.smoke
@pytest.mark.regression
def test_homepage_title_and_branding(home_page: HomePage):
    """Verify homepage title and brand logo visibility."""
    home_page.load()
    assert "Northline" in home_page.get_title(), "Expected 'Northline' in homepage title"
    assert home_page.logo.is_visible(), "Brand logo must be visible in header"


@pytest.mark.smoke
@pytest.mark.regression
def test_header_navigation_links(home_page: HomePage):
    """Verify header links navigate to expected routes."""
    home_page.load()
    
    # Click Products link
    home_page.products_link.click()
    home_page.page.wait_for_load_state("networkidle")
    assert "/products" in home_page.get_current_url()

    # Click Logo to return home
    home_page.logo.click()
    home_page.page.wait_for_load_state("networkidle")
    assert home_page.get_current_url().rstrip("/").endswith("netlify.app")


@pytest.mark.regression
def test_dark_light_theme_toggle(home_page: HomePage):
    """Verify switching dark and light theme updates HTML class."""
    home_page.load()
    initial_dark = home_page.is_dark_mode()
    
    # Toggle theme
    home_page.toggle_theme()
    assert home_page.is_dark_mode() != initial_dark, "Theme should toggle state"

    # Toggle back
    home_page.toggle_theme()
    assert home_page.is_dark_mode() == initial_dark, "Theme should return to initial state"


@pytest.mark.regression
def test_hero_cta_navigation(home_page: HomePage):
    """Verify hero CTAs navigate to catalog with proper parameters."""
    home_page.load()
    home_page.click_shop_collection()
    assert "/products" in home_page.get_current_url()

    home_page.load()
    home_page.click_new_arrivals()
    assert "sort=createdAt" in home_page.get_current_url()


@pytest.mark.regression
def test_invalid_url_route_behavior(home_page: HomePage):
    """Verify requirement 20: Navigating to unknown URL returns SPA shell without crash."""
    response = home_page.navigate("/non-existent-page-404")
    assert response is not None
    assert response.status == 200, "Netlify SPA catch-all serves HTTP 200 index.html shell"
    assert "/non-existent-page-404" in home_page.get_current_url()

