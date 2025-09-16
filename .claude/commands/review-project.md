# /review-project

**Trunk-based ultrathink project reviewer** that creates a feature branch, performs deep architectural analysis to evaluate CCI as a modern, stable, and powerful TUI IDE with native Claude Code integration, and generates comprehensive markdown reports with frontmatter metadata saved to `docs/reviews/` directory.

**Paired Command**: Use `/resolve-reviews` after running this command to systematically fix identified issues on the same branch.

**Branch Strategy**: Follows trunk-based development - creates `review/YYYY-MM-DD-HHMMSS` branch from main for the review process.

## Overview

Conducts an **ultrathink-level analysis** focusing on:
- **Source Code Quality**: Architecture, patterns, maintainability
- **Test Coverage**: Unit, integration, and E2E test effectiveness
- **Documentation**: README.md, CLAUDE.md, and technical docs
- **Claude Code Integration**: Native AI capabilities assessment
- **TUI Excellence**: Modern terminal UI implementation
- **Stability & Power**: Production readiness evaluation

Results are saved to `reviews/YYYY-MM-DD-HH-MM-review.md` with comprehensive metrics and actionable recommendations.

## Usage

```bash
# Full ultrathink review (creates new branch, comprehensive analysis)
/review-project

# Quick review on current branch (no branch creation)
/review-project --quick --no-branch

# Review with custom branch name
/review-project --branch=review/architecture-analysis

# Quick review (faster, focused on critical areas)
/review-project --quick

# Focus on specific aspect
/review-project --focus=claude-integration
/review-project --focus=tui-quality
/review-project --focus=test-coverage
/review-project --focus=documentation

# Compare with previous review
/review-project --compare

# Custom output filename
/review-project --output=custom-review.md
```

## Options

- `--quick`: Fast review focusing on critical items only
- `--branch=<name>`: Custom branch name (default: review/YYYY-MM-DD-HHMMSS)
- `--no-branch`: Skip branch creation, work on current branch
- `--focus=<area>`: Deep dive into specific area
  - `claude-integration`: Claude Code integration quality
  - `tui-quality`: Terminal UI implementation
  - `test-coverage`: Test suite effectiveness
  - `documentation`: Docs completeness and clarity
  - `architecture`: System design and patterns
- `--compare`: Compare with most recent review
- `--output=<filename>`: Custom output filename (default: auto-generated)
- `--metrics-only`: Generate only metrics without recommendations

## Ultrathink Analysis Framework

### Phase 1: Deep Code Analysis
```markdown
@review-analyzer performs ultrathink-level analysis:

1. **Architecture Evaluation**
   - Design patterns identification
   - SOLID principles adherence
   - Dependency management
   - Module coupling and cohesion
   - Scalability assessment

2. **Code Quality Metrics**
   - Cyclomatic complexity
   - Code duplication
   - Type coverage
   - Error handling patterns
   - Performance bottlenecks

3. **Claude Code Integration Assessment**
   - Native integration quality
   - Zero-configuration validation
   - Context management effectiveness
   - AI feature utilization
   - Claude Code workflow optimization
```

### Phase 2: Test Suite Evaluation
```markdown
@test-analyzer performs comprehensive test analysis:

1. **Coverage Analysis**
   - Line coverage percentage
   - Branch coverage
   - Function coverage
   - Critical path coverage

2. **Test Quality Assessment**
   - Test isolation
   - Mock effectiveness
   - Edge case coverage
   - Integration test completeness
   - E2E test scenarios

3. **Test Performance**
   - Execution time
   - Flaky test detection
   - Resource usage
   - Parallelization potential
```

### Phase 3: Documentation Excellence Review
```markdown
@doc-analyzer evaluates documentation quality:

1. **README.md Analysis**
   - First impression score
   - Quick start clarity
   - Feature completeness
   - Installation accuracy
   - Usage examples quality

2. **CLAUDE.md Evaluation**
   - AI instruction clarity
   - Claude Code integration docs
   - Memory persistence strategy
   - Workflow documentation
   - Token efficiency

3. **Technical Documentation**
   - API completeness
   - Architecture documentation
   - Development guides
   - Contributing guidelines
```

