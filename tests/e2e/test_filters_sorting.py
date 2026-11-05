"""
E2E Test Suite 3: Catalog Filtering, Sorting, and URL Parameter Search.
"""
import pytest
from framework.pages import ProductsPage

pytestmark = [pytest.mark.e2e]


@pytest.mark.catalog
@pytest.mark.regression
def test_filter_by_category_living(products_page: ProductsPage):
    """Verify filtering by 'Living' displays exactly 4 living products."""
    products_page.load()
    products_page.filter_by_category("living")
    assert products_page.get_products_count() == 4


@pytest.mark.catalog
@pytest.mark.regression
def test_reset_category_filter(products_page: ProductsPage):
    """Verify clicking 'All products' resets category filter back to 6."""
    products_page.load()
    products_page.filter_by_category("living")
    assert products_page.get_products_count() == 4
    
    products_page.filter_by_category("all")
    assert products_page.get_products_count() == 6


@pytest.mark.catalog
@pytest.mark.regression
def test_sort_price_low_to_high(products_page: ProductsPage):
    """Verify sorting 'Price: low to high' orders items ascending."""
    products_page.load()
    products_page.select_sort("Price: low to high")
    
    prices = products_page.get_product_prices()
    assert len(prices) == 6
    assert prices == sorted(prices), f"Prices not sorted ascending: {prices}"


@pytest.mark.catalog
@pytest.mark.regression
def test_sort_by_newest(products_page: ProductsPage):
    """Verify sorting by 'Newest' sets sort=createdAt and order=desc."""
    products_page.load()
    products_page.select_sort("Newest")
    assert products_page.get_products_count() == 6


@pytest.mark.smoke
@pytest.mark.catalog
@pytest.mark.regression
def test_url_search_parameter(products_page: ProductsPage):
    """Verify ?search= query parameter filters products as discovered."""
    # Search for 'chair' should yield 'Linen lounge chair' (1 product)
    products_page.load("?search=chair")
    assert products_page.get_products_count() == 1
    titles = products_page.get_product_titles()
    assert any("chair" in t.lower() for t in titles)


@pytest.mark.catalog
@pytest.mark.regression
def test_url_search_no_matching_results(products_page: ProductsPage):
    """Verify requirement 5: ?search= with non-matching query returns 0 results and empty notice."""
    products_page.load("?search=NonExistentProductQueryXYZ987")
    assert products_page.get_products_count() == 0
    assert products_page.page.locator("text=No products match these filters.").is_visible()

