"""
Configuration module for Northline Store Automation Testing.
"""
import os
from typing import Dict, Any

# Primary Base URLs (Kept strictly separate per project specification)
WEBSITE_BASE_URL: str = os.getenv("WEBSITE_BASE_URL") or os.getenv("TARGET_URL") or "https://ecomcicid.netlify.app"
API_BASE_URL: str = os.getenv("API_BASE_URL") or os.getenv("MOCK_API_URL") or "https://681444af225ff1af16285b31.mockapi.io/electronicapi"

# Aliases for backwards compatibility
BASE_URL = WEBSITE_BASE_URL
MOCK_API_BASE_URL = API_BASE_URL

# Thresholds & Financial Constants Discovered from App Source
FREE_SHIPPING_THRESHOLD: float = 75.00
STANDARD_SHIPPING_FEE: float = 9.99
TAX_RATE: float = 0.08  # 8% tax

# Synthetic Test Credentials
TEST_CUSTOMER = {
    "email": "customer.test@example.com",
    "password": "Password123!",
    "name": "Jane Tester",
}

TEST_ADMIN = {
    "email": "admin.qa@northline.com",
    "password": "Password123!",
    "name": "Admin Tester",
}

# Synthetic Shipping Address for Checkout
TEST_SHIPPING_ADDRESS: Dict[str, str] = {
    "line1": "742 Evergreen Terrace",
    "line2": "Suite 101",
    "city": "Springfield",
    "state": "IL",
    "postalCode": "62704",
    "country": "US",  # Must be 2-letter ISO code
    "phone": "555-0199-281",
}
