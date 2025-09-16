"""CCI main entry point."""

import sys
from pathlib import Path

from cci.cli import app


def main() -> None:
    """Main entry point that handles both direct paths and commands."""
    # Check if we have any arguments
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]

        # List of known commands
        commands = ['new', 'list', 'remove', 'open', '--help', '-h', '--version', '-v']

        # If first argument is not a known command and doesn't start with -, treat as path
        if first_arg not in commands and not first_arg.startswith('-'):
            # Check if it looks like a file or directory path
            Path(first_arg)

            # Insert 'open' command before the path
            sys.argv.insert(1, 'open')

    # Now let Typer handle it
    app()

if __name__ == "__main__":
    main()