### Phase 4: TUI & Modern IDE Assessment
```markdown
@tui-analyzer evaluates terminal UI excellence:

1. **TUI Implementation**
   - Textual framework utilization
   - Widget quality and responsiveness
   - Keyboard navigation
   - Theme and styling
   - Accessibility features

2. **IDE Capabilities**
   - File management
   - Project navigation
   - Git integration
   - Syntax highlighting
   - Search functionality

3. **User Experience**
   - Response time
   - Error handling
   - Visual feedback
   - Help system
   - Customization options
```

## Review Output Structure

### Generated Report: `docs/reviews/YYYY-MM-DD-HH-MM-review.md`

```markdown
---
status: completed
type: review-report
branch: review/YYYY-MM-DD-HHMMSS
commit: abc123def456
started: 2025-01-17T14:30:22Z
completed: 2025-01-17T14:35:45Z
duration_seconds: 323
health_score: 78
claude_integration_score: 98
tui_excellence_score: 85
production_readiness: 72
critical_issues: 5
high_priority_issues: 8
medium_priority_issues: 12
low_priority_issues: 7
total_issues: 32
resolved: false
resolution_status: pending
pr_url: null
issue_url: null
files_analyzed: 127
lines_of_code: 8456
test_coverage: 63
type_coverage: 87
author: Claude Code
tool_version: 1.0.0
---

# CCI Project Review - [Date]

## Executive Summary

**Project Health Score: [0-100]%**
**Claude Code Integration: [0-100]%**
**TUI Excellence: [0-100]%**
**Production Readiness: [0-100]%**

### Key Strengths
- ✅ [Strength 1]
- ✅ [Strength 2]
- ✅ [Strength 3]

### Critical Issues
- 🔴 [Issue 1]
- 🔴 [Issue 2]

### Quick Wins
- 🎯 [Quick win 1]
- 🎯 [Quick win 2]

---

## 1. Architecture & Code Quality

### Overall Architecture Score: [0-100]%

#### Design Patterns
- **MVC/MVP/MVVM**: [Assessment]
- **Dependency Injection**: [Assessment]
- **Repository Pattern**: [Assessment]
- **Factory Pattern**: [Assessment]

#### Code Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Cyclomatic Complexity | X | <10 | ✅/⚠️/🔴 |
| Code Duplication | X% | <3% | ✅/⚠️/🔴 |
| Type Coverage | X% | >95% | ✅/⚠️/🔴 |
| Technical Debt | X hrs | <40 hrs | ✅/⚠️/🔴 |

#### Module Analysis
```
src/cci/
├── cli/ [Score: X/100] - [Assessment]
├── tui/ [Score: X/100] - [Assessment]
├── core/ [Score: X/100] - [Assessment]
├── services/ [Score: X/100] - [Assessment]
└── utils/ [Score: X/100] - [Assessment]
```

---

## 2. Claude Code Integration

### Integration Score: [0-100]%

#### Native Integration Quality
- **Zero Configuration**: ✅ Working perfectly
- **Context Management**: [Assessment]
- **Prompt Processing**: [Assessment]
- **AI Workflow Integration**: [Assessment]

#### Claude Code Features
| Feature | Implementation | Quality | Notes |
|---------|---------------|---------|-------|
| Prompt Command | ✅ Implemented | Excellent | No API keys needed |
| Context Gathering | [Status] | [Quality] | [Notes] |
| File Analysis | [Status] | [Quality] | [Notes] |
| Smart Suggestions | [Status] | [Quality] | [Notes] |

#### Integration Code Review
```python
# Example of excellent Claude Code integration
class ClaudeCodeProvider:
    # Native integration without API keys ✅
    # Automatic context management ✅
    # Seamless workflow integration ✅
