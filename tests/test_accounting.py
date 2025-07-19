import math
import time
import pytest

from defi_fund.accounting import (
    MGMT_RATE,
    PERF_RATE,
    YEAR_SECONDS,
    accrue_management_fee,
    accrue_performance_fee,
    settle_fees,
)


def test_performance_fee_and_hwm():
    state = {
        "total_assets": 120.0,
        "total_shares": 100.0,
        "mgmt_acc": 0.0,
        "perf_acc": 0.0,
        "hwm": 1.0,
        "last_update": 0.0,
    }
    accrue_performance_fee(state)
    expected_perf = (1.2 - 1.0) * 100.0 * PERF_RATE
    assert state["perf_acc"] == pytest.approx(expected_perf)
    assert state["hwm"] == pytest.approx(1.2)

    settle_fees(state)
    expected_shares = 100.0 + expected_perf / 1.2
    assert state["total_shares"] == pytest.approx(expected_shares)
    assert state["perf_acc"] == 0.0


def test_management_fee_over_time():
    state = {
        "total_assets": 100.0,
        "total_shares": 100.0,
        "mgmt_acc": 0.0,
        "perf_acc": 0.0,
        "hwm": 1.0,
        "last_update": 0.0,
    }
    accrue_management_fee(state, timestamp=YEAR_SECONDS)
    expected_mgmt = 100.0 * MGMT_RATE
    assert state["mgmt_acc"] == pytest.approx(expected_mgmt)

    settle_fees(state)
    assert state["mgmt_acc"] == 0.0
    assert state["total_shares"] == pytest.approx(100.0 + expected_mgmt / 1.0)


def test_extreme_profit_no_overflow():
    state = {
        "total_assets": 1e9,
        "total_shares": 1.0,
        "mgmt_acc": 0.0,
        "perf_acc": 0.0,
        "hwm": 1.0,
        "last_update": 0.0,
    }
    accrue_performance_fee(state)
    assert math.isfinite(state["perf_acc"])
    assert state["hwm"] == pytest.approx(1e9)
