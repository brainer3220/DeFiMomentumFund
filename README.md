# DeFi Momentum Fund

This repository provides a minimal implementation of an on-chain fund vault written in Python. It issues ERC‑20 shares for deposits and allows a manager account to execute trades while assets remain in the vault. Fees and state are tracked locally for demonstration.

Documentation is available in English and Korean:
- [English overview](docs/overview_en.md)
- [한국어 문서](docs/overview_ko.md)
- Detailed design notes: [docs/manual_trading_fund_design.md](docs/manual_trading_fund_design.md)
- Vault specification (KO): [docs/vault_spec_ko.md](docs/vault_spec_ko.md)
- Logic diagrams: [docs/logic_diagrams.md](docs/logic_diagrams.md)

## Quick Start
1. **Install `uv`**
   ```bash
   pipx install uv
   ```
2. **Create a virtual environment and install dependencies**
   ```bash
   uv venv
   uv pip install -e '.[dev]'
   ```
3. **Run the CLI**
   ```bash
   source .venv/bin/activate
   defi-cli --help
   ```

Example commands:
```bash
# Deposit 10 tokens and withdraw 5 shares
defi-cli deposit 10
defi-cli withdraw 5
```

Set `WEB3_PROVIDER_URI` and `PRIVATE_KEY` in `.env` to connect your wallet. See `docs/overview_en.md` for details and risk warnings.

---

# DeFi 모멘텀 펀드

이 저장소는 Python으로 작성된 간단한 DeFi 펀드 Vault 예제입니다. 예치 시 ERC-20 지분 토큰을 발행하고, 매니저가 Vault 내 자산을 이용해 거래할 수 있습니다. 자세한 내용은 위 문서 링크를 참고하세요.

## 사용 방법
1. **UV 설치**
   ```bash
   pipx install uv
   ```
2. **의존성 설치 및 가상환경 생성**
   ```bash
   uv venv
   uv pip install -e '.[dev]'
   ```
3. **CLI 실행**
   ```bash
   source .venv/bin/activate
   defi-cli --help
   ```

### 예시
```bash
# 10 토큰 예치 후 5 지분 상환
defi-cli deposit 10
defi-cli withdraw 5
```

관리 페이지를 사용하려면 `ADMIN_PASS` 환경변수를 설정한 뒤 `defi-admin` 명령을 실행하십시오.
