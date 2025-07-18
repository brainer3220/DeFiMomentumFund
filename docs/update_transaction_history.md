# 거래내역 업데이트 가이드

이 문서는 펀드 운용 중 발생하는 입금과 출금 내역을 기록하여 추적하는 방법을 설명합니다. 기본적으로 `fund_state.json` 파일에 현재 자산과 지분 상태가 저장되지만, 별도의 거래 기록을 남겨 두면 보고서를 작성하거나 회계 처리를 할 때 유용합니다.

## 1. 기록 방식

- 각 CLI 명령 실행 후 거래 정보를 CSV 혹은 JSON 형식으로 저장합니다.
- 예시는 CSV 파일(`transactions.csv`)을 사용하며, 다음 항목을 포함합니다.
  - `timestamp` – 명령 실행 시각
  - `action` – `deposit` 또는 `withdraw`
  - `amount` – 토큰 수량 또는 상환된 지분 수량

## 2. 예시 스크립트

아래 스크립트는 Typer CLI를 호출한 뒤 거래 내역을 CSV 파일에 추가하는 간단한 방법을 보여 줍니다.

```python
import csv
import time
from defi_fund.cli.app import deposit, withdraw

LOG_FILE = "transactions.csv"


def log_transaction(action: str, amount: float) -> None:
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([int(time.time()), action, amount])


def deposit_with_log(amount: float) -> None:
    deposit(amount)
    log_transaction("deposit", amount)


def withdraw_with_log(shares: float) -> None:
    withdraw(shares)
    log_transaction("withdraw", shares)
```

## 3. 사용 방법

1. 위 스크립트를 프로젝트 루트에 저장한 뒤 필요한 함수(`deposit_with_log`, `withdraw_with_log`)를 호출합니다.
2. `transactions.csv` 파일이 없으면 자동으로 생성되며, 각 행에는 `timestamp,action,amount` 순으로 기록됩니다.
3. CSV 파일을 스프레드시트나 BI 도구로 불러와 거래내역을 분석할 수 있습니다.

이와 같이 간단한 로깅만으로도 펀드의 거래 흐름을 손쉽게 추적할 수 있습니다.
