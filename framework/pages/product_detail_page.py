"""
Product Detail Page (PDP) Object Model.
"""
from typing import Optional
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class ProductDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_title = page.locator("h1")
        self.product_price = page.locator("main p.text-2xl.font-semibold, main p.font-semibold").first
        
        # Quantity controls
        self.qty_decrement_btn = page.locator("button[aria-label='Decrease quantity']")
        self.qty_increment_btn = page.locator("button[aria-label='Increase quantity']")
        
        # Action Buttons
        self.add_to_cart_btn = page.locator("button:has-text('Add to cart')")
        self.buy_now_btn = page.locator("button:has-text('Buy now')")
        self.save_wishlist_btn = page.locator("button:has-text('Save')")
        
        # Tabs
        self.tab_description = page.locator("button:has-text('Description')")
        self.tab_specifications = page.locator("button:has-text('Specifications')")
        self.tab_reviews = page.locator("button:has-text('Reviews')")

    def load(self, slug: str) -> None:
        self.navigate(f"/products/{slug}")

    def get_title_text(self) -> str:
        # Wait for PDP heading to update (not catalog 'All products')
        heading = self.page.locator("main h1")
        heading.filter(has_not_text="All products").wait_for(state="visible", timeout=10000)
        return heading.filter(has_not_text="All products").inner_text().strip()

    def get_price_value(self) -> float:
        text = self.product_price.inner_text().strip()
        import re
        match = re.search(r"\$([0-9]+\.[0-9]{2})", text)
        return float(match.group(1)) if match else 0.0

    def increase_quantity(self, times: int = 1) -> None:
        for _ in range(times):
            self.qty_increment_btn.click()
            self.page.wait_for_timeout(200)

    def decrease_quantity(self, times: int = 1) -> None:
        for _ in range(times):
            self.qty_decrement_btn.click()
            self.page.wait_for_timeout(200)

    def add_to_cart(self) -> None:
        self.add_to_cart_btn.click()
        self.page.wait_for_timeout(800)

    def buy_now(self) -> None:
        self.buy_now_btn.click()
        self.page.wait_for_load_state("networkidle")

    def switch_tab(self, tab_name: str) -> None:
        mapping = {
            "description": self.tab_description,
            "specifications": self.tab_specifications,
            "reviews": self.tab_reviews,
        }
        btn = mapping.get(tab_name.lower())
        if btn:
            btn.click()
            self.page.wait_for_timeout(300)
