import allure

from pages.base_page import BasePage

SUCCESS_CARD = "4242424242424242"
DECLINED_CARD = "4000000000000002"
PROCESSING_CARD = "4000000000003220"


class OrderPage(BasePage):
    """Страница заказа: /orders/{order_id} - статус, оплата, история платежей."""

    url = "/orders"

    def __init__(self, page):
        super().__init__(page)

        self.order_id = page.get_by_test_id("order-id")
        self.status = page.get_by_test_id("order-status")
        self.order_total = page.get_by_test_id("order-total")
        self.items = page.get_by_test_id("order-item")

        self.payment_form = page.get_by_test_id("payment-form")
        self.card_number = page.get_by_test_id("card-number")
        self.card_holder = page.get_by_test_id("card-holder")
        self.exp_month = page.get_by_test_id("card-exp-month")
        self.exp_year = page.get_by_test_id("card-exp-year")
        self.cvc = page.get_by_test_id("card-cvc")
        self.pay_button = page.get_by_test_id("pay-button")

        self.processing = page.get_by_test_id("payment-processing")
        self.payments = page.get_by_test_id("payment-row")
        self.decline_code = page.get_by_test_id("payment-decline-code")
        self.cancel_button = page.get_by_test_id("cancel-order-button")

    def open_by_id(self, order_id):
        self.url = f"/orders/{order_id}"
        return self.open()

    @allure.step("Оплачиваем заказ картой {card_number}")
    def pay(self, card_number=SUCCESS_CARD, holder="TEST STUDENT", month="12", year="2030", cvc="123"):
        """Оплата картой: номер карты решает, чем всё закончится (см. тестовые карты стенда)."""
        self.card_number.fill(card_number)
        self.card_holder.fill(holder)
        self.exp_month.fill(month)
        self.exp_year.fill(year)
        self.cvc.fill(cvc)
        self.pay_button.click()

    def cancel(self):
        self.cancel_button.click()

class OrdersPage(BasePage):
    """Список заказов покупателя: /orders."""

    url = "/orders"

    def __init__(self, page):
        super().__init__(page)

        self.table = page.get_by_test_id("orders-table")
        self.rows = page.get_by_test_id("order-row")
        self.empty = page.get_by_test_id("orders-empty")

    def row(self, order_id):
        return self.rows.filter(has_text=str(order_id)[:8])

    def open_first(self):
        self.rows.first.get_by_test_id("order-link").click()