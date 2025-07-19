import typer
from loguru import logger
from defi_fund.state import load_state, save_state
from defi_fund.accounting import SPREAD_RATE, update_fees
from defi_fund.txlog import log_transaction

app = typer.Typer(help="DeFi Fund CLI")


@app.command("deposit")
def deposit(amount: float):
    """예치 기능: 자산을 예치하고 지분을 발행합니다."""
    state = load_state()
    update_fees(state)
    fee = amount * SPREAD_RATE
    net_amount = amount - fee
    price = state["total_assets"] / state["total_shares"] if state["total_shares"] > 0 else 1.0
    new_shares = net_amount / price
    state["total_assets"] += net_amount
    state["total_shares"] += new_shares
    save_state(state)
    log_transaction("deposit", amount)
    typer.echo(
        f"Deposited {amount} tokens -> {new_shares:.4f} shares (fee {fee:.4f})"
    )


@app.command("withdraw")
def withdraw(shares: float):
    """출금 기능: 보유 지분을 상환합니다."""
    state = load_state()
    update_fees(state)
    if shares > state["total_shares"]:
        typer.echo("Not enough shares", err=True)
        raise typer.Exit(code=1)
    price = state["total_assets"] / state["total_shares"] if state["total_shares"] > 0 else 1.0
    amount = shares * price
    fee = amount * SPREAD_RATE
    net_amount = amount - fee
    state["total_assets"] -= net_amount
    state["total_shares"] -= shares
    save_state(state)
    log_transaction("withdraw", shares)
    typer.echo(
        f"Withdrew {shares} shares -> {net_amount:.4f} tokens (fee {fee:.4f})"
    )


@app.command("crystallize")
def crystallize():
    """Accrue and settle outstanding fees."""
    state = load_state()
    update_fees(state)
    save_state(state)
    typer.echo("Fees crystallized")


@app.command("info")
def info():
    """펀드 정보 조회."""
    state = load_state()
    update_fees(state)
    price = state["total_assets"] / state["total_shares"] if state["total_shares"] > 0 else 1.0
    typer.echo(
        f"Assets: {state['total_assets']:.4f}, Shares: {state['total_shares']:.4f}, Price: {price:.4f}, "
        f"MgmtAcc: {state['mgmt_acc']:.4f}, PerfAcc: {state['perf_acc']:.4f}, HWM: {state['hwm']:.4f}"
    )


if __name__ == "__main__":
    app()
