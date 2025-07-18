import pytest
from defi_fund.cli.app import deposit, withdraw

def test_deposit_and_withdraw(capsys):
    deposit(1.0)
    withdraw(0.5)
    out, _ = capsys.readouterr()
    assert "Depositing" in out and "Withdrawing" in out
