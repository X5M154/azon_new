import re

import allure
import pytest
from config.hosts import FRONTEND_URL
from playwright.sync_api import expect
from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, pytest.mark.mobile]

MOBILE_WIDTH = 390


def page_width(page):
    return page.evaluate(
        "() => ({scroll: document.documentElement.scrollWidth,"
        " client: document.documentElement.clientWidth})"
    )

@allure.epic("Витрина AZON")
@allure.feature("Мобильная версия")
class TestMobileUI:

    @allure.story("Просмотр страницы")
    @allure.title("Корректное отображение мобильной версии страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_viewport_is_phone_sized(self, mobile_page):
        mobile_page.goto(FRONTEND_URL)

        assert mobile_page.viewport_size["width"] == MOBILE_WIDTH

    @allure.story("Просмотр страницы")
    @allure.title("Корректное отображение ширины страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_guest_catalog_has_no_side_scroll(self, mobile_page):
        mobile_page.goto(FRONTEND_URL)

        width = page_width(mobile_page)

        assert width["scroll"] <= width["client"], (
            f"Страница шире экрана: {width['scroll']} px против {width['client']} px"
        )

    @allure.story("Просмотр витрины")
    @allure.title("При добавлении товара в корзину неавторизованный пользователь переходит на страницу входа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tap_on_add_to_cart_sends_guest_to_login(self, mobile_page):
        login_page = LoginPage(mobile_page)
        catalog_page = CatalogPage(mobile_page).open()

        catalog_page.add_first_to_cart()

        expect(mobile_page).to_have_url(re.compile(r"/login"))
        expect(login_page.form).to_be_visible()

    @pytest.mark.xfail(strict=True, reason="AZON-207: шапка авторизованного пользователя не помещается в 390 px")
    def test_logged_in_catalog_has_no_side_scroll(self, logged_in_mobile_page):
        CatalogPage(logged_in_mobile_page).open()

        width = page_width(logged_in_mobile_page)

        assert width["scroll"] <= width["client"], (
            f"Страница шире экрана: {width['scroll']} px против {width['client']} px"
        )

    @allure.story("Просмотр витрины")
    @allure.title("Каталог отображается в одну колонку")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_catalog_is_single_column(self, mobile_page):
        catalog_page = CatalogPage(mobile_page).open()

        card = catalog_page.cards.first.bounding_box()

        assert card["width"] > MOBILE_WIDTH * 0.9, (
            f"Карточка занимает {card['width']} px - на телефоне ожидали одну колонку во всю ширину"
        )

    @allure.story("Просмотр витрины")
    @allure.title("Поиск на телефоне находит товар")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_on_phone_finds_product(self, mobile_page, created_product):
        catalog_page = CatalogPage(mobile_page).open()

        catalog_page.search(created_product.name)

        expect(catalog_page.cards).to_have_count(1)
        expect(catalog_page.card(created_product.name)).to_be_visible()
