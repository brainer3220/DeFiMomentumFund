from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from defi_fund.state import load_state, save_state
from defi_fund.accounting import SPREAD_RATE, update_fees
from defi_fund.txlog import log_transaction
from defi_fund.oracle import get_price
from defi_fund.config import settings

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="DeFi Fund Frontend")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


class DepositRequest(BaseModel):
    amount: float


@app.post("/api/deposit")
def api_deposit(req: DepositRequest) -> dict:
    state = load_state()
    update_fees(state)
    fee = req.amount * SPREAD_RATE
    net_amount = req.amount - fee
    asset_price = get_price(settings.DEPOSIT_ASSET)
    nav_usd = state["total_assets"] * asset_price
    share_price = nav_usd / state["total_shares"] if state["total_shares"] > 0 else asset_price
    new_shares = (net_amount * asset_price) / share_price
    state["total_assets"] += net_amount
    state["total_shares"] += new_shares
    save_state(state)
    log_transaction("deposit", req.amount)
    return {"new_shares": new_shares, "fee": fee}


class WithdrawRequest(BaseModel):
    shares: float


@app.post("/api/withdraw")
def api_withdraw(req: WithdrawRequest) -> dict:
    state = load_state()
    update_fees(state)
    if req.shares > state["total_shares"]:
        raise HTTPException(status_code=400, detail="Not enough shares")
    asset_price = get_price(settings.DEPOSIT_ASSET)
    nav_usd = state["total_assets"] * asset_price
    share_price = nav_usd / state["total_shares"] if state["total_shares"] > 0 else asset_price
    amount_usd = req.shares * share_price
    amount = amount_usd / asset_price
    fee = amount * SPREAD_RATE
    net_amount = amount - fee
    state["total_assets"] -= net_amount
    state["total_shares"] -= req.shares
    save_state(state)
    log_transaction("withdraw", req.shares)
    return {"amount": net_amount, "fee": fee}


@app.get("/api/state")
def api_state() -> dict:
    state = load_state()
    update_fees(state)
    asset_price = get_price(settings.DEPOSIT_ASSET)
    nav_usd = state["total_assets"] * asset_price
    price = nav_usd / state["total_shares"] if state["total_shares"] > 0 else asset_price
    return {
        "total_assets": state["total_assets"],
        "total_shares": state["total_shares"],
        "share_price": price,
        "mgmt_acc": state["mgmt_acc"],
        "perf_acc": state["perf_acc"],
        "hwm": state["hwm"],
    }


def main() -> None:
    import uvicorn

    uvicorn.run("defi_fund.web.frontend:app", host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
