---
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task", "TodoWrite"]
model: "claude-opus-4-1-20250805"
description: "Run comprehensive test suite with intelligent analysis and self-healing"
argument-hint: "[--fix] [--focus=<module>] [--strategy=<type>]"
thinking-level: "think hard"
subagents: ["test-optimizer", "coverage-analyzer", "fix-suggester"]
project-aware: true
---

# /cci-test

think hard about executing comprehensive testing with intelligent failure analysis, automatic fix suggestions, and continuous test suite optimization.

## Project Context Integration

This command understands the CCI project's testing philosophy:
- Architecture: Python with UV package manager, pytest framework
- Standards: 90%+ coverage target from CLAUDE.md
- Tools: pytest, pytest-cov, pytest-mock, ruff, mypy, bandit
- Patterns: TDD approach, fixture-based testing
- Memory: Updates docs/STATUS.md with test results

## Intelligent Execution Strategy

### Phase 1: Pre-Test Intelligence Gathering

1. **Test Discovery & Analysis**
   @Task: Analyze test structure and patterns:
   - Discover all test files and their dependencies
   - Map test categories (unit/integration/e2e)
   - Identify test fixtures and mocks
   - Check for flaky test patterns
   - Review recent test failures from logs/

2. **Coverage History Analysis**
   - Read previous coverage reports
   - Identify consistently uncovered code
   - Track coverage trends over time
   - Prioritize critical untested paths

3. **Project State Verification**
   - Ensure virtual environment is activated
   - Verify all test dependencies installed
   - Check for uncommitted changes that might affect tests
   - Validate test configuration files

### Phase 2: Smart Test Execution

1. **Adaptive Test Strategy**
   Based on context, choose optimal approach:
   - **Quick Smoke**: Fast subset for rapid feedback
   - **Changed Files**: Test only modified code paths
   - **Full Suite**: Complete test coverage
   - **Focused**: Target specific module or feature
   - **Regression**: Previous failure points

2. **Parallel & Optimized Execution**
   ```bash
   # Run tests in parallel with intelligent ordering
   uv run pytest -n auto --failed-first --tb=short

   # With coverage and detailed reporting
   uv run pytest --cov=cci --cov-report=term-missing --cov-report=html
   ```

3. **Quality Checks Integration**
   Execute in optimal order for fast feedback:
   - Format check: `uv run ruff format src tests --check`
   - Linting: `uv run ruff check src tests`
   - Type checking: `uv run mypy src`
   - Security: `uv run bandit -r src/ -ll`

### Phase 3: Intelligent Failure Analysis

When tests fail, perform deep analysis:

1. **Failure Pattern Recognition**
   @Task: Analyze failure patterns:
   - Group related failures
   - Identify root causes vs symptoms
   - Detect environment-specific issues
   - Recognize timing/race conditions

2. **Automatic Fix Generation**
   For common failure patterns:
   - Missing imports → Add required imports
   - Type mismatches → Correct type hints
   - Assertion failures → Suggest correct values
   - Mock issues → Fix mock configurations

3. **Smart Debugging Assistance**
   - Generate minimal reproduction cases
   - Suggest debug points and logging
   - Identify similar historical failures
   - Propose isolation strategies

### Phase 4: Coverage Intelligence

1. **Coverage Gap Analysis**
   @coverage-analyzer: Analyze uncovered code:
   - Identify critical untested paths
   - Suggest test cases for gaps
   - Generate test skeletons
   - Prioritize by risk/importance

2. **Test Generation**
   For uncovered code, generate:
   - Unit test templates
   - Edge case scenarios
   - Error condition tests
   - Integration test suggestions

3. **Coverage Reporting**
   - Visual coverage maps
   - Module-by-module breakdown
   - Trend analysis with charts
   - Actionable improvement steps

### Phase 5: Self-Healing & Optimization

1. **Auto-Fix Mode** (--fix flag)
   When enabled, automatically:
   - Fix formatting issues
   - Correct simple type hints
   - Update deprecated assertions
   - Adjust import statements
   - Fix docstring formats

2. **Test Suite Optimization**
   @test-optimizer: Optimize test performance:
   - Identify slow tests for optimization
   - Suggest fixture improvements
   - Detect redundant tests
   - Recommend parallelization opportunities

3. **Continuous Improvement**
   - Log test metrics for analysis
   - Track flaky test occurrences
   - Build failure pattern database
   - Update test best practices

### Phase 6: Documentation & Reporting

1. **Update Project Memory**
   ```python
   # Update docs/STATUS.md with results
   - Test Status: ✅ Passing (92.3% coverage)
   - Last Run: <timestamp>
   - Failed Tests: None
   - Coverage Gaps: src/cci/core/patch.py
   ```

2. **Generate Reports**
   - HTML coverage report in htmlcov/
   - Test performance metrics in reports/
   - Failure analysis in logs/test-failures.log
   - Recommendations in test-improvements.md

3. **Notification & Communication**
   - macOS notification on completion
   - Slack/Discord webhook if configured
   - Summary in terminal with colors
   - Quick link to HTML report

