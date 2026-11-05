"""
Home Page Object Model.
"""
from typing import List, Dict
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Hero Locators
        self.hero_heading = page.locator("h1")
        self.shop_collection_btn = page.locator("a:has-text('Shop the collection'), button:has-text('Shop the collection')").first
        self.new_arrivals_btn = page.locator("a:has-text('View new arrivals'), button:has-text('View new arrivals')").first

        # Category shortcuts ("Shop by room")
        self.category_living = page.locator("a[href*='category=living']")
        self.category_apparel = page.locator("a[href*='category=apparel']")
        self.category_objects = page.locator("a[href*='category=objects']")
        self.category_wellness = page.locator("a[href*='category=wellness']")

        # Featured Pieces
        self.featured_cards = page.locator("a[href^='/products/']")
        self.shop_all_link = page.locator("a:has-text('Shop all')")

    def load(self) -> None:
        self.navigate("/")

    def click_shop_collection(self) -> None:
        self.shop_collection_btn.click()
        self.page.wait_for_load_state("networkidle")

    def click_new_arrivals(self) -> None:
        self.new_arrivals_btn.click()
        self.page.wait_for_load_state("networkidle")

    def click_category(self, name: str) -> None:
        cat_map = {
            "living": self.category_living,
            "apparel": self.category_apparel,
            "objects": self.category_objects,
            "wellness": self.category_wellness,
        }
        loc = cat_map.get(name.lower())
        if loc:
            loc.click()
            self.page.wait_for_load_state("networkidle")

    def get_featured_product_names(self) -> List[str]:
        elements = self.featured_cards.all()
        names = []
        for el in elements:
            text = el.inner_text().strip()
            # First line is usually name
            lines = [l for l in text.split("\n") if l.strip()]
            if lines:
                names.append(lines[0])
        return names
