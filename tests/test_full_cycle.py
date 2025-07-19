import time
import csv
import pytest
from defi_fund.cli.app import deposit, withdraw, crystallize
from defi_fund.state import load_state
from defi_fund.accounting import YEAR_SECONDS


def test_full_deposit_withdraw_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    tx_file = tmp_path / "tx.csv"
    monkeypatch.setenv("FUND_STATE_FILE", str(state_file))
    monkeypatch.setenv("FUND_TX_LOG", str(tx_file))

    # start at t=0
    monkeypatch.setattr(time, "time", lambda: 0)
    deposit(100.0)

    # mid year additional deposit
    monkeypatch.setattr(time, "time", lambda: YEAR_SECONDS // 2)
    deposit(50.0)

    # late year withdrawal
    monkeypatch.setattr(time, "time", lambda: 3 * YEAR_SECONDS // 4)
    withdraw(30.0)

    # settle fees after a year and a half
    monkeypatch.setattr(time, "time", lambda: int(1.5 * YEAR_SECONDS))
    crystallize()

    state = load_state()
    # after crystallization fee accounts should be cleared
    assert state["mgmt_acc"] == pytest.approx(0.0)
    assert state["perf_acc"] == pytest.approx(0.0)
    # shares remain positive after operations
    assert state["total_shares"] > 0

    # transaction log should contain all actions
    with open(tx_file) as f:
        rows = list(csv.reader(f))
    assert len(rows) == 3
