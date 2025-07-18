import os
import pytest
from defi_fund.cli.app import deposit, withdraw
from defi_fund.web.admin import app as admin_app
from fastapi.testclient import TestClient
from defi_fund.state import load_state
import time

def test_deposit_and_withdraw(tmp_path, capsys, monkeypatch):
    state_file = tmp_path / "state.json"
    monkeypatch.setenv("FUND_STATE_FILE", str(state_file))
    monkeypatch.setattr(time, "time", lambda: 0)

    deposit(10.0)
    withdraw(5.0)
    out, _ = capsys.readouterr()
    assert "Deposited" in out and "Withdrew" in out

    state = load_state()
    assert state["total_assets"] == pytest.approx(5.0)
    assert state["total_shares"] == pytest.approx(5.0)


def test_admin_page(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    monkeypatch.setenv("FUND_STATE_FILE", str(state_file))
    monkeypatch.setenv("ADMIN_PASS", "secret")
    deposit(1.0)

    client = TestClient(admin_app)
    resp = client.get("/")
    assert resp.status_code == 401

    resp = client.get("/", auth=("admin", "secret"))
    assert resp.status_code == 200
    assert "Fund State" in resp.text
