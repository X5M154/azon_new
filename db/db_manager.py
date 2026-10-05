from config.db import AUTH_DB, PAYMENT_DB, PRODUCT_DB, conninfo
from db.auth_db import AuthDB
from db.payment_db import PaymentDB
from db.product_db import ProductDB


class DBManager:

    def __init__(self):
        self.auth = AuthDB(conninfo(AUTH_DB))
        self.product = ProductDB(conninfo(PRODUCT_DB))
        self.payment = PaymentDB(conninfo(PAYMENT_DB))

    def close(self):
        for client in (self.auth, self.product, self.payment):
            client.close()