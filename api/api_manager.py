from api.auth_api import AuthAPI
from api.payment_api import PaymentAPI
from api.products_api import ProductsAPI
from api.user_api import UserAPI
from api.categories_api import CategoriesAPI

class ApiManager:
    """Единая точка доступа ко всем API стенда."""

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.products_api = ProductsAPI(session)
        self.payment_api = PaymentAPI(session)
        self.categories_api = CategoriesAPI(session)
