---
allowed-tools: ["Bash", "Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "Task", "TodoWrite", "WebSearch", "WebFetch"]
model: "claude-sonnet-4-20250514"
description: "Intelligent finding implementation with finding-based workflow and subagent orchestration"
argument-hint: "[--from-review] [--finding=<id>] [--next] [--strategy=<type>] [--parallel]"
thinking-level: "ultrathink"
subagents: ["workflow-analyzer", "doc-optimizer", "architect", "implementer", "tester", "security-auditor", "performance-optimizer", "ui-designer", "documenter", "workflow-validator"]
project-aware: true
---

# /cci-implement

ultrathink about creating an intelligent finding implementation workflow that seamlessly integrates with the finding-based project-review system and sophisticated subagent orchestration patterns.

## Enhanced Finding-Based Workflow Intelligence

**This command orchestrates complete finding implementation by:**
- **Finding-Based Implementation**: Works with findings from project-review workflow
- **Review Branch Integration**: Assumes we're already on a review branch from project-review
- **Intelligent Orchestration**: Leverages subagents with clear phases and parallel execution
- **Finding State Management**: Moves findings through active → in-progress → completed
- **Quality-First Approach**: Multiple validation gates with comprehensive testing

## Core Improvements for Finding-Based Workflow

### 1. Finding Integration
- Reads findings from docs/findings/active/ directory
- Moves findings through workflow states (active → in-progress → completed)
- Updates finding frontmatter with implementation progress
- Supports both specific finding selection and automatic next-priority selection

### 2. Simplified Git Workflow
- Assumes we're already on a review branch from project-review
- Focuses on implementation without branch management
- Commits changes directly to existing review branch
- Updates SESSION.md with implementation progress

### 3. Intelligent Subagent Orchestration
- Clear phase separation with defined inputs/outputs
- Parallel execution where dependencies allow
- Agent specialization with focused responsibilities
- Dynamic workflow adaptation based on finding complexity

### 4. Enhanced Finding Documentation
- Updates finding files with implementation details
- Tracks actual vs estimated effort
- Maintains implementation audit trail
- Updates project progress tracking in SESSION.md

## Workflow Architecture

### Phase 0: Finding Selection & Setup

#### 0.1 Finding Selection & Validation
```bash
@workflow-analyzer: Select and validate finding for implementation:
1. **Finding Selection**
   - If --finding=<id>: Load specific finding from docs/findings/active/
   - If --next or --from-review: Select highest priority finding
   - Validate finding exists and is in active state
   - Ensure finding is not already in progress

2. **Finding Analysis**
   - Parse finding frontmatter (priority, effort_estimate, dependencies)
   - Extract implementation requirements from content
   - Check for any blocking dependencies
   - Validate finding is ready for implementation

3. **State Transition**
   - Move finding from docs/findings/active/ to docs/findings/in-progress/
   - Update frontmatter with started_date and implementation status
   - Update SESSION.md with current implementation progress
```

#### 0.2 Review Context Integration
```bash
@doc-optimizer: Load review context and finding details:
1. **Review Context Loading**
   - Assume we're on review branch from project-review
   - Load SESSION.md for current review context
   - Extract architectural decisions from review
   - Import quality criteria and acceptance criteria

2. **Finding Context Integration**
   - Parse finding requirements and implementation notes
   - Load any referenced documentation or examples
   - Understand finding dependencies and relationships
   - Extract copy-paste prompts and implementation hints

3. **Implementation Strategy**
   - Use finding-recommended approach
   - Adapt workflow based on finding complexity (effort_estimate)
   - Apply finding-specific quality criteria and testing requirements
```

#### 0.3 Implementation Workflow Planning
```bash
@workflow-analyzer: Design execution strategy based on finding:

Workflow Pattern Selection (based on effort_estimate):
- **Simple Linear** (Small findings: < 2 hours)
  → analyze → test → implement → validate

- **Parallel Development** (Medium findings: 2-6 hours)
  → analyze → [design, test-spec] → [implement, doc] → validate

- **Complex Orchestration** (Large findings: 6+ hours)
  → analyze → design → test-spec → [implement, security, performance] → [doc, validate]

Finding-Based Orchestration Plan:
- Use finding priority to determine validation rigor
- Apply finding-specific testing requirements
- Integrate finding acceptance criteria into validation
- Plan finding completion and state transition
```

### Phase 1: Deep Analysis & Architecture

#### 1.1 Requirements & Complexity Analysis
**Agents**: @workflow-analyzer (primary), @architect (consulting)
**Pattern**: Sequential → Parallel consultation
**Outputs**: Finding analysis, complexity assessment, orchestration plan

```markdown
@workflow-analyzer: Analyze finding implementation requirements:

Finding Analysis:
1. **Requirements Extraction**
   - Parse finding description and implementation notes
   - Extract explicit requirements and acceptance criteria
   - Map to existing system capabilities and components
   - Identify integration touchpoints from finding context

2. **Complexity Assessment**
   - Use finding effort_estimate as baseline complexity indicator
   - Assess component count and interdependencies
   - Evaluate risk level based on finding impact and scope
   - Determine testing needs from finding requirements

3. **Finding Integration Analysis**
   - Use finding dependencies to understand prerequisites
   - Check for related findings that might be affected
   - Plan integration based on finding architectural notes
   - Validate finding acceptance criteria are achievable

Output Format:
- Finding Type: [feature|enhancement|fix|refactor] (from finding metadata)
- Effort Level: [small|medium|large] (from effort_estimate)
- Risk Level: [low|medium|high] (from finding priority and impact)
- Components: [affected modules from finding scope]
- Dependencies: [from finding frontmatter]
- Success Criteria: [finding acceptance criteria]
```

#### 1.2 Architecture Design & Validation
**Agents**: @architect (primary), @security-auditor, @performance-optimizer (consulting)
**Pattern**: Sequential with parallel consultation
**Outputs**: Technical design, security considerations, performance plan

```markdown
@architect: Design technical implementation:

Design Components:
1. **System Architecture**
   - Module structure and relationships
   - Data flow and state management
   - API design and interfaces
   - Configuration and defaults

2. **Integration Strategy**
   - Touchpoints with existing system
   - Database/file system changes
   - CLI/TUI interface updates
   - Backward compatibility plan

3. **Quality Attributes**
   - Performance targets and constraints
   - Security requirements and threat model
   - Scalability and maintainability considerations
   - Error handling and recovery strategies

Parallel Consultation:
- @security-auditor: Security design review
- @performance-optimizer: Performance impact analysis

Output: docs/architecture/feature-{name}-design.md
```

### Phase 2: Test-Driven Development Foundation

#### 2.1 Test Strategy & Specification
**Agents**: @tester (primary)
**Pattern**: Sequential with comprehensive planning
**Outputs**: Test specifications, test files, validation criteria

```markdown
@tester: Design comprehensive test strategy:

Test Planning:
1. **Test Categories**
   - Unit tests: Individual component testing
   - Integration tests: Component interaction testing
   - End-to-end tests: Full workflow validation
   - Performance tests: Benchmarking and load testing

2. **Test Specifications**
   - Test scenarios and edge cases
   - Mock strategy for external dependencies
   - Test data and fixtures needed
   - Coverage targets (90%+ for new code)

3. **Test Implementation**
   - Generate test file structure
   - Create test fixtures and helpers
   - Implement failing tests (TDD red phase)
   - Validate test quality and coverage

Generated Test Files:
- tests/unit/test_{feature}.py
- tests/integration/test_{feature}_integration.py
- tests/e2e/test_{feature}_e2e.py
- tests/fixtures/test_{feature}_fixtures.py
```

#### 2.2 Test Execution & Validation
**Agents**: @tester (primary)
**Pattern**: Sequential validation
**Outputs**: Test results, coverage baseline

```bash
Test Execution (Red Phase):
1. Run generated tests → Confirm expected failures
2. Validate test quality → Check assertions and scenarios
3. Measure baseline coverage → Establish improvement targets
4. Document test strategy → Update test documentation
```

### Phase 3: Intelligent Parallel Implementation

#### 3.1 Core Implementation
**Agents**: @implementer (primary), @architect (consulting)
**Pattern**: Sequential with architecture validation
**Outputs**: Production code, type definitions, core logic

```markdown
@implementer: Implement production code:

Implementation Strategy:
1. **Minimal Viable Implementation**
   - Write minimal code to pass tests
   - Follow existing patterns and conventions
   - Maintain type hints and documentation
   - Use project coding standards

2. **Incremental Development**
   - Implement component by component
   - Run tests after each component
   - Fix failures immediately
   - Maintain green test suite

3. **Code Quality**
   - Follow PEP 8 and project style guide
   - Use descriptive names and clear logic
   - Add docstrings for public APIs
   - Handle errors gracefully

Architecture Validation:
- @architect: Review implementation against design
- Validate design pattern adherence
- Check for architectural drift
```

#### 3.2 UI/UX Implementation (Parallel)
**Agents**: @ui-designer (primary), @implementer (consulting)
**Pattern**: Parallel with implementer (if UI components needed)
**Outputs**: UI components, CLI commands, user interactions

```markdown
@ui-designer: Create user interfaces (if applicable):

UI Development:
1. **TUI Components** (using Textual)
   - Design screens and widgets
   - Implement keyboard navigation
   - Add accessibility features
   - Create responsive layouts

2. **CLI Commands** (using Typer)
   - Design command structure
   - Add help text and examples
   - Implement argument validation
   - Create intuitive workflows

3. **User Experience**
   - Design error messages and feedback
   - Add progress indicators
   - Create consistent interaction patterns
   - Test usability scenarios

Integration with @implementer:
- Coordinate on shared models and interfaces
- Ensure UI components use core logic
- Validate integration points
```

### Phase 4: Comprehensive Quality Assurance (Parallel)

#### 4.1 Security Audit
**Agents**: @security-auditor (primary)
**Pattern**: Parallel with other quality checks
**Outputs**: Security assessment, vulnerability report, fixes

```markdown
@security-auditor: Comprehensive security review:

Security Assessment:
1. **Input Validation**
   - Check all user input handling
   - Validate file path sanitization
   - Test for injection vulnerabilities
   - Verify data type validation

2. **Dependency Security**
   - Scan for known vulnerabilities
   - Check for insecure dependencies
   - Validate version constraints
   - Review transitive dependencies

3. **Code Security**
   - Look for hardcoded secrets
   - Check for unsafe operations
   - Review file/network operations
   - Validate authentication/authorization

Security Fixes:
- Implement identified security improvements
- Add security tests where needed
- Update documentation with security considerations
```

#### 4.2 Performance Optimization
**Agents**: @performance-optimizer (primary)
**Pattern**: Parallel with security audit
**Outputs**: Performance analysis, optimizations, benchmarks

```markdown
@performance-optimizer: Optimize implementation performance:

Performance Analysis:
1. **Profiling**
   - Profile critical code paths
   - Identify performance bottlenecks
   - Measure memory usage patterns
   - Benchmark key operations

2. **Optimization**
   - Optimize algorithms and data structures
   - Reduce memory allocations
   - Improve I/O efficiency
   - Cache expensive operations

3. **Validation**
   - Run performance tests
   - Compare against targets
   - Document performance characteristics
   - Add performance regression tests

Performance Targets:
- CLI commands: < 500ms response time
- TUI operations: < 100ms interaction time
- Memory usage: < 100MB for normal operations
- File operations: Efficient for large files
```

#### 4.3 Code Quality & Refactoring
**Agents**: @implementer (primary)
**Pattern**: After core implementation
**Outputs**: Refactored code, improved design, quality metrics

```markdown
@implementer: Refine and polish implementation:

Code Quality Improvements:
1. **Refactoring**
   - Extract reusable components
   - Eliminate code duplication
   - Improve naming and clarity
   - Optimize imports and organization

2. **Error Handling**
   - Add comprehensive error handling
   - Create informative error messages
   - Implement graceful degradation
   - Add logging where appropriate

3. **Code Review**
   - Self-review against best practices
   - Check for edge cases
   - Validate error scenarios
   - Ensure maintainability

Quality Validation:
- Run linting and type checking
- Verify test coverage meets targets
- Check documentation completeness
- Validate against requirements
```

### Phase 5: Documentation & Memory Management

#### 5.1 Technical Documentation
**Agents**: @documenter (primary), @architect (consulting)
**Pattern**: Parallel with final testing
**Outputs**: API docs, user guides, examples

```markdown
@documenter: Create comprehensive documentation:

Documentation Strategy:
1. **API Documentation**
   - Document new public APIs
   - Add usage examples
   - Include parameter descriptions
   - Show return value formats

2. **User Documentation**
   - Create user guides for new features
   - Add configuration examples
   - Write troubleshooting guides
   - Include screenshots/demos where helpful

3. **Developer Documentation**
   - Document architecture decisions
   - Add contribution guidelines
   - Create development setup instructions
   - Include testing guidelines

Integration with Architecture:
- @architect: Review technical accuracy
- Ensure architectural decisions are documented
- Validate code examples and snippets
```

#### 5.2 Project Memory Updates
**Agents**: @doc-optimizer (primary)
**Pattern**: Sequential after implementation
**Outputs**: Updated project status, progress tracking, decision log

```markdown
@doc-optimizer: Update project memory and tracking:

Documentation Updates:
1. **Status Documentation**
   - Update docs/STATUS.md with implementation details
   - Log completion in docs/PROGRESS.md
   - Add feature to docs/development/FEATURE_LOG.md
   - Update docs/development/CURRENT_SPRINT.md

2. **Decision Documentation**
   - Log architecture decisions in docs/development/DECISIONS.md
   - Document trade-offs and alternatives considered
   - Record performance and security considerations
   - Note any technical debt or future improvements

3. **UAT Preparation**
   - Add feature to docs/UAT_READY.md with test instructions
   - Create demo scenarios and usage examples
   - Document expected behavior and edge cases
   - Provide rollback instructions if needed

Memory Persistence:
- Ensure documentation survives across sessions
- Create searchable knowledge base
- Maintain decision audit trail
- Support future development
```

### Phase 6: Integration & Validation

#### 6.1 Integration Testing & Validation
**Agents**: @workflow-validator (primary), @tester (consulting)
**Pattern**: Sequential comprehensive validation
**Outputs**: Integration test results, validation report

```markdown
@workflow-validator: Validate complete implementation:

Integration Validation:
1. **Feature Integration**
   - Test feature with existing system
   - Verify backward compatibility
   - Check configuration migrations
   - Validate data integrity

2. **End-to-End Validation**
   - Run complete workflow tests
   - Test user scenarios and edge cases
   - Verify error handling and recovery
   - Check performance under load

3. **Quality Gate Validation**
   - Verify test coverage meets targets (90%+)
   - Confirm security scan is clean
   - Validate performance meets requirements
   - Check documentation completeness

Collaboration with @tester:
- Run full test suite
- Analyze test results and coverage
- Identify any gaps or regressions
```

#### 6.2 Final Documentation & Commit Preparation
**Agents**: @doc-optimizer (primary)
**Pattern**: Sequential preparation for commit
**Outputs**: Commit message, changelog, final docs

```markdown
@doc-optimizer: Prepare for commit and deployment:

Commit Preparation:
1. **Change Documentation**
   - Generate changelog entries
   - Document breaking changes
   - List new features and improvements
   - Note any migration requirements

2. **Git Workflow**
   - Stage all changes appropriately
   - Generate conventional commit message
   - Prepare merge request description
   - Document testing instructions

3. **Deployment Readiness**
   - Update version numbers if needed
   - Generate deployment notes
   - Prepare rollback procedures
   - Document monitoring considerations

Final Checklist:
- All tests passing
- Documentation complete
- Security scan clean
- Performance validated
- Ready for UAT
```

## Enhanced Orchestration Patterns

### Workflow Execution Framework
```python
orchestration_patterns = {
    "simple_linear": {
        "phases": ["analyze", "test", "implement", "validate"],
        "parallelization": "none",
        "duration_estimate": "15-30 minutes",
        "use_case": "Small features, bug fixes, simple enhancements"
    },

    "parallel_development": {
        "phases": [
            "analyze",
            ["design", "test_spec"],
            ["implement", "ui_design"],
            ["security", "performance"],
            "validate"
        ],
        "parallelization": "moderate",
        "duration_estimate": "30-60 minutes",
        "use_case": "Medium features with UI components"
    },

    "complex_orchestration": {
        "phases": [
            "git_setup",
            "analyze",
            ["design", "security_model"],
            "test_strategy",
            ["implement", "ui_design", "performance_opt"],
            ["security_audit", "doc_creation"],
            "integration_test",
            "final_validation"
        ],
        "parallelization": "high",
        "duration_estimate": "60-120 minutes",
        "use_case": "Major features, architectural changes"
    }
}
```

### Agent Communication Protocol
```python
agent_interfaces = {
    "input_format": {
        "context": "Previous phase outputs",
        "requirements": "Specific agent requirements",
        "constraints": "Technical and business constraints",
        "success_criteria": "Definition of done"
    },

    "output_format": {
        "deliverable": "Primary work product",
        "metadata": "Quality metrics and validation",
        "handoff_notes": "Information for next phase",
        "issues": "Blockers or concerns identified"
    },

    "communication_channels": {
        "sequential": "Direct handoff between phases",
        "parallel": "Shared context with coordination",
        "consultation": "Expert advice without blocking",
        "validation": "Quality gates and approvals"
    }
}
```

## Command Arguments & Options

### Basic Usage
```bash
# Implement next priority finding from active findings
/cci-implement --next

# Implement from project-review (selects highest priority finding)
/cci-implement --from-review

# Implement specific finding by ID
/cci-implement --finding=F001-implement-file-viewer

# Use specific strategy for complex finding
/cci-implement --finding=F002-search-system --strategy=complex

# Maximum parallelization for large finding
/cci-implement --next --parallel --metrics
```

### Command Options
- `--from-review`: Select next priority finding from review workflow
- `--finding=<id>`: Implement specific finding by ID (from docs/findings/active/)
- `--next`: Automatically select highest priority finding
- `--strategy=<type>`: Execution strategy
  - `simple`: Linear workflow for small findings
  - `moderate`: Balanced approach with some parallelization
  - `complex`: Full orchestration with maximum parallelization
  - `auto`: Intelligent strategy selection based on effort_estimate (default)
- `--parallel`: Enable maximum parallel execution where possible
- `--dry-run`: Show execution plan without implementing
- `--metrics`: Track detailed performance and implementation metrics

### Integration Flags
- `--update-session`: Update SESSION.md with implementation progress (default: true)
- `--skip-tests`: Skip test generation/execution (not recommended)
- `--docs-only`: Generate documentation without code changes
- `--quick`: Fast implementation with essential checks only

## Simplified Git Workflow

### Review Branch Workflow
```bash
# Assumes we're already on a review branch from project-review
# No branch creation or switching needed

# Current workflow:
1. Validate we're on appropriate review branch
2. Check for uncommitted changes (warn if present)
3. Implement finding
4. Stage and commit changes with finding reference
5. Update SESSION.md with progress
6. Continue with next finding or complete review
```

### Git Operations
```bash
# Simplified git workflow:
1. Validate current branch state
2. Warn about uncommitted changes
3. Implement finding
4. Commit changes with conventional message
5. Update finding state and session progress
6. No branch switching or creation needed

# Commit message format:
# feat(finding): implement F001 file viewer functionality
# fix(finding): resolve F002 authentication timeout issue
# refactor(finding): F003 cleanup configuration system
```

## Finding-Based Integration

### Finding State Management
```markdown
Finding Workflow:
1. **Finding Selection**
   - Read findings from docs/findings/active/
   - Select by ID, priority, or automatic next selection
   - Validate finding is ready for implementation
   - Check dependencies are satisfied

2. **State Transitions**
   - Move finding: active/ → in-progress/ (start implementation)
   - Update frontmatter with started_date and implementation details
   - Track actual vs estimated effort during implementation
   - Move finding: in-progress/ → completed/ (finish implementation)

3. **Progress Tracking**
   - Update SESSION.md with finding implementation status
   - Track implementation time and complexity
   - Document any issues or deviations discovered
   - Maintain finding audit trail for future reference
```

### Finding Metadata Management
```python
finding_integration = {
    "finding_id": "F001-implement-file-viewer",
    "finding_file": "docs/findings/in-progress/F001-implement-file-viewer.md",
    "priority": "P0",
    "effort_estimate": "medium",
    "started_date": "2025-01-15T10:30:00Z",
    "actual_effort": "2.5 hours",
    "implementation_notes": "Added syntax highlighting support",
    "dependencies": ["FileViewerScreen", "syntax highlighting"],
    "acceptance_criteria": [
        "Can view text files with syntax highlighting",
        "Supports keyboard navigation",
        "Handles large files efficiently"
    ]
}
```

## Quality Gates & Validation

### Phase Gates
```markdown
Each phase must pass validation before proceeding:

Phase 1 Gate: Requirements & Design
- [ ] Requirements clearly documented
- [ ] Architecture design approved
- [ ] Complexity assessment complete
- [ ] Dependencies identified

Phase 2 Gate: Test Foundation
- [ ] Test strategy documented
- [ ] Test files generated
- [ ] Tests failing appropriately (TDD red)
- [ ] Coverage baseline established

Phase 3 Gate: Implementation
- [ ] Core functionality implemented
- [ ] UI components complete (if applicable)
- [ ] Tests passing (TDD green)
- [ ] Code quality standards met

Phase 4 Gate: Quality Assurance
- [ ] Security audit clean
- [ ] Performance targets met
- [ ] Code quality acceptable
- [ ] Error handling robust

Phase 5 Gate: Documentation
- [ ] Technical documentation complete
- [ ] User documentation available
- [ ] Project memory updated
- [ ] UAT instructions ready

Phase 6 Gate: Final Validation
- [ ] Integration tests passing
- [ ] Full test suite clean
- [ ] All quality metrics met
- [ ] Ready for deployment
```

### Rollback Procedures
```bash
Rollback Triggers:
- Critical test failures
- Security vulnerabilities detected
- Performance regressions
- Breaking changes to existing functionality

Rollback Process:
1. Stash current work
2. Switch back to main branch
3. Delete feature branch
4. Restore original state
5. Document rollback reason
6. Plan remediation approach
```

## Error Handling & Recovery

### Failure Modes & Recovery
```markdown
1. **Git Operation Failures**
   - Merge conflicts → Manual resolution or rollback
   - Branch creation issues → Alternative naming
   - Remote push failures → Local branch preservation

2. **Implementation Failures**
   - Test failures → Debug and fix cycle
   - Security issues → Immediate remediation
   - Performance regressions → Optimization required

3. **Agent Failures**
   - Agent timeout → Retry with simplified prompt
   - Context overflow → Reduce context size
   - Tool failures → Fallback to manual steps

4. **Integration Failures**
   - Dependency conflicts → Version resolution
   - Breaking changes → Compatibility shims
   - Configuration issues → Migration scripts
```

### Recovery Strategies
```python
recovery_strategies = {
    "retry_with_context_reduction": "Reduce agent context by 50%",
    "fallback_to_manual_steps": "Provide manual instructions",
    "rollback_and_reassess": "Return to main, analyze failure",
    "phased_implementation": "Break into smaller pieces",
    "expert_consultation": "Request human intervention"
}
```

## Performance & Metrics

### Execution Metrics
```python
performance_tracking = {
    "execution_time": {
        "total": "45 minutes",
        "by_phase": {
            "analysis": "5 minutes",
            "testing": "8 minutes",
            "implementation": "20 minutes",
            "quality": "10 minutes",
            "documentation": "2 minutes"
        }
    },

    "agent_efficiency": {
        "workflow-analyzer": "95% success rate",
        "implementer": "88% first-pass success",
        "tester": "92% coverage achievement",
        "security-auditor": "100% clean scans"
    },

    "quality_metrics": {
        "test_coverage": "94.2%",
        "security_score": "10/10",
        "performance_rating": "Optimal",
        "documentation_completeness": "95%"
    }
}
```

### Continuous Improvement
```markdown
Learning Mechanisms:
1. **Pattern Recognition**
   - Track successful orchestration patterns
   - Identify common failure modes
   - Learn optimal agent combinations
   - Recognize feature complexity indicators

2. **Performance Optimization**
   - Measure phase execution times
   - Optimize agent prompt efficiency
   - Identify parallelization opportunities
   - Reduce context switching overhead

3. **Quality Enhancement**
   - Track quality gate pass rates
   - Monitor test coverage trends
   - Analyze security scan results
   - Measure documentation effectiveness

4. **Workflow Refinement**
   - Update orchestration patterns based on results
   - Improve agent specialization
   - Enhance error recovery procedures
   - Optimize tool usage patterns
```

## Integration with Other Commands

### Command Workflow
```bash
# Typical development session:
/project-review                    # Identify what to build
/cci-implement "feature" --from-review  # Implement from review
/cci-test --strategy=full          # Comprehensive validation
/cci-uat                          # Prepare for user testing
/cci-smart-commit                 # Commit with intelligent message

# Emergency workflows:
/cci-implement "critical fix" --strategy=simple --no-branch
/cci-security                     # Additional security validation
/cci-implement --rollback         # Rollback on issues
```

### Data Flow
```python
command_integration = {
    "inputs": {
        "project-review": "Gap analysis, priorities, copy-paste prompts",
        "cci-status": "Current project state and progress",
        "docs/STATUS.md": "Session memory and context"
    },

    "outputs": {
        "docs/STATUS.md": "Implementation status update",
        "docs/PROGRESS.md": "Feature completion tracking",
        "docs/UAT_READY.md": "Features ready for testing",
        "git_branch": "Feature branch with implementation"
    }
}
```

## Example Outputs

### Simple Finding Implementation
```
🚀 IMPLEMENTING FINDING: F001-implement-dark-mode

📋 Finding Setup
  Finding: F001-implement-dark-mode (Priority: P1, Effort: small)
  Moved: docs/findings/active/ → docs/findings/in-progress/ ✅
  Started: 2025-01-15 10:30:00 ✅

📋 Phase 1: Analysis (Simple Strategy)
  @workflow-analyzer: Finding requirements analyzed ✅
  Effort Level: Small | Risk: Low | Components: 2
  Acceptance Criteria: 3 criteria identified ✅

🧪 Phase 2: Test Foundation
  @tester: 8 tests generated ✅
  tests/unit/test_dark_mode.py → 5 tests
  tests/integration/test_ui_theming.py → 3 tests
  Red phase: All tests failing as expected ✅

⚡ Phase 3: Implementation
  @implementer: Core logic implemented ✅
  @ui-designer: Toggle component created ✅
  Files modified:
    - src/cci/tui/themes.py
    - src/cci/models/config.py
    - src/cci/tui/widgets/settings.py

  Tests: 8/8 passing ✅
  Acceptance Criteria: 3/3 satisfied ✅

🔒 Phase 4: Quality Assurance
  @security-auditor: No security issues ✅
  @performance-optimizer: 2 optimizations applied ✅

📚 Phase 5: Documentation
  @documenter: User guide updated ✅
  @doc-optimizer: Finding and session updated ✅

✅ Phase 6: Validation
  Integration tests: PASS
  Acceptance criteria: All validated ✅

🎯 FINDING IMPLEMENTATION COMPLETE!

Finding "F001-implement-dark-mode" successfully implemented in 18 minutes.
Actual effort: 18 minutes (estimated: small)
Moved: docs/findings/in-progress/ → docs/findings/completed/ ✅
SESSION.md updated with progress ✅

Next steps:
1. Continue with next priority finding: /cci-implement --next
2. Test completed findings: /cci-uat
3. Complete review when all findings done
```

### From Review Finding Implementation
```
🔍 REVIEW FINDING IMPLEMENTATION

📋 Finding Context:
  Finding: F003-implement-file-viewer (Priority: P0, Effort: large)
  Source: Project-review workflow
  Review Branch: review/2025-01-15-comprehensive-analysis

🚀 IMPLEMENTING: File viewer functionality

📋 Finding Setup
  Current branch: review/2025-01-15-comprehensive-analysis ✅
  Finding moved: active/ → in-progress/ ✅
  Review context loaded ✅

📋 Phase 1: Analysis (Complex Strategy - large effort)
  @workflow-analyzer: Finding requirements analyzed ✅
  @architect: Design from finding specifications ✅
  Effort Level: Large | Risk: Medium | Components: 5

  Finding Integration:
  ✅ Loaded acceptance criteria (5 criteria)
  ✅ Applied finding priority weighting
  ✅ Using finding-recommended patterns
  ✅ Dependencies validated

🧪 Phase 2: Test Foundation
  @tester: 23 tests generated (from finding specs) ✅
  Coverage target: 90%+ (finding requirement)

⚡ Phase 3: Implementation (Parallel)
  @implementer: FileViewerScreen created ✅
  @ui-designer: Syntax highlighting added ✅
  @implementer: File operations implemented ✅

  Files created:
    - src/cci/tui/screens/file_viewer.py
    - src/cci/core/file_handler.py
    - src/cci/utils/syntax_highlighter.py

  Acceptance Criteria: 5/5 satisfied ✅
  Tests: 23/23 passing ✅

🔒 Phase 4: Quality Assurance (Parallel)
  @security-auditor: File handling security ✅
  @performance-optimizer: Large file optimization ✅

📚 Phase 5: Documentation
  @documenter: API and user docs created ✅
  @doc-optimizer: Finding and session updated ✅

  Finding Updates:
  ✅ Updated frontmatter with implementation details
  ✅ Documented actual effort: 52 minutes
  ✅ Added implementation notes and decisions
  ✅ SESSION.md progress updated

✅ Phase 6: Validation
  All acceptance criteria validated ✅
  Integration with existing TUI confirmed ✅

🎯 FINDING IMPLEMENTATION COMPLETE!

Successfully implemented P0 critical finding from review.
Finding: F003-implement-file-viewer
Actual effort: 52 minutes (estimated: large)
Moved: docs/findings/in-progress/ → docs/findings/completed/ ✅

SESSION.md Status:
- Critical finding resolved ✅
- 3 findings remaining in active/
- Review progress: 60% complete

Next Steps:
1. Continue with next finding: /cci-implement --next
2. Complete remaining findings to finish review
3. Run /cci-uat when all findings complete
```

## Success Criteria

### Implementation Success
- All quality gates passed
- Tests provide 90%+ coverage
- Security scan clean
- Performance targets met
- Documentation complete
- Git workflow clean

### Workflow Success
- Intelligent strategy selection
- Efficient agent orchestration
- Minimal human intervention required
- Clear audit trail maintained
- Rollback capability preserved

### Integration Success
- Project-review recommendations consumed
- Documentation memory maintained
- Progress tracking updated
- Ready for UAT validation
- Seamless command chaining

This enhanced cci-implement workflow creates a sophisticated yet user-friendly system that intelligently orchestrates feature development while maintaining high quality standards and excellent integration with the broader development ecosystem.