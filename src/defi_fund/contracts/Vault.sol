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

    /// @notice Initialize the vault
    /// @param asset_ Token accepted for deposits
    /// @param manager Address with permission to execute trades
    /// @param guardian Multisig guardian able to pause and upgrade the vault
    function initialize(address asset_, address manager, address guardian) public initializer {
        __ERC20_init("FUND SHARE", "FUND");
        __AccessControl_init();
        __Pausable_init();
        __UUPSUpgradeable_init();

        asset = IERC20Upgradeable(asset_);
        _grantRole(DEFAULT_ADMIN_ROLE, guardian);
        _grantRole(MANAGER_ROLE, manager);
        _grantRole(GUARDIAN_ROLE, guardian);
    }

    /// @notice Deposit assets and mint vault shares
    function deposit(uint256 amount) external whenNotPaused {
        uint256 shares = totalSupply() == 0 ? amount : amount * totalSupply() / assetBalance();
        require(asset.transferFrom(msg.sender, address(this), amount), "transfer failed");
        _mint(msg.sender, shares);
    }

    /// @notice Redeem shares for underlying asset
    function redeem(uint256 shares) external whenNotPaused {
        uint256 amount = shares * assetBalance() / totalSupply();
        _burn(msg.sender, shares);
        require(asset.transfer(msg.sender, amount), "transfer failed");
    }

    /// @notice Execute arbitrary call for asset management
    function executeTrade(address target, bytes calldata data)
        external
        whenNotPaused
        onlyRole(MANAGER_ROLE)
        returns (bytes memory)
    {
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

    /// @dev Required for UUPS upgrades, restricted to guardian
    function _authorizeUpgrade(address newImplementation) internal override onlyRole(GUARDIAN_ROLE) {}

    /// @return current balance of underlying asset in vault
    function assetBalance() public view returns (uint256) {
        return asset.balanceOf(address(this));
    }
}
