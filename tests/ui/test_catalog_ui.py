import allure
import pytest
from playwright.sync_api import expect
import re

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, pytest.mark.products]


@allure.epic("Витрина AZON")
@allure.feature("Страница каталога")
class TestCatalogUI:

    @allure.story("Просмотр витрины")
    @allure.title("На витрине отображаются товары")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_catalog_shows_products(self, page):
        catalog_page = CatalogPage(page).open()

        expect(catalog_page.title).to_have_text("Каталог")
        expect(catalog_page.total).to_contain_text("Найдено товаров")
        assert catalog_page.cards.count() > 0, "На витрине не нашлось ни одного товара"

    @pytest.mark.negative
    @allure.story("Просмотр витрины")
    @allure.title("Поиск без результата показывает пустую выдачу")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_without_results_shows_empty_state(self, page):
        catalog_page = CatalogPage(page).open()

        catalog_page.search("товара-точно-нет-123")

        expect(catalog_page.empty).to_be_visible()
        expect(catalog_page.cards).to_have_count(0)

    @allure.story("Просмотр витрины")
    @allure.title("Отображается выбранная категория товаров")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_category_filter_narrows_catalog(self, page):
        catalog_page = CatalogPage(page).open()
        all_products = catalog_page.total.inner_text()

        catalog_page.choose_category("Книги")

        expect(catalog_page.category_select.locator("option:checked")).to_have_text("Книги")
        assert catalog_page.total.inner_text() != all_products

    @allure.story("Просмотр витрины")
    @allure.title("В поиске отображается созданный товар")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_finds_created_product(self, logged_in_page, created_product):
        catalog_page = CatalogPage(logged_in_page).open()

        catalog_page.search(created_product.name)

        expect(catalog_page.cards).to_have_count(1)
        expect(catalog_page.card(created_product.name)).to_be_visible()

    @allure.story("Просмотр витрины")
    @allure.title("При добавлении товара в корзину неавторизованный пользователь переходит на страницу входа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_guest_add_to_cart_goes_to_login(self, page, created_product):
        login_page = LoginPage(page)
        catalog_page = CatalogPage(page).open()

        catalog_page.search(created_product.name)
        catalog_page.add_to_cart(created_product.name)

        expect(page).to_have_url(re.compile(r"/login"))
        expect(login_page.form).to_be_visible()

    @allure.story("Просмотр витрины")
    @allure.title("Сортировка цены по возрастанию")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sorting_by_price_ascending(self, page):
        catalog_page = CatalogPage(page).open()

        catalog_page.sort_by("По цене")

        expect(catalog_page.sort_select.locator("option:checked")).to_have_text("По цене")

        prices = catalog_page.prices()

        assert prices == sorted(prices), f"Цены пришли не по возрастанию: {prices}"
