---
allowed-tools: ["Bash", "Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "Task", "TodoWrite", "WebFetch"]
model: "claude-opus-4-1-20250805"
description: "Intelligent development environment setup with configuration optimization"
argument-hint: "[--fresh] [--profile=<type>] [--verify]"
thinking-level: "think hard"
subagents: ["environment-architect", "dependency-resolver", "config-optimizer"]
project-aware: true
---

# /cci-setup

think hard about intelligently setting up the complete CCI development environment by detecting system capabilities, optimizing configurations, resolving dependencies, and ensuring all tools are properly configured for maximum productivity.

## Project Context Integration

This command understands CCI's development requirements:
- Stack: Python 3.12+, UV package manager, Typer, Textual
- Tools: ruff, mypy, pytest, bandit, pre-commit
- Structure: src/ layout with proper packaging
- Memory: Creates initial docs/ structure if missing
- Standards: Enforces development conventions from CLAUDE.md

## Intelligent Setup Strategy

### Phase 1: System Analysis & Compatibility Check

1. **Environment Detection**
   @environment-architect: Analyze system capabilities:
   ```python
   system_analysis = {
       "os": "detect: darwin|linux|windows",
       "python_versions": "find all installed versions",
       "package_managers": "uv|pip|conda|poetry",
       "shell": "bash|zsh|fish|powershell",
       "ide": "vscode|pycharm|vim|emacs",
       "git_config": "user, editor, hooks"
   }
   ```

2. **Prerequisite Validation**
   Check and install requirements:
   ```bash
   # Check Python version
   python --version >= 3.12

   # Install UV if missing
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Verify git installation
   git --version
   ```

3. **Performance Optimization**
   Configure for optimal development:
   - CPU cores for parallel operations
   - Available memory for caching
   - SSD detection for I/O optimization
   - Network speed for package downloads

### Phase 2: Intelligent Virtual Environment Setup

1. **Virtual Environment Creation**
   Smart environment configuration:
   ```bash
   # Create optimized virtual environment
   uv venv --python 3.12

   # Configure activation scripts
   echo 'alias cci-activate="source .venv/bin/activate"' >> ~/.zshrc
   ```

2. **Dependency Resolution**
   @dependency-resolver: Intelligent package installation:
   ```python
   dependency_strategy = {
       "production": "Core packages only",
       "development": "All dev tools included",
       "testing": "Test frameworks and fixtures",
       "documentation": "MkDocs and themes"
   }
   ```

3. **Dependency Optimization**
   - Parallel installation
   - Cache optimization
   - Version conflict resolution
   - Security audit during install

### Phase 3: Development Tools Configuration

1. **Code Quality Tools**
   @config-optimizer: Configure development tools:
   ```toml
   # pyproject.toml optimizations
   [tool.ruff]
   line-length = 100
   target-version = "py312"
   select = ["E", "F", "I", "N", "UP", "S", "B", "A", "C4", "T20"]

   [tool.mypy]
   python_version = "3.12"
   strict = true
   warn_return_any = true

   [tool.pytest.ini_options]
   addopts = "-ra -q --strict-markers --cov=cci"
   testpaths = ["tests"]
   ```

2. **Pre-commit Hooks**
   Intelligent hook configuration:
   ```yaml
   # .pre-commit-config.yaml
   repos:
     - repo: local
       hooks:
         - id: ruff-format
         - id: ruff-check
         - id: mypy
         - id: pytest-quick
         - id: security-scan
   ```

3. **Editor Integration**
   Configure IDE/editor settings:
   - VSCode: .vscode/settings.json
   - PyCharm: .idea configurations
   - Vim: .vimrc project settings
   - EditorConfig: .editorconfig

### Phase 4: Project Structure Initialization

1. **Directory Structure**
   Create optimal project layout:
   ```
   cci/
   ├── src/cci/            # Source code
   ├── tests/              # Test suites
   ├── docs/               # Documentation
   │   ├── STATUS.md       # Project status
   │   ├── PROGRESS.md     # Feature tracking
   │   ├── development/    # Dev docs
   │   ├── security/       # Security docs
   │   └── uat/           # UAT docs
   ├── scripts/            # Utility scripts
   ├── logs/              # Log files
   ├── reports/           # Generated reports
   └── .claude/           # Claude Code config
   ```

2. **Initial Documentation**
   Create project memory structure:
   ```markdown
   # docs/STATUS.md
   Project initialized: <timestamp>
   Environment: Development
   Python: 3.12.x

   # docs/PROGRESS.md
   ## Feature Tracking
   - [ ] Core functionality
   - [ ] CLI interface
   - [ ] TUI implementation
   ```

3. **Configuration Files**
   Generate optimized configs:
   - .gitignore (comprehensive)
   - .env.example (with all variables)
   - Makefile (common tasks)
   - docker-compose.yml (if needed)

### Phase 5: Git Configuration

1. **Repository Setup**
   Configure git for optimal workflow:
   ```bash
   # Initialize if needed
   git init

   # Configure git
   git config core.autocrlf input
   git config core.filemode false
   git config pull.rebase true

   # Set up git aliases
   git config alias.st "status -sb"
   git config alias.lg "log --oneline --graph"
   ```

2. **Branch Protection**
   Set up branch rules:
   - Protect main branch
   - Require PR reviews (if team)
   - Enable auto-merge
   - Configure CI checks

3. **Git Hooks**
   Install productive hooks:
   - pre-commit: Quality checks
   - commit-msg: Message validation
   - pre-push: Test execution
   - post-merge: Dependency updates

### Phase 6: Verification & Health Check

1. **Environment Verification**
   Comprehensive validation:
   ```bash
   # Run verification suite
   uv pip check              # Dependencies OK
   ruff check src/          # Linting works
   mypy src/                # Type checking works
   pytest --co              # Tests discoverable
   cci --version           # CLI works
   ```

2. **Performance Benchmarks**
   Test development environment:
   - Package installation speed
   - Test execution time
   - Build performance
   - IDE responsiveness

3. **Setup Report**
   Generate comprehensive report:
   ```markdown
   # Setup Complete!

   ## Environment
   - Python: 3.12.1
   - UV: 0.1.0
   - Virtual Env: .venv

   ## Tools Configured
   - ✅ Ruff (formatting & linting)
   - ✅ Mypy (type checking)
   - ✅ Pytest (testing)
   - ✅ Pre-commit hooks

   ## Next Steps
   1. Activate: source .venv/bin/activate
   2. Verify: cci --help
   3. Test: pytest
   ```

## Self-Optimization Protocol

This command learns and improves:

1. **Configuration Learning**
   - Track successful configurations
   - Build optimization database
   - Learn from setup failures
   - Adapt to new tools

2. **Performance Tuning**
   - Optimize installation order
   - Cache common packages
   - Parallelize where possible
   - Reduce setup time

3. **Error Recovery**
   - Build fix database
   - Suggest solutions
   - Auto-retry with fixes
   - Learn from errors

## Arguments

- `--fresh`: Clean setup (remove existing environment)
- `--profile=<type>`: Setup profile (minimal|standard|full|custom)
- `--verify`: Run verification only
- `--fast`: Quick setup with minimal checks
- `--repair`: Fix existing environment issues
- `--upgrade`: Upgrade all tools to latest versions

## Subagent Delegation

### @environment-architect
- Expertise: System analysis, compatibility
- Focus: Optimal environment design
- Output: Environment specifications

### @dependency-resolver
- Expertise: Package management, conflicts
- Focus: Clean dependency tree
- Output: Resolved dependencies

### @config-optimizer
- Expertise: Tool configuration, performance
- Focus: Developer productivity
- Output: Optimized configurations

## Enhanced Output Format

```
🚀 CCI Development Environment Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 System Analysis
  OS: macOS 14.2 (Apple Silicon)
  Python: 3.12.1 detected ✅
  Shell: zsh 5.9
  Cores: 10 (8 performance, 2 efficiency)
  Memory: 32 GB available

📦 Package Manager
  Installing UV... ████████████ Done
  UV Version: 0.1.0
  Cache: ~/.cache/uv configured

🐍 Virtual Environment
  Creating .venv...       ████████████ Done
  Python: 3.12.1
  Location: /Users/you/cci/.venv

📚 Dependencies Installation
  Production (23 packages)
    Installing...         ████████████ 23/23
  Development (15 packages)
    Installing...         ████████████ 15/15

  All dependencies resolved ✅
  No conflicts detected ✅
  Security scan passed ✅

⚙️ Tool Configuration
  Ruff:        ✅ Configured for Python 3.12
  Mypy:        ✅ Strict mode enabled
  Pytest:      ✅ Coverage enabled
  Pre-commit:  ✅ 5 hooks installed
  Git:         ✅ Aliases configured

📁 Project Structure
  Created directories:
    ✅ src/cci/
    ✅ tests/ (unit, integration, e2e)
    ✅ docs/ (with initial structure)
    ✅ logs/, reports/, scripts/

  Generated files:
    ✅ pyproject.toml (optimized)
    ✅ .gitignore (comprehensive)
    ✅ .pre-commit-config.yaml
    ✅ Makefile (helper commands)

🔒 Git Setup
  Repository:  ✅ Initialized
  Hooks:       ✅ Installed (pre-commit, commit-msg)
  Config:      ✅ Optimized for development

✅ Verification Results
  Dependency Check:  PASS
  Import Test:       PASS (all modules importable)
  Linting:          PASS (no issues)
  Type Checking:    PASS (fully typed)
  Test Discovery:   PASS (0 tests found - expected)
  CLI Check:        PASS (cci command works)

📊 Performance Metrics
  Setup Time:       2m 34s
  Download Size:    145 MB
  Disk Usage:       312 MB
  Import Speed:     < 100ms

🎯 Setup Complete!

Quick Start:
  1. Activate environment:
     $ source .venv/bin/activate

  2. Verify installation:
     $ cci --version

  3. Run tests:
     $ pytest

  4. Start development:
     $ cci --help

Useful Commands:
  make format  - Format code
  make lint    - Run linters
  make test    - Run tests
  make build   - Build package

Happy coding! 🚀
```

## Error Handling

1. **Dependency Conflicts**
   - Automatic resolution attempts
   - Clear conflict explanations
   - Manual resolution guidance

2. **System Incompatibilities**
   - Alternative tool suggestions
   - Workaround documentation
   - Compatibility mode setup

3. **Network Issues**
   - Retry with exponential backoff
   - Offline mode with cached packages
   - Mirror repository configuration

## Integration Points

- `/cci-test`: Verify setup with tests
- `/cci-status`: Check environment health
- `/cci-implement`: Ready for development
- `/cci-security`: Security baseline established
- CI/CD: Environment reproducibility

## Examples

### Fresh Installation
```
/cci-setup --fresh
# Complete clean setup from scratch
```

### Minimal Setup
```
/cci-setup --profile=minimal
# Quick setup with core dependencies only
```

### Repair Existing Environment
```
/cci-setup --repair
# Fix issues in current environment
```

### Verification Only
```
/cci-setup --verify
# Check if environment is properly configured
```

## Continuous Intelligence

This command demonstrates intelligent setup capabilities:
1. **System Awareness**: Adapts to different environments
2. **Smart Configuration**: Optimizes for developer productivity
3. **Self-Healing**: Detects and fixes common issues
4. **Learning System**: Improves setup based on patterns
5. **Complete Automation**: Zero-touch environment setup