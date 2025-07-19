import time
import pytest

from defi_fund.cli.app import deposit, withdraw, crystallize
from defi_fund.state import load_state
from defi_fund.accounting import YEAR_SECONDS


def test_crystallize_after_multiple_actions(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    tx_file = tmp_path / "tx.csv"
    monkeypatch.setenv("FUND_STATE_FILE", str(state_file))
    monkeypatch.setenv("FUND_TX_LOG", str(tx_file))

    monkeypatch.setattr(time, "time", lambda: 0)
    deposit(10.0)

    monkeypatch.setattr(time, "time", lambda: YEAR_SECONDS // 2)
    deposit(5.0)
    withdraw(3.0)

    monkeypatch.setattr(time, "time", lambda: YEAR_SECONDS)
    crystallize()

    state = load_state()
    assert state["mgmt_acc"] == pytest.approx(0.0)
    assert state["perf_acc"] == pytest.approx(0.0)
    assert state["total_shares"] > 0
