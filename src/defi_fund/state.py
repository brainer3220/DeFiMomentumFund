"""State management backed by PostgreSQL."""

import os
from typing import Dict

import psycopg2
from psycopg2.extras import RealDictCursor

DEFAULT_STATE = {"total_assets": 0.0, "total_shares": 0.0}


def get_connection():
    """Return a new PostgreSQL connection using ``DATABASE_URL`` env var."""
    dsn = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1/postgres"
    )
    return psycopg2.connect(dsn)


def _init_table(cur) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS fund_state (
            id INTEGER PRIMARY KEY,
            total_assets DOUBLE PRECISION NOT NULL,
            total_shares DOUBLE PRECISION NOT NULL
        )
        """
    )


def load_state() -> Dict[str, float]:
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        _init_table(cur)
        cur.execute("SELECT total_assets, total_shares FROM fund_state WHERE id=1")
        row = cur.fetchone()
        if row is None:
            cur.execute(
                "INSERT INTO fund_state (id, total_assets, total_shares) VALUES (1, %s, %s)",
                (DEFAULT_STATE["total_assets"], DEFAULT_STATE["total_shares"]),
            )
            return DEFAULT_STATE.copy()
        return {"total_assets": row["total_assets"], "total_shares": row["total_shares"]}


def save_state(state: Dict[str, float]) -> None:
    with get_connection() as conn, conn.cursor() as cur:
        _init_table(cur)
        cur.execute(
            """
            INSERT INTO fund_state (id, total_assets, total_shares)
            VALUES (1, %s, %s)
            ON CONFLICT (id) DO UPDATE
              SET total_assets = EXCLUDED.total_assets,
                  total_shares = EXCLUDED.total_shares
            """,
            (state["total_assets"], state["total_shares"]),
        )
