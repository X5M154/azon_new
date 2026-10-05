import pytest
from playwright.sync_api import expect

from config.hosts import FRONTEND_URL
from data.users import UserData
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

pytestmark = [pytest.mark.ui, pytest.mark.auth]

class TestAuthUI:

    @pytest.mark.negative
    def test_login_with_wrong_password(self, page, api_manager):
        user = UserData.registration_data()
        api_manager.auth_api.register_user(user)

        page.goto(f"{FRONTEND_URL}/login")
        page.get_by_test_id("email-input").fill(user.email)
        page.get_by_test_id("password-input").fill("WrongPassword123")
        page.get_by_test_id("login-submit").click()

        expect(page.get_by_test_id("login-error")).to_be_visible()
        expect(page.get_by_test_id("login-error")).to_have_text("Invalid email or password")

    def test_registration_through_form_leads_to_login(self, page):
        user = UserData.registration_data()
        register_page = RegisterPage(page).open()

        register_page.register(user.full_name, user.email, user.password)

        login_page = LoginPage(page)
        expect(login_page.flash).to_have_text("Аккаунт создан — войдите")
        expect(login_page.form).to_be_visible()
