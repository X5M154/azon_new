import allure
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.order_page import OrdersPage


@allure.epic("Витрина AZON")
@allure.feature("Страница с заказами")
class TestOrdersUI:

    @allure.story("Заказы покупателя")
    @allure.title("Новый заказ добавлен в список заказов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_new_order_appears_in_list(self, logged_in_page, created_product):
        catalog_page = CatalogPage(logged_in_page).open()

        catalog_page.search(created_product.name)
        catalog_page.add_to_cart(created_product.name)
        expect(catalog_page.cart_count).to_have_text("1")

        CartPage(logged_in_page).open().checkout()
        order_id = logged_in_page.url.rsplit("/", 1)[-1]

        orders_page = OrdersPage(logged_in_page).open()

        expect(orders_page.row(order_id)).to_be_visible()
        expect(orders_page.row(order_id).get_by_test_id("order-status")).to_have_text(
            "AWAITING_PAYMENT"
        )