---
allowed-tools: ["Bash", "Read", "Glob", "Grep", "Task", "TodoWrite", "WebSearch"]
model: "claude-opus-4-1-20250805"
description: "AI-powered commit message generation with semantic analysis and conventional commits"
argument-hint: "[--interactive] [--split] [--format=<type>]"
thinking-level: "think harder"
subagents: ["code-analyzer", "commit-formatter", "change-classifier"]
project-aware: true
---

# /cci-smart-commit

think harder about generating intelligent commit messages by deeply analyzing code changes, understanding semantic meaning, detecting patterns, and creating conventional commit messages that accurately describe the intent and impact of changes.

## Project Context Integration

This command understands CCI's commit conventions:
- Standards: Conventional Commits specification
- Patterns: Project-specific commit types from CLAUDE.md
- Memory: Reads recent commits for style consistency
- Integration: Works with git worktree workflow
- Quality: Ensures commits are atomic and well-described

## Intelligent Commit Analysis Strategy

### Phase 1: Deep Change Analysis

1. **Multi-Layer Git Analysis**
   Comprehensive change detection:
   ```bash
   # Staged changes analysis
   git diff --cached --name-status
   git diff --cached --numstat
   git diff --cached --stat

   # Detailed diff with context
   git diff --cached -U10

   # File type detection
   git diff --cached --name-only | xargs -I {} file {}
   ```

2. **Semantic Code Analysis**
   @code-analyzer: Understand code meaning:
   ```python
   semantic_analysis = {
       "change_type": "Detect: addition|modification|deletion|refactor",
       "functionality": "Identify what the code does",
       "impact": "Assess scope of changes",
       "breaking": "Detect breaking changes",
       "dependencies": "Check for dependency updates",
       "patterns": "Recognize common patterns"
   }
   ```

3. **Project Memory Integration**
   Learn from project history:
   - Read last 50 commits for style
   - Analyze commit message patterns
   - Understand project-specific conventions
   - Learn scope terminology

### Phase 2: Intelligent Classification

1. **Change Type Detection**
   @change-classifier: Categorize changes:
   ```python
   commit_types = {
       "feat": "New feature or functionality",
       "fix": "Bug fixes or corrections",
       "docs": "Documentation only changes",
       "style": "Code style/formatting",
       "refactor": "Code restructuring",
       "perf": "Performance improvements",
       "test": "Test additions/modifications",
       "build": "Build system changes",
       "ci": "CI/CD configuration",
       "chore": "Maintenance tasks",
       "revert": "Reverting previous commits",
       "wip": "Work in progress (optional)"
   }
   ```

2. **Scope Identification**
   Intelligent scope detection:
   - Module-based scoping (cli, tui, core)
   - Feature-based scoping
   - Component-based scoping
   - Cross-cutting concerns

3. **Breaking Change Detection**
   Identify breaking changes:
   - API signature changes
   - Configuration schema changes
   - Dependency major version updates
   - Removed functionality
   - Changed behavior

### Phase 3: Commit Message Generation

1. **AI-Powered Message Creation**
   @commit-formatter: Generate messages:
   ```python
   message_components = {
       "type": "Determined from analysis",
       "scope": "Optional but recommended",
       "subject": "Imperative, present tense",
       "body": "Explain what and why",
       "footer": "Breaking changes, issues"
   }
   ```

2. **Multiple Message Suggestions**
   Provide options based on perspective:
   ```markdown
   Primary Suggestion:
   feat(tui): add dark mode toggle with system preference detection

   Alternative Perspectives:
   1. feat(ui): implement theme switching functionality
   2. feat: add dark/light mode support to terminal interface
   3. enhancement(tui): support system theme preferences
   ```

3. **Contextual Body Generation**
   For complex changes, generate body:
   ```markdown
   feat(search): implement fuzzy search with scoring algorithm

   - Add Levenshtein distance calculation for fuzzy matching
   - Implement TF-IDF scoring for result ranking
   - Cache search indices for performance
   - Support regex patterns as fallback

   Performance: 10x faster than previous implementation
   Closes #123
   ```

### Phase 4: Smart Commit Strategies

1. **Atomic Commit Suggestions**
   When changes are too large:
   ```python
   if changes_too_complex:
       suggest_split_strategy = {
           "group_by_type": "Separate features from fixes",
           "group_by_module": "Split by component",
           "group_by_dependency": "Isolate dependency updates",
           "staged_approach": "Interactive staging suggestions"
       }
   ```

2. **Interactive Mode**
   Guide through commit process:
   - Show changes grouped by type
   - Suggest staging strategy
   - Generate message for each group
   - Provide commit command

3. **Batch Commit Generation**
   For multiple related changes:
   ```bash
   # Generate series of commits
   1. test(auth): add unit tests for JWT validation
   2. feat(auth): implement JWT authentication
   3. docs(auth): add authentication API documentation
   4. chore: update dependencies for auth support
   ```

### Phase 5: Quality Assurance

1. **Message Validation**
   Ensure quality standards:
   - Length constraints (50/72 rule)
   - Imperative mood verification
   - No trailing punctuation
   - Proper capitalization
   - Conventional format compliance

2. **Content Verification**
   Validate message accuracy:
   - Changes match description
   - Scope is correct
   - Type is appropriate
   - Breaking changes noted

3. **Style Consistency**
   Match project conventions:
   - Use project-specific terminology
   - Follow established patterns
   - Maintain voice consistency
   - Apply team preferences

### Phase 6: Advanced Features

