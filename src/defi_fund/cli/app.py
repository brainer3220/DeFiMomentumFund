import typer, sys
from loguru import logger
from defi_fund.config import settings

app = typer.Typer(help="DeFi Fund CLI")


@app.command("deposit")
def deposit(amount: float):
    """예치 기능 (Mock)."""
    logger.info(f"Depositing {amount} tokens (mock)")


@app.command("withdraw")
def withdraw(shares: float):
    """출금 기능 (Mock)."""
    logger.info(f"Withdrawing {shares} shares (mock)")


@app.command("info")
def info():
    """펀드 정보 조회 (Mock)."""
    typer.echo("Fund NAV: 0.0 (mock)")


if __name__ == "__main__":
    app()
