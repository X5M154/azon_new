import pytest
import allure
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage

pytestmark = [pytest.mark.ui, pytest.mark.payment]


@allure.epic("Витрина AZON")
@allure.feature("Корзина")
class TestCartUI:

    @allure.story("Добавление товара")
    @allure.title("Добавленный товар отображается в корзине")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cart_shows_added_product(self, logged_in_page, created_product):
        catalog_page = CatalogPage(logged_in_page).open()

        catalog_page.search(created_product.name)
        catalog_page.add_to_cart(created_product.name)
        expect(catalog_page.cart_count).to_have_text("1")

        catalog_page.go_to_cart()

        cart_page = CartPage(logged_in_page)
        expect(cart_page.items).to_have_count(1)
        expect(cart_page.item(created_product.name)).to_be_visible()

    @allure.story("Содержимое корзины")
    @allure.title("Удаление товара делает корзину пустой")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_removed_product_leaves_cart_empty(self, logged_in_page, created_product):
        catalog_page = CatalogPage(logged_in_page).open()

        catalog_page.search(created_product.name)
        catalog_page.add_to_cart(created_product.name)
        expect(catalog_page.cart_count).to_have_text("1")

        catalog_page.go_to_cart()

        cart_page = CartPage(logged_in_page)

        cart_page.remove(created_product.name)
        expect(cart_page.items).to_have_count(0)
        expect(cart_page.empty).to_be_visible()

    @allure.story("Добавление товара")
    @allure.title("Кнопка «В корзину» показывает тост и обновляет бейдж")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_to_cart_shows_toast_and_updates_badge(self, logged_in_page, created_product):
        catalog_page = CatalogPage(logged_in_page).open()

        catalog_page.search(created_product.name)
        catalog_page.add_to_cart(created_product.name)

        expect(catalog_page.toast).to_have_text("Товар добавлен в корзину")
        expect(catalog_page.cart_count).to_have_text("1")

    @allure.story("Содержимое корзины")
    @allure.title("Смена количества пересчитывает итог")
    @allure.severity(allure.severity_level.MINOR)
    def test_quantity_change_updates_total(self, logged_in_page, created_product):
        catalog_page = CatalogPage(logged_in_page).open()

        catalog_page.search(created_product.name)
        catalog_page.add_to_cart(created_product.name)
        expect(catalog_page.page.get_by_test_id("cart-count")).to_have_text("1")

        catalog_page.go_to_cart()

        cart_page = CartPage(logged_in_page)
        one_item_total = cart_page.total.inner_text()

        cart_page.set_quantity(created_product.name, 3)

        row = cart_page.item(created_product.name)

        expect(row.get_by_test_id("cart-item-quantity")).to_have_value("3")
        assert cart_page.total.inner_text() != one_item_total

    @allure.story("Содержимое корзины")
    @allure.title("Пустая корзина показывает заглушку")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_cart_shows_empty_state(self, logged_in_page):
        cart_page = CartPage(logged_in_page).open()

        expect(cart_page.empty).to_be_visible()
        expect(cart_page.checkout_button).to_have_count(0)

