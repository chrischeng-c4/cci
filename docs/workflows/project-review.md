# Project Review Workflow

## Overview

The Project Review workflow provides comprehensive project analysis to identify gaps between documentation and implementation, delivering actionable guidance for development priorities.

## Purpose

This workflow acts as an expert project manager that:
- Analyzes documentation completeness
- Evaluates code implementation status
- Identifies misalignments and gaps
- Provides prioritized action items
- Generates copy-paste ready development prompts

## Architecture

```mermaid
graph TD
    A[/project-review Command] --> B[project-review-coordinator]
    B --> C[project-review-analyzer]
    B --> D[project-review-validator]
    C --> E[Documentation Analysis]
    C --> F[Code Analysis]
    C --> G[Gap Detection]
    D --> H[Finding Validation]
    D --> I[Priority Verification]
    B --> J[Final Report]
    J --> K[Executive Summary]
    J --> L[Prioritized Actions]
    J --> M[Development Prompts]
```

## Components

### 1. Command Entry Point
**Location**: `.claude/commands/project-review.md`
**Purpose**: User-facing interface for triggering reviews
**Options**:
- `--quick`: Fast review of critical items
- `--focus=<area>`: Targeted analysis
- `--report-only`: Non-interactive mode
- `--compare`: Show changes since last review

### 2. Coordinator Agent
**Location**: `.claude/agents/project-review-coordinator.md`
**Role**: Orchestrates the review workflow
**Responsibilities**:
- Manages parallel agent execution
- Synthesizes findings
- Generates final report
- Makes strategic recommendations

### 3. Analyzer Agent
**Location**: `.claude/agents/project-review-analyzer.md`
**Role**: Performs deep project analysis
**Responsibilities**:
- Scans all documentation
- Analyzes codebase
- Identifies gaps and misalignments
- Calculates metrics

### 4. Validator Agent
**Location**: `.claude/agents/project-review-validator.md`
**Role**: Ensures accuracy and quality
**Responsibilities**:
- Verifies findings
- Validates priorities
- Enhances recommendations
- Checks feasibility

## Workflow Execution

### Phase 1: Discovery (5 seconds)
1. Read project configuration
2. Understand current state
3. Determine review scope
4. Load previous review (if exists)

### Phase 2: Analysis (15 seconds)
1. Launch analyzer agent
2. Scan documentation structure
3. Analyze code implementation
4. Detect gaps and misalignments
5. Calculate coverage metrics

### Phase 3: Validation (10 seconds)
1. Launch validator agent
2. Verify findings accuracy
3. Adjust priorities
4. Enhance recommendations
5. Add risk assessments

### Phase 4: Synthesis (5 seconds)
1. Merge agent reports
2. Resolve conflicts
3. Apply strategic prioritization
4. Generate action items
5. Create development prompts

### Phase 5: Reporting (5 seconds)
1. Generate executive summary
2. Format findings by category
3. Create copy-paste prompts
4. Save review to history
5. Display results

## Output Categories

### Documentation Ahead of Code
Features that are documented but not implemented.
- **Indicator**: 📝 Documented, ❌ Not Implemented
- **Action**: Implement following documentation
- **Priority**: Usually HIGH

### Code Ahead of Documentation
Features that are implemented but not documented.
- **Indicator**: ✅ Implemented, 📝 Not Documented
- **Action**: Create documentation
- **Priority**: Usually MEDIUM

### Misalignments
Logic differences between docs and code.
- **Indicator**: ⚠️ Misaligned
- **Action**: Fix inconsistencies
- **Priority**: CRITICAL if breaking, HIGH otherwise

### Missing Tests
Code without adequate test coverage.
- **Indicator**: 🧪 No Tests
- **Action**: Add test coverage
- **Priority**: Varies by component criticality

## Priority Framework

### CRITICAL (🔴)
- Breaking functionality
- Security vulnerabilities
- Severe inconsistencies
- **Response**: Fix immediately

### HIGH (🟠)
- Core features missing
- Major gaps
- Important functionality
- **Response**: Address this session

### MEDIUM (🟡)
- Documentation gaps
- Minor features
- Nice-to-have improvements
- **Response**: Schedule for next session

### LOW (🟢)
- Cosmetic issues
- Future enhancements
- Technical debt
- **Response**: Add to backlog

## Development Prompts

Each finding includes a structured prompt:

```markdown
📋 Copy-Paste Prompt:
"[Action verb] [specific feature] [location details].
[Implementation requirements]:
- [Requirement 1]
- [Requirement 2]
[Acceptance criteria]
[Testing requirements]"
```

