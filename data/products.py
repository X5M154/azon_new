from utils.data_generator import DataGenerator


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
        return product_data

    @staticmethod
    def update_product_data():
        update_data = {
            "name": DataGenerator.generate_product_name(),
            "description": DataGenerator.generate_description(),
            "stock": DataGenerator.generate_stock(),
        }
        return update_data

    @staticmethod
    def update_product_price():
        update_price = {"price": str(DataGenerator.generate_price())}
        return update_price