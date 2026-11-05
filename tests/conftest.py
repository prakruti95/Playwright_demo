"""
Pytest configuration, fixtures, browser settings, and Page Object providers.
"""
import os
import pytest
from typing import Generator
from playwright.sync_api import Page, BrowserContext, Browser
from framework.pages import (
    HomePage,
    ProductsPage,
    ProductDetailPage,
    CartPage,
    CheckoutPage,
    OrderConfirmationPage,
    LoginPage,
    AccountPage,
    AdminPage,
)


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Provide isolated browser context with video and trace capture."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        record_video_dir="test-results/videos/",
        record_video_size={"width": 1280, "height": 800},
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.tracing.stop(path="test-results/traces/trace.zip")
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Provide clean page with isolated storage."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def mobile_page(browser: Browser) -> Generator[Page, None, None]:
    """Provide mobile viewport page (iPhone 13 dimensions: 390x844)."""
    context = browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        is_mobile=True,
        has_touch=True,
    )
    page = context.new_page()
    yield page
    context.close()


# Page Object Fixtures
@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def pdp(page: Page) -> ProductDetailPage:
    return ProductDetailPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def order_confirm_page(page: Page) -> OrderConfirmationPage:
    return OrderConfirmationPage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def account_page(page: Page) -> AccountPage:
    return AccountPage(page)


@pytest.fixture
def admin_page(page: Page) -> AdminPage:
    return AdminPage(page)


# Screenshot on failure hook
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            os.makedirs("test-results/screenshots", exist_ok=True)
            screenshot_path = f"test-results/screenshots/{item.name}.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True)
            except Exception:
                pass
