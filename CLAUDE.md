# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ IMPORTANT: Documentation is Your Memory!
The `docs/` folder is your persistent memory between sessions. You MUST read and update it during every session. See "Documentation Maintenance" section below for detailed workflow.

## 🤖 AI-First Development Model

This project is developed entirely by Claude Code. Human involvement is limited to:
- Providing requirements
- Conducting User Acceptance Testing (UAT)
- Approving deployments

## Project Overview
CCI (Claude Code IDE) is a git worktree-first IDE that focuses on prompt-driven patch workflow. It provides an intelligent development environment for managing multiple projects through AI-assisted development.

## Development Workflow

### Single Branch Strategy
- All development happens on `main` branch
- No feature branches needed (AI doesn't create conflicts)
- Each commit is atomic and fully tested
- Rollback via git revert if needed

### AI Development Phases
1. **Requirements Analysis** → Parse human requirements
2. **Design & Architecture** → Create technical design
3. **Implementation** → Write code with tests
4. **Security Review** → Scan for vulnerabilities
5. **Performance Optimization** → Ensure efficiency
6. **UI/UX Polish** → Refine user experience
7. **Testing** → Run comprehensive test suite
8. **UAT Preparation** → Package for human testing
9. **Deployment** → Apply approved changes

## Sub-Agent Responsibilities

### 🏗️ Architecture Agent
- Design system architecture
- Review code structure
- Ensure design patterns compliance
- Validate dependency choices

### 💻 Implementation Agent
- Write production code
- Implement features
- Refactor existing code
- Ensure code quality

### 🧪 Testing Agent
- Write unit tests (100% coverage target)
- Create integration tests
- Design E2E test scenarios
- Validate test results

### 🔒 Security Agent
- Review for vulnerabilities
- Check for secrets/credentials
- Validate input sanitization
- Ensure secure defaults

### ⚡ Performance Agent
- Profile code performance
- Optimize algorithms
- Reduce memory usage
- Improve response times

### 🎨 UI/UX Agent
- Design TUI layouts
- Ensure accessibility
- Create intuitive workflows
- Polish user interactions

### 📚 Documentation Agent
- Write user documentation
- Create API docs
- Update README
- Generate changelog

## Hooks Configuration

Create `.claude/hooks.json`:
```json
{
  "hooks": {
    "task-complete": {
      "command": "echo '✅ Task completed: {task_name}' | tee -a .claude/task-log.txt",
      "notify": true
    },
    "tests-passed": {
      "command": "echo '🧪 All tests passed!' && date >> .claude/test-log.txt",
      "notify": true
    },
    "uat-ready": {
      "command": "echo '🎯 Ready for UAT' && git log --oneline -5",
      "notify": true
    },
    "security-check": {
      "command": "echo '🔒 Security scan complete' >> .claude/security-log.txt",
      "notify": false
    }
  }
}
```

## Slash Commands

### `/cci-smart-commit`
Intelligently analyze git changes and suggest conventional commit messages
```bash
# Usage: Stage your changes first, then run the command
git add <files>
/cci-smart-commit

# Features:
# - Analyzes staged changes to determine commit type
# - Suggests multiple commit messages following conventions
# - Detects: feat, fix, docs, test, refactor, build, chore, etc.
# - Provides context-aware suggestions based on file types
```

### `/cci-status`
Show current development status and progress
```bash
# Implementation in .claude/commands/cci-status.sh
#!/bin/bash
echo "📊 CCI Development Status"
echo "========================"
git log --oneline -5
echo ""
echo "Test Coverage:"
uv run pytest --cov=cci --cov-report=term-missing | tail -5
echo ""
echo "Code Quality:"
uv run ruff check src --statistics
```

### `/cci-test`
Run full test suite with quality checks
```bash
# Implementation in .claude/commands/cci-test.sh
#!/bin/bash
echo "🧪 Running Full Test Suite..."
uv run ruff format src tests --check
uv run ruff check src tests
uv run mypy src
uv run pytest --cov=cci --cov-report=term-missing
echo "✅ Test suite complete"
```

### `/cci-uat`
Prepare for User Acceptance Testing
```bash
# Implementation in .claude/commands/cci-uat.sh
#!/bin/bash
echo "🎯 Preparing for UAT..."
# Build the package
uv build
# Generate test report
uv run pytest --html=uat-report.html --self-contained-html
# Create UAT checklist
cat > UAT_CHECKLIST.md << EOF
# UAT Checklist
- [ ] Core functionality works
- [ ] UI is responsive
- [ ] Error handling is graceful
- [ ] Performance is acceptable
- [ ] Documentation is clear
EOF
echo "✅ UAT package ready"
```

### `/cci-security`
Run security audit
```bash
# Implementation in .claude/commands/cci-security.sh
#!/bin/bash
echo "🔒 Running Security Audit..."
# Check for secrets
git secrets --scan
# Check dependencies
uv pip audit
# Check code
bandit -r src/
echo "✅ Security audit complete"
```

### `/cci-deploy`
Deploy approved changes
```bash
# Implementation in .claude/commands/cci-deploy.sh
#!/bin/bash
echo "🚀 Deploying CCI..."
# Run final tests
uv run pytest
# Build distribution
uv build
# Tag release
git tag -a v$(python -c "import toml; print(toml.load('pyproject.toml')['project']['version'])") -m "Release"
echo "✅ Deployment complete"
```

## Tech Stack
- **CLI**: Typer (with rich for beautiful output)
- **TUI**: Textual (with custom themes)
- **Data**: Pydantic (strict validation)
- **Config**: TOML (human-friendly)
- **Git**: GitPython (worktree management)
- **AI**: Anthropic SDK (for AI features)
- **Testing**: pytest (with pytest-cov, pytest-mock)
- **Quality**: ruff, mypy, bandit
- **Docs**: MkDocs with Material theme
- **Package**: UV (fast, modern)
- **Python**: 3.12+ (latest features)

## Project Structure
```
cci/
├── src/cci/
│   ├── __init__.py
│   ├── __main__.py              # Entry point
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── app.py               # Main Typer app
│   │   ├── commands/            # CLI commands
│   │   └── options.py           # Shared CLI options
│   ├── tui/
│   │   ├── __init__.py
│   │   ├── app.py               # Main Textual app
│   │   ├── screens/             # TUI screens
│   │   ├── widgets/             # Custom widgets
│   │   └── themes/              # UI themes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── worktree.py          # Git worktree logic
│   │   ├── prompt.py            # Prompt processing
│   │   ├── patch.py             # Patch management
│   │   └── project.py           # Project management
│   ├── models/                  # Pydantic models
│   ├── services/                # External services
│   ├── utils/                   # Utilities
│   └── config.py                # Configuration
├── tests/
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   ├── e2e/                     # End-to-end tests
│   └── conftest.py              # Fixtures
├── docs/                        # MkDocs documentation
├── .claude/                     # Claude Code config
│   ├── hooks.json               # Hook configuration
│   └── commands/                # Slash commands
└── [config files]               # pyproject.toml, etc.
```

## Quality Standards

### Code Quality
- 100% type hints
- 90%+ test coverage
- Zero linting errors
- No security vulnerabilities
- Documented public APIs

### Performance Targets
- TUI startup: < 100ms
- Command execution: < 500ms
- Memory usage: < 100MB
- Git operations: Optimized with libgit2

### Security Requirements
- No hardcoded secrets
- Input validation on all user data
- Secure subprocess execution
- Safe file operations
- Audit logging

### UI/UX Principles
- Keyboard-first navigation
- Clear error messages
- Progress indicators
- Responsive design
- Accessibility support (screen readers)

## Development Commands

### Setup & Development
```bash
# Initial setup
uv venv
uv sync --all-extras

# Development
uv run cci                       # Run application
uv run textual run --dev app.py # Run TUI in dev mode
```

### Quality Checks
```bash
# Format
uv run ruff format src tests

# Lint
uv run ruff check src tests
uv run mypy src

# Test
uv run pytest
uv run pytest --cov=cci

# Security
uv run bandit -r src
uv run pip-audit
```

### Build & Release
```bash
# Build
uv build

# Install locally
uv pip install -e .

# Create release
git tag -a v0.1.0 -m "Release v0.1.0"
```

## Configuration Schema

### Global Config: `~/.config/cci/config.toml`
```toml
[ai]
provider = "anthropic"
model = "claude-3-opus"
api_key_env = "ANTHROPIC_API_KEY"

[ui]
theme = "monokai"
editor_mode = "vim"
show_line_numbers = true
syntax_highlighting = true

[git]
default_branch = "main"
auto_fetch = true
signing_key = ""

[performance]
max_workers = 4
cache_enabled = true
cache_size_mb = 100
```

### Project Config: `<project>/.cci/config.toml`
```toml
[project]
name = "my-project"
description = "Project description"
worktree_path = ".cci/worktrees"

[prompt]
max_context_files = 20
include_patterns = ["*.py", "*.md"]
exclude_patterns = ["__pycache__", "*.pyc"]

[workflow]
auto_commit = false
require_tests = true
require_review = true
```

## AI Agent Guidelines

### Documentation Maintenance (CRITICAL)

You MUST update the following documentation files during EVERY work session:

#### Start of Session
1. Read `docs/STATUS.md` to understand current state
2. Read `docs/development/CURRENT_SPRINT.md` for active tasks
3. Read `docs/development/TODO.md` for next priorities
4. Check `docs/ISSUES.md` for any blockers

#### During Development
1. Update `docs/development/CURRENT_SPRINT.md` with current task
2. Log decisions in `docs/development/DECISIONS.md` as you make them
3. Track completion in `docs/PROGRESS.md` (change 📋 to 🚧 to ✅)
4. Document any issues in `docs/ISSUES.md`

#### After Implementing Features
1. Log complete implementation details in `docs/development/FEATURE_LOG.md`
2. Update `docs/PROGRESS.md` with completion status
3. If ready for testing, add to `docs/UAT_READY.md` with instructions
4. Update `docs/STATUS.md` with what was accomplished

#### End of Session
1. Update `docs/STATUS.md` with final status
2. Update `docs/development/TODO.md` with next steps
3. Ensure all documentation reflects current state

This documentation IS your memory between sessions!

### When Implementing Features
1. Always write tests first (TDD)
2. Ensure backward compatibility
3. Document breaking changes
4. Update relevant documentation (see above)
5. Add to changelog

### Code Style
- Follow PEP 8 strictly
- Use descriptive variable names
- Keep functions small (< 50 lines)
- Prefer composition over inheritance
- Use type hints everywhere

### Error Handling
- Use custom exceptions
- Provide helpful error messages
- Log errors appropriately
- Graceful degradation
- Never expose internal details

### Testing Strategy
- Unit test every function
- Integration test workflows
- E2E test user journeys
- Mock external dependencies
- Use fixtures for test data

## Human Interaction Points

### Requirements Phase
Human provides requirements through prompts. AI analyzes and creates technical specifications.

### UAT Phase
Human tests the implementation. AI addresses feedback and iterates.

### Approval Phase
Human approves deployment. AI executes release process.

## Documentation as Communication

The `docs/` folder serves as the primary communication channel between AI and Human:

### Status & Progress Tracking
- **docs/STATUS.md** - Current development status, updated after each session
- **docs/PROGRESS.md** - Visual feature tracker with completion percentages
- **docs/ISSUES.md** - Known issues requiring human input

### Testing Communication
- **docs/UAT_READY.md** - Features ready for human testing with instructions
- **docs/TESTING.md** - Comprehensive testing guide for all features

### AI Self-Documentation
- **docs/development/CURRENT_SPRINT.md** - What AI is working on now
- **docs/development/FEATURE_LOG.md** - Completed features with details
- **docs/development/DECISIONS.md** - Architecture decisions and rationale
- **docs/development/TODO.md** - Backlog and planned features

### Documentation Update Workflow
1. AI updates docs during development
2. Human reviews changes via git diff
3. Human provides feedback in ISSUES.md
4. AI addresses feedback and updates docs
5. Cycle continues until feature complete

This ensures persistent memory across sessions and clear communication.

## Success Metrics
- Zero manual code changes needed
- All tests passing
- No security vulnerabilities
- Performance targets met
- Positive UAT feedback
- Documentation always current