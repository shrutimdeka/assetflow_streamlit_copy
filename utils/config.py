import os
from pathlib import Path

from dotenv import load_dotenv


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load local environment variables from .env
load_dotenv(BASE_DIR / ".env")


# ============================================================
# ZOHO CONFIGURATION
# ============================================================

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")

ZOHO_API_DOMAIN = os.getenv(
    "ZOHO_API_DOMAIN")

ZOHO_ACCOUNTS_URL = os.getenv(
    "ZOHO_ACCOUNTS_URL")

ZOHO_REDIRECT_URI = os.getenv("ZOHO_REDIRECT_URI")


# ============================================================
# VALIDATION
# ============================================================

REQUIRED_ZOHO_SETTINGS = {
    "ZOHO_CLIENT_ID": ZOHO_CLIENT_ID,
    "ZOHO_CLIENT_SECRET": ZOHO_CLIENT_SECRET,
    "ZOHO_REFRESH_TOKEN": ZOHO_REFRESH_TOKEN,
}


def validate_config():
    """
    Raise a clear error if required configuration is missing.
    """
    missing = [
        key
        for key, value in REQUIRED_ZOHO_SETTINGS.items()
        if not value
    ]

    if missing:
        raise EnvironmentError(
            "Missing required environment variables: "
            + ", ".join(missing)
        )