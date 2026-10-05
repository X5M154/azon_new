import allure

from pages.base_page import BasePage


class LoginPage(BasePage):

    url = "/login"

    def __init__(self, page):
        super().__init__(page)

        self.form = page.get_by_test_id("login-form")
        self.email_input = page.get_by_test_id("email-input")
        self.password_input = page.get_by_test_id("password-input")
        self.submit_button = page.get_by_test_id("login-submit")
        self.error = page.get_by_test_id("login-error")

    @allure.step("Вход")
    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()