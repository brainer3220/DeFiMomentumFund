"""State management backed by PostgreSQL."""

import os
from typing import Dict

import psycopg2
from psycopg2.extras import RealDictCursor

DEFAULT_STATE = {
    "total_assets": 0.0,
    "total_shares": 0.0,
    "mgmt_acc": 0.0,
    "perf_acc": 0.0,
    "hwm": 1.0,
    "last_update": 0.0,
}


def get_connection():
    """Return a new PostgreSQL connection using ``DATABASE_URL`` env var."""
    dsn = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1/postgres")
    return psycopg2.connect(dsn)


def _init_table(cur) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS fund_state (
            id INTEGER PRIMARY KEY,
            total_assets DOUBLE PRECISION NOT NULL,
            total_shares DOUBLE PRECISION NOT NULL,
            mgmt_acc DOUBLE PRECISION NOT NULL,
            perf_acc DOUBLE PRECISION NOT NULL,
            hwm DOUBLE PRECISION NOT NULL,
            last_update DOUBLE PRECISION NOT NULL
        )
        """
    )


def load_state() -> Dict[str, float]:
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        _init_table(cur)
        cur.execute(
            "SELECT total_assets, total_shares, mgmt_acc, perf_acc, hwm, last_update "
            "FROM fund_state WHERE id=1"
        )
        row = cur.fetchone()
        if row is None:
            cur.execute(
                "INSERT INTO fund_state (id, total_assets, total_shares, mgmt_acc, perf_acc, hwm, last_update) "
                "VALUES (1, %s, %s, %s, %s, %s, %s)",
                (
                    DEFAULT_STATE["total_assets"],
                    DEFAULT_STATE["total_shares"],
                    DEFAULT_STATE["mgmt_acc"],
                    DEFAULT_STATE["perf_acc"],
                    DEFAULT_STATE["hwm"],
                    DEFAULT_STATE["last_update"],
                ),
            )
            return DEFAULT_STATE.copy()
        state = dict(row)
        for k, v in DEFAULT_STATE.items():
            state.setdefault(k, v)
        return state


def save_state(state: Dict[str, float]) -> None:
    with get_connection() as conn, conn.cursor() as cur:
        _init_table(cur)
        cur.execute(
            """
            INSERT INTO fund_state (id, total_assets, total_shares, mgmt_acc, perf_acc, hwm, last_update)
            VALUES (1, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE
                SET total_assets = EXCLUDED.total_assets,
                    total_shares = EXCLUDED.total_shares,
                    mgmt_acc = EXCLUDED.mgmt_acc,
                    perf_acc = EXCLUDED.perf_acc,
                    hwm = EXCLUDED.hwm,
                    last_update = EXCLUDED.last_update
            """,
            (
                state["total_assets"],
                state["total_shares"],
                state.get("mgmt_acc", 0.0),
                state.get("perf_acc", 0.0),
                state.get("hwm", 1.0),
                state.get("last_update", 0.0),
            ),
        )
        conn.commit()
