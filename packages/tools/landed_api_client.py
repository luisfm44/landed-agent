import requests

from packages.shared.config import LANDED_API_BASE_URL


def call_landed_api(path: str, params: dict | None = None) -> dict:
    try:
        response = requests.get(
            f"{LANDED_API_BASE_URL}{path}",
            params=params or {},
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
