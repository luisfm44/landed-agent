import os

import requests
from dotenv import load_dotenv

load_dotenv()

LANDED_API_BASE_URL = os.getenv("LANDED_API_BASE_URL", "http://localhost:3001")


def call_landed_api(path: str, params: dict) -> dict:
    try:
        response = requests.get(
            f"{LANDED_API_BASE_URL}{path}",
            params=params,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {
            "error": "LANDED_TIMEOUT",
            "message": "Landed backend took too long to respond.",
        }
    except requests.exceptions.RequestException as error:
        return {
            "error": "LANDED_API_ERROR",
            "message": str(error),
        }
