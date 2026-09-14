import uuid
from faker import Faker
from decimal import Decimal
import random

fake = Faker("en_US")

class DataGenerator:

    @staticmethod
    def generate_email():
        return f"student-{uuid.uuid4().hex[:8]}@example.com"

    @staticmethod
    def generate_password():
        return fake.password(length=12)

    @staticmethod
    def generate_fullname():
        return fake.name()

    @staticmethod
    def generate_product_name():
        return fake.word()

    @staticmethod
    def generate_sku():
        return f"{uuid.uuid4().hex[:33]}"

    @staticmethod
    def generate_description():
        return fake.sentence(nb_words=12)

    @staticmethod
    def generate_price():
        cents = fake.random_int(min=100, max=999_999)
        price = Decimal(cents) / Decimal(100)
        return price

    @staticmethod
    def generate_stock():
        return fake.random_int(min=1, max=1000000) # min=0 надо или нет?

