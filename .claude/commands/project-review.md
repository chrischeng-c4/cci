# /project-review

Expert project manager that comprehensively reviews your project to identify gaps between documentation and code, then provides actionable next steps. Uses trunk-based development with short-lived review branches for organized findings management.

## Overview

Acts as an expert project manager to analyze your entire project and provide strategic guidance on what to build next. The review identifies:
- Documentation ahead of code (what to implement)
- Code ahead of documentation (what to document)
- Misalignments between docs and code (what to fix)
- Prioritized action items with copy-paste prompts

Uses git branch management and structured finding files for organized review sessions following trunk-based development principles.

## Usage

```bash
# Full comprehensive review (creates new review branch)
/project-review

# Continue existing review session
/project-review --continue

# Force new session (creates new branch even if current exists)
/project-review --new-session

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

- `--continue`: Continue existing review branch session
- `--new-session`: Force new branch creation
- `--quick`: Fast review focusing on critical items only
- `--focus=<area>`: Focus on specific area (testing/documentation/implementation)
- `--report-only`: Generate report without interactive elements
- `--compare`: Show changes since last review
- `--depth=<level>`: Analysis depth (shallow/normal/deep)
- `--output=<file>`: Save report to file

## Workflow

The command orchestrates a sophisticated review process with git branch management:

1. **Branch Setup Phase**
   - Checks for uncommitted changes (stashes if needed)
   - Creates or switches to review branch: `review/YYYY-MM-DD-session`
   - Creates SESSION.md in docs/findings/ with metadata
   - Ensures clean workspace for review

2. **Discovery Phase**
   - Reads all documentation files
   - Scans entire codebase
   - Analyzes test coverage
   - Checks configuration

3. **Analysis Phase**
   - @project-review-analyzer performs deep analysis
   - Identifies gaps and misalignments
   - Calculates metrics and coverage

4. **Validation Phase**
   - @project-review-validator verifies findings
   - Adjusts priorities
   - Enhances recommendations

5. **Finding Generation Phase**
   - Creates individual markdown files in docs/findings/active/
   - Each finding gets unique file with frontmatter metadata
   - Generates actionable prompts for each finding

6. **Synthesis Phase**
   - @project-review-coordinator merges findings
   - Generates consolidated report
   - Updates session tracking
   - Commits findings to review branch

## Output

### Git Branch Management
- Creates review branch: `review/2025-01-15-session`
- Session tracking in `docs/findings/SESSION.md`
- Individual finding files in `docs/findings/active/`
- Ready for squash merge back to main

### Executive Dashboard
Shows at-a-glance project health metrics:
- Overall completion percentage
- Documentation coverage
- Code implementation status
- Test coverage
- Alignment score

### Individual Finding Files

Each finding is saved as an individual file in `docs/findings/active/` with naming pattern:
`YYYY-MM-DD-{type}-{priority}-{brief-description}.md`

Example finding file frontmatter:
```yaml
---
id: "finding-001"
title: "Git worktree management not implemented"
type: "documentation-ahead"
priority: "critical"
status: "open"
complexity: "medium"
effort_hours: 4
created: "2025-01-15T10:30:00Z"
session: "review/2025-01-15-session"
tags: ["git", "core", "worktree"]
---
```

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

### Session Management

The review creates and manages review sessions:

#### Session File: `docs/findings/SESSION.md`
```yaml
---
session_id: "review-2025-01-15"
branch: "review/2025-01-15-session"
created: "2025-01-15T10:30:00Z"
status: "active"
goals:
  - "Complete core worktree implementation"
  - "Add missing test coverage"
  - "Align documentation with code"
findings_count: 15
priority_breakdown:
  critical: 3
  high: 7
  medium: 4
  low: 1
---

## Session Progress

### Active Findings
- 3 Critical findings requiring immediate attention
- 7 High priority items for this session
- Review branch ready for trunk-based development

### Next Steps
1. Address critical findings first
2. Implement high priority features
3. Merge back to main via squash merge
```

### Prioritized Action Plan

Recommendations organized by priority and effort:

1. **Immediate** (Do Now) - Critical fixes and quick wins
2. **Short-term** (This Session) - Important features
3. **Medium-term** (Next Session) - Nice-to-have items
4. **Long-term** (Backlog) - Future enhancements

## Examples

### Example 1: Full Review with Branch Creation
```bash
/project-review
```
Output:
```
🌟 Starting Project Review Session
📂 Creating review branch: review/2025-01-15-session
📋 Session file: docs/findings/SESSION.md

🎯 Project Review Report

Project Health: ████████░░ 85%

Critical Findings (3):
1. 2025-01-15-documentation-ahead-critical-git-worktree.md
   📋 Copy this prompt: "Implement git worktree..."

2. 2025-01-15-code-ahead-high-tui-documentation.md
   📋 Copy this prompt: "Document TUI features..."