```

---

## 3. Test Coverage & Quality

### Test Suite Score: [0-100]%

#### Coverage Metrics
```
Overall Coverage: X%
├── Unit Tests: X% (X/Y files)
├── Integration Tests: X% (X/Y scenarios)
└── E2E Tests: X% (X/Y workflows)

Critical Path Coverage: X%
Edge Case Coverage: X%
Error Handling Coverage: X%
```

#### Test Quality Assessment
- **Test Isolation**: [Score]/10
- **Mock Effectiveness**: [Score]/10
- **Assertion Quality**: [Score]/10
- **Test Naming**: [Score]/10
- **Performance**: Xs average runtime

#### Areas Needing Tests
1. `[Module/Function]` - 0% coverage - CRITICAL
2. `[Module/Function]` - X% coverage - HIGH
3. `[Module/Function]` - X% coverage - MEDIUM

---

## 4. Documentation Excellence

### Documentation Score: [0-100]%

#### README.md Evaluation
- **First Impression**: [Score]/10
- **Installation Guide**: [Score]/10
- **Quick Start**: [Score]/10
- **Feature List**: [Score]/10
- **Examples**: [Score]/10

**Strengths**:
- Clear Claude Code integration explanation
- Good visual hierarchy
- Comprehensive examples

**Improvements Needed**:
- [Specific improvement]
- [Specific improvement]

#### CLAUDE.md Assessment
- **AI Instruction Clarity**: [Score]/10
- **Memory Strategy**: [Score]/10
- **Workflow Documentation**: [Score]/10
- **Token Efficiency**: X tokens (Target: <2000)

**Claude Code Integration Docs**: ✅ Excellent
- Zero-config clearly explained
- Integration benefits highlighted
- Usage patterns documented

#### Technical Documentation
| Document | Completeness | Clarity | Up-to-date |
|----------|-------------|---------|------------|
| API Reference | X% | [Score]/10 | ✅/⚠️/🔴 |
| Architecture | X% | [Score]/10 | ✅/⚠️/🔴 |
| Development Guide | X% | [Score]/10 | ✅/⚠️/🔴 |
| Testing Guide | X% | [Score]/10 | ✅/⚠️/🔴 |

---

## 5. TUI & Modern IDE Capabilities

### TUI Excellence Score: [0-100]%

#### Terminal UI Implementation
- **Framework Usage**: Textual [Version]
- **Widget Quality**: [Score]/10
- **Responsiveness**: [Score]/10
- **Theme/Styling**: [Score]/10
- **Accessibility**: [Score]/10

#### IDE Features
| Feature | Status | Quality | Notes |
|---------|--------|---------|-------|
| File Browser | ✅ | Excellent | Tree view with icons |
| File Viewer | ✅ | Good | Syntax highlighting works |
| Project Management | [Status] | [Quality] | [Notes] |
| Git Integration | [Status] | [Quality] | [Notes] |
| Search | [Status] | [Quality] | [Notes] |
| Settings | [Status] | [Quality] | [Notes] |

#### User Experience Metrics
- **Startup Time**: Xms
- **Response Time**: Xms average
- **Memory Usage**: XMB
- **CPU Usage**: X%

---

## 6. Stability & Production Readiness

### Production Readiness: [0-100]%

#### Stability Indicators
- **Crash Rate**: X per 1000 operations
- **Error Recovery**: [Assessment]
- **Data Integrity**: [Assessment]
- **Backward Compatibility**: [Assessment]

#### Security Assessment
- Input Validation: ✅/⚠️/🔴
- Path Traversal Protection: ✅/⚠️/🔴
- Dependency Vulnerabilities: X found
- Secret Management: ✅/⚠️/🔴

#### Performance Profile
```
Operation | Time | Target | Status
----------|------|--------|-------
Startup | Xms | <500ms | ✅/⚠️/🔴
File Open | Xms | <100ms | ✅/⚠️/🔴
Search | Xms | <200ms | ✅/⚠️/🔴
Claude Prompt | Xms | <1000ms | ✅/⚠️/🔴
```

---

## 7. Actionable Recommendations

### 🔴 Critical (Address Immediately)
1. **[Issue Title]**
   - Problem: [Description]
   - Impact: [High/Critical]
   - Solution: `[Specific fix or command]`
   - Effort: X hours

### 🟡 High Priority (This Week)
1. **[Improvement Title]**
   - Current: [State]
   - Target: [Goal]
   - Steps: [Action items]
   - Effort: X hours

### 🟢 Nice to Have (Future)
1. **[Enhancement Title]**
   - Benefit: [Description]
   - Implementation: [Approach]
   - Effort: X hours

---

## 8. Comparison with Previous Review

*[Only if --compare flag used]*

### Progress Since [Previous Date]
- **Overall Health**: [Previous]% → [Current]% ([+/-X]%)
- **Test Coverage**: [Previous]% → [Current]% ([+/-X]%)
- **Documentation**: [Previous]% → [Current]% ([+/-X]%)

### Completed Recommendations
- ✅ [Previous recommendation that was completed]
- ✅ [Previous recommendation that was completed]

### Outstanding Issues
- ⏳ [Previous issue still pending]
- ⏳ [Previous issue still pending]

---

## 9. Modern TUI IDE Assessment

### Is CCI a Modern, Stable, Powerful TUI IDE?

**Overall Assessment**: [YES with caveats / ALMOST / NOT YET]

#### Modern ✅
- Uses latest Textual framework
- Claude Code native integration
- Modern Python 3.12+
- Async architecture

#### Stable [Status]
- [Stability assessment]
- [Test coverage assessment]
- [Error handling assessment]

#### Powerful [Status]
- [Feature set assessment]
- [Performance assessment]
- [Extensibility assessment]

#### TUI Excellence [Status]
- [UI quality assessment]
- [UX assessment]
- [Accessibility assessment]

#### Claude Code Integration ✅
- Zero configuration required
- Native integration implemented
- Context-aware AI features
- Seamless workflow

### Final Verdict
[Comprehensive assessment of whether CCI achieves its goal as a modern TUI IDE with Claude Code integration]

---

## Metadata

[All metadata is now in frontmatter for machine readability]

---

*Generated by /review-project - Ultrathink Level Analysis*
```

