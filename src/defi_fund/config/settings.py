"""Global configuration management using dotenv."""
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

WEB3_PROVIDER_URI: str = os.getenv("WEB3_PROVIDER_URI", "http://localhost:8545")
DEFAULT_GAS: int = int(os.getenv("DEFAULT_GAS", 250000))

# Asset symbol accepted for deposits (used for price oracle lookup)
DEPOSIT_ASSET: str = os.getenv("DEPOSIT_ASSET", "TOKEN")
# Optional Chainlink price feed address for the deposit asset
PRICE_FEED: str | None = os.getenv("PRICE_FEED")
