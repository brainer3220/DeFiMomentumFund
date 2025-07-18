"""Entry point for programmatic usage."""
from .cli.app import app as cli_app

def main():
    # Delegate to CLI when called as module
    cli_app()

if __name__ == "__main__":
    main()