📊 Generated 15 finding files in docs/findings/active/
🔗 Review branch ready for trunk-based development

Recommended Next Step: Address critical findings first
```

### Example 2: Continue Existing Session
```bash
/project-review --continue
```
Output:
```
🔄 Continuing Review Session
📂 Switched to: review/2025-01-15-session
📋 Session: 7 findings resolved, 8 remaining

Updated Findings:
- 2 Critical findings still open
- 5 High priority findings updated
- 1 New medium priority finding added

Next: Complete remaining critical items
```

### Example 3: Force New Session
```bash
/project-review --new-session
```
Output:
```
🆕 Creating New Review Session
📂 Archiving current session findings
📂 New branch: review/2025-01-15-session-2
📋 Fresh SESSION.md created

Starting clean review with current project state...
```

### Example 4: Quick Documentation Check
```bash
/project-review --quick --focus=documentation
```
Output:
```
📝 Quick Documentation Review
📂 Working in: review/2025-01-15-session

Missing Documentation (3 findings):
- 2025-01-15-code-ahead-high-tui-usage-guide.md
- 2025-01-15-code-ahead-medium-api-reference.md
- 2025-01-15-code-ahead-low-config-options.md

📋 Quick Fix Prompt: "Create documentation for TUI, API, and config..."
```

### Example 5: Testing Focus with Findings
```bash
/project-review --focus=testing
```
Output:
```
🧪 Testing Review
📂 Branch: review/2025-01-15-session

Test Coverage: 60%

Missing Tests (4 findings):
- 2025-01-15-missing-tests-critical-worktree-coverage.md (0%)
- 2025-01-15-missing-tests-high-tui-integration.md (40%)

📊 Individual finding files ready for targeted development
📋 Testing Prompt: "Add comprehensive tests for worktree and TUI..."
```

## Integration

The project-review workflow integrates with:
- **Git Branches**: Review branches following `review/YYYY-MM-DD-session` pattern
- **Session Management**: docs/findings/SESSION.md for current session tracking
- **Individual Findings**: docs/findings/active/ for structured finding files
- **Documentation tracking**: docs/STATUS.md for overall project status
- **Progress tracking**: docs/PROGRESS.md for feature completion
- **Issue tracking**: docs/ISSUES.md for blockers and problems
- **Review history**: docs/reviews/ for historical review reports
- **Trunk-based Development**: Short-lived branches ready for squash merge

### Directory Structure
```
docs/
├── findings/
│   ├── SESSION.md                           # Current session metadata
│   ├── active/                              # Active finding files
│   │   ├── 2025-01-15-documentation-ahead-critical-git-worktree.md
│   │   ├── 2025-01-15-code-ahead-high-tui-documentation.md
│   │   └── 2025-01-15-missing-tests-medium-coverage.md
│   └── archived/                            # Completed findings
│       └── 2025-01-14-session/              # Previous session findings
├── reviews/                                 # Historical consolidated reports
└── [other docs]
```

## Best Practices

1. **Session Management**: Start new sessions for major changes, continue for ongoing work
2. **Branch Hygiene**: Use review branches, merge back to main via squash merge
3. **Finding Files**: Work on individual findings to maintain focus and track progress
4. **Regular Reviews**: Run weekly to track progress and identify new gaps
5. **Focus Areas**: Use --focus for targeted reviews when time is limited
6. **Follow Prompts**: Copy and execute suggested prompts for consistency
7. **Track Progress**: Use --continue to see session progress over time
8. **Update Docs**: Keep STATUS.md current after addressing findings
9. **Archive Completed**: Move resolved findings to archived/ directory
10. **Trunk-Based Development**: Keep review branches short-lived (max 1-2 days)

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

## Finding File Structure

Individual finding files use structured frontmatter for metadata:

```yaml
---
# Unique identifier for this finding
id: "finding-001"

# Human-readable title
title: "Git worktree management not implemented"

# Finding type (documentation-ahead, code-ahead, misalignment, missing-tests)
type: "documentation-ahead"

# Priority level (critical, high, medium, low)
priority: "critical"

# Current status (open, in-progress, completed, archived)
status: "open"

# Implementation complexity (low, medium, high)
complexity: "medium"

# Estimated effort in hours
effort_hours: 4

# When finding was created
created: "2025-01-15T10:30:00Z"

# Session that created this finding
session: "review/2025-01-15-session"

# Related tags for categorization
tags: ["git", "core", "worktree", "implementation"]

# Files or components affected
components:
  - "src/cci/core/worktree.py"
  - "docs/api/worktree.md"

# Related findings (if any)
related: ["finding-002", "finding-007"]
---

## Problem Description
Git worktree management is documented in the API documentation but the implementation is missing from the core module.

## Current State
- Documentation exists in docs/api/worktree.md
- No implementation in src/cci/core/worktree.py
- Tests are failing due to missing module

