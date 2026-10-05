import os

from dotenv import load_dotenv

load_dotenv()

AUTH_URL = "https://auth.azon.130-17-2-195.sslip.io"
PRODUCT_URL = "https://product.azon.130-17-2-195.sslip.io"
PAYMENT_URL = "https://payment.azon.130-17-2-195.sslip.io"

MOCK_URL = os.getenv("MOCK_URL", "http://localhost:8090")

FRONTEND_URL = "https://azon.130-17-2-195.sslip.io"