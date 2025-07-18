import os
import psycopg2
import pytest
from defi_fund.cli.app import deposit, withdraw
from defi_fund.state import load_state

def test_deposit_and_withdraw(monkeypatch, capsys):
    dsn = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://postgres:postgres@127.0.0.1/postgres",
    )
    monkeypatch.setenv("DATABASE_URL", dsn)
    with psycopg2.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS fund_state")

    deposit(10.0)
    withdraw(5.0)
    out, _ = capsys.readouterr()
    assert "Deposited" in out and "Withdrew" in out

    state = load_state()
    assert state["total_assets"] == pytest.approx(5.0)
    assert state["total_shares"] == pytest.approx(5.0)