## Workflow Implementation

### Phase 0: Branch Setup (Trunk-Based Development)
```bash
@workflow-coordinator: Setup review branch:
1. Ensure git repo is clean (no uncommitted changes)
2. Fetch latest from origin/main
3. Create new branch from main: review/YYYY-MM-DD-HHMMSS
   - Alternative: Use --branch=<name> if provided
   - Skip if --no-branch flag is set
4. Checkout to new review branch
5. Log branch creation for review metadata
```

### Phase 1: Ultrathink Analysis Orchestration
```bash
@review-analyzer --ultrathink: Perform deep code analysis:
1. Parse entire codebase with AST analysis
2. Calculate complexity metrics for every function
3. Identify design patterns and anti-patterns
4. Analyze dependency graphs
5. Evaluate Claude Code integration points
6. Assess TUI implementation quality
7. Generate architectural insights
```

### Phase 2: Test Suite Deep Dive
```bash
@test-analyzer --comprehensive: Analyze test effectiveness:
1. Run coverage with branch analysis
2. Identify untested critical paths
3. Evaluate test quality (not just quantity)
4. Detect testing anti-patterns
5. Measure test execution performance
6. Generate test improvement roadmap
```

### Phase 3: Documentation Intelligence
```bash
@doc-analyzer --excellence: Evaluate documentation:
1. Parse README.md for user journey
2. Analyze CLAUDE.md for AI effectiveness
3. Check all doc links and references
4. Measure documentation coverage
5. Assess Claude Code integration docs
6. Generate doc quality score
```

### Phase 4: Report Generation
```bash
@review-coordinator: Generate final report:
1. Aggregate all analysis results
2. Calculate composite scores
3. Generate actionable recommendations
4. Create comparison if previous exists
5. Add comprehensive frontmatter metadata:
   - Branch name, commit SHA
   - Issue counts by priority
   - Scores and metrics
   - Timestamps and status
6. Format as comprehensive markdown with frontmatter
7. Save to docs/reviews/YYYY-MM-DD-HH-MM-review.md
8. Commit review report to branch
```

