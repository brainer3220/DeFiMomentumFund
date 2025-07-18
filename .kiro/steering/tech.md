# Technology Stack

## Build System & Package Management
- **Package Manager**: UV (modern Python package manager)
- **Build System**: setuptools with PEP 621 (pyproject.toml)
- **Python Version**: 3.11 (minimum 3.10 required)

## Core Dependencies
- **Web3**: `web3>=6.17.0` - Blockchain interaction library
- **Typer**: `typer>=0.12.3` - CLI framework
- **Python-dotenv**: `python-dotenv>=1.0.0` - Environment variable management
- **Loguru**: `loguru>=0.7.2` - Advanced logging

## Development Dependencies
- **Testing**: pytest>=8.2.0
- **Code Formatting**: black>=24.4.2
- **Import Sorting**: isort>=5.13.2
- **Type Checking**: mypy>=1.10.0

## Common Commands

### Environment Setup
```bash
# Install UV package manager
pipx install uv

# Create virtual environment and install dependencies
uv venv
uv pip install -e .[dev]

# Activate virtual environment (Windows)
.venv\Scripts\activate
```

### Development Workflow
```bash
# Run tests
pytest

# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Run CLI application
defi-cli --help
```

### CLI Usage Examples
```bash
defi-cli deposit 10    # Deposit 10 tokens
defi-cli withdraw 5    # Withdraw 5 shares
defi-cli info          # Show fund information
```

## Environment Configuration
- Copy `.env.example` to `.env` and configure:
  - `WEB3_PROVIDER_URI`: Blockchain RPC endpoint
  - `PRIVATE_KEY`: Wallet private key
  - `DEFAULT_GAS`: Default gas limit