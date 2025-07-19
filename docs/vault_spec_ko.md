# Vault 스마트컨트랙트 상세 명세

이 문서는 `Vault.sol`의 각 함수 동작과 수학적 계산, 보안 고려사항을 정리한 개발자용 설계 명세서입니다. 오픈소스 공개 및 외부 보안 감사 시 참고 자료로 활용할 수 있습니다.

## 1. 기본 상수 및 역할

- `MGMT_RATE = 2e16` – 연 2% 운용 수수료를 의미하며 `RATE_SCALE(1e18)` 기준으로 계산됩니다.
- `PERF_RATE = 2e17` – 성과 보수 20%를 나타냅니다.
- `DAO_SHARE = 1e17 / 10` – 성과 보수 중 10%가 DAO 금고로 분배됩니다.
- `MANAGER_ROLE` – 거래 실행 및 가스비 청구 권한 보유.
- `GUARDIAN_ROLE` – 비상 정지 및 업그레이드 승인 권한 보유.

## 2. 외부 함수

### `initialize(address asset, address manager, address dao, address guardian)`
- 업그레이드 가능한 ERC-20 Vault 초기화 함수입니다.
- 역할 배분과 기본 수수료 지표(`lastAccrual`, `hwm`)를 설정합니다.

### `deposit(uint256 amount)`
- 자산을 예치하면 0.10% 스프레드가 공제되고, 나머지 금액에 따라 지분이 발행됩니다.
- 계산식: `shares = supply == 0 ? net : (net * supply) / assetsBefore`.
- 공제된 스프레드는 `feeReserves`와 `gasAcc`에 적립되어 가스 환급 재원으로 사용됩니다.

### `redeem(uint256 shares)`
- 보유 지분을 상환해 자산을 인출합니다. 출금액에도 동일한 스프레드가 적용됩니다.
- 현재 순자산가치 대비 지분 비율만큼 자산이 지급됩니다.

### `executeTrade(address target, bytes data)`
- 매니저가 화이트리스트된 계약(`approvedTargets`)에 임의 호출을 수행합니다.
- 특정 함수 시그니처가 `blockedFunctions`에 등록되어 있으면 실행이 거부됩니다.
- 모든 자산은 Vault 주소에 남아 있으므로 외부 호출 실패 시 자금 손실을 막을 수 있습니다.

### `pauseVault()` / `unpauseVault()`
- 가디언이 Vault를 비상 정지하거나 다시 활성화할 수 있습니다.

### `setApprovedTarget(address target, bool approved)`
- 거래 대상 화이트리스트를 갱신합니다. 악성 계약 호출을 방지하기 위해 철저한 검증이 필요합니다.

### `setBlockedFunction(bytes4 selector, bool blocked)`
- 취약점이 발견된 외부 함수 시그니처를 즉시 차단할 수 있습니다.

### `claimGas(uint256 amount, address to)`
- 매니저가 누적된 가스비를 청구합니다. `gasAcc`와 `feeReserves`가 감소하며, 실 자산이 전송됩니다.

### `assetBalance()`
- Vault가 보유한 기초 자산의 잔액을 반환합니다.

## 3. 내부 회계 로직

### `_updateFees()`
1. `_accrueManagement()` – `elapsed = block.timestamp - lastAccrual`을 구해 운용 수수료를 `mgmtAcc`에 누적합니다. 계산식은 `(netAssets * MGMT_RATE * elapsed) / YEAR / RATE_SCALE`입니다.
2. `_accruePerformance()` – 지분 가격이 `hwm`을 초과하면 초과분에 성과 보수를 적용하여 `perfAcc`에 누적합니다.
3. `_settleFees()` – 위에서 누적된 `mgmtAcc`와 `perfAcc`를 지분으로 정산하여 매니저와 DAO에게 발행합니다.

### `_netAssets()`
- `feeReserves`를 제외한 실제 자산 잔액을 반환합니다.

## 4. 보안 고려사항

- **권한 관리**: 역할 기반 접근 제어를 통해 매니저와 가디언의 권한을 구분합니다. 멀티시그 지갑 사용을 권장합니다.
- **화이트리스트**: `executeTrade` 호출 대상과 차단 함수 목록을 주기적으로 점검하여 악성 계약이나 의도치 않은 호출을 방지합니다.
- **업그레이드**: `_authorizeUpgrade`는 가디언만 호출할 수 있습니다. 업그레이드 전 충분한 검토와 테스트가 필요합니다.
- **오라클 의존성**: 지분 가격과 수수료 계산이 오라클 가격에 의존한다면, 오라클 조작 위험을 반드시 고려해야 합니다.

## 5. 개발 가이드라인

- 함수별 의도와 계산 근거를 주석으로 명확히 남기고, 중요한 상수 값 변경 시 문서도 함께 업데이트합니다.
- 테스트 코드 추가 시 실제 수수료 계산 결과와 일치하는지 검증하여 회귀 오류를 방지합니다.
- 잠재적 업그레이드나 포크를 대비해 본 명세서를 최신 상태로 유지합니다.

