"""
E2E Test Suite 8: Authentication, Customer & Admin Role-Based Redirections.
"""
import pytest
from framework.pages import LoginPage, AccountPage, AdminPage
from framework.config import TEST_CUSTOMER, TEST_ADMIN

pytestmark = [pytest.mark.e2e]


@pytest.mark.smoke
@pytest.mark.regression
def test_customer_login_redirects_to_account(login_page: LoginPage, account_page: AccountPage):
    """Verify regular customer login redirects to /account profile."""
    login_page.load()
    login_page.login(TEST_CUSTOMER["email"], TEST_CUSTOMER["password"])
    
    assert "/account" in login_page.get_current_url()
    account_page.profile_heading.wait_for(state="visible", timeout=10000)
    assert account_page.profile_heading.is_visible()


@pytest.mark.smoke
@pytest.mark.regression
def test_admin_login_redirects_to_admin_dashboard(login_page: LoginPage, admin_page: AdminPage):
    """Verify admin email login redirects to /admin dashboard."""
    login_page.load()
    login_page.login(TEST_ADMIN["email"], TEST_ADMIN["password"])
    
    assert "/admin" in login_page.get_current_url()
    admin_page.admin_brand.wait_for(state="visible", timeout=10000)
    assert admin_page.admin_brand.is_visible()


@pytest.mark.regression
def test_sign_out_clears_session(login_page: LoginPage, account_page: AccountPage):
    """Verify clicking Sign Out removes session and displays Sign In link."""
    login_page.load()
    login_page.login(TEST_CUSTOMER["email"], TEST_CUSTOMER["password"])
    assert "/account" in login_page.get_current_url()
    
    account_page.sign_out()
    assert account_page.sign_in_link.is_visible()


@pytest.mark.regression
def test_invalid_email_format_validation(login_page: LoginPage):
    """Verify requirement 15: Invalid email format triggers HTML5 validation error."""
    login_page.load()
    login_page.email_input.fill("invalid-email-address")
    login_page.submit_btn.click()
    
    # HTML5 validation prevents submission and flags input as invalid
    is_valid = login_page.email_input.evaluate("el => el.checkValidity()")
    assert is_valid is False, "Email input should be flagged invalid for non-email string"
    assert "/login" in login_page.get_current_url()

