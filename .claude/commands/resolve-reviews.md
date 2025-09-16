# /resolve-reviews

**Intelligent review resolution system** that pairs with `/review-project` to systematically address findings, fix issues, and track resolution progress. Reads review reports from `docs/reviews/` and orchestrates fixes through specialized agents.

## Overview

Acts as the **implementation partner** to `/review-project`:
- **Reads Review Reports**: Parses findings from `docs/reviews/*.md`
- **Prioritizes Issues**: Addresses critical → high → medium priority items
- **Orchestrates Fixes**: Uses specialized agents for each issue type
- **Tracks Progress**: Updates review status and documents resolutions
- **Validates Fixes**: Ensures each fix meets quality gates

## Usage

```bash
# Resolve issues from latest review
/resolve-reviews

# Resolve from specific review file
/resolve-reviews --review=2025-01-16-project-review.md

# Focus on critical issues only
/resolve-reviews --priority=critical

# Resolve specific category
/resolve-reviews --category=tests
/resolve-reviews --category=linting
/resolve-reviews --category=type-checking

# Dry run to see resolution plan
/resolve-reviews --dry-run

# Continue previous resolution session
/resolve-reviews --continue
```

## Options

- `--review=<filename>`: Specific review file to resolve (default: latest)
- `--priority=<level>`: Focus on specific priority (critical/high/medium/low)
- `--category=<type>`: Focus on issue category (tests/linting/types/coverage/docs)
- `--dry-run`: Show resolution plan without executing
- `--continue`: Continue from last resolution session
- `--parallel`: Enable parallel resolution where safe
- `--validate-only`: Just validate previous fixes
- `--max-issues=<n>`: Limit number of issues to resolve

## Resolution Workflow

### Phase 1: Review Analysis & Planning
```markdown
@review-analyzer: Parse and analyze review report:

1. **Load Review Report**
   - Read from docs/reviews/ (latest or specified)
   - Parse executive summary and scores
   - Extract critical issues list
   - Identify actionable recommendations
   - Map issues to resolution strategies

2. **Prioritize Issues**
   - Critical issues (🔴): Must fix immediately
   - High priority (🟡): Should fix soon
   - Medium priority (🟢): Nice to have
   - Sort by impact and effort

3. **Create Resolution Plan**
   - Group related issues for batch fixing
   - Identify dependencies between fixes
   - Estimate time for each resolution
   - Plan validation approach
```

### Phase 2: Issue Categorization & Agent Assignment
```markdown
@workflow-coordinator: Assign specialized agents to issue categories:

Issue Categories & Agents:
1. **Test Failures** → @tester
   - Fix failing tests
   - Add missing tests
   - Improve coverage

2. **Type Checking Errors** → @type-fixer
   - Add missing type annotations
   - Fix type incompatibilities
   - Resolve generic type issues

3. **Linting Violations** → @code-cleaner
   - Fix style violations
   - Remove unused imports
   - Resolve formatting issues

4. **Architecture Issues** → @architect
   - Fix design problems
   - Improve module structure
   - Resolve coupling issues

5. **Documentation Gaps** → @documenter
   - Update outdated docs
   - Add missing documentation
   - Align docs with code

6. **Performance Issues** → @performance-optimizer
   - Optimize slow operations
   - Reduce memory usage
   - Improve response times

7. **Security Vulnerabilities** → @security-auditor
   - Fix security issues
   - Add input validation
   - Remove hardcoded secrets
```

### Phase 3: Systematic Resolution Execution

#### 3.1 Critical Issues Resolution (Priority 1)
```markdown
For each critical issue from review:

@implementer + specialized agent:
1. **Understand Issue**
   - Read issue description
   - Analyze root cause
   - Plan fix approach

2. **Implement Fix**
   - Make minimal necessary changes
   - Follow project conventions
   - Maintain backward compatibility

3. **Validate Fix**
   - Run relevant tests
   - Verify issue resolved
   - Check for regressions

4. **Document Resolution**
   - Update resolution log
   - Note any side effects
   - Record validation results
```

#### 3.2 Test Suite Fixes
```markdown
@tester: Fix failing tests systematically:

Test Resolution Strategy:
1. **Analyze Failures**
   - Group related test failures
   - Identify common root causes
   - Prioritize by impact

2. **Fix Test Issues**
   ```python
   # Example: Fix TUI widget selector issues
   - Update widget queries to match current implementation
   - Fix mock configurations
   - Resolve async test issues
   - Update test fixtures
   ```

3. **Improve Coverage**
   - Add tests for uncovered critical paths
   - Create integration tests
   - Add edge case tests
```

