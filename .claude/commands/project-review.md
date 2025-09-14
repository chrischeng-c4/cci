# /project-review

Expert project manager that comprehensively reviews your project to identify gaps between documentation and code, then provides actionable next steps.

## Overview

Acts as an expert project manager to analyze your entire project and provide strategic guidance on what to build next. The review identifies:
- Documentation ahead of code (what to implement)
- Code ahead of documentation (what to document)
- Misalignments between docs and code (what to fix)
- Prioritized action items with copy-paste prompts

## Usage

```bash
# Full comprehensive review
/project-review

# Quick review (faster, less detailed)
/project-review --quick

# Focus on specific area
/project-review --focus=testing
/project-review --focus=documentation
/project-review --focus=implementation

# Generate report only (no interactive prompts)
/project-review --report-only

# Compare with last review
/project-review --compare
```

## Options

- `--quick`: Fast review focusing on critical items only
- `--focus=<area>`: Focus on specific area (testing/documentation/implementation)
- `--report-only`: Generate report without interactive elements
- `--compare`: Show changes since last review
- `--depth=<level>`: Analysis depth (shallow/normal/deep)
- `--output=<file>`: Save report to file

## Workflow

The command orchestrates a sophisticated review process:

1. **Discovery Phase**
   - Reads all documentation files
   - Scans entire codebase
   - Analyzes test coverage
   - Checks configuration

2. **Analysis Phase**
   - @project-review-analyzer performs deep analysis
   - Identifies gaps and misalignments
   - Calculates metrics and coverage

3. **Validation Phase**
   - @project-review-validator verifies findings
   - Adjusts priorities
   - Enhances recommendations

4. **Synthesis Phase**
   - @project-review-coordinator merges findings
   - Generates actionable report
   - Creates copy-paste prompts

## Output

### Executive Dashboard
Shows at-a-glance project health metrics:
- Overall completion percentage
- Documentation coverage
- Code implementation status
- Test coverage
- Alignment score

### Categorized Findings

#### 📝 Documentation Ahead
Features that are documented but not yet implemented.
**Action**: Implement these features following the documentation.

#### 💻 Code Ahead
Features that are implemented but lack documentation.
**Action**: Document these features for users and developers.

#### ⚠️ Misalignments
Logic differences between documentation and implementation.
**Action**: Fix inconsistencies to ensure docs match code.

#### 🧪 Missing Tests
Code without adequate test coverage.
**Action**: Add tests to ensure reliability.

### Copy-Paste Prompts

Each finding includes a ready-to-use prompt that you can copy and paste to address the issue:

```
📋 Copy-Paste Prompt:
"Implement git worktree management functionality as documented...
Create src/cci/core/worktree.py with:
- GitWorktree class for worktree operations
- Methods: create_worktree(), list_worktrees()...
"
```

### Prioritized Action Plan

Recommendations organized by priority and effort:

1. **Immediate** (Do Now) - Critical fixes and quick wins
2. **Short-term** (This Session) - Important features
3. **Medium-term** (Next Session) - Nice-to-have items
4. **Long-term** (Backlog) - Future enhancements

## Examples

### Example 1: Full Review
```bash
/project-review
```
Output:
```
🎯 Project Review Report

Project Health: ████████░░ 85%

Critical Findings:
1. Git worktree management documented but not implemented
   📋 Copy this prompt: "Implement git worktree..."

2. TUI features implemented but not documented
   📋 Copy this prompt: "Document TUI features..."

Recommended Next Step: Implement git worktree management
```

### Example 2: Quick Documentation Check
```bash
/project-review --quick --focus=documentation
```
Output:
```
📝 Quick Documentation Review

Missing Documentation:
- TUI usage guide
- API reference
- Configuration options

📋 Quick Fix Prompt: "Create documentation for TUI, API, and config..."
```

### Example 3: Testing Focus
```bash
/project-review --focus=testing
```
Output:
```
🧪 Testing Review

Test Coverage: 60%

Missing Tests:
- src/cci/core/worktree.py (0%)
- src/cci/tui/app.py (40%)

📋 Testing Prompt: "Add comprehensive tests for worktree and TUI..."
```

## Integration

The project-review workflow integrates with:
- Documentation tracking in docs/STATUS.md
- Progress tracking in docs/PROGRESS.md
- Issue tracking in docs/ISSUES.md
- Review history in docs/reviews/

## Best Practices

1. **Regular Reviews**: Run weekly to track progress
2. **Focus Areas**: Use --focus for targeted reviews
3. **Follow Prompts**: Copy and execute suggested prompts
4. **Track Progress**: Compare reviews to measure velocity
5. **Update Docs**: Keep STATUS.md current after changes

## Workflow Agents

### @project-review-analyzer
Performs deep analysis of documentation and code to identify gaps.

### @project-review-validator
Validates findings and ensures recommendations are accurate.

### @project-review-coordinator
Orchestrates the review and generates the final report.

## Report Sections

### 1. Executive Summary
High-level project status and health metrics.

### 2. Key Achievements
What has been completed since last review.

### 3. Critical Findings
Most important issues requiring immediate attention.

### 4. Detailed Analysis
Comprehensive breakdown of all findings.

### 5. Action Items
Prioritized list of next steps.

### 6. Development Prompts
Copy-paste ready prompts for each action item.

### 7. Strategic Recommendations
Long-term suggestions for project improvement.

## Metrics Tracked

- **Documentation Coverage**: % of features documented
- **Code Completion**: % of planned features implemented
- **Test Coverage**: % of code covered by tests
- **Alignment Score**: How well docs match code (0-10)
- **Technical Debt**: Amount of refactoring needed
- **Progress Velocity**: Rate of completion

## Output Destinations

Reports can be saved to:
- Console output (default)
- Markdown file with `--output=<file>`
- docs/reviews/YYYY-MM-DD.md (automatic)
- Project status updates in STATUS.md

## Error Handling

The review handles various edge cases:
- Empty projects: Provides bootstrapping guidance
- No documentation: Suggests documentation structure
- No tests: Recommends testing strategy
- Conflicts: Validator resolves discrepancies

## Performance

- Full review: ~30 seconds
- Quick review: ~10 seconds
- Focused review: ~15 seconds
- Report generation: ~5 seconds

## Tips

1. **Start Sessions with Review**: Run before coding to get direction
2. **End Sessions with Review**: Run after coding to track progress
3. **Use Focus Mode**: Target specific areas when time is limited
4. **Follow Priorities**: Address CRITICAL items first
5. **Copy Prompts**: Use provided prompts for consistency

## Customization

The review can be customized in CLAUDE.md:
- Priority weights
- Focus areas
- Report format
- Metrics tracked
- Recommendation style

## Success Metrics

A successful review provides:
- Clear understanding of project state
- Actionable next steps
- Measurable progress tracking
- Reduced development friction
- Improved documentation quality

This command transforms project management into a data-driven, systematic process that ensures continuous progress and alignment between documentation and implementation.