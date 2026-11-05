"""
Account Page Object Model.
"""
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class AccountPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.profile_heading = page.locator("text='Profile'").first
        self.orders_tab = page.locator("a[href='/account/orders'], button:has-text('Orders')")
        self.addresses_tab = page.locator("a[href='/account/addresses'], button:has-text('Addresses')")
        self.wishlist_tab = page.locator("a[href='/account/wishlist'], button:has-text('Wishlist')")
        self.sign_out_btn = page.locator("button:has-text('Sign out')")

    def load(self) -> None:
        self.navigate("/account")

    def sign_out(self) -> None:
        self.sign_out_btn.click()
        self.page.wait_for_timeout(500)