1. **Emoji Integration**
   Optional emoji prefixes:
   ```python
   emoji_map = {
       "feat": "✨",
       "fix": "🐛",
       "docs": "📚",
       "style": "💎",
       "refactor": "♻️",
       "perf": "⚡",
       "test": "🧪",
       "build": "📦",
       "ci": "👷",
       "chore": "🔧"
   }
   ```

2. **Issue Linking**
   Intelligent issue detection:
   - Scan for issue numbers in code
   - Check branch names for issues
   - Look for TODO comments
   - Suggest appropriate linking

3. **Co-author Attribution**
   When applicable:
   ```
   feat(core): implement caching layer

   Co-authored-by: Team Member <email>
   Helped-by: Contributor <email>
   ```

## Self-Optimization Protocol

This command learns and improves:

1. **Pattern Learning**
   - Analyze accepted vs rejected suggestions
   - Learn project-specific patterns
   - Adapt to team preferences
   - Build vocabulary database

2. **Accuracy Improvement**
   - Track suggestion acceptance rate
   - Learn from corrections
   - Improve scope detection
   - Better type classification

3. **Performance Optimization**
   - Cache analysis results
   - Optimize diff parsing
   - Speed up pattern matching
   - Reduce redundant operations

## Arguments

- `--interactive`: Interactive mode with guided staging
- `--split`: Suggest splitting into multiple commits
- `--format=<type>`: Output format (conventional|emoji|simple)
- `--dry-run`: Show message without committing
- `--amend`: Suggest amendment to last commit
- `--squash`: Help squash related commits

## Subagent Delegation

### @code-analyzer
- Expertise: Code semantics, change impact
- Focus: Understanding what changed and why
- Output: Semantic change analysis

### @commit-formatter
- Expertise: Conventional commits, message formatting
- Focus: Clear, compliant messages
- Output: Well-formatted commit messages

### @change-classifier
- Expertise: Change categorization, pattern detection
- Focus: Accurate type and scope identification
- Output: Change classifications

## Enhanced Output Format

```
🎯 Smart Commit Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Change Summary
  Files Changed: 5
  Insertions: +142
  Deletions: -23

  Components Affected:
  - src/cci/tui/themes.py (new file)
  - src/cci/tui/app.py (modified)
  - src/cci/config.py (modified)
  - tests/test_themes.py (new file)
  - docs/features.md (modified)

🔍 Semantic Analysis
  Primary Change: Feature Addition
  Functionality: Theme switching capability
  Scope: TUI module
  Breaking: No
  Dependencies: No changes

📝 Suggested Commit Messages

  🏆 Primary Suggestion:
  ────────────────────────────────────
  feat(tui): add dark mode with automatic system detection

  Implement comprehensive theme support including:
  - Dark and light theme definitions
  - Automatic OS theme detection
  - Manual theme toggle command
  - Theme persistence in config

  Uses system preferences on macOS/Windows/Linux
  Fixes #45
  ────────────────────────────────────

  🔄 Alternative Options:

  1️⃣ Concise Version:
  feat(tui): implement dark/light theme switching

  2️⃣ Detailed Technical:
  feat(tui): add theme engine with OS integration and persistence

  3️⃣ User-Focused:
  feat: add dark mode support to terminal interface

⚠️ Recommendations:

  📦 Consider splitting docs changes:
  Your documentation changes could be a separate commit:
  - docs: document theme configuration options

  🧪 Test changes are substantial:
  Consider separate commit for tests:
  - test(tui): add comprehensive theme switching tests

💡 Quick Actions:

  1. Use primary suggestion:
     git commit -m "feat(tui): add dark mode with automatic system detection" -m "..."

  2. Interactive commit with split:
     /cci-smart-commit --split

  3. Stage and commit separately:
     git add src/cci/tui/
     git commit -m "feat(tui): add dark mode support"
     git add tests/
     git commit -m "test(tui): add theme tests"

📈 Commit Style Analysis:
  Your recent commits follow: conventional (strict)
  Scope usage: 87% (recommended)
  Average subject length: 42 chars (good)
  Body included: 65% of commits
```

## Error Handling

1. **No Staged Changes**
   - Clear message about staging requirement
   - Suggest files to stage
   - Offer to analyze unstaged changes

2. **Ambiguous Changes**
   - Provide multiple interpretations
   - Ask for clarification
   - Suggest splitting strategy

3. **Large Changesets**
   - Warn about atomic commit principle
   - Suggest logical groupings
   - Provide split commands

## Integration Points

- `/cci-implement`: Commit after feature completion
- `/cci-test`: Commit after tests pass
- `/cci-status`: Check uncommitted changes
- Git hooks: Validate message format
- CI/CD: Changelog generation

## Examples

### Simple Commit
```
/cci-smart-commit
# Analyzes staged changes and suggests message
```

### Interactive Mode
```
/cci-smart-commit --interactive
# Guides through staging and message creation
```

### Split Large Changes
```
/cci-smart-commit --split
# Suggests how to split into atomic commits
```

### With Emoji Format
```
/cci-smart-commit --format=emoji
# ✨ feat(core): add new feature
```

## Continuous Intelligence

This command demonstrates AI-powered commit intelligence:
1. **Semantic Understanding**: Comprehends code changes meaning
2. **Pattern Recognition**: Learns from project history
3. **Smart Suggestions**: Context-aware message generation
4. **Quality Enforcement**: Ensures conventional compliance
5. **Adaptive Learning**: Improves based on usage patterns