#### 3.3 Type Checking Fixes
```markdown
@type-fixer: Resolve type checking errors:

Type Fix Strategy:
1. **Categorize Errors**
   - Missing annotations: Add type hints
   - Incompatible types: Fix assignments
   - Generic issues: Specify type parameters

2. **Apply Fixes**
   ```python
   # Example fixes
   - Add return type annotations
   - Fix Optional type usage
   - Resolve Any type issues
   - Add generic type parameters
   ```

3. **Validate Type Safety**
   - Run mypy check
   - Verify no new errors
   - Document type decisions
```

#### 3.4 Linting & Code Quality
```markdown
@code-cleaner: Clean up code quality issues:

Cleanup Strategy:
1. **Auto-fixable Issues**
   ```bash
   # Run auto-fixes
   uv run ruff format src tests --fix
   uv run ruff check src tests --fix
   ```

2. **Manual Fixes**
   - Refactor long functions
   - Improve variable naming
   - Reduce complexity
   - Remove dead code

3. **Validation**
   - Run linters
   - Check code metrics
   - Ensure standards met
```

### Phase 4: Progress Tracking & Documentation

#### 4.1 Resolution Status Tracking
```markdown
Create/Update: docs/reviews/YYYY-MM-DD-resolution-status.md

# Resolution Status for [Review Date]

## Progress Overview
- Total Issues: X
- Resolved: Y (Z%)
- In Progress: A
- Remaining: B

## Resolution Log

### Critical Issues ✅
1. **[Issue Title]** - RESOLVED
   - Problem: [Description]
   - Fix: [What was done]
   - Validation: [How verified]
   - Time: X minutes

### High Priority 🔄
1. **[Issue Title]** - IN PROGRESS
   - Problem: [Description]
   - Approach: [Plan]
   - Blockers: [If any]

### Not Started ⏳
1. **[Issue Title]**
   - Reason: [Why not started]
   - Dependencies: [What's needed first]
```

#### 4.2 Validation Report
```markdown
After each resolution batch:

@workflow-validator: Validate all fixes:
1. **Run Test Suite**
   - Verify tests pass
   - Check coverage improved
   - No regressions

2. **Run Quality Checks**
   - Type checking clean
   - Linting passes
   - Security scan clean

3. **Update Metrics**
   - New health score
   - Coverage percentage
   - Quality metrics
```

### Phase 5: Review Update & Completion

#### 5.1 Update Original Review
```markdown
Append to original review file:

## Resolution Update - [Date]

### Issues Resolved ✅
- 🔴 Critical: X of Y resolved
- 🟡 High: A of B resolved
- 🟢 Medium: C of D resolved

### Improvements Achieved
- Test Coverage: Before% → After%
- Type Errors: Before → After
- Linting Issues: Before → After
- Health Score: Before → After

### Outstanding Items
[List of unresolved issues with reasons]

### Next Steps
[Recommended actions for remaining issues]
```

#### 5.2 Generate Resolution Report
```markdown
Create: docs/reviews/YYYY-MM-DD-resolution-report.md

# Resolution Report

## Executive Summary
Successfully resolved X% of issues from [Review Date] review.

## Metrics Improvement
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Health Score | X% | Y% | +Z% |
| Test Coverage | X% | Y% | +Z% |
| Passing Tests | X% | Y% | +Z% |
| Type Errors | X | Y | -Z |
| Lint Issues | X | Y | -Z |

## Key Achievements
1. [Major fix accomplished]
2. [Significant improvement]
3. [Critical issue resolved]

## Validation Results
- All fixes validated ✅
- No regressions introduced ✅
- Quality gates passed ✅

## Time Analysis
- Total Resolution Time: X hours
- Average Time per Issue: Y minutes
- Efficiency Score: Z%
```

## Example Resolution Session

### Example 1: Resolving Critical Issues
```bash
/resolve-reviews --priority=critical
```
Output:
```
📋 Loading Review: 2025-01-16-project-review.md
Found 5 critical issues to resolve

🔴 Critical Issues:
1. 14% test failure rate (34 tests failing)
2. 47 type checking errors
3. 321 linting violations
4. Core worktree 0% coverage
5. TUI test failures

📊 Resolution Plan:
- Estimated Time: 3.5 hours
- Parallel Execution: Enabled
- Validation: After each fix

Starting Resolution...

[1/5] 🧪 Fixing Test Failures
  @tester: Analyzing 34 failing tests...
  - Fixed widget selector issues (13 tests) ✅
  - Updated mock configurations (8 tests) ✅
  - Resolved async issues (6 tests) ✅
  - Fixed integration tests (7 tests) ✅
  Result: All tests passing! ✅

[2/5] 📝 Fixing Type Errors
  @type-fixer: Resolving 47 type errors...
  - Added 23 missing annotations ✅
  - Fixed 15 incompatible assignments ✅
  - Resolved 9 generic type issues ✅
  Result: Type checking clean! ✅

[3/5] 🧹 Fixing Lint Issues
  @code-cleaner: Addressing 321 violations...
  - Auto-fixed 245 issues ✅
  - Manual fixes for 76 issues ✅
  Result: Linting clean! ✅

[4/5] 🏗️ Implementing Worktree System
  @implementer: Creating core worktree...
  - Implemented GitWorktree class ✅
  - Added all required methods ✅
  - Created comprehensive tests ✅
  Result: Worktree coverage at 95%! ✅

[5/5] 🖥️ Fixing TUI Issues
  @ui-designer: Resolving TUI test failures...
  - Fixed widget selectors ✅
  - Updated Textual queries ✅
  Result: TUI tests passing! ✅

✅ Resolution Complete!
- Issues Resolved: 5/5 (100%)
- Time Taken: 3.2 hours
- Health Score: 42% → 78% (+36%)

📄 Reports generated:
- docs/reviews/2025-01-16-resolution-status.md
- docs/reviews/2025-01-16-resolution-report.md
```

