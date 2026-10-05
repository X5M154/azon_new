import allure

from pages.base_page import BasePage


class CartPage(BasePage):
    """Корзина: /cart."""

    url = "/cart"

    def __init__(self, page):
        super().__init__(page)

        self.table = page.get_by_test_id("cart-table")
        self.items = page.get_by_test_id("cart-item")
        self.total = page.get_by_test_id("cart-total")
        self.empty = page.get_by_test_id("cart-empty")

        self.clear_button = page.get_by_test_id("cart-clear")
        self.checkout_button = page.get_by_test_id("checkout-button")

    def item(self, name):
        """Строка корзины с нужным товаром."""
        return self.items.filter(has_text=name)

    def set_quantity(self, name, quantity):
        row = self.item(name)
        row.get_by_test_id("cart-item-quantity").fill(str(quantity))
        row.get_by_test_id("cart-item-update").click()

    @allure.step("Очищаем корзину")
    def clear(self):
        self.clear_button.click()

    @allure.step("Оформляем заказ")
    def checkout(self):
        self.checkout_button.click()

    @allure.step("Удаляем из корзины товар {name}")
    def remove(self, name):
        self.item(name).get_by_test_id("cart-item-remove").click()