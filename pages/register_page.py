import allure

from pages.base_page import BasePage



class RegisterPage(BasePage):

    url = "/register"

    def __init__(self, page):
        super().__init__(page)

        self.form = page.get_by_test_id("login-form")
        self.name_input = page.get_by_test_id("name-input")
        self.email_input = page.get_by_test_id("email-input")
        self.password_input = page.get_by_test_id("password-input")
        self.submit_button = page.get_by_test_id("register-submit")
        self.error = page.get_by_test_id("login-error")

    @allure.step("Регистрируем покупателя")
    def register(self, full_name, email, password, invite_code=None):
        self.name_input.fill(full_name)
        self.email_input.fill(email)
        self.password_input.fill(password)

        if invite_code:
            self.invite_code_input.fill(invite_code)

        self.submit_button.click()