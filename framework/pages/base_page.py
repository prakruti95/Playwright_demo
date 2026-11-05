"""
Base Page Object providing reusable interactions, navigation, and header/footer locators.
"""
from typing import Optional
from playwright.sync_api import Page, Locator
from framework.config import BASE_URL


class BasePage:
    def __init__(self, page: Page):
        self.page = page

        # Global Header Locators
        self.header = page.locator("header")
        self.logo = page.locator("header a[href='/']")
        self.products_link = page.locator("header a[href='/products']")
        self.sign_in_link = page.locator("header a[href='/login']")
        self.account_link = page.locator("header a[href='/account']")
        self.cart_button = page.locator("header button:has-text('Cart')")
        self.theme_toggle_btn = page.locator("button[aria-label='Toggle theme']")

        # Cart Drawer (Slide-over Aside)
        self.cart_drawer = page.locator("aside:has-text('Your cart'), [role='dialog']")
        self.cart_drawer_close = page.locator("button[aria-label='Close cart'], button[aria-label='Close']")

        # Footer Locators
        self.footer = page.locator("footer, [class*='footer']")
        self.footer_all_products = page.locator("footer a:has-text('All products')")
        self.footer_cart = page.locator("footer a:has-text('Cart')")
        self.newsletter_input = page.locator("input[aria-label='Email address']")
        self.newsletter_subscribe_btn = page.locator("button:has-text('Subscribe')")

    def navigate(self, path: str = "/") -> None:
        full_url = f"{BASE_URL.rstrip('/')}{path}"
        self.page.goto(full_url, wait_until="networkidle")

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

    def toggle_theme(self) -> None:
        self.theme_toggle_btn.click()
        self.page.wait_for_timeout(300)

    def is_dark_mode(self) -> bool:
        html_class = self.page.locator("html").get_attribute("class") or ""
        return "dark" in html_class

    def open_cart_drawer(self) -> None:
        self.cart_button.click()
        self.cart_drawer.wait_for(state="visible", timeout=5000)

    def get_cart_badge_count(self) -> int:
        btn_text = self.cart_button.inner_text().strip()
        # Format is "Cart" or "Cart (1)"
        if "(" in btn_text and ")" in btn_text:
            count_str = btn_text.split("(")[1].split(")")[0]
            return int(count_str)
        return 0

    def clear_local_storage(self) -> None:
        self.page.evaluate("() => window.localStorage.clear()")
