import csv
import os
import time
from pathlib import Path

from .config import settings


def get_log_file() -> Path:
    """Return path for transaction log file."""
    return Path(os.getenv("FUND_TX_LOG", str(settings.BASE_DIR / "transactions.csv")))


def log_transaction(action: str, amount: float) -> None:
    """Append a transaction record to the log."""
    log_file = get_log_file()
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([int(time.time()), action, amount])
