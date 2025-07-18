# Defi_fund Project Scaffold

초기 DeFi 펀드 Python 프로젝트 스캐폴드입니다.

상세한 펀드 설계와 수수료 구조는 [`docs/manual_trading_fund_design.md`](docs/manual_trading_fund_design.md) 문서를 참고하세요.

## 구조
```
.
├── src/defi_fund/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   └── settings.py
│   ├── contracts/
│   │   └── __init__.py
│   └── cli/
│       └── app.py
├── tests/
│   └── test_basic.py
├── pyproject.toml
├── .gitignore
└── .env.example
```

## 사용 방법
1. **UV 설치**
   ```bash
   pipx install uv
   ```
2. **의존성 설치 및 가상환경 생성**
   ```bash
   uv venv
   uv pip install -e .[dev]
   ```
3. **CLI 실행**
   ```bash
   source .venv/bin/activate
   defi-cli --help
   ```

### 예시 사용법
```bash
# 10 토큰 예치 후 5 지분 상환
defi-cli deposit 10
defi-cli withdraw 5
defi-cli info
```
