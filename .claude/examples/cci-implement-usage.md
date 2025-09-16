# Improved /cci-implement Workflow Examples

## Example 1: Standard Feature Implementation
```bash
# Automatically creates feature branch and orchestrates subagents
/cci-implement "Add search functionality to TUI"

# What happens:
# 1. Creates branch: feature/add-search-functionality
# 2. Switches to new branch
# 3. Orchestrates subagents in intelligent phases:
#    - @workflow-analyzer: Analyzes requirements
#    - @architect: Designs technical architecture
#    - @tester: Creates test specifications
#    - @implementer + @ui-designer: Parallel implementation
#    - @security-auditor + @performance-optimizer: Parallel QA
#    - @documenter: Updates documentation
# 4. Updates project memory throughout
```

## Example 2: Implementation from Project Review
```bash
# First run project review to identify gaps
/project-review

# Then implement the recommended feature
/cci-implement "Implement git worktree management" --from-review

# What happens:
# 1. Detects project-review context automatically
# 2. Creates branch: feature/git-worktree-management
# 3. Uses review gap analysis as requirements
# 4. Follows review-recommended approach
# 5. Updates review tracking when complete
```

## Example 3: Hotfix with Custom Branch
```bash
# Create hotfix on specific branch
/cci-implement "Fix authentication bug" --branch=hotfix/auth-fix --strategy=simple

# What happens:
# 1. Creates branch: hotfix/auth-fix
# 2. Uses simple linear strategy for speed
# 3. Minimal orchestration for quick fix
# 4. Still maintains quality gates
```

## Example 4: Complex Feature with Parallel Execution
```bash
# Maximum parallelization for complex feature
/cci-implement "Multi-tenant architecture" --strategy=complex --parallel

# What happens:
# 1. Creates branch: feature/multi-tenant-architecture
# 2. Full parallel orchestration:
#    - Multiple subagents work simultaneously
#    - Design, testing, security run in parallel
#    - Implementation phases optimized
# 3. Comprehensive quality assurance
# 4. Full documentation update
```

## Key Improvements Over Previous Version

### 1. Git Branch Management (NEW)
- Automatically creates and switches to feature branches
- Follows naming conventions (feature/, fix/, hotfix/)
- Handles uncommitted changes with stash
- Supports rollback to main on failure

### 2. Better Subagent Orchestration (ENHANCED)
- Clear phase separation with defined inputs/outputs
- Intelligent parallel execution where possible
- Dynamic strategy selection based on complexity
- 10 specialized subagents working in concert

### 3. Project-Review Integration (NEW)
- Seamlessly consumes /project-review recommendations
- Uses review gap analysis as requirements
- Tracks implementation against review findings
- Updates review status upon completion

## Workflow Comparison

### Previous Version
```
User → /cci-implement → Implementation (no branching, limited orchestration)
```

### New Version
```
User → /project-review → Gap Analysis
          ↓
      /cci-implement --from-review
          ↓
      Git Branch Creation
          ↓
      Intelligent Orchestration
          ↓
      [Parallel Subagent Execution]
          ↓
      Quality Gates & Validation
          ↓
      Documentation & Memory Updates
```

## Command Options

- `--from-review`: Use project-review recommendation context
- `--branch=<name>`: Custom branch name
- `--strategy=<type>`: Execution strategy (simple/moderate/complex/auto)
- `--parallel`: Enable maximum parallel execution
- `--no-branch`: Skip branch creation
- `--dry-run`: Show execution plan without implementing
- `--rollback`: Rollback to main branch on failure
- `--metrics`: Track detailed performance metrics

## Integration with Other Commands

```bash
# Complete development workflow
/project-review                           # Identify gaps
/cci-implement "feature" --from-review    # Implement from review
/cci-test --strategy=full                 # Validate implementation
/cci-uat                                  # Prepare for testing
/cci-smart-commit                         # Commit with intelligent message
```

This improved workflow transforms /cci-implement into a sophisticated, git-integrated, review-aware orchestration system that provides professional development practices with AI efficiency.