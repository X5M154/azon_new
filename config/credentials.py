import os
from dotenv import load_dotenv

load_dotenv()

MANAGER_INVITE = os.getenv("MANAGER_INVITE", "")
ADMIN_INVITE = os.getenv("ADMIN_INVITE", "")