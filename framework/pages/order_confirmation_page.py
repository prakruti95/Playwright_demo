"""
Order Confirmation Page Object Model.
"""
import re
from typing import Optional
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class OrderConfirmationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.confirmation_heading = page.locator("h1:has-text('Order confirmed'), main:has-text('Order confirmed')")
        self.thank_you_heading = page.locator("text='Thank you'")
        self.order_number_text = page.locator("main:has-text('Order ORD-LOCAL-')")
        self.estimated_delivery_text = page.locator("text=Estimated delivery")
        
        self.keep_shopping_btn = page.locator("a:has-text('Keep shopping'), button:has-text('Keep shopping')")
        self.view_orders_btn = page.locator("a:has-text('View orders'), button:has-text('View orders')")

    def is_confirmed(self, timeout: int = 10000) -> bool:
        try:
            self.confirmation_heading.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_order_number(self) -> Optional[str]:
        text = self.page.locator("main").inner_text()
        match = re.search(r"(ORD-LOCAL-[0-9A-Z\-]+)", text)
        return match.group(1) if match else None

    def click_keep_shopping(self) -> None:
        self.keep_shopping_btn.first.click()
        self.page.wait_for_load_state("networkidle")
