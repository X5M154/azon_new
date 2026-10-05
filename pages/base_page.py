from playwright.sync_api import Page

from config.hosts import FRONTEND_URL


class BasePage:
    """Общий предок всех страниц витрины.

    Здесь живёт то, что одинаково везде: адрес страницы, переход на неё
    и шапка сайта, которая нарисована на каждой странице AZON.
    """

    url = "/"

    def __init__(self, page: Page):
        self.page = page

        # шапка: одна на все страницы, поэтому её локаторы в предке
        self.catalog_link = page.get_by_test_id("nav-catalog")
        self.cart_link = page.get_by_test_id("nav-cart")
        self.cart_count = page.get_by_test_id("cart-count")
        self.orders_link = page.get_by_test_id("nav-orders")
        self.profile_link = page.get_by_test_id("nav-profile")
        self.user_role = page.get_by_test_id("user-role")
        self.logout_button = page.get_by_test_id("logout-button")

        # два вида сообщений: flash приходит с сервера, toast рисует JS
        self.flash = page.get_by_test_id("flash-message")
        self.toast = page.get_by_test_id("toast")

        self.title = page.get_by_test_id("page-title")

    def open(self):
        """Открыть страницу и вернуть саму себя - чтобы можно было писать цепочкой."""
        self.page.goto(f"{FRONTEND_URL}{self.url}")
        return self

    def go_to_cart(self):
        self.cart_link.click()

    def go_to_orders(self):
        self.orders_link.click()

    def go_to_catalog(self):
        self.catalog_link.click()

    def logout(self):
        self.logout_button.click()