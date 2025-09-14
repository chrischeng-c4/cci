---
allowed-tools: ["Bash", "Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "Task", "TodoWrite", "WebSearch", "WebFetch"]
model: "claude-opus-4-1-20250805"
description: "Orchestrate complete feature implementation with intelligent workflow orchestration"
argument-hint: "<feature-description> [--docs-first] [--token-optimize] [--strategy=<type>]"
thinking-level: "ultrathink"
subagents: ["workflow-analyzer", "doc-optimizer", "architect", "implementer", "tester", "security-auditor", "performance-optimizer", "ui-designer", "documenter", "workflow-validator"]
project-aware: true
---

# /cci-implement

ultrathink about creating a comprehensive feature implementation workflow that combines documentation intelligence, multi-agent orchestration, and continuous self-improvement into a unified development ecosystem.

## Workflow Intelligence Framework

**This command creates complete development ecosystems by:**
- Understanding complex requirements and mapping to capabilities
- Reorganizing documentation for optimal AI comprehension
- Creating specialized agent networks with clear orchestration patterns
- Generating intuitive command interfaces and workflow documentation
- Maintaining project memory and decision history
- Ensuring token-efficient documentation structure (<1000 tokens CLAUDE.md)

### Workflow Philosophy
- **Documentation First**: Optimize knowledge structure before implementation
- **Token Efficiency**: Maintain concise CLAUDE.md with smart references
- **Agent Specialization**: Each agent has clear, focused responsibilities
- **Continuous Learning**: Track patterns and improve with each execution
- **Quality Gates**: Enforce standards at every phase

## Phase 0: Documentation Intelligence & Optimization

### 0.1 Documentation Analysis
@doc-optimizer: Analyze and reorganize project documentation:
```markdown
Documentation Strategy:
1. **Token Usage Analysis**
   - Measure current CLAUDE.md size
   - Identify redundancies and inefficiencies
   - Calculate optimal structure

2. **Reorganization Plan**
   - README.md: Human-focused quick start
   - CLAUDE.md: AI-optimized instructions (<1000 tokens)
   - docs/: Hierarchical knowledge base
```

### 0.2 CLAUDE.md Optimization
Compress CLAUDE.md for token efficiency:
```markdown
# Before (5000+ tokens)
## Detailed Testing Guidelines
[500 tokens of testing details...]

# After (100 tokens)
## Testing
- Framework: pytest
- Coverage: 90%+ required
- Details: → docs/guides/testing.md
```

### 0.3 Documentation Structure Update
```bash
@Task: Reorganize docs/ folder:
docs/
├── STATUS.md              # Current state (AI memory)
├── PROGRESS.md            # Feature tracking
├── workflows/
│   └── <feature>.md       # This implementation workflow
├── architecture/
│   ├── decisions/         # ADRs for this feature
│   └── <feature>-design.md
└── development/
    ├── CURRENT_SPRINT.md  # Active work
    └── FEATURE_LOG.md     # Implementation history
```

## Phase 1: Deep Understanding & Workflow Planning

### 1.1 Requirements Analysis
@workflow-analyzer: Deeply analyze the feature request:

```markdown
Workflow Analysis:
1. **Intent Extraction**: What does the user really want to achieve?
2. **Capability Mapping**: What agents and tools are needed?
3. **Workflow Pattern**: Sequential, parallel, or hybrid execution?
4. **Integration Points**: How does this fit with existing system?
5. **Documentation Needs**: What knowledge must be captured?
6. **Quality Criteria**: How do we measure success?

Feature Classification:
- Type: feature|enhancement|fix|refactor|performance
- Complexity: simple|moderate|complex|critical
- Risk Level: low|medium|high
- Testing Strategy: unit|integration|e2e|all
```

### 1.2 Workflow Architecture Design
@architect: Design the implementation workflow:
```markdown
Workflow Components:
1. **Entry Points**: Commands and interfaces
2. **Execution Layer**: Agent orchestration pattern
3. **Data Flow**: Information passing between phases
4. **Error Handling**: Recovery and rollback strategies
5. **Feedback Loops**: Progress tracking and updates

Orchestration Pattern:
- Sequential: Design → Test → Implement → Validate
- Parallel: [Security, Performance, Documentation]
- Conditional: If tests fail → Debug → Retry
```

### 1.3 Workflow Documentation Generation
Create comprehensive workflow documentation:
```markdown
# docs/workflows/<feature>.md

## <Feature> Implementation Workflow

### Architecture
- Orchestrator: @workflow-analyzer
- Specialists: [list of agents]
- Pattern: <orchestration-pattern>

### Execution Flow
[Visual workflow diagram]

### Quality Gates
- Coverage: 90%+
- Security: Clean scan
- Performance: Meets targets

### Integration Points
- Upstream: Dependencies
- Downstream: Dependents
```

## Phase 2: Test-Driven Development with Intelligence

1. **Test Specification**
   @tester: Design comprehensive test suite:
   - Unit test specifications
   - Integration test scenarios
   - End-to-end test cases
   - Performance benchmarks
   - Edge case coverage

2. **Test Implementation**
   Write tests before code (TDD):
   ```python
   # Generate test files first
   tests/unit/test_<feature>.py
   tests/integration/test_<feature>_integration.py
   tests/e2e/test_<feature>_e2e.py
   ```

3. **Test Execution (Red Phase)**
   Verify tests fail appropriately:
   - Run generated tests
   - Confirm expected failures
   - Validate test quality

## Phase 3: Intelligent Implementation

1. **Core Implementation**
   @implementer: Write production code:
   - Follow project conventions from CLAUDE.md
   - Implement minimal code to pass tests
   - Use existing patterns and utilities
   - Maintain type hints and docstrings

2. **UI/UX Implementation** (if applicable)
   @ui-designer: Create user interfaces:
   - Design TUI components with Textual
   - Implement CLI commands with Typer
   - Ensure keyboard navigation
   - Add accessibility features

3. **Incremental Testing (Green Phase)**
   Continuously validate implementation:
   - Run tests after each component
   - Fix failures immediately
   - Maintain coverage above 90%

## Phase 4: Comprehensive Quality Assurance

1. **Security Audit**
   @security-auditor: Comprehensive security review:
   - Input validation checks
   - Dependency vulnerability scan
   - Secret/credential detection
   - Secure coding patterns
   - Threat modeling

2. **Performance Optimization**
   @performance-optimizer: Optimize implementation:
   - Profile code execution
   - Identify bottlenecks
   - Optimize algorithms
   - Reduce memory usage
   - Improve response times

3. **Code Quality (Refactor Phase)**
   @implementer: Refine and polish:
   - Refactor for clarity
   - Remove duplication
   - Improve naming
   - Enhance error handling
   - Optimize imports

## Phase 5: Documentation Intelligence & Memory Persistence

1. **Technical Documentation**
   @documenter: Create comprehensive docs:
   - API documentation
   - User guides
   - Configuration examples
   - Troubleshooting guides
   - Architecture diagrams

2. **Project Memory Updates**
   Maintain persistent context:
   ```markdown
   # Update multiple documentation files
   docs/STATUS.md           → Current implementation status
   docs/PROGRESS.md          → Feature completion tracking
   docs/development/FEATURE_LOG.md → Implementation details
   docs/UAT_READY.md        → Mark feature for testing
   ```

3. **Changelog Generation**
   Document changes systematically:
   - Feature additions
   - Breaking changes
   - Bug fixes
   - Performance improvements

## Phase 6: Workflow Validation & Self-Improvement

1. **Integration Testing**
   Validate feature in context:
   - Test with existing features
   - Verify backward compatibility
   - Check configuration migrations
   - Validate data integrity

2. **Full Test Suite**
   Run comprehensive validation:
   ```bash
   /cci-test --strategy=full --coverage-min=90
   /cci-security
   /cci-status --detail
   ```

3. **UAT Preparation & Workflow Learning**
   Prepare for validation and capture learnings:
   ```markdown
   @Task: Complete implementation:
   1. Update UAT_READY.md with test instructions
   2. Generate test scenarios and demo scripts
   3. Package for testing

   @Task: Capture workflow intelligence:
   1. Log execution patterns to WORKFLOW_LOG.md
   2. Update DECISIONS.md with learnings
   3. Optimize agent prompts based on experience
   4. Track performance metrics:
      - Execution time per phase
      - Token usage optimization
      - Error recovery patterns
      - Success rate metrics
   ```

## Intelligent Orchestration Patterns

### Workflow Execution Patterns

#### 1. Documentation-First Pattern
```python
workflow_phases = {
    "0_documentation": {
        "agents": ["@doc-optimizer"],
        "parallel": False,
        "critical": True,
        "output": "Optimized knowledge structure"
    },
    "1_analysis": {
        "agents": ["@workflow-analyzer", "@architect"],
        "parallel": True,
        "critical": True,
        "output": "Workflow design + Architecture"
    },
    "2_test_design": {
        "agents": ["@tester"],
        "parallel": False,
        "critical": True,
        "output": "Test specifications"
    },
    "3_implementation": {
        "agents": ["@implementer", "@ui-designer"],
        "parallel": True,
        "critical": True,
        "output": "Production code"
    },
    "4_quality": {
        "agents": ["@security-auditor", "@performance-optimizer"],
        "parallel": True,
        "critical": False,
        "output": "Quality reports"
    },
    "5_documentation": {
        "agents": ["@documenter"],
        "parallel": False,
        "critical": False,
        "output": "Complete documentation"
    },
    "6_validation": {
        "agents": ["@workflow-validator"],
        "parallel": False,
        "critical": True,
        "output": "Validation report"
    }
}
```

#### 2. Token-Optimized Communication
```python
# Minimize context passing between agents
optimized_context = {
    "refs": {  # Use references instead of content
        "spec": "→ docs/architecture/<feature>-design.md",
        "tests": "→ tests/<feature>/",
        "impl": "→ src/cci/<module>/"
    },
    "metrics": {  # Only essential metrics
        "coverage": 94.2,
        "performance": "50ms",
        "security": "clean"
    }
}
```

#### 3. Adaptive Orchestration
```python
# Adjust workflow based on feature complexity
if complexity == "simple":
    workflow = "linear: analyze → implement → test"
elif complexity == "moderate":
    workflow = "parallel: [design, test] → implement → validate"
else:  # complex
    workflow = "full: docs → design → test → implement → optimize → validate"
```

## Workflow Intelligence & Self-Improvement

### Continuous Learning Mechanisms

#### 1. Pattern Recognition
```markdown
@Task: Track and learn from each execution:
1. **Success Patterns**
   - Log to: docs/development/WORKFLOW_LOG.md
   - Identify: What worked well?
   - Capture: Reusable patterns

2. **Failure Analysis**
   - Log to: docs/ISSUES.md
   - Identify: What failed and why?
   - Solution: Recovery strategies

3. **Performance Metrics**
   - Execution time per phase
   - Token usage optimization
   - Agent efficiency scores
   - Quality gate pass rates
```

#### 2. Documentation Evolution
```markdown
After each execution:
1. **Token Optimization**
   - Measure CLAUDE.md size
   - Identify compression opportunities
   - Update references vs content balance

2. **Knowledge Capture**
   - Update docs/development/DECISIONS.md
   - Enhance docs/development/FEATURE_LOG.md
   - Refine workflow documentation

3. **Agent Prompt Refinement**
   - Analyze agent performance
   - Update system prompts
   - Optimize tool usage patterns
```

#### 3. Workflow Optimization
```python
optimization_metrics = {
    "token_efficiency": {
        "before": "5000 tokens",
        "after": "950 tokens",
        "improvement": "81% reduction"
    },
    "execution_time": {
        "baseline": "15 minutes",
        "optimized": "8 minutes",
        "improvement": "47% faster"
    },
    "quality_scores": {
        "coverage": "94.2%",
        "security": "0 vulnerabilities",
        "performance": "exceeds targets"
    }
}
```

## Enhanced Arguments

- `<feature-description>`: Natural language feature description
- `--docs-first`: Prioritize documentation optimization before implementation
- `--token-optimize`: Aggressively optimize CLAUDE.md for token efficiency
- `--strategy=<type>`: Execution strategy
  - `workflow`: Full workflow with documentation intelligence (default)
  - `tdd`: Traditional test-driven development
  - `rapid`: Fast implementation with essential checks
  - `comprehensive`: All quality gates and optimizations
- `--agents=<list>`: Specific agents to use (comma-separated)
- `--parallel`: Enable maximum parallel execution
- `--metrics`: Track detailed performance metrics
- `--learning`: Enable workflow learning and optimization

## Enhanced Subagent Specializations

### @workflow-analyzer
- Expertise: Requirement analysis, workflow design, orchestration
- Focus: Understanding intent, mapping capabilities, pattern selection
- Output: Workflow architecture and execution plan

### @doc-optimizer
- Expertise: Documentation structure, token optimization, knowledge organization
- Focus: Concise CLAUDE.md, hierarchical docs, smart references
- Output: Optimized documentation structure

### @architect
- Expertise: System design, patterns, architecture
- Focus: Scalability, maintainability, extensibility
- Output: Technical design documents

### @implementer
- Expertise: Code writing, refactoring, optimization
- Focus: Clean code, best practices, efficiency
- Output: Production-ready code

### @tester
- Expertise: Test design, coverage, quality assurance
- Focus: Edge cases, reliability, regression prevention
- Output: Comprehensive test suites

### @security-auditor
- Expertise: Security vulnerabilities, threat modeling
- Focus: Input validation, authentication, authorization
- Output: Security audit reports

### @performance-optimizer
- Expertise: Profiling, optimization, efficiency
- Focus: Speed, memory usage, scalability
- Output: Performance improvements

### @ui-designer
- Expertise: User interfaces, accessibility, UX
- Focus: Usability, consistency, responsiveness
- Output: UI components and interactions

### @documenter
- Expertise: Technical writing, API docs, guides
- Focus: Clarity, completeness, examples
- Output: Documentation and tutorials

### @workflow-validator
- Expertise: Quality validation, metrics tracking, compliance checking
- Focus: Ensuring all gates pass, tracking improvements
- Output: Validation reports and metrics

## Workflow-Intelligent Output Format

```
🧠 WORKFLOW IMPLEMENTATION: Advanced Search Functionality
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Phase 0: Documentation Intelligence
  @doc-optimizer analyzing...     ✅ Structure optimized
  Token Reduction: 5000 → 950 tokens (81% reduction)
  Knowledge Structure: Hierarchical with smart references
  Workflow Documented: docs/workflows/search-feature.md

📋 Phase 1: Requirements & Design
  @architect analyzing...        ✅ Architecture designed
  @tester planning tests...       ✅ Test strategy ready
  Complexity: Moderate
  Components: core.search, ui.search_widget

📐 Phase 2: Test-Driven Development
  Writing test specifications... ✅
  Generated Tests:
    - tests/unit/test_search.py (15 tests)
    - tests/integration/test_search_integration.py (8 tests)
    - tests/e2e/test_search_e2e.py (5 tests)
  Running tests (Red phase)...   ✅ All failing as expected

⚡ Phase 3: Implementation
  @implementer coding core...    ████████████ 100%
  @ui-designer creating UI...    ████████████ 100%

  Files Created/Modified:
    ✅ src/cci/core/search.py
    ✅ src/cci/tui/widgets/search_widget.py
    ✅ src/cci/models/search_result.py

  Tests Passing: 28/28 ✅

🔒 Phase 4: Quality Assurance
  @security-auditor scanning...  ✅ No vulnerabilities
  @performance-optimizer...      ✅ 3 optimizations applied

  Metrics:
    Coverage: 94.2% (exceeds 90% requirement)
    Security: All inputs validated
    Performance: 50ms average search time
    Code Quality: A+ (no issues)

📚 Phase 5: Documentation
  @documenter writing...         ✅ Complete

  Documentation Generated:
    - API Reference: docs/api/search.md
    - User Guide: docs/guides/search-feature.md
    - Examples: docs/examples/search-usage.md

  Memory Updated:
    - docs/STATUS.md ✅
    - docs/PROGRESS.md ✅
    - docs/UAT_READY.md ✅

✅ Phase 6: Validation
  Integration Tests: PASS
  Full Test Suite: PASS (147/147)
  Security Scan: CLEAN
  Performance: OPTIMAL

🎯 WORKFLOW COMPLETE!

Feature "Advanced Search Functionality" successfully implemented.
All quality gates passed. Ready for UAT.

📊 WORKFLOW METRICS:
━━━━━━━━━━━━━━━━━━━━
Execution Time: 8 minutes 32 seconds
Token Efficiency: 81% reduction achieved
Agents Orchestrated: 10
Parallel Executions: 3

Quality Metrics:
  Coverage: 94.2% ✅
  Security: Clean ✅
  Performance: Optimal ✅
  Documentation: Complete ✅

Workflow Intelligence:
  Patterns Captured: 5
  Optimizations Applied: 3
  Learning Points: 2

📈 CONTINUOUS IMPROVEMENT:
- Next execution will be ~15% faster
- Documentation structure optimized for future features
- Agent prompts refined based on this execution

Next Steps:
1. Review: docs/workflows/search-feature.md
2. Test: /cci-uat
3. Deploy: /cci-smart-commit
```

## Error Handling & Recovery

1. **Agent Failures**
   - Automatic retry with context
   - Fallback to general-purpose agent
   - Manual intervention points

2. **Test Failures**
   - Intelligent debugging assistance
   - Automatic fix suggestions
   - Rollback capabilities

3. **Integration Issues**
   - Conflict resolution strategies
   - Compatibility checks
   - Migration path generation

## Integration Points

- `/cci-status`: Monitor implementation progress
- `/cci-test`: Validate implementation quality
- `/cci-security`: Security validation
- `/cci-uat`: Package for testing
- `/cci-smart-commit`: Commit completed feature

## Workflow-Driven Examples

### Full Workflow Implementation (Default)
```bash
/cci-implement "Add dark mode support to TUI" --docs-first --token-optimize
# Complete workflow with documentation intelligence
# Optimizes CLAUDE.md, creates workflow docs, orchestrates all agents
```

### Complex Feature with Learning
```bash
/cci-implement "Multi-tenant architecture" --strategy=workflow --learning --metrics
# Captures patterns, tracks metrics, improves future executions
```

### Documentation-First Development
```bash
/cci-implement "API versioning system" --docs-first
# Reorganizes documentation before implementation
# Ensures optimal knowledge structure
```

### Parallel Execution Optimization
```bash
/cci-implement "Performance monitoring dashboard" --parallel --metrics
# Maximizes parallel agent execution
# Tracks detailed performance metrics
```

### Token-Optimized Implementation
```bash
/cci-implement "Search functionality" --token-optimize
# Aggressively reduces documentation tokens
# Maintains quality with smart references
```

## Workflow Intelligence Summary

This command creates complete development ecosystems by:

1. **Documentation Intelligence**:
   - Optimizes knowledge structure before implementation
   - Maintains token-efficient CLAUDE.md (<1000 tokens)
   - Creates hierarchical documentation with smart references

2. **Workflow Orchestration**:
   - Understands complex requirements deeply
   - Maps capabilities to specialized agents
   - Implements adaptive execution patterns
   - Coordinates 10+ agents seamlessly

3. **Continuous Improvement**:
   - Tracks execution patterns and metrics
   - Learns from successes and failures
   - Optimizes future executions automatically
   - Refines agent prompts based on experience

4. **Quality Excellence**:
   - Enforces TDD with 90%+ coverage
   - Multiple quality gates at each phase
   - Security and performance by default
   - Comprehensive validation and testing

5. **Knowledge Persistence**:
   - Maintains project memory across sessions
   - Documents all decisions and rationales
   - Creates reusable workflow patterns
   - Builds institutional knowledge

This creates a perfect balance: **simple for humans, sophisticated for AI, excellent in execution**.

The workflow continuously evolves, becoming more intelligent with each feature implementation, ultimately achieving a self-improving development ecosystem that delivers consistent, high-quality results.