### Phase 5: Branch Management & Next Steps
```bash
@workflow-coordinator: Finalize review branch:
1. Stage review report: git add docs/reviews/*.md
2. Commit with message: "feat(review): project review YYYY-MM-DD"
3. Push branch to origin (if remote exists)
4. Create draft PR with review summary (optional)
5. Update review frontmatter with PR link if created
6. Provide instructions for next steps:
   - Run /resolve-reviews on this branch to fix issues
   - Or merge review to main if only documentation
   - Or finalize PR for team review
```

## Advanced Features

### Incremental Reviews
```bash
# Compare with last review automatically
/review-project --incremental
```

### CI/CD Integration
```bash
# Generate machine-readable metrics
/review-project --format=json --output=metrics.json
```

### Custom Evaluation Criteria
```bash
# Focus on specific quality attributes
/review-project --criteria="performance,security,accessibility"
```

### Team Review Mode
```bash
# Generate review for team discussion
/review-project --team --output=team-review.md
```

## Review Storage Structure
```
docs/reviews/
├── 2025-01-16-10-30-review.md    # Full review
├── 2025-01-16-10-30-metrics.json # Metrics data
├── 2025-01-15-14-20-review.md    # Previous review
├── latest-review.md → 2025-01-16-10-30-review.md  # Symlink to latest
└── .review-history.json          # Review metadata and trends
```

## Paired Workflow with /resolve-reviews (Trunk-Based)

### Review → Resolve → Validate → Merge Cycle
```bash
# Step 1: Run comprehensive review (creates review branch)
/review-project
# → Creates branch: review/YYYY-MM-DD-HHMMSS
# → Generates: docs/reviews/YYYY-MM-DD-project-review.md with frontmatter
# → Commits review to branch

# Step 2: Resolve identified issues (on same branch)
/resolve-reviews
# → Reads frontmatter to get branch info
# → Continues on review branch
# → Fixes issues systematically by priority
# → Updates frontmatter with resolution progress
# → Commits fixes incrementally
# → Updates: docs/reviews/YYYY-MM-DD-resolution-status.md

# Step 3: Validate improvements
/review-project --compare --no-branch
# → Shows progress since last review
# → Updates frontmatter with validation results
# → Confirms fixes are working

# Step 4: Merge to main (after validation)
git checkout main
git merge review/YYYY-MM-DD-HHMMSS --no-ff
git push origin main
# → Or finalize PR for team review
# → Update frontmatter with merge status
```

### Continuous Improvement Process
```markdown
1. **Initial Review** (/review-project)
   - Identifies all issues and gaps
   - Provides health scores and metrics
   - Prioritizes problems to fix

2. **Resolution Phase** (/resolve-reviews)
   - Reads review report automatically
   - Fixes issues in priority order
   - Tracks progress and validates fixes

3. **Progress Validation** (/review-project --compare)
   - Measures improvement
   - Identifies remaining issues
   - Documents progress

Repeat cycle until desired quality level achieved.
```

## Integration with Development Workflow

### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
/review-project --quick --metrics-only --no-branch
if [ $? -ne 0 ]; then
  echo "Project review failed. Run /resolve-reviews to fix issues."
  exit 1
fi
```

### Weekly Review & Resolution
```bash
# Run comprehensive review and fix critical issues weekly
0 0 * * 1 cd /project && /review-project && /resolve-reviews --priority=critical
```

## Success Metrics

A successful ultrathink review provides:

1. **Comprehensive Analysis**: Every aspect thoroughly evaluated
2. **Actionable Insights**: Specific, implementable recommendations
3. **Progress Tracking**: Clear comparison with previous reviews
4. **Quality Metrics**: Quantifiable measurements of excellence
5. **Claude Code Validation**: Native integration assessment
6. **TUI Excellence Rating**: Terminal UI quality evaluation
7. **Production Readiness**: Clear go/no-go assessment

## Branch Management Examples

### Example: Standard Review with Branch
```bash
$ /review-project

