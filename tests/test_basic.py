import os
import pytest
from defi_fund.cli.app import deposit, withdraw
from defi_fund.web.admin import app as admin_app
from defi_fund.web.frontend import app as web_app
from fastapi.testclient import TestClient
from defi_fund.state import load_state
from defi_fund.oracle import get_price
import time

def test_deposit_and_withdraw(tmp_path, capsys, monkeypatch):
    state_file = tmp_path / "state.json"
    tx_file = tmp_path / "tx.csv"
    monkeypatch.setenv("FUND_STATE_FILE", str(state_file))
    monkeypatch.setenv("FUND_TX_LOG", str(tx_file))
    monkeypatch.setattr(time, "time", lambda: 0)

    deposit(10.0)
    withdraw(5.0)
    out, _ = capsys.readouterr()
    assert "Deposited" in out and "Withdrew" in out

    state = load_state()
    assert state["total_assets"] == pytest.approx(4.995)
    assert state["total_shares"] == pytest.approx(4.99)
    assert tx_file.exists()


def test_admin_page(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    tx_file = tmp_path / "tx.csv"
    monkeypatch.setenv("FUND_STATE_FILE", str(state_file))
    monkeypatch.setenv("FUND_TX_LOG", str(tx_file))
    monkeypatch.setenv("ADMIN_PASS", "secret")
    deposit(1.0)

    client = TestClient(admin_app)
    resp = client.get("/")
    assert resp.status_code == 401

    resp = client.get("/", auth=("admin", "secret"))
    assert resp.status_code == 200
    assert "Fund State" in resp.text


def test_oracle_env_override(monkeypatch):
    monkeypatch.setenv("MOCK_PRICE_TOKEN", "2.0")
    price = get_price("TOKEN")
    assert price == 2.0


def test_web_api(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    tx_file = tmp_path / "tx.csv"
    monkeypatch.setenv("FUND_STATE_FILE", str(state_file))
    monkeypatch.setenv("FUND_TX_LOG", str(tx_file))

    client = TestClient(web_app)
    resp = client.post("/api/deposit", json={"amount": 1.0})
    assert resp.status_code == 200
    resp = client.get("/api/state")
    data = resp.json()
    assert data["total_assets"] > 0