### Example 2: Category-Focused Resolution
```bash
/resolve-reviews --category=tests
```
Output:
```
📋 Focusing on Test Issues Only

Found 3 test-related issues:
1. 34 failing tests
2. Low CLI coverage (45%)
3. Missing worktree tests

Resolving Test Issues...
[Progress details...]

✅ Test Resolution Complete!
- Tests Fixed: 34
- Coverage Improved: 63% → 85%
- New Tests Added: 47
```

### Example 3: Dry Run Planning
```bash
/resolve-reviews --dry-run
```
Output:
```
🔍 Resolution Plan (Dry Run)

Would resolve 12 issues in this order:

Critical (4 issues) - 2 hours estimated:
1. Fix 34 failing tests
2. Resolve 47 type errors
3. Address 321 lint violations
4. Implement worktree system

High Priority (5 issues) - 3 hours estimated:
5. Improve CLI coverage 45% → 75%
6. Fix TUI file operations
7. Complete Claude Code integration
8. Update documentation
9. Add security validations

Medium Priority (3 issues) - 1 hour estimated:
10. Optimize performance
11. Add missing docstrings
12. Improve error messages

Total Estimated Time: 6 hours
Parallelizable Tasks: 7
Sequential Dependencies: 5

No changes made (dry run mode)
```

## Integration with Review Workflow

### Paired Command Design
```markdown
/review-project → /resolve-reviews

1. **Review Phase** (/review-project)
   - Analyzes project comprehensively
   - Identifies all issues
   - Generates review report
   - Saves to docs/reviews/

2. **Resolution Phase** (/resolve-reviews)
   - Reads review report
   - Plans fix strategy
   - Executes resolutions
   - Updates review status

3. **Validation Phase** (/review-project --compare)
   - Re-runs review
   - Compares with previous
   - Confirms improvements
   - Documents progress
```

### Continuous Improvement Loop
```bash
# Iteration 1
/review-project                    # Identify issues
/resolve-reviews --priority=critical  # Fix critical issues
/review-project --compare          # Verify improvements

# Iteration 2
/resolve-reviews --priority=high   # Fix high priority
/review-project --compare          # Check progress

# Iteration 3
/resolve-reviews --priority=medium # Polish remaining
/review-project --compare          # Final validation
```

## Resolution Strategies

### Intelligent Batching
```markdown
Group related issues for efficient resolution:
- All test failures together
- All type errors together
- All linting issues together
- Related architectural changes together
```

### Parallel Execution
```markdown
Safe parallel resolution:
- Type fixes + Lint fixes (independent)
- Test fixes + Documentation (independent)
- Different module fixes (if isolated)

Sequential requirements:
- Architecture changes → Implementation
- Core fixes → Integration tests
- API changes → Documentation
```

### Rollback Safety
```markdown
Each resolution is atomic:
1. Create checkpoint before fix
2. Apply resolution
3. Validate immediately
4. Rollback if validation fails
5. Document any rollback
```

## Success Metrics

### Resolution Success
- All critical issues resolved
- Validation passes for each fix
- No regressions introduced
- Improvements measurable
- Documentation updated

### Quality Metrics
- Health Score improvement
- Test coverage increase
- Type safety improvement
- Linting compliance
- Performance gains

### Efficiency Metrics
- Time per issue resolved
- Parallel execution utilization
- First-attempt success rate
- Rollback frequency

## Best Practices

1. **Start with Critical**: Always resolve critical issues first
2. **Validate Often**: Check after each resolution batch
3. **Document Everything**: Track what was fixed and how
4. **Use Parallel**: Enable parallel for faster resolution
5. **Compare Reviews**: Run review-project after resolution
6. **Incremental Progress**: Resolve in priority batches
7. **Track Metrics**: Monitor improvement trends

## Conclusion

The `/resolve-reviews` command creates a systematic approach to addressing project issues identified by `/review-project`, ensuring continuous improvement through intelligent orchestration, specialized agents, and comprehensive tracking.