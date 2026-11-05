"""
Products Catalog Page Object Model.
Handles product grid, filters, price range, ratings, and sorting.
"""
from typing import List, Dict, Optional
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Catalog Locators
        self.page_heading = page.locator("h1")
        self.product_cards = page.locator("a[href^='/products/']")
        self.sort_button = page.locator("main button:has-text('Newest'), main button:has-text('Price: low to high'), main button:has-text('Popularity')").first

        # Category Filters
        self.cat_all = page.locator("button:has-text('All products')").first
        self.cat_living = page.locator("button:has-text('Living')").first
        self.cat_apparel = page.locator("button:has-text('Apparel')").first
        self.cat_objects = page.locator("button:has-text('Objects')").first
        self.cat_wellness = page.locator("button:has-text('Wellness')").first

        # Price Range Inputs
        self.min_price_slider = page.locator("input[type='range'][aria-label='Minimum price']")
        self.max_price_slider = page.locator("input[type='range'][aria-label='Maximum price']")

        # Rating Filters
        self.rating_any = page.locator("button:has-text('Any rating')").first

        # Mobile Filters Button
        self.mobile_filters_btn = page.locator("button:has-text('Filters')")

    def load(self, query_params: str = "") -> None:
        path = f"/products{query_params}"
        self.navigate(path)
        if "nonexistent" not in query_params.lower():
            try:
                self.product_cards.first.wait_for(state="visible", timeout=10000)
            except Exception:
                pass

    def get_products_count(self) -> int:
        return self.product_cards.count()

    def get_product_titles(self) -> List[str]:
        titles = []
        for card in self.product_cards.all():
            lines = [l.strip() for l in card.inner_text().split("\n") if l.strip()]
            # Usually: Category, Title, Price
            if len(lines) >= 2:
                titles.append(lines[1])
            elif lines:
                titles.append(lines[0])
        return titles

    def get_product_prices(self) -> List[float]:
        prices = []
        for card in self.product_cards.all():
            text = card.inner_text()
            # Find dollar amount
            import re
            matches = re.findall(r"\$([0-9]+\.[0-9]{2})", text)
            if matches:
                # The last match or second is usually the active price
                prices.append(float(matches[-1]))
        return prices

    def filter_by_category(self, category_name: str) -> None:
        mapping = {
            "all": self.cat_all,
            "living": self.cat_living,
            "apparel": self.cat_apparel,
            "objects": self.cat_objects,
            "wellness": self.cat_wellness,
        }
        btn = mapping.get(category_name.lower())
        if btn and btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(500)

    def select_sort(self, sort_option: str) -> None:
        """
        Options: 'Newest', 'Price: low to high', 'Popularity'
        """
        self.sort_button.wait_for(state="visible", timeout=10000)
        self.sort_button.click()
        self.page.wait_for_timeout(300)
        option_btn = self.page.locator(f"button:has-text('{sort_option}')").last
        option_btn.wait_for(state="visible", timeout=5000)
        option_btn.click()
        self.page.wait_for_timeout(500)
        try:
            self.product_cards.first.wait_for(state="visible", timeout=10000)
        except Exception:
            pass

    def click_product(self, title_or_slug: str) -> None:
        selector = f"a[href*='{title_or_slug}'], a[href^='/products/']:has-text('{title_or_slug}')"
        self.page.locator(selector).first.click()
        self.page.wait_for_load_state("networkidle")
