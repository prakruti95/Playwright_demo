"""
Shopping Cart Page & Drawer Object Model.
Handles Cart item management, quantities, removal, financial totals, and checkout trigger.
"""
from typing import List, Dict, Optional
import re
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_heading = page.locator("h1:has-text('Cart')")
        self.empty_cart_msg = page.locator("text=Your cart is empty")
        self.continue_shopping_link = page.locator("a:has-text('Continue shopping')")

        # Line items
        self.cart_items = page.locator("main div.space-y-4 > div, [role='dialog'] div.space-y-4 > div")
        self.remove_buttons = page.locator("button:has-text('Remove')")
        self.qty_increase_btns = page.locator("button[aria-label='Increase quantity']")
        self.qty_decrease_btns = page.locator("button[aria-label='Decrease quantity']")

        # Summary Totals
        self.subtotal_val = page.locator("dl dt:has-text('Subtotal') + dd").last
        self.shipping_val = page.locator("dl dt:has-text('Shipping') + dd").last
        self.tax_val = page.locator("dl dt:has-text('Tax') + dd").last
        self.total_val = page.locator("dl dt:has-text('Total') + dd").last

        # Promo Code
        self.promo_input = page.locator("input[placeholder*='Promo' i], input[placeholder*='code' i], input").last
        self.apply_promo_btn = page.locator("button:has-text('Apply')")

        # Checkout Button
        self.checkout_btn = page.locator("button:has-text('Checkout'), a:has-text('Checkout')").first

    def load(self) -> None:
        self.navigate("/cart")

    def is_empty(self) -> bool:
        return self.empty_cart_msg.is_visible()

    def get_items_count(self) -> int:
        return self.remove_buttons.count()

    def remove_item(self, index: int = 0) -> None:
        btns = self.remove_buttons.all()
        if index < len(btns):
            btns[index].click()
            self.page.wait_for_timeout(500)

    def increment_item(self, index: int = 0) -> None:
        btns = self.qty_increase_btns.all()
        if index < len(btns):
            btns[index].click()
            self.page.wait_for_timeout(500)

    def decrement_item(self, index: int = 0) -> None:
        btns = self.qty_decrease_btns.all()
        if index < len(btns):
            btns[index].click()
            self.page.wait_for_timeout(500)

    def _parse_currency(self, locator: Locator) -> float:
        if locator.is_visible():
            text = locator.inner_text().strip()
            if "free" in text.lower():
                return 0.0
            match = re.search(r"\$([0-9]+\.[0-9]{2})", text)
            if match:
                return float(match.group(1))
        return 0.0

    def get_subtotal(self) -> float:
        return self._parse_currency(self.subtotal_val)

    def get_shipping(self) -> float:
        return self._parse_currency(self.shipping_val)

    def is_shipping_free(self) -> bool:
        if self.shipping_val.is_visible():
            return "free" in self.shipping_val.inner_text().lower()
        return False

    def get_tax(self) -> float:
        return self._parse_currency(self.tax_val)

    def get_total(self) -> float:
        return self._parse_currency(self.total_val)

    def proceed_to_checkout(self) -> None:
        self.checkout_btn.click()
        self.page.wait_for_load_state("networkidle")
