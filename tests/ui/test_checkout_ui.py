from playwright.sync_api import expect
import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.order_page import OrderPage

pytestmark = [pytest.mark.ui, pytest.mark.payment]

def put_product_in_cart(page, product):
    """Подготовка: положить товар в корзину руками покупателя."""
    catalog_page = CatalogPage(page).open()
    catalog_page.search(product.name)
    catalog_page.add_to_cart(product.name)
    expect(catalog_page.cart_count).to_have_text("1")


@allure.epic("Витрина AZON")
@allure.feature("Оформление и оплата заказа")
class TestCheckoutUI:

    @allure.story("Оформление заказа")
    @allure.title("Из корзины создаётся заказ в статусе AWAITING_PAYMENT")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_creates_order(self, logged_in_page, created_product):
        put_product_in_cart(logged_in_page, created_product)
        cart_page = CartPage(logged_in_page).open()

        cart_page.checkout()

        order_page = OrderPage(logged_in_page)
        expect(order_page.flash).to_have_text("Заказ создан — оплатите его")
        expect(order_page.status).to_have_text("AWAITING_PAYMENT")

    def test_successful_payment_marks_order_paid(self, logged_in_page, created_product):
        put_product_in_cart(logged_in_page, created_product)
        CartPage(logged_in_page).open().checkout()
        order_page = OrderPage(logged_in_page)

        order_page.pay()

        expect(order_page.flash).to_have_text("Оплата прошла успешно!")
        expect(order_page.status).to_have_text("PAID")
        expect(order_page.payments).to_have_count(1)

    def test_order_can_be_cancelled(self, logged_in_page, created_product):
        put_product_in_cart(logged_in_page, created_product)
        CartPage(logged_in_page).open().checkout()
        order_page = OrderPage(logged_in_page)

        order_page.cancel()

        expect(order_page.flash).to_have_text("Заказ отменён")
        expect(order_page.status).to_have_text("CANCELLED")