## Action Required
Implement the GitWorktree class with the following methods:
- create_worktree()
- list_worktrees()
- switch_worktree()
- delete_worktree()

## Copy-Paste Prompt
```
Implement git worktree management functionality as documented in docs/api/worktree.md.

Create src/cci/core/worktree.py with:
- GitWorktree class for worktree operations
- Methods: create_worktree(), list_worktrees(), switch_worktree(), delete_worktree()
- Error handling for git operations
- Integration with GitPython library
- Full type hints and documentation

Follow the API specification exactly as documented.
```

## Acceptance Criteria
- [ ] GitWorktree class implemented
- [ ] All documented methods working
- [ ] Error handling in place
- [ ] Tests passing
- [ ] Type hints complete
```

## Metrics Tracked

- **Documentation Coverage**: % of features documented
- **Code Completion**: % of planned features implemented
- **Test Coverage**: % of code covered by tests
- **Alignment Score**: How well docs match code (0-10)
- **Technical Debt**: Amount of refactoring needed
- **Progress Velocity**: Rate of completion
- **Session Progress**: Findings resolved per session
- **Finding Age**: Days since finding was created

## Output Destinations

Reports and findings are saved to:
- **Console Output**: Interactive display (default)
- **Individual Finding Files**: docs/findings/active/YYYY-MM-DD-{type}-{priority}-{description}.md
- **Session Tracking**: docs/findings/SESSION.md (current session)
- **Consolidated Reports**: docs/reviews/YYYY-MM-DD.md (historical)
- **Custom Output**: With `--output=<file>` option
- **Project Status Updates**: Integration with STATUS.md
- **Git Branch**: Committed to review/YYYY-MM-DD-session branch

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

## Trunk-Based Development Workflow

The project-review command follows trunk-based development principles:

### Review Branch Lifecycle
1. **Create**: New review branch for each session
2. **Work**: All findings and fixes happen on review branch
3. **Commit**: Findings are committed as they're created
4. **Squash Merge**: Merge back to main with single commit
5. **Archive**: Move completed findings to archived directory

### Branch Management Commands
```bash
# Start new session (creates branch)
/project-review

# Continue existing session (switches to branch)
/project-review --continue

# Check branch status
git branch | grep review

# Manual merge when ready (squash recommended)
git checkout main
git merge --squash review/2025-01-15-session
git commit -m "feat: complete project review findings for 2025-01-15"
```

### Session Workflow
```
main ──┬── review/2025-01-15-session
       │   ├── finding files created
       │   ├── implementations added
       │   ├── tests written
       │   └── documentation updated
       │
       └── squash merge back to main
```

## Tips

1. **Session Workflow**: Start with `/project-review`, end with squash merge to main
2. **Branch Naming**: Use descriptive session names for easy identification
3. **Finding Focus**: Work on individual finding files to maintain focus
4. **Start Sessions with Review**: Run before coding to get direction
5. **End Sessions with Review**: Run after coding to track progress
6. **Use Focus Mode**: Target specific areas when time is limited
7. **Follow Priorities**: Address CRITICAL items first
8. **Copy Prompts**: Use provided prompts for consistency
9. **Archive Completed**: Move resolved findings to maintain clean active directory
10. **Continue Sessions**: Use --continue to preserve context across work sessions

## Customization

The review can be customized in CLAUDE.md:
- Priority weights
- Focus areas
- Report format
- Metrics tracked
- Recommendation style

## Success Metrics

A successful review provides:
- **Clear Understanding**: Project state visible through individual finding files
- **Actionable Next Steps**: Copy-paste prompts for each finding
- **Measurable Progress**: Session tracking and finding resolution metrics
- **Organized Workflow**: Trunk-based development with review branches
- **Reduced Friction**: Structured findings eliminate decision paralysis
- **Quality Documentation**: Alignment between code and docs tracked systematically
- **Session Continuity**: Ability to pause and resume review sessions
- **Historical Tracking**: Archive of completed findings and sessions

### Key Performance Indicators
- **Finding Resolution Rate**: Findings completed per session
- **Session Efficiency**: Time from finding to implementation
- **Documentation Alignment**: Reduction in misalignment findings
- **Code Quality**: Improvement in test coverage and complexity metrics
- **Development Velocity**: Features implemented per sprint/session
- **Branch Lifecycle**: Average time from review branch creation to merge

## Implementation Notes

This enhanced project-review command transforms project management into a data-driven, systematic process that:

1. **Ensures Continuity**: Git branches and session files preserve context
2. **Promotes Focus**: Individual finding files prevent task switching
3. **Enables Tracking**: Structured metadata supports progress analytics
4. **Supports Collaboration**: Findings can be assigned and tracked
5. **Maintains Quality**: Trunk-based development with review gates
6. **Reduces Overhead**: Automated branch and file management

The command maintains backward compatibility while adding powerful new features for enterprise-grade project management and development workflow optimization.