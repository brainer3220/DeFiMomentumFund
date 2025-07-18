"""Persistent fund state using PostgreSQL."""

import os
from typing import Dict

import psycopg2

DEFAULT_STATE = {"total_assets": 0.0, "total_shares": 0.0}


def get_conn():
    url = os.getenv("DATABASE_URL", "postgresql://postgres@localhost/defi_test")
    return psycopg2.connect(url)


def init_db() -> None:
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS fund_state ("
                "id INT PRIMARY KEY, total_assets FLOAT, total_shares FLOAT)"
            )
            cur.execute(
                "INSERT INTO fund_state (id, total_assets, total_shares)"
                " VALUES (1, 0.0, 0.0) ON CONFLICT (id) DO NOTHING"
            )
    conn.close()


def load_state() -> Dict[str, float]:
    init_db()
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT total_assets, total_shares FROM fund_state WHERE id=1"
            )
            row = cur.fetchone()
    conn.close()
    if row:
        return {"total_assets": float(row[0]), "total_shares": float(row[1])}
    return DEFAULT_STATE.copy()


def save_state(state: Dict[str, float]) -> None:
    init_db()
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE fund_state SET total_assets=%s, total_shares=%s WHERE id=1",
                (state["total_assets"], state["total_shares"]),
            )
    conn.close()


def reset_state() -> None:
    """Helper for tests: reset stored values to zero."""
    init_db()
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE fund_state SET total_assets=0.0, total_shares=0.0 WHERE id=1"
            )
    conn.close()
