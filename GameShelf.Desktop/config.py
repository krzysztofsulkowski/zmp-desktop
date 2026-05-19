import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
VERIFY_SSL = os.getenv("VERIFY_SSL", "true").lower() == "true"