### Prompt Quality Criteria
- Specific file paths included
- Clear acceptance criteria
- Concrete examples provided
- Testable outcomes defined
- Context fully contained

## Integration Points

### Input Sources
- `CLAUDE.md`: Project guidelines
- `docs/STATUS.md`: Current state
- `docs/PROGRESS.md`: Feature tracking
- `docs/ISSUES.md`: Known problems
- Source code: Implementation status
- Test files: Coverage information

### Output Destinations
- Console: Interactive display
- `docs/reviews/`: Historical records
- `docs/STATUS.md`: Status updates
- `docs/development/TODO.md`: Action items

## Metrics Tracked

### Coverage Metrics
- **Documentation Coverage**: % of features documented
- **Code Completion**: % of features implemented
- **Test Coverage**: % of code tested
- **Alignment Score**: Docs/code consistency (0-10)

### Quality Metrics
- **Technical Debt**: Refactoring needed
- **Complexity**: Code complexity score
- **Maintainability**: Maintainability index
- **Security**: Vulnerability count

### Progress Metrics
- **Velocity**: Features/session
- **Burndown**: Remaining work
- **Cycle Time**: Feature completion time
- **Review Frequency**: Reviews/week

## Configuration

### Review Depth Levels

#### Shallow
- Quick scan of major files
- Basic gap detection
- High-level recommendations
- **Time**: ~10 seconds

#### Normal (Default)
- Comprehensive analysis
- Detailed gap detection
- Prioritized recommendations
- **Time**: ~30 seconds

#### Deep
- Exhaustive analysis
- Cross-reference validation
- Risk assessment
- Alternative approaches
- **Time**: ~60 seconds

### Focus Areas

#### Testing Focus
- Test coverage analysis
- Missing test identification
- Test quality assessment
- Testing strategy recommendations

#### Documentation Focus
- Documentation completeness
- API documentation
- User guides
- Example coverage

#### Implementation Focus
- Feature completion
- Code quality
- Performance issues
- Security concerns

## Best Practices

### For Developers
1. Run review at session start for direction
2. Run review at session end for progress tracking
3. Follow priority order (CRITICAL → HIGH → MEDIUM → LOW)
4. Use provided prompts for consistency
5. Update STATUS.md after completing items

### For Project Managers
1. Schedule weekly comprehensive reviews
2. Use --compare to track velocity
3. Monitor alignment scores
4. Review technical debt trends
5. Plan sprints based on priorities

## Error Handling

### Common Issues

#### No Documentation Found
- **Cause**: Missing documentation structure
- **Solution**: Creates documentation template
- **Recovery**: Suggests initial documentation

#### No Code Found
- **Cause**: Empty project
- **Solution**: Provides bootstrapping guide
- **Recovery**: Suggests project structure

#### Conflicting Findings
- **Cause**: Ambiguous specifications
- **Solution**: Validator resolves conflicts
- **Recovery**: Requests clarification

## Performance Optimization

### Caching Strategy
- Cache file contents for session
- Reuse AST parsing results
- Store metrics calculations
- Remember previous findings

### Parallel Execution
- Run analyzer and validator concurrently
- Batch file operations
- Async metric calculations
- Parallel report generation

## Success Metrics

### Workflow Success
- Completion time < 30 seconds
- Zero false positives
- > 90% actionable recommendations
- Clear priority assignments

### Project Impact
- Reduced development friction
- Improved documentation quality
- Higher test coverage
- Better code-doc alignment

## Evolution Path

### Version 1.0 (Current)
- Basic gap detection
- Priority assignment
- Prompt generation

### Version 2.0 (Planned)
- AI-powered code understanding
- Dependency analysis
- Impact assessment
- Auto-fix capabilities

### Version 3.0 (Future)
- Predictive recommendations
- Team collaboration features
- CI/CD integration
- Real-time monitoring

## Related Workflows

- `/cci-test`: Run tests identified by review
- `/cci-implement`: Implement features from review
- `/cci-smart-commit`: Commit completed items
- `/cci-status`: Check implementation progress

## Troubleshooting

### Review Takes Too Long
- Use `--quick` flag
- Focus on specific area with `--focus`
- Check for large files slowing analysis

### Incorrect Findings
- Validator should catch most issues
- Check for recent uncommitted changes
- Ensure documentation is up to date

### Missing Recommendations
- Check review depth setting
- Ensure all files are accessible
- Verify project structure is standard

## Summary

The Project Review workflow transforms project management from intuition-based to data-driven decision making. By systematically analyzing the gap between documentation and implementation, it provides clear, actionable guidance that accelerates development and maintains project coherence.