# DeFi Momentum Fund Overview

This document provides a high level description of the DeFi Momentum Fund project and how the on-chain vault operates.

## Project Goals
- Create a chain-agnostic vault that mints ERC-20 shares for deposited assets.
- Allow a fund manager to execute trades while assets remain in the vault.
- Accrue management and performance fees automatically on every interaction.

## Vault Mechanics
1. **Deposit**
   - Users call `deposit(amount)` on the vault contract.
   - A 0.10% spread is deducted and recorded for gas reimbursement.
   - New shares are minted based on the current Net Asset Value (NAV).
2. **Redeem**
   - Users call `redeem(shares)` to withdraw their share of the underlying asset.
   - The same 0.10% spread applies to withdrawals.
3. **Fee Accrual**
   - Management fee: 2% per year, accrued continuously.
   - Performance fee: 20% of profits above the high‑water mark.
   - A portion of performance fees is sent to the DAO treasury.
4. **Trade Execution**
   - The manager invokes `executeTrade(target, data)` which performs a call on an approved contract.
   - Guardians can block functions or pause the vault in emergencies.
5. **Gas Reimbursement**
   - Spread fees accumulate as a gas buffer and can be claimed via `claimGas(amount, to)`.

## Using the Python CLI
The repository ships with a Typer CLI for local testing:
```bash
# Deposit 10 tokens
defi-cli deposit 10

# Withdraw 5 shares
defi-cli withdraw 5

# Settle fees
defi-cli crystallize
```
State is stored in `fund_state.json` by default and can be overridden with the `FUND_STATE_FILE` environment variable.

## Wallet Configuration
1. Copy `.env.example` to `.env` and fill in `WEB3_PROVIDER_URI` and `PRIVATE_KEY`.
2. Optional variables include `DEFAULT_GAS` and `PRICE_FEED` for price oracle integration.
3. The CLI and web interfaces will read these values using `python-dotenv`.

## Risks
DeFi investments are inherently risky. This project is for demonstration purposes only and does not provide financial advice. Use at your own risk and test on a local network before deploying real assets.
