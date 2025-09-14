# CCI Testing Guide

> Comprehensive testing instructions for CCI features
> For UAT-ready features, see UAT_READY.md

## 🧪 Testing Environment Setup

### Prerequisites
```bash
# Ensure Python 3.12+ is installed
python --version

# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup CCI
cd /path/to/cci
uv venv
uv sync --all-extras
```

### Quick Test Commands
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=cci --cov-report=html

# Run specific test file
uv run pytest tests/test_module.py -v

# Run tests matching pattern
uv run pytest -k "worktree" -v

# Run with live output
uv run pytest -s

# Run in watch mode (if pytest-watch installed)
uv run ptw
```

## 📋 Test Categories

### Unit Tests
Location: `tests/unit/`

```bash
# Run only unit tests
uv run pytest tests/unit/ -v
```

**What to test:**
- Individual functions
- Class methods
- Data validation
- Error handling
- Edge cases

### Integration Tests
Location: `tests/integration/`

```bash
# Run integration tests
uv run pytest tests/integration/ -v
```

**What to test:**
- Component interactions
- Service integrations
- File system operations
- Git operations

### End-to-End Tests
Location: `tests/e2e/`

```bash
# Run E2E tests
uv run pytest tests/e2e/ -v
```

**What to test:**
- Complete workflows
- User journeys
- CLI commands
- TUI interactions

## 🎯 Feature Testing Checklist

When testing a new feature, verify:

### Functionality
- [ ] Feature works as described
- [ ] All acceptance criteria met
- [ ] Edge cases handled properly
- [ ] Error messages are helpful

### Performance
- [ ] Response time acceptable
- [ ] Memory usage reasonable
- [ ] No performance degradation
- [ ] Handles large inputs well

### Security
- [ ] Input validation works
- [ ] No credential exposure
- [ ] Safe file operations
- [ ] Proper error handling

### User Experience
- [ ] Intuitive to use
- [ ] Clear feedback
- [ ] Helpful documentation
- [ ] Keyboard shortcuts work

## 🔍 Manual Testing Procedures

### CLI Testing
```bash
# Test help system
cci --help
cci worktree --help
cci prompt --help

# Test version
cci --version

# Test configuration
cci config show
cci config set ui.theme dark

# Test project management
cci                           # Open dashboard
cci /path/to/project         # Open specific project
```

### TUI Testing
```bash
# Launch TUI
uv run cci

# Test navigation
# - Arrow keys for movement
# - Tab for focus change
# - Enter for selection
# - Esc for back/cancel
# - ? for help
```

### Worktree Testing
```bash
# Create worktree
cci worktree new feature-branch

# List worktrees
cci worktree list

# Switch worktree
cci worktree switch feature-branch

# Delete worktree
cci worktree delete feature-branch
```

### Prompt Testing
```bash
# Simple prompt
cci prompt "Add logging to the application"

# Prompt with context
cci prompt "Refactor the user authentication" --context src/auth

# Review patches
cci prompt review

# Apply patches
cci prompt apply
```

## 🐛 Debugging Tests

### Verbose Output
```bash
# Maximum verbosity
uv run pytest -vvv

# Show print statements
uv run pytest -s

# Show local variables on failure
uv run pytest -l
```

### Debug Specific Test
```bash
# Run with debugger
uv run pytest tests/test_file.py::test_function --pdb

# Set breakpoint in code
import pdb; pdb.set_trace()
```

### Coverage Analysis
```bash
# Generate HTML report
uv run pytest --cov=cci --cov-report=html
open htmlcov/index.html

# Show missing lines
uv run pytest --cov=cci --cov-report=term-missing
```

## 📊 Test Quality Metrics

### Coverage Goals
- Unit Tests: 90%+
- Integration Tests: 80%+
- Overall: 85%+

### Performance Benchmarks
- Unit test suite: < 5 seconds
- Integration tests: < 30 seconds
- E2E tests: < 2 minutes

### Code Quality
```bash
# Run all quality checks
uv run ruff format src tests --check
uv run ruff check src tests
uv run mypy src
uv run bandit -r src
```

## 🔄 Continuous Testing

### Pre-commit Testing
```bash
# Install pre-commit hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

### Watch Mode Development
```bash
# Auto-run tests on file change
uv run ptw -- -x

# With coverage
uv run ptw -- --cov=cci
```

## 📝 Test Documentation

### Writing Test Cases
```python
def test_feature_description():
    """
    Test that [feature] does [expected behavior].

    Given: [setup conditions]
    When: [action taken]
    Then: [expected outcome]
    """
    # Arrange
    # Act
    # Assert
```

### Test Naming Convention
- `test_<feature>_<scenario>_<expected_result>`
- Example: `test_worktree_create_with_invalid_name_raises_error`

## 🚨 Reporting Issues

When you find an issue:

1. **Document it** in `docs/ISSUES.md`
2. **Include**:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Error messages
   - Environment details

3. **Severity**:
   - 🔴 Critical: Blocks all usage
   - 🟠 Major: Blocks feature
   - 🟡 Minor: Workaround exists
   - 🟢 Trivial: Cosmetic issue

---
*Keep this document updated with new testing procedures*