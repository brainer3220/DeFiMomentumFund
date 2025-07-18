import os
import time
import psycopg2
import pytest
from fastapi.testclient import TestClient

from defi_fund.cli.app import deposit, withdraw
from defi_fund.state import load_state
from defi_fund.web.admin import app as admin_app


def reset_db(dsn: str) -> None:
    with psycopg2.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS fund_state")


def test_deposit_and_withdraw(monkeypatch, capsys):
    dsn = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1/postgres")
    monkeypatch.setenv("DATABASE_URL", dsn)
    reset_db(dsn)
    monkeypatch.setattr(time, "time", lambda: 0)

    deposit(10.0)
    withdraw(5.0)
    out, _ = capsys.readouterr()
    assert "Deposited" in out and "Withdrew" in out

    state = load_state()
    assert state["total_assets"] == pytest.approx(5.0)
    assert state["total_shares"] == pytest.approx(5.0)


def test_admin_page(monkeypatch):
    dsn = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1/postgres")
    monkeypatch.setenv("DATABASE_URL", dsn)
    monkeypatch.setenv("ADMIN_PASS", "secret")
    reset_db(dsn)
    deposit(1.0)

    client = TestClient(admin_app)
    resp = client.get("/")
    assert resp.status_code == 401

    resp = client.get("/", auth=("admin", "secret"))
    assert resp.status_code == 200
    assert "Fund State" in resp.text
