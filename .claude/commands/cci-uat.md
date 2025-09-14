---
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task", "TodoWrite", "WebFetch"]
model: "claude-opus-4-1-20250805"
description: "Prepare comprehensive UAT package with intelligent validation and documentation"
argument-hint: "[--preview] [--environment=<env>] [--checklist-from-memory]"
thinking-level: "think harder"
subagents: ["uat-validator", "documentation-generator", "environment-builder"]
project-aware: true
---

# /cci-uat

think harder about preparing a comprehensive UAT package by validating readiness, generating intelligent test scenarios, building deployment artifacts, and creating context-aware documentation from project memory.

## Project Context Integration

This command deeply understands UAT requirements for CCI:
- Architecture: Python CLI/TUI application with UV packaging
- Memory: Reads docs/UAT_READY.md for features ready to test
- Standards: Quality gates from CLAUDE.md (90%+ coverage, zero security issues)
- Workflow: AI-first development requiring human validation
- Documentation: Maintains UAT history in docs/uat/

## Intelligent Execution Strategy

### Phase 1: UAT Readiness Assessment

1. **Feature Completeness Analysis**
   @Task: Analyze project readiness for UAT:
   - Read docs/UAT_READY.md for features marked ready
   - Check docs/PROGRESS.md for completion status
   - Review docs/development/FEATURE_LOG.md for implementation details
   - Validate docs/ISSUES.md for blockers
   - Assess docs/STATUS.md for current state

2. **Quality Gate Validation**
   Enforce project standards before UAT:
   ```python
   quality_gates = {
       "test_coverage": {"minimum": 90, "current": None},
       "test_passing": {"required": True, "status": None},
       "security_issues": {"maximum": 0, "found": None},
       "type_checking": {"errors": 0, "current": None},
       "documentation": {"complete": True, "status": None}
   }
   ```

3. **Dependency Verification**
   - Check all runtime dependencies are stable versions
   - Verify no development dependencies in production
   - Validate compatibility matrix
   - Ensure reproducible builds

### Phase 2: Intelligent Test Scenario Generation

1. **Feature-Based Scenarios**
   @documentation-generator: Generate UAT scenarios from features:
   - Parse implemented features from docs/
   - Create user journey test cases
   - Generate edge case scenarios
   - Build regression test checklist

2. **Context-Aware Test Data**
   Generate realistic test data:
   - Sample git repositories for testing
   - Mock project structures
   - Example configuration files
   - Test user credentials (if needed)

3. **Environment-Specific Tests**
   Create tests for target environments:
   - macOS specific features
   - Linux compatibility
   - Windows WSL support
   - Performance benchmarks

### Phase 3: Artifact Generation

1. **Build Distribution Package**
   @environment-builder: Create deployable artifacts:
   ```bash
   # Clean previous builds
   rm -rf dist/ build/

   # Build wheel and source distribution
   uv build --wheel --sdist

   # Generate standalone executable (if applicable)
   uv run pyinstaller --onefile src/cci/__main__.py
   ```

2. **Environment Package**
   Create isolated test environment:
   - Virtual environment snapshot
   - Dependency lock file
   - Configuration templates
   - Sample data sets

3. **Documentation Bundle**
   Compile comprehensive docs:
   - User manual from docs/
   - API documentation
   - Configuration guide
   - Troubleshooting guide

### Phase 4: UAT Checklist Generation

1. **Dynamic Checklist from Memory**
   Generate checklist from project documentation:
   ```markdown
   # UAT Checklist - Generated from Project Memory

   ## Core Features (from docs/UAT_READY.md)
   - [ ] Feature 1: <description from docs>
   - [ ] Feature 2: <description from docs>

   ## User Journeys (from docs/development/FEATURE_LOG.md)
   - [ ] New user onboarding flow
   - [ ] Advanced user workflow

   ## Edge Cases (intelligently generated)
   - [ ] Large repository handling
   - [ ] Network interruption recovery

   ## Performance (from requirements)
   - [ ] TUI startup < 100ms
   - [ ] Command execution < 500ms
   ```

2. **Test Execution Guide**
   Step-by-step testing instructions:
   - Environment setup procedures
   - Test data preparation
   - Execution sequences
   - Result recording templates

3. **Feedback Collection Templates**
   Structured feedback forms:
   - Bug report template
   - Feature request form
   - Usability feedback survey
   - Performance metrics sheet

### Phase 5: Validation & Preview

1. **Pre-UAT Validation**
   @uat-validator: Validate package completeness:
   - Test installation in clean environment
   - Verify all documentation links
   - Check sample data integrity
   - Validate checklist items

2. **Preview Mode** (--preview flag)
   Dry run without building:
   - Show what would be included
   - List quality gate status
   - Display checklist preview
   - Estimate package size

3. **Smoke Test Execution**
   Quick validation of package:
   ```bash
   # Install in temporary environment
   uv venv temp-uat
   uv pip install dist/*.whl

   # Run basic commands
   cci --version
   cci --help
   cci status
   ```

### Phase 6: Package Assembly & Communication

1. **Package Structure**
   ```
   uat-package-YYYY-MM-DD/
   ├── dist/               # Built distributions
   ├── docs/               # Documentation bundle
   ├── tests/              # UAT test scenarios
   ├── data/               # Sample test data
   ├── reports/            # Quality reports
   ├── UAT_CHECKLIST.md    # Generated checklist
   ├── UAT_GUIDE.md        # Testing instructions
   ├── FEEDBACK_FORM.md    # Feedback template
   └── README.md           # Package overview
   ```

