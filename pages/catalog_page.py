import allure

from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Главная страница витрины: каталог товаров с фильтрами и постраничной выдачей."""

    url = "/"

    def __init__(self, page):
        super().__init__(page)

        self.grid = page.get_by_test_id("catalog-grid")
        self.cards = page.get_by_test_id("product-card")
        self.total = page.get_by_test_id("catalog-total")
        self.empty = page.get_by_test_id("catalog-empty")

        self.search_input = page.get_by_test_id("search-input")
        self.category_select = page.get_by_test_id("category-select")
        self.sort_select = page.get_by_test_id("sort-select")
        self.order_select = page.get_by_test_id("order-select")
        self.apply_button = page.get_by_test_id("apply-filters")

        self.pagination = page.get_by_test_id("pagination")
        self.next_page_button = page.get_by_test_id("pagination-next")

    def card(self, name):
        """Карточка нужного товара: ищем среди всех карточек ту, где есть это название."""
        return self.cards.filter(has_text=name)

    @allure.step("Ищем в каталоге: {text}")
    def search(self, text):
        self.search_input.fill(text)
        self.apply_button.click()

    @allure.step("Выбираем категорию {name}")
    def choose_category(self, name):
        self.category_select.select_option(label=name)
        self.apply_button.click()

    @allure.step("Сортируем: {label}, {order}")
    def sort_by(self, label, order="По возрастанию"):
        self.sort_select.select_option(label=label)
        self.order_select.select_option(label=order)
        self.apply_button.click()

    @allure.step("Кладём в корзину товар {name}")
    def add_to_cart(self, name):
        self.card(name).get_by_test_id("add-to-cart").click()

    def open_product(self, name):
        self.card(name).get_by_test_id("product-name").click()

    def prices(self):
        """Цены всех карточек на странице числами: «58 171.00 ₽» -> 58171.0."""
        return [
            float(text.replace("₽", "").replace("\xa0", "").replace(" ", ""))
            for text in self.cards.get_by_test_id("product-price").all_inner_texts()
        ]