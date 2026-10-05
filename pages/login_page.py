from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница входа: /login."""

    url = "/login"

    def __init__(self, page):
        super().__init__(page)

        self.form = page.get_by_test_id("login-form")
        self.email_input = page.get_by_test_id("email-input")
        self.password_input = page.get_by_test_id("password-input")
        self.submit_button = page.get_by_test_id("login-submit")
        self.error = page.get_by_test_id("login-error")

    def login(self, email, password):
        """Один шаг пользователя: заполнил форму и нажал «Войти»."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()