# Defi_fund Project Scaffold

초기 DeFi 펀드 Python 프로젝트 스캐폴드입니다.

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
1. Poetry 설치
   ```bash
   pipx install poetry
   ```
2. 의존성 설치
   ```bash
   poetry install
   ```
3. CLI 실행
   ```bash
   poetry run defi-cli --help
   ```
