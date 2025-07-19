import time
from typing import Dict

YEAR_SECONDS = 365 * 24 * 60 * 60
MGMT_RATE = 0.02  # 2% annual management fee
PERF_RATE = 0.20  # 20% performance fee
SPREAD_RATE = 0.001  # 0.10% deposit/withdraw spread


def accrue_management_fee(state: Dict[str, float], timestamp: float | None = None) -> None:
    """Accrue management fee based on elapsed time."""
    now = timestamp or time.time()
    elapsed = now - state.get("last_update", now)
    if elapsed <= 0:
        return
    rate_per_sec = MGMT_RATE / YEAR_SECONDS
    accrual = state.get("total_assets", 0.0) * rate_per_sec * elapsed
    state["mgmt_acc"] = state.get("mgmt_acc", 0.0) + accrual
    state["last_update"] = now


def accrue_performance_fee(state: Dict[str, float]) -> None:
    """Accrue performance fee if NAV exceeds the high-water mark."""
    total_assets = state.get("total_assets", 0.0)
    total_shares = state.get("total_shares", 0.0)
    if total_shares == 0:
        state["hwm"] = 1.0
        return
    price = total_assets / total_shares
    if price > state.get("hwm", price):
        accrual = (price - state["hwm"]) * total_shares * PERF_RATE
        state["perf_acc"] = state.get("perf_acc", 0.0) + accrual
        state["hwm"] = price


def settle_fees(state: Dict[str, float]) -> None:
    """Mint shares equivalent to accrued fees."""
    total_assets = state.get("total_assets", 0.0)
    total_shares = state.get("total_shares", 0.0)
    price = total_assets / total_shares if total_shares > 0 else 1.0
    fees = state.get("mgmt_acc", 0.0) + state.get("perf_acc", 0.0)
    if fees == 0:
        return
    new_shares = fees / price if price > 0 else 0.0
    state["total_shares"] = total_shares + new_shares
    # fees are represented by newly minted shares; assets remain unchanged
    state["mgmt_acc"] = 0.0
    state["perf_acc"] = 0.0


def update_fees(state: Dict[str, float], timestamp: float | None = None) -> None:
    """Accrue and settle all outstanding fees."""
    accrue_management_fee(state, timestamp)
    accrue_performance_fee(state)
    settle_fees(state)
