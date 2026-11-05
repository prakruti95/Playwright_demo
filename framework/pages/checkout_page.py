"""
Checkout Page Object Model.
Handles multi-stage checkout: Stage 1 Shipping Address Form and Stage 2 Review & Order.
"""
from typing import Dict, List, Optional
import re
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Stage 1 Inputs
        self.address_line1_input = page.locator("#line1, input[name='line1']")
        self.address_line2_input = page.locator("#line2, input[name='line2']")
        self.city_input = page.locator("#city, input[name='city']")
        self.state_input = page.locator("#state, input[name='state']")
        self.postal_code_input = page.locator("#postalCode, input[name='postalCode']")
        self.country_input = page.locator("#country, input[name='country']")
        self.phone_input = page.locator("#phone, input[name='phone']")
        
        # Stage 1 Submit
        self.continue_to_review_btn = page.locator("button[type='submit']:has-text('Continue to review')")
        
        # Validation error messages
        self.validation_errors = page.locator("form p.text-xs, p.text-danger-600, .text-red-500")

        # Stage 2 Locators
        self.review_heading = page.locator("text='Review'")
        self.back_button = page.locator("button:has-text('Back')")
        self.place_order_btn = page.locator("button:has-text('Place order')")
        self.shipping_to_text = page.locator("main:has-text('Shipping to')")

    def load(self) -> None:
        self.navigate("/checkout")

    def fill_shipping_address(self, address: Dict[str, str]) -> None:
        if "line1" in address:
            self.address_line1_input.fill(address["line1"])
        if "line2" in address:
            self.address_line2_input.fill(address["line2"])
        if "city" in address:
            self.city_input.fill(address["city"])
        if "state" in address:
            self.state_input.fill(address["state"])
        if "postalCode" in address:
            self.postal_code_input.fill(address["postalCode"])
        if "country" in address:
            self.country_input.fill(address["country"])
        if "phone" in address:
            self.phone_input.fill(address["phone"])

    def submit_shipping_form(self) -> None:
        self.continue_to_review_btn.click()
        self.page.wait_for_timeout(1000)

    def get_validation_errors(self) -> List[str]:
        texts = []
        for el in self.validation_errors.all():
            t = el.inner_text().strip()
            if t and t not in ["ISO code, e.g. US"]:
                texts.append(t)
        return texts

    def is_review_stage_visible(self) -> bool:
        return self.place_order_btn.is_visible()

    def go_back_to_shipping(self) -> None:
        self.back_button.click()
        self.page.wait_for_timeout(500)

    def place_order(self) -> None:
        self.place_order_btn.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)
