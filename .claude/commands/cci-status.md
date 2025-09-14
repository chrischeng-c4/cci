---
allowed-tools: ["Bash", "Read", "Glob", "Grep", "Task", "TodoWrite"]
model: "claude-opus-4-1-20250805"
description: "Show comprehensive CCI development status with project intelligence"
argument-hint: "[--detail] [--focus=<area>]"
thinking-level: "think"
subagents: ["status-analyzer", "progress-tracker"]
project-aware: true
---

# /cci-status

think about providing comprehensive project status by analyzing git state, test coverage, code quality, and project memory from documentation.

## Project Context Integration

This command understands the CCI project structure and conventions:
- Architecture: Git worktree-first IDE with prompt-driven patch workflow
- Patterns: AI-first development model from CLAUDE.md
- Memory: Reads docs/ for persistent context and current sprint status
- Codebase: Aware of Python/Typer/Textual stack and UV tooling

## Intelligent Execution Strategy

### Phase 1: Deep Project Analysis
Gather comprehensive status from multiple sources:

1. **Git Repository State**
   - Current branch and remote tracking
   - Uncommitted changes (staged/unstaged)
   - Recent commits with semantic analysis
   - Worktree status if applicable

2. **Project Memory from Documentation**
   @Task: Read and analyze project documentation:
   - docs/STATUS.md for last known state
   - docs/PROGRESS.md for feature completion tracking
   - docs/development/CURRENT_SPRINT.md for active work
   - docs/ISSUES.md for known blockers
   - docs/development/TODO.md for upcoming tasks

3. **Code Quality Metrics**
   - Test coverage percentage and missing lines
   - Linting issues by category (ruff statistics)
   - Type checking status (mypy)
   - Security vulnerabilities (if available)

4. **Development Velocity**
   - Commits in last 24 hours/week
   - Test additions/modifications
   - Documentation updates
   - Feature completion rate from PROGRESS.md

### Phase 2: Strategic Status Compilation

Intelligently compile status based on context:

1. **Priority Assessment**
   - Critical issues blocking progress
   - Test failures requiring attention
   - Security vulnerabilities needing fixes
   - Incomplete sprint items

2. **Progress Visualization**
   - Feature completion percentages
   - Sprint burndown if applicable
   - Test coverage trends
   - Code quality trajectory

### Phase 3: Intelligent Reporting

Generate context-aware status report:

1. **Executive Summary**
   - Overall project health (🟢 Good / 🟡 Warning / 🔴 Critical)
   - Current sprint progress percentage
   - Key achievements since last status

2. **Detailed Sections**
   - Git & Version Control Status
   - Test Coverage & Quality Metrics
   - Active Development (from CURRENT_SPRINT.md)
   - Blockers & Issues
   - Next Steps (from TODO.md)

3. **Smart Recommendations**
   Based on analysis, suggest:
   - Priority fixes for failing tests
   - Code quality improvements
   - Documentation gaps to address
   - Next logical development steps

### Phase 4: Validation & Memory Update

1. **Cross-Reference Validation**
   - Verify git status matches documentation
   - Ensure test results are current
   - Validate sprint items against commits

2. **Documentation Update**
   If significant changes detected:
   - Update docs/STATUS.md with current timestamp
   - Log status check in activity log
   - Note any anomalies found

## Self-Optimization Protocol

This command continuously improves through:

1. **Adaptive Analysis**
   - Learn project-specific patterns over time
   - Adjust focus based on development phase
   - Recognize recurring issues

2. **Intelligent Caching**
   - Cache expensive operations when appropriate
   - Detect when full analysis needed vs quick check
   - Optimize based on frequency of use

3. **Context Enhancement**
   - Build understanding of project conventions
   - Learn team-specific terminology
   - Adapt to project evolution

## Arguments

- `--detail`: Show expanded information for each section
- `--focus=<area>`: Focus on specific area (git|tests|quality|sprint|docs)
- Default: Balanced overview of all areas

## Subagent Delegation Points

### @status-analyzer
- Condition: Complex multi-file changes need semantic analysis
- Task: Analyze code changes for impact assessment
- Expected Output: Change categorization and risk assessment

### @progress-tracker
- Condition: Sprint tracking or velocity metrics requested
- Task: Calculate sprint progress and velocity trends
- Expected Output: Burndown metrics and completion forecasts

## Enhanced Output Format

```
🚀 CCI Development Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Overall Health: [🟢 Good | 🟡 Warning | 🔴 Critical]

📝 Git Repository
  Branch: main → origin/main [↑ in sync]
  Changes: 3 staged, 2 unstaged
  Recent: feat(tui): add dark mode (2 hours ago)

🧪 Test Coverage: 92.3% (+1.2% ↑)
  Missing: src/cci/core/patch.py (lines 45-52)
  Status: ✅ All tests passing (47 tests)

📐 Code Quality
  Ruff: ✅ No issues
  Mypy: ⚠️ 2 type hints missing
  Security: ✅ No vulnerabilities

🎯 Current Sprint (Week 2/3)
  Progress: ████████░░ 75% complete
  Active: Implementing worktree management
  Blocked: None

📚 Documentation
  Last Updated: docs/STATUS.md (3 hours ago)
  Sprint Items: 6/8 completed
  Known Issues: 0 critical, 2 minor

💡 Recommendations
  1. Add type hints to src/cci/cli/app.py:34
  2. Increase test coverage for patch.py
  3. Ready for UAT: Dark mode feature

⏭️ Next Steps (from TODO.md)
  - Complete worktree listing feature
  - Add patch preview functionality
  - Update API documentation
```

## Error Handling and Recovery

- Graceful degradation if git not initialized
- Handle missing test dependencies
- Fallback to basic status if docs/ unavailable
- Clear error messages with resolution steps

## Performance Optimization

- Parallel execution of independent checks
- Smart caching of expensive operations
- Incremental updates when possible
- Configurable depth of analysis

## Integration Points

This command integrates with:
- `/cci-test` for detailed test analysis
- `/cci-uat` for UAT readiness check
- `/cci-implement` for sprint planning
- Project documentation for persistent memory

## Examples

### Quick Status Check
```
/cci-status
# Provides balanced overview of project health
```

### Detailed Sprint Focus
```
/cci-status --detail --focus=sprint
# Deep dive into current sprint progress with task details
```

### Test Coverage Analysis
```
/cci-status --focus=tests
# Detailed test coverage with recommendations
```

## Continuous Intelligence

This command demonstrates:
1. **Project Awareness**: Deep understanding of CCI architecture
2. **Memory Integration**: Leverages docs/ as persistent memory
3. **Adaptive Behavior**: Adjusts based on project phase
4. **Smart Recommendations**: Context-aware suggestions
5. **Multi-Source Synthesis**: Combines git, tests, docs, and code analysis