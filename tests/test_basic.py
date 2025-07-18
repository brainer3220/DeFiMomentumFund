import pytest
from defi_fund.cli.app import deposit, withdraw
from defi_fund.state import load_state, reset_state

def test_deposit_and_withdraw(capsys, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql:///defi_test")
    reset_state()

    deposit(10.0)
    withdraw(5.0)
    out, _ = capsys.readouterr()
    assert "Deposited" in out and "Withdrew" in out

    state = load_state()
    assert state["total_assets"] == pytest.approx(5.0)
    assert state["total_shares"] == pytest.approx(5.0)
