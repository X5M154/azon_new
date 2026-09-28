from utils.data_generator import DataGenerator
from models.products import ProductRequest, ProductUpdate, ProductUpdatePrice
from decimal import Decimal
from uuid import UUID
from models.products import CartItemAddRequest, ProductPriceUpdateRequest


class ProductData:

    @staticmethod
    def creation_product_data(category_id):
        product_data = {
            "name": DataGenerator.generate_product_name(),
            "sku": DataGenerator.generate_sku(),
            "description": DataGenerator.generate_description(),
            "price": str(DataGenerator.generate_price()),
            "stock": DataGenerator.generate_stock(),
            "category_id": category_id,
        }
        return ProductRequest(**product_data)

    @staticmethod
    def update_product_data():
        update_data = {
            "name": DataGenerator.generate_product_name(),
            "description": DataGenerator.generate_description(),
            "stock": DataGenerator.generate_stock(),
        }
        return ProductUpdate(**update_data)

    @staticmethod
    def update_product_price():
        update_price = {"price": str(DataGenerator.generate_price())}
        return ProductUpdatePrice(**update_price)

    @staticmethod
    def cart_item_data(product_id: UUID, quantity: int = 1) -> CartItemAddRequest:
        return CartItemAddRequest(product_id=product_id, quantity=quantity)

    @staticmethod
    def price_data(
        current_price: Decimal | str | None = None,
    ) -> ProductPriceUpdateRequest:
        """Новая цена, отличающаяся от переданной текущей цены."""
        price = Decimal("19990.00")
        if current_price is not None and Decimal(str(current_price)) == price:
            price = Decimal("19991.00")

        return ProductPriceUpdateRequest(price=price)