2. **Update Project Memory**
   Document UAT preparation:
   ```python
   # Update docs/uat/history.md
   - Date: <timestamp>
   - Version: <from pyproject.toml>
   - Features: <from UAT_READY.md>
   - Quality Metrics: <test results>
   ```

3. **Notification & Handoff**
   - Generate package checksum
   - Create release notes
   - Send notification with location
   - Provide quick start command

## Self-Optimization Protocol

This command learns from UAT cycles:

1. **Feedback Integration**
   - Parse previous UAT feedback
   - Identify common issues
   - Update checklist generation
   - Improve test scenarios

2. **Process Refinement**
   - Track UAT cycle times
   - Optimize build processes
   - Streamline documentation
   - Enhance validation checks

3. **Memory Evolution**
   - Build UAT pattern database
   - Learn tester preferences
   - Adapt to project growth
   - Improve predictions

## Arguments

- `--preview`: Dry run showing what would be included
- `--environment=<env>`: Target environment (dev|staging|prod)
- `--checklist-from-memory`: Generate checklist from docs/
- `--include-history`: Add previous UAT results
- `--fast`: Skip extensive validation for quick package
- `--interactive`: Guide through package creation

## Subagent Delegation

### @uat-validator
- Condition: Package ready for validation
- Task: Comprehensive validation of UAT package
- Output: Validation report with pass/fail status

### @documentation-generator
- Condition: Need test scenarios and guides
- Task: Generate intelligent documentation
- Output: UAT guides and test scenarios

### @environment-builder
- Condition: Creating deployment artifacts
- Task: Build and validate environments
- Output: Deployment-ready packages

## Enhanced Output Format

```
🎯 UAT Package Preparation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Readiness Assessment
  ✅ Quality Gates Passed:
     Coverage: 92.3% (> 90% required)
     Tests: All 147 passing
     Security: No vulnerabilities
     Types: Fully typed
     Docs: Complete

  📊 Features Ready for UAT (from docs/UAT_READY.md):
     1. Git worktree management ✅
     2. Prompt-driven patches ✅
     3. TUI navigation ✅
     4. Project switching ✅

🔨 Building Artifacts
  Creating distribution... ████████████████ Done
  Generating docs...       ████████████████ Done
  Preparing test data...   ████████████████ Done
  Validating package...    ████████████████ Done

📦 Package Contents
  uat-package-2024-01-15/
  ├── dist/
  │   ├── cci-0.1.0-py3-none-any.whl (2.3 MB)
  │   └── cci-0.1.0.tar.gz (1.8 MB)
  ├── docs/
  │   ├── user-manual.pdf (45 pages)
  │   ├── quick-start.md
  │   └── api-reference.html
  ├── tests/
  │   ├── scenarios/ (12 test scenarios)
  │   └── data/ (sample repositories)
  ├── UAT_CHECKLIST.md (37 items)
  └── README.md

📝 Generated UAT Checklist
  Core Features:     12 items
  User Journeys:     8 items
  Edge Cases:        10 items
  Performance:       7 items
  Total Items:       37

🔍 Validation Results
  ✅ Package installs correctly
  ✅ All commands executable
  ✅ Documentation complete
  ✅ Test data valid
  ✅ No missing dependencies

💾 Package Location
  Path: ./uat-packages/uat-package-2024-01-15.tar.gz
  Size: 4.2 MB
  Checksum: sha256:3b4f5e6a...

📢 Next Steps
  1. Extract package: tar -xzf uat-package-2024-01-15.tar.gz
  2. Follow UAT_GUIDE.md for setup
  3. Complete UAT_CHECKLIST.md
  4. Submit feedback via FEEDBACK_FORM.md

✨ UAT Package Ready!
  Package has been validated and is ready for testing.
  All quality gates passed. Happy testing!
```

## Error Handling

1. **Quality Gate Failures**
   - Clear indication of what failed
   - Steps to remediate
   - Option to force with --override

2. **Build Failures**
   - Detailed error messages
   - Rollback to previous state
   - Debugging suggestions

3. **Missing Dependencies**
   - Auto-install if possible
   - Clear instructions if not
   - Dependency conflict resolution

## Integration Points

- `/cci-test`: Ensures quality gates pass
- `/cci-status`: Validates current state
- `/cci-implement`: Completes features for UAT
- `/cci-security`: Security validation
- Project docs/: Source of truth for features

## Examples

### Standard UAT Package
```
/cci-uat
# Full UAT package with all validations
```

### Preview Mode
```
/cci-uat --preview
# Shows what would be included without building
```

### Quick Package for Internal Testing
```
/cci-uat --fast --environment=dev
# Minimal validation for development testing
```

### Memory-Driven Checklist
```
/cci-uat --checklist-from-memory
# Generates comprehensive checklist from docs/
```

## Continuous Intelligence

This command demonstrates:
1. **Memory Integration**: Leverages docs/ for feature awareness
2. **Intelligent Generation**: Creates context-aware test scenarios
3. **Quality Enforcement**: Ensures standards before UAT
4. **Adaptive Learning**: Improves from UAT feedback
5. **Complete Automation**: End-to-end package preparation