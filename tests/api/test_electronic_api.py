"""
API Test Suite 1: Supplied Electronic API Validation.
Endpoint: https://681444af225ff1af16285b31.mockapi.io/electronicapi
"""
import pytest
import requests
from framework.config import MOCK_API_BASE_URL

pytestmark = [pytest.mark.api]


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_electronics_status_and_count():
    """Verify GET /electronicapi returns 200 and a non-empty list of products."""
    resp = requests.get(MOCK_API_BASE_URL, timeout=10)
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 20, f"Expected at least 20 items, got {len(data)}"


@pytest.mark.api
def test_get_single_product_by_id_schema():
    """Verify GET /electronicapi/:id returns expected data schema."""
    resp = requests.get(f"{MOCK_API_BASE_URL}/1", timeout=10)
    assert resp.status_code == 200
    item = resp.json()
    
    required_keys = ["id", "name", "price", "description", "category", "brand", "stock", "createdAt"]
    for key in required_keys:
        assert key in item, f"Missing key '{key}' in product response"
    assert item["id"] == "1"


@pytest.mark.api
def test_pagination_with_page_and_limit():
    """Verify ?page=1&limit=5 returns exactly 5 items."""
    resp = requests.get(f"{MOCK_API_BASE_URL}?page=1&limit=5", timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 5, f"Expected 5 items, got {len(data)}"


@pytest.mark.api
def test_filter_by_category_headphones():
    """Verify filtering by ?category=Headphones returns only Headphones."""
    resp = requests.get(f"{MOCK_API_BASE_URL}?category=Headphones", timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    for item in data:
        assert item.get("category") == "Headphones"


@pytest.mark.api
def test_search_by_brand_query():
    """Verify ?search=Sony returns matching brand or product items."""
    resp = requests.get(f"{MOCK_API_BASE_URL}?search=Sony", timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert any("sony" in (item.get("brand") or "").lower() or "sony" in (item.get("name") or "").lower() for item in data)


@pytest.mark.api
def test_sort_by_price_descending():
    """Verify ?sortBy=price&order=desc queries MockAPI and returns sorted products."""
    resp = requests.get(f"{MOCK_API_BASE_URL}?sortBy=price&order=desc&page=1&limit=10", timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 1
    # MockAPI stores price as string and sorts lexicographically
    price_strings = [str(item["price"]) for item in data if item.get("price")]
    assert price_strings == sorted(price_strings, reverse=True), "MockAPI sorts string price values in descending order"


@pytest.mark.api
def test_create_new_electronic_product_post():
    """Verify POST /electronicapi creates a new synthetic product."""
    new_product = {
        "name": "QA Synthetic Wireless Earbuds",
        "price": "99.99",
        "description": "High performance test device for automation verification.",
        "category": "Headphones",
        "brand": "QA-Tech",
        "stock": "50",
    }
    resp = requests.post(MOCK_API_BASE_URL, json=new_product, timeout=10)
    assert resp.status_code in [200, 201], f"Expected 200/201, got {resp.status_code}"
    created = resp.json()
    assert created.get("name") == new_product["name"]
    assert "id" in created

    # Clean up test artifact
    created_id = created["id"]
    requests.delete(f"{MOCK_API_BASE_URL}/{created_id}", timeout=10)


@pytest.mark.api
def test_update_electronic_product_put():
    """Verify PUT /electronicapi/:id updates product details."""
    # Create temporary item
    temp_item = {
        "name": "Temporary Test Item",
        "price": "10.00",
        "category": "Accessories",
    }
    create_resp = requests.post(MOCK_API_BASE_URL, json=temp_item, timeout=10)
    assert create_resp.status_code in [200, 201]
    item_id = create_resp.json()["id"]

    try:
        updated_data = {"name": "Updated Test Item", "price": "19.99"}
        update_resp = requests.put(f"{MOCK_API_BASE_URL}/{item_id}", json=updated_data, timeout=10)
        assert update_resp.status_code == 200
        assert update_resp.json().get("name") == "Updated Test Item"
    finally:
        requests.delete(f"{MOCK_API_BASE_URL}/{item_id}", timeout=10)


@pytest.mark.api
def test_delete_electronic_item():
    """Verify DELETE /electronicapi/:id removes the product."""
    temp_item = {"name": "Item To Delete", "price": "5.00"}
    create_resp = requests.post(MOCK_API_BASE_URL, json=temp_item, timeout=10)
    item_id = create_resp.json()["id"]

    delete_resp = requests.delete(f"{MOCK_API_BASE_URL}/{item_id}", timeout=10)
    assert delete_resp.status_code == 200

    # Verify subsequent GET returns 404
    get_resp = requests.get(f"{MOCK_API_BASE_URL}/{item_id}", timeout=10)
    assert get_resp.status_code == 404


@pytest.mark.api
def test_get_non_existent_product_returns_404():
    """Verify requesting non-existent ID returns 404."""
    resp = requests.get(f"{MOCK_API_BASE_URL}/non_existent_id_99999", timeout=10)
    assert resp.status_code == 404
