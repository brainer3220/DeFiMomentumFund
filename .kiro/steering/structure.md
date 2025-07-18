# Project Structure

## Directory Layout
```
.
├── src/defi_fund/           # Main application package
│   ├── __init__.py          # Package initialization with version
│   ├── main.py              # Entry point for programmatic usage
│   ├── state.py             # Fund state management
│   ├── cli/                 # Command-line interface
│   │   └── app.py           # Typer CLI application
│   ├── config/              # Configuration management
│   │   └── settings.py      # Environment and global settings
│   └── contracts/           # Smart contract interactions
│       └── __init__.py
├── tests/                   # Test suite
│   └── test_basic.py        # Basic functionality tests
├── .kiro/                   # Kiro AI assistant configuration
│   └── steering/            # AI guidance documents
├── pyproject.toml           # Project configuration (PEP 621)
├── .env.example             # Environment variable template
└── README.md                # Project documentation
```

## Architecture Patterns

### Package Organization
- **src-layout**: All source code under `src/` directory
- **Namespace packages**: Clear separation of concerns with submodules
- **CLI separation**: Command-line interface isolated in `cli/` module
- **Configuration centralization**: Settings managed in `config/` module

### Code Organization Principles
- **Single responsibility**: Each module has a focused purpose
- **Dependency injection**: Configuration loaded from environment
- **State management**: Persistent state handling in dedicated module
- **CLI as facade**: CLI commands delegate to core business logic

### File Naming Conventions
- **Snake_case**: All Python files and directories use snake_case
- **Descriptive names**: Module names clearly indicate their purpose
- **Standard patterns**: Follow Python packaging conventions

### Import Structure
- **Relative imports**: Use relative imports within the package
- **Absolute imports**: External dependencies use absolute imports
- **Organized imports**: Group standard library, third-party, and local imports

### Testing Organization
- **Mirror structure**: Test files mirror the source structure
- **Descriptive test names**: Test functions clearly describe what they test
- **Fixtures**: Use pytest fixtures for test setup and teardown