"""
Login Page Object Model.
"""
from typing import Optional
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("input[type='email']")
        self.password_input = page.locator("input[type='password']")
        self.sign_in_submit_btn = page.locator("button[type='submit']:has-text('Sign in')")
        self.submit_btn = self.sign_in_submit_btn
        self.create_account_link = page.locator("a:has-text('Create one')")
        self.toast_alert = page.locator("[role='status'], [role='alert'], .toast")

    def load(self) -> None:
        self.navigate("/login")

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_submit_btn.click()
        try:
            self.page.wait_for_url(lambda u: "/account" in u or "/admin" in u, timeout=10000)
        except Exception:
            self.page.wait_for_timeout(2000)