## Self-Optimization Protocol

This command learns and improves:

1. **Pattern Learning**
   - Remember common failure fixes
   - Learn project-specific test patterns
   - Adapt to team conventions
   - Build fix suggestion database

2. **Performance Tuning**
   - Cache test discovery results
   - Optimize test execution order
   - Skip unchanged test paths
   - Parallelize independent tests

3. **Intelligence Evolution**
   - Improve failure predictions
   - Enhance fix suggestions
   - Better coverage recommendations
   - Smarter test generation

## Arguments

- `--fix`: Enable auto-fix mode for common issues
- `--focus=<module>`: Test specific module (e.g., cli, core, tui)
- `--strategy=<type>`: smoke|changed|full|focused|regression
- `--coverage-min=<percent>`: Fail if coverage below threshold
- `--parallel`: Force parallel execution
- `--verbose`: Detailed output with explanations

## Subagent Delegation

### @test-optimizer
- Condition: Test suite takes >30 seconds
- Task: Analyze and optimize slow tests
- Output: Optimization recommendations

### @coverage-analyzer
- Condition: Coverage below 90% threshold
- Task: Deep analysis of coverage gaps
- Output: Test generation templates

### @fix-suggester
- Condition: Test failures detected
- Task: Generate fix suggestions
- Output: Code patches and explanations

## Enhanced Output Format

```
🧪 CCI Test Suite Execution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Pre-Test Analysis
  Environment: ✅ UV Python 3.12.0
  Dependencies: ✅ All installed
  Strategy: Full suite with coverage

⚙️ Quality Checks
  Format: ✅ All files formatted correctly
  Linting: ✅ No issues found
  Types: ⚠️ 2 type hints missing (auto-fixing...)
  Security: ✅ No vulnerabilities

🏃 Test Execution [████████████████████] 100%
  Collected: 147 tests across 23 modules
  Duration: 8.3s (parallel on 4 cores)

  ✅ Passed: 145
  ⚠️ Skipped: 1 (requires API key)
  ❌ Failed: 1

📊 Coverage Report: 92.3% (+0.5%)

  Module Coverage:
  src/cci/cli/     ████████████████████ 98%
  src/cci/core/    ████████████████░░░░ 87%
  src/cci/tui/     ████████████████████ 95%
  src/cci/models/  ████████████████████ 100%

  Uncovered Lines:
  - src/cci/core/patch.py: 45-52 (error handling)
  - src/cci/core/worktree.py: 123 (edge case)

❌ Failure Analysis

  test_patch_apply_conflict:
    AssertionError: Expected ConflictError

    💡 Auto-Fix Available:
    The test expects ConflictError but gets MergeError.
    Update the assertion to match new behavior.

    Run with --fix to apply suggested changes.

📈 Test Performance
  Slowest Tests:
  1. test_large_repo_clone: 2.1s
  2. test_tui_rendering: 1.8s
  3. test_patch_generation: 1.2s

  💡 Consider mocking external calls in slow tests

🎯 Recommendations
  1. Add tests for error handling in patch.py
  2. Mock git operations in test_large_repo_clone
  3. Increase coverage in core module to meet 90% target
  4. Fix the failing assertion in test_patch_apply_conflict

📝 Reports Generated
  - HTML Coverage: htmlcov/index.html
  - Test Report: reports/test-report-2024-01-15.html
  - Metrics: logs/test-metrics.json

✨ Overall Status: NEEDS ATTENTION
  1 test failure requires fix before proceeding.
  Coverage is good but could improve in core module.
```

## Error Recovery Strategies

1. **Environment Issues**
   - Auto-install missing dependencies
   - Suggest virtual environment setup
   - Provide clear setup instructions

2. **Flaky Test Handling**
   - Automatic retry with backoff
   - Isolation mode for problematic tests
   - Environment reset between retries

3. **Performance Problems**
   - Switch to parallel execution
   - Suggest test splitting
   - Recommend mock strategies

## Integration Points

- `/cci-status`: Updates overall project health
- `/cci-implement`: Ensures tests before feature completion
- `/cci-uat`: Validates test suite before UAT
- `/cci-security`: Includes security testing
- CI/CD: Integrates with GitHub Actions

## Examples

### Quick Smoke Test
```
/cci-test --strategy=smoke
# Runs essential tests in <10 seconds
```

### Fix Failed Tests
```
/cci-test --fix
# Runs tests and auto-fixes common issues
```

### Focus on Module
```
/cci-test --focus=core --coverage-min=95
# Deep test of core module with high coverage requirement
```

### Changed Files Only
```
/cci-test --strategy=changed
# Tests only files modified in current branch
```

## Continuous Intelligence

This command demonstrates:
1. **Adaptive Testing**: Chooses optimal strategy based on context
2. **Self-Healing**: Automatically fixes common issues
3. **Learning System**: Improves suggestions over time
4. **Deep Analysis**: Goes beyond pass/fail to provide insights
5. **Project Integration**: Updates documentation and tracks metrics