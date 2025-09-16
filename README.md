# CCI - Claude Code IDE

A universal file and directory tool with **native Claude Code integration**, providing intelligent AI-powered development features directly from your terminal. Developed entirely by Claude Code.

## 🤖 Powered by Claude Code

CCI integrates seamlessly with Claude Code (claude.ai/code) - no API keys or configuration needed! When you run CCI in a Claude Code environment, you get instant access to AI-powered features:

- **Intelligent Prompts**: Send prompts to Claude Code with automatic project context
- **Code Analysis**: Claude Code understands your entire codebase
- **Smart Suggestions**: Context-aware recommendations for your development tasks
- **Zero Configuration**: Works immediately in Claude Code environments

## Installation

### System-wide Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url> cci
cd cci

# Build the package
uv build

# Install system-wide
pip install dist/cci-*.whl

# Now use CCI anywhere!
cci                    # Open current directory
cci file.txt          # Open any file
cci ~/Documents       # Open any directory
```

### Development Installation

```bash
# Clone and install in editable mode
git clone <repository-url> cci
cd cci
pip install -e .

# Or use UV for development
uv sync --all-extras
uv run cci
```

## Features

### Implemented
- Project management with welcome screen
- CLI commands (new, open, list, remove)
- Project registry with persistence
- TUI with Textual framework
- Pydantic data models
- Comprehensive test suite

### Coming Soon
- Git worktree operations
- Prompt-driven development
- Patch review and application
- Enhanced AI workflows

## Usage

### 🤖 AI-Powered Features (Claude Code Integration)

```bash
# Send a prompt to Claude Code with project context
cci prompt "explain this function"

# Analyze specific files
cci prompt "refactor for better performance" --file src/main.py

# Multiple file context
cci prompt "find security issues" --file app.py --file config.py

# Control context inclusion
cci prompt "what does this code do?" --no-context

# Include specific file patterns
cci prompt "add type hints" --include "*.py" --exclude "*test*"
```

Claude Code automatically understands:
- Your project structure and files
- Current git branch and changes
- File contents and relationships
- Best practices for your language/framework

No API keys or configuration required - just works!

### Universal File/Directory Opening

```bash
# Open current directory
cci

# Open a specific file
cci README.md
cci ~/Documents/notes.txt

# Open a directory
cci ~/Projects
cci /usr/local/bin

# Open with explicit path
cci .
cci ../parent-directory
```

### Project Management (Optional)

```bash
# Create a new project
cci new ~/my-project --name "My Project"

# List registered projects
cci list

# Remove project from registry
cci remove "Project Name"
```

### TUI Navigation

- `N` - Create new project
- `O` - Open existing project
- `R` - Remove selected project
- `Enter` - Open selected project
- `S` - Settings
- `Q` - Quit
- `?` - Help

## Architecture

CCI is built with:
- **CLI**: Typer with Rich formatting
- **TUI**: Textual for terminal UI
- **Data**: Pydantic for validation
- **Config**: TOML for settings
- **Git**: GitPython for operations
- **Testing**: pytest with fixtures
- **Package**: UV for management

## Development

### Run Tests
```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=cci

# Specific test file
uv run pytest tests/unit/test_models.py -v
```

### Code Quality
```bash
# Format code
uv run ruff format src tests

# Lint
uv run ruff check src tests

# Type checking
uv run mypy src
```

### Documentation
```bash
# Serve docs locally
uv run mkdocs serve

# Build docs
uv run mkdocs build
```

### Build
```bash
# Build package
uv build

# Install locally
uv pip install -e .
```

## Project Structure

```
cci/
├── src/cci/           # Source code
│   ├── cli.py         # CLI application
│   ├── core/          # Core logic
│   ├── models/        # Data models
│   └── tui/           # TUI screens
├── tests/             # Test suite
├── docs/              # Documentation
└── pyproject.toml     # Project config
```

## AI-First Development

This project is developed entirely by Claude Code. Human involvement is limited to:
- Providing requirements
- User Acceptance Testing (UAT)
- Deployment approval

See [CLAUDE.md](CLAUDE.md) for AI development guidelines.

## Documentation

- [Status](docs/STATUS.md) - Current development status
- [Progress](docs/PROGRESS.md) - Feature completion tracker
- [Testing](docs/TESTING.md) - Testing instructions
- [UAT Ready](docs/UAT_READY.md) - Features ready for testing

## License

MIT License - See LICENSE file for details.

## Acknowledgments

Built with Claude Code by Anthropic.