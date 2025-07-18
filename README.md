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
1. **UV 설치**
   ```bash
   pipx install uv
   ```
2. **의존성 설치 및 가상환경 생성**
   ```bash
   uv venv
   uv pip install -e .[dev]
   ```
3. **PostgreSQL 준비**
   로컬에서 서버를 실행하고 데이터베이스를 생성합니다.
   ```bash
   sudo service postgresql start
   sudo -u postgres createdb defi_test
   ```
4. **CLI 실행**
   ```bash
   source .venv/bin/activate
   # DATABASE_URL 환경변수를 지정하여 사용합니다
   export DATABASE_URL=postgresql://postgres@localhost/defi_test
   defi-cli --help
   ```

### 예시 사용법
```bash
# 10 토큰 예치 후 5 지분 상환
defi-cli deposit 10
defi-cli withdraw 5
defi-cli info
```
