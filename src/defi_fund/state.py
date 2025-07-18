import json
import os
import time
from pathlib import Path
from typing import Dict

from .config import settings

DEFAULT_STATE = {
    "total_assets": 0.0,
    "total_shares": 0.0,
    "mgmt_acc": 0.0,
    "perf_acc": 0.0,
    "hwm": 1.0,
    "last_update": 0.0,
}


def get_state_file() -> Path:
    """Return the path to the state file (evaluated lazily)."""
    return Path(os.getenv("FUND_STATE_FILE", str(settings.BASE_DIR / "fund_state.json")))


def load_state() -> Dict[str, float]:
    state_file = get_state_file()
    if state_file.exists():
        with open(state_file) as f:
            state = json.load(f)
    else:
        state = DEFAULT_STATE.copy()

    # ensure all keys exist
    for k, v in DEFAULT_STATE.items():
        state.setdefault(k, v)

    if state["last_update"] == 0.0:
        state["last_update"] = time.time()
    return state


def save_state(state: Dict[str, float]) -> None:
    state_file = get_state_file()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(state, f)
