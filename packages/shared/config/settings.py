import os

from dotenv import load_dotenv

load_dotenv()

LANDED_API_BASE_URL = os.getenv("LANDED_API_BASE_URL", "http://localhost:3001")
