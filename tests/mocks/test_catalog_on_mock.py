from decimal import Decimal

import pytest

from mocks.stubs import JSON_HEADERS, PRODUCTS_ENDPOINT, product_body
from models.products import ProductPage

pytestmark = [pytest.mark.mock, pytest.mark.products]


def catalog_page(items):
    return {
        "request": {
            "method": "GET",
            "urlPath": PRODUCTS_ENDPOINT,
            "queryParameters": {"page": {"equalTo": "1"}, "size": {"equalTo": "2"}},
        },
        "response": {
            "status": 200,
            "headers": JSON_HEADERS,
            "jsonBody": {
                "items": items,
                "total": len(items),
                "page": 1,
                "size": 2,
                "pages": 1,
            },
        },
    }


def test_catalog_page_turns_into_model(wiremock, mock_products_api):
    items = [
        product_body("11111111-1111-1111-1111-111111111111", sku="MOCK-1"),
        product_body("22222222-2222-2222-2222-222222222222", sku="MOCK-2", price="1000.00"),
    ]
    wiremock.add_stub(catalog_page(items))

    response = mock_products_api.get_products(params={"page": 1, "size": 2})

    page = ProductPage.model_validate(response.json())
    assert page.total == 2
    assert [product.sku for product in page.items] == ["MOCK-1", "MOCK-2"]
    assert page.items[1].price == Decimal("1000.00")