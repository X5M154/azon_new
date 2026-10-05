import logging

import requests

from config.hosts import MOCK_URL
from requester.custom_requester import CustomRequester

logger = logging.getLogger("azon_tests")


class WireMockAdmin(CustomRequester):
    """Клиент админского API WireMock: создаёт стабы и читает журнал запросов.

    Наследуемся от CustomRequester по той же причине, что и API-клиенты стенда:
    админка WireMock - это обычный HTTP API, а логирование и проверка статуса
    у нас уже написаны.
    """

    MAPPINGS_ENDPOINT = "/__admin/mappings"
    REQUESTS_ENDPOINT = "/__admin/requests"

    def __init__(self, session=None, base_url=MOCK_URL):
        super().__init__(session or requests.Session(), base_url)

    def is_running(self):
        """Отвечает ли WireMock: если нет - тесты с моками честно пропускаем."""
        try:
            self.send_request("GET", "/__admin/health", timeout=2)
        except (requests.RequestException, AssertionError):
            return False
        return True

    def add_stub(self, mapping):
        """Создаёт один стаб. WireMock отвечает 201 и телом созданного мэппинга."""
        return self.send_request(
            "POST", self.MAPPINGS_ENDPOINT, json=mapping, expected_status=201
        )

    def reset(self):
        """Сбрасывает и стабы, и журнал - следующий тест начинает с чистого листа."""
        return self.send_request("POST", "/__admin/reset")

    def count_requests(self, matcher):
        """Сколько запросов, подходящих под matcher, WireMock получил."""
        response = self.send_request(
            "POST", f"{self.REQUESTS_ENDPOINT}/count", json=matcher
        )
        return response.json()["count"]

    def find_requests(self, matcher):
        """Сами запросы, подходящие под matcher: метод, url, заголовки, тело."""
        response = self.send_request(
            "POST", f"{self.REQUESTS_ENDPOINT}/find", json=matcher
        )
        return response.json()["requests"]

    def _log_request_and_response(self, response):
        # ответы админки WireMock длинные: в логе прогона хватит одной строки на вызов
        logger.info(
            "мок: %s %s -> %s",
            response.request.method,
            response.request.url,
            response.status_code,
        )