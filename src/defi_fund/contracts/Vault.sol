pragma solidity ^0.8.20;

import "@openzeppelin/contracts-upgradeable/token/ERC20/IERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/PausableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

/// @title DeFiMomentumFund Vault
/// @notice ERC20 share issuing vault with upgradeability and access control.
contract Vault is ERC20Upgradeable, AccessControlUpgradeable, PausableUpgradeable, UUPSUpgradeable {
    bytes32 public constant MANAGER_ROLE = keccak256("MANAGER_ROLE");
    bytes32 public constant GUARDIAN_ROLE = keccak256("GUARDIAN_ROLE");

    IERC20Upgradeable public asset;

    uint256 public constant RATE_SCALE = 1e18;
    uint256 public constant YEAR = 365 days;

    uint256 public constant MGMT_RATE = 2e16; // 2% annual
    uint256 public constant PERF_RATE = 2e17; // 20% of profit
    uint256 public constant DAO_SHARE = 1e17 / 10; // 10% of performance fee
    uint256 public constant SPREAD_RATE = 1e15; // 0.1% deposit/withdraw spread

    address public manager;
    address public daoTreasury;

    uint256 public lastAccrual;
    uint256 public hwm; // high-water mark scaled by 1e18

    uint256 public mgmtAcc;
    uint256 public perfAcc;

    uint256 public feeReserves; // accumulated spreads
    uint256 public gasAcc; // available gas reimbursement

    mapping(address => bool) public approvedTargets;
    mapping(bytes4 => bool) public blockedFunctions;

    event TargetApproved(address indexed target, bool approved);
    event FunctionBlocked(bytes4 indexed selector, bool blocked);

    /// @notice Initialize the vault
    /// @param asset_ Token accepted for deposits
    /// @param manager Address receiving fees and able to execute trades
    /// @param dao Address of DAO treasury for protocol fees
    /// @param guardian Multisig guardian able to pause and upgrade the vault
    function initialize(address asset_, address manager_, address dao_, address guardian) public initializer {
        __ERC20_init("FUND SHARE", "FUND");
        __AccessControl_init();
        __Pausable_init();
        __UUPSUpgradeable_init();

        asset = IERC20Upgradeable(asset_);
        _grantRole(DEFAULT_ADMIN_ROLE, guardian);
        _grantRole(MANAGER_ROLE, manager_);
        _grantRole(GUARDIAN_ROLE, guardian);

        manager = manager_;
        daoTreasury = dao_;
        lastAccrual = block.timestamp;
        hwm = RATE_SCALE;
    }

    /// @notice Deposit assets and mint vault shares with spread fee
    function deposit(uint256 amount) external whenNotPaused {
        _updateFees();

        uint256 assetsBefore = _netAssets();
        uint256 balBefore = asset.balanceOf(address(this));
        require(asset.transferFrom(msg.sender, address(this), amount), "transfer failed");
        uint256 received = asset.balanceOf(address(this)) - balBefore;
        uint256 spread = (received * SPREAD_RATE) / RATE_SCALE;
        uint256 net = received - spread;

        feeReserves += spread;
        gasAcc += spread;

        uint256 supply = totalSupply();
        uint256 shares = supply == 0 ? net : (net * supply) / assetsBefore;
        _mint(msg.sender, shares);
    }

    /// @notice Redeem shares for underlying asset with spread fee
    function redeem(uint256 shares) external whenNotPaused {
        _updateFees();

        uint256 supply = totalSupply();
        uint256 assetsBefore = _netAssets();
        uint256 amount = (shares * assetsBefore) / supply;
        uint256 spread = (amount * SPREAD_RATE) / RATE_SCALE;
        uint256 netAmount = amount - spread;

        feeReserves += spread;
        gasAcc += spread;

        _burn(msg.sender, shares);
        require(asset.transfer(msg.sender, netAmount), "transfer failed");
    }

    /// @notice Execute arbitrary call for asset management
    function executeTrade(address target, bytes calldata data)
        external
        whenNotPaused
        onlyRole(MANAGER_ROLE)
        returns (bytes memory)
    {
        require(approvedTargets[target], "target not approved");
        bytes4 selector;
        assembly {
            selector := calldataload(data.offset)
        }
        require(!blockedFunctions[selector], "function blocked");
        (bool ok, bytes memory ret) = target.call(data);
        require(ok, "trade failed");
        return ret;
    }

    /// @notice Pause vault in emergencies
    function pauseVault() external onlyRole(GUARDIAN_ROLE) {
        _pause();
    }

    /// @notice Unpause vault
    function unpauseVault() external onlyRole(GUARDIAN_ROLE) {
        _unpause();
    }

    /// @notice Approve or revoke a target contract for trading
    function setApprovedTarget(address target, bool approved) external onlyRole(GUARDIAN_ROLE) {
        approvedTargets[target] = approved;
        emit TargetApproved(target, approved);
    }

    /// @notice Block or allow a specific function selector
    function setBlockedFunction(bytes4 selector, bool blocked) external onlyRole(GUARDIAN_ROLE) {
        blockedFunctions[selector] = blocked;
        emit FunctionBlocked(selector, blocked);
    }

    /// @dev Required for UUPS upgrades, restricted to guardian
    function _authorizeUpgrade(address newImplementation) internal override onlyRole(GUARDIAN_ROLE) {}

    function _netAssets() internal view returns (uint256) {
        return asset.balanceOf(address(this)) - feeReserves;
    }

    function _accrueManagement() internal {
        uint256 elapsed = block.timestamp - lastAccrual;
        if (elapsed > 0) {
            mgmtAcc += (_netAssets() * MGMT_RATE * elapsed) / YEAR / RATE_SCALE;
            lastAccrual = block.timestamp;
        }
    }

    function _accruePerformance() internal {
        uint256 supply = totalSupply();
        if (supply == 0) {
            hwm = RATE_SCALE;
            return;
        }
        uint256 price = (_netAssets() * RATE_SCALE) / supply;
        if (price > hwm) {
            uint256 gain = ((price - hwm) * supply) / RATE_SCALE;
            perfAcc += (gain * PERF_RATE) / RATE_SCALE;
            hwm = price;
        }
    }

    function _settleFees() internal {
        uint256 supply = totalSupply();
        if (supply == 0) {
            mgmtAcc = 0;
            perfAcc = 0;
            return;
        }
        uint256 price = (_netAssets() * RATE_SCALE) / supply;
        uint256 daoAmt = (perfAcc * DAO_SHARE) / RATE_SCALE;
        uint256 mgrAmt = mgmtAcc + perfAcc - daoAmt;

        if (mgrAmt > 0) {
            uint256 sharesMgr = (mgrAmt * RATE_SCALE) / price;
            _mint(manager, sharesMgr);
        }
        if (daoAmt > 0) {
            uint256 sharesDao = (daoAmt * RATE_SCALE) / price;
            _mint(daoTreasury, sharesDao);
        }

        mgmtAcc = 0;
        perfAcc = 0;
    }

    function _updateFees() internal {
        _accrueManagement();
        _accruePerformance();
        _settleFees();
    }

    /// @notice Claim accumulated gas cost reimbursement
    function claimGas(uint256 amount, address to) external onlyRole(MANAGER_ROLE) {
        require(amount <= gasAcc, "exceeds gas accrual");
        gasAcc -= amount;
        feeReserves -= amount;
        require(asset.transfer(to, amount), "transfer failed");
    }

    /// @return current balance of underlying asset in vault
    function assetBalance() public view returns (uint256) {
        return asset.balanceOf(address(this));
    }
}