🌿 Creating review branch from main...
✅ Created and switched to: review/2025-01-17-143022
🔍 Starting ultrathink analysis...
[... review process ...]
📊 Review complete! Report saved with frontmatter metadata.
📋 Committed to branch: review/2025-01-17-143022

Next steps:
1. Run: /resolve-reviews  (to fix issues on this branch)
2. Or: gh pr create --draft (to create draft PR for tracking)
3. Or: git checkout main && git merge review/2025-01-17-143022 --no-ff
```

### Example: Quick Review Without Branch
```bash
$ /review-project --quick --no-branch

🔍 Running quick review on current branch (main)...
[... review process ...]
📊 Review complete! Report saved to docs/reviews/
⚠️ Note: No branch created, review on current branch
```

## Frontmatter Benefits

The frontmatter in review reports enables:

1. **Machine Readability**: Parse review data programmatically
2. **Status Tracking**: Track resolution progress via `resolved` field
3. **Branch Management**: Know which branch contains fixes
4. **PR Integration**: Link to pull requests and issues
5. **Metrics History**: Track improvement over time
6. **Automation**: CI/CD can read scores and gate deployments

### Example: Reading Frontmatter Programmatically
```python
import yaml
import re

def read_review_metadata(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        # Extract frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            metadata = yaml.safe_load(match.group(1))
            return metadata
    return None

# Use in CI/CD
metadata = read_review_metadata('docs/reviews/latest-review.md')
if metadata['health_score'] < 70:
    print(f"Health score {metadata['health_score']}% too low for deployment")
    exit(1)
```

## Output Examples

### Example: Excellent Project
```markdown
---
health_score: 92
branch: review/2025-01-17-143022
resolved: true
---

Project Health Score: 92%
Claude Code Integration: 98% ✨
TUI Excellence: 89%
Production Readiness: 85%

CCI successfully implements a modern, stable, and powerful TUI IDE with
exceptional Claude Code integration. Ready for production use with minor
improvements recommended.
```

### Example: Needs Improvement
```markdown
Project Health Score: 68%
Claude Code Integration: 95% ✨
TUI Excellence: 62%
Production Readiness: 55%

CCI shows strong Claude Code integration but requires improvements in
test coverage (45%) and TUI responsiveness before production deployment.
Critical issues identified in error handling and memory management.
```

## Best Practices

1. **Run Weekly**: Regular reviews track progress
2. **Focus Reviews**: Deep dive into problem areas
3. **Track Metrics**: Monitor trends over time
4. **Act on Recommendations**: Implement suggested improvements
5. **Compare Reviews**: Measure improvement velocity

## Integration with Git Workflow

### Automatic PR Creation
```bash
# Review with automatic draft PR
/review-project --create-pr

# Creates branch, runs review, and opens draft PR with:
# - Review summary extracted from frontmatter
# - Links to full review report
# - Checklist of issues to resolve
# - Updates frontmatter with PR URL
```

### Issue Tracking Integration
```bash
# Link review to GitHub issue
/review-project --issue=123

# Updates frontmatter with issue link
# Comments on issue with review summary
# Links PR to issue when created
```

### CI/CD Integration via Frontmatter
```yaml
# .github/workflows/review.yml
- name: Check Review Metrics
  run: |
    python -c "
    import yaml, re
    with open('docs/reviews/latest-review.md') as f:
        content = f.read()
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            data = yaml.safe_load(match.group(1))
            if data['health_score'] < 70:
                exit(1)
    "
```

## Conclusion

The `/review-project` command provides trunk-based ultrathink-level analysis with comprehensive frontmatter metadata in review reports, enabling seamless integration with git workflows, automated CI/CD pipelines, and systematic issue resolution.

*This enhanced review system with frontmatter metadata ensures full traceability, machine readability, and integration with modern development workflows.*