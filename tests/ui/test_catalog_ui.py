import pytest
from playwright.sync_api import expect
import re

from config.hosts import FRONTEND_URL

pytestmark = [pytest.mark.ui, pytest.mark.products]


class TestCatalogUI:
    def test_catalog_shows_products(self, page):
        page.goto(FRONTEND_URL)

        expect(page.get_by_test_id("page-title")).to_have_text("Каталог")
        expect(page.get_by_test_id("catalog-total")).to_contain_text("Найдено товаров")
        assert page.get_by_test_id("product-card").count() > 0, "На витрине не нашлось ни одного товара"

    @pytest.mark.negative
    def test_search_without_results_shows_empty_state(self, page):
        page.goto(FRONTEND_URL)

        page.get_by_test_id("search-input").fill("такого-товара-точно-нет-12345")
        page.get_by_test_id("apply-filters").click()

        expect(page.get_by_test_id("catalog-empty")).to_be_visible()
        expect(page.get_by_test_id("product-card")).to_have_count(0)

    def test_category_filter_narrows_catalog(self, page):
        page.goto(FRONTEND_URL)
        all_products = page.get_by_test_id("catalog-total").inner_text()

        page.get_by_test_id("category-select").select_option(label="Книги")
        page.get_by_test_id("apply-filters").click()

        expect(page.get_by_test_id("category-select").locator("option:checked")).to_have_text("Книги")
        assert page.get_by_test_id("catalog-total").inner_text() != all_products

    def test_search_finds_created_product(self, page, created_product):
        page.goto(FRONTEND_URL)

        page.get_by_test_id("search-input").fill(created_product.name)
        page.get_by_test_id("apply-filters").click()

        cards = page.get_by_test_id("product-card")
        expect(cards).to_have_count(1)
        expect(cards.filter(has_text=created_product.name)).to_be_visible()

    def test_guest_add_to_cart_goes_to_login(self, page, created_product):
        page.goto(FRONTEND_URL)
        page.get_by_test_id("search-input").fill(created_product.name)
        page.get_by_test_id("apply-filters").click()

        page.get_by_test_id("product-card").filter(
            has_text=created_product.name
        ).get_by_test_id("add-to-cart").click()

        expect(page).to_have_url(re.compile(r"/login"))
        expect(page.get_by_test_id("login-form")).to_be_visible()

    def test_sorting_by_price_ascending(self, page):
        page.goto(FRONTEND_URL)

        page.get_by_test_id("sort-select").select_option(label="По цене")
        page.get_by_test_id("order-select").select_option(label="По возрастанию")
        page.get_by_test_id("apply-filters").click()

        expect(page.get_by_test_id("sort-select").locator("option:checked")).to_have_text("По цене")

        prices = [
            float(text.replace("₽", "").replace("\xa0", "").replace(" ", ""))
            for text in page.get_by_test_id("product-card")
            .get_by_test_id("product-price")
            .all_inner_texts()
        ]

        assert prices == sorted(prices), f"Цены пришли не по возрастанию: {prices}"
