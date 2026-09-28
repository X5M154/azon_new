import os
from dotenv import load_dotenv
from psycopg.conninfo import make_conninfo


load_dotenv()

DB_HOST = os.getenv("DB_HOST", "db.azon.130-17-2-195.sslip.io")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "student")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

AUTH_DB = "azon_auth"
PRODUCT_DB = "azon_product"
PAYMENT_DB = "azon_payment"

def conninfo(dbname):
    
    return make_conninfo(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=dbname,
        connect_timeout=10,
    )