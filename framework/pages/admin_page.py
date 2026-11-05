"""
Admin Dashboard Page Object Model.
"""
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class AdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.admin_brand = page.locator("text='Northline Admin'").first
        self.nav_dashboard = page.locator("a[href='/admin']:has-text('Dashboard')")
        self.nav_products = page.locator("a[href='/admin/products']:has-text('Products')")
        self.nav_orders = page.locator("a[href='/admin/orders']:has-text('Orders')")
        self.nav_customers = page.locator("a[href='/admin/customers']:has-text('Customers')")
        self.nav_categories = page.locator("a[href='/admin/categories']:has-text('Categories')")
        self.nav_settings = page.locator("a[href='/admin/settings']:has-text('Settings')")

        # Admin Products View
        self.product_search_input = page.locator("input[name='product-search']")

    def load(self) -> None:
        self.navigate("/admin")
