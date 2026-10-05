from models.orders import PaymentRequest


SUCCESS_CARD = "4242424242424242"
DECLINED_CARD = "4000000000000002"
NO_MONEY_CARD = "4000000000009995"
GATEWAY_ERROR_CARD = "4000000000000119"
SLOW_CARD = "4000000000003220"
TIMEOUT_CARD = "4000000000069999"

class OrderData:

    @staticmethod
    def payment(card_number=SUCCESS_CARD):
        payment_data = {
            "card_number": card_number,
            "card_holder": "IVAN TESTIROVSHCHIKOV",
            "exp_month": 12,
            "exp_year": 2030,
            "cvc": "123",
        }

        return PaymentRequest(**payment_data)
