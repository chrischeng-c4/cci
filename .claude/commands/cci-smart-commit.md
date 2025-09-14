# /cci-smart-commit

Intelligently analyze git changes and generate meaningful commit messages following conventional commit standards.

## Description

This Claude command analyzes your staged git changes and suggests appropriate commit messages based on:
- Type of changes (feat, fix, docs, refactor, test, etc.)
- Files modified
- Code context
- Conventional commit standards

## Usage

```
/cci-smart-commit
```

## Command Implementation

When this command is invoked, Claude will:

1. **Check Git Repository**
   - Verify the current directory is a git repository
   - Check for staged changes using `git diff --cached`

2. **Analyze Changes**
   - Run `git status` to see staged/unstaged files
   - Run `git diff --cached` to examine staged changes
   - Count additions and deletions
   - Identify change patterns

3. **Determine Commit Type**
   - `feat`: New feature or functionality
   - `fix`: Bug fixes or corrections
   - `docs`: Documentation changes
   - `style`: Code style/formatting (no logic changes)
   - `refactor`: Code restructuring without behavior change
   - `perf`: Performance improvements
   - `test`: Test additions or modifications
   - `build`: Build system or dependency changes
   - `ci`: CI/CD configuration changes
   - `chore`: Maintenance tasks

4. **Generate Message**
   - Format: `<type>(<scope>): <subject>`
   - Keep subject line under 50 characters
   - Use imperative mood ("add" not "added")
   - Don't capitalize first letter after type
   - No period at end

5. **Provide Options**
   - Suggest primary commit message
   - Offer alternatives if changes are complex
   - Allow custom message if needed

## Examples

### Example 1: Feature Addition
```bash
# Changes: Added new Calculator class in src/calc.py
Suggested: feat(calc): add Calculator class with basic operations
```

### Example 2: Bug Fix
```bash
# Changes: Fixed divide by zero in src/math/division.py
Suggested: fix(math): handle divide by zero exception
```

### Example 3: Documentation
```bash
# Changes: Updated README.md with installation instructions
Suggested: docs: add installation guide to README
```

### Example 4: Multiple Changes
```bash
# Changes: Multiple files across features
Suggested commits (split recommended):
1. feat(auth): implement JWT authentication
2. test(auth): add authentication unit tests
3. docs(api): update API documentation for auth endpoints
```

## Claude Implementation

When you invoke `/cci-smart-commit`, Claude will:

1. **Execute Git Commands** to analyze your repository:
   ```bash
   git status                    # Check current state
   git diff --cached --name-status  # List staged files
   git diff --cached             # Examine actual changes
   git diff --cached --numstat   # Count line changes
   ```

2. **Intelligent Analysis** using AI capabilities:
   - Parse code changes to understand intent
   - Detect patterns (new features, bug fixes, refactoring)
   - Identify affected components/modules
   - Recognize framework-specific changes

3. **Generate Contextual Messages**:
   - Primary suggestion based on deep analysis
   - Alternative messages for different perspectives
   - Scope detection from file paths
   - Breaking change detection

4. **Provide Interactive Feedback**:
   - Show staged files with visual indicators
   - Display line change statistics
   - Offer multiple commit message options
   - Explain the reasoning behind suggestions

## Advanced Features

### Context-Aware Analysis
- Detect programming language from file extensions
- Identify common patterns (CRUD operations, API endpoints, etc.)
- Recognize framework-specific changes

### Multi-Commit Suggestions
When changes span multiple concerns:
```
🔀 Multiple commits recommended:
1. Backend changes:
   feat(api): add user authentication endpoint

2. Frontend changes:
   feat(ui): implement login form component

3. Documentation:
   docs(api): document authentication flow
```

### Integration with AI
Future enhancement to use Claude for deeper analysis:
- Understand semantic meaning of code changes
- Generate more descriptive commit messages
- Suggest breaking changes or impacts

## Configuration

Create `.claude/commit-config.toml`:
```toml
[commit]
# Preferred commit types for the project
types = ["feat", "fix", "docs", "test", "refactor", "chore"]

# Scopes specific to your project
scopes = ["cli", "tui", "core", "api", "docs"]

# Maximum subject line length
max_subject_length = 50

# Require scope
require_scope = false

# Emoji prefix mapping
[commit.emoji]
feat = "✨"
fix = "🐛"
docs = "📚"
style = "💎"
refactor = "♻️"
perf = "⚡"
test = "🧪"
build = "📦"
ci = "👷"
chore = "🔧"
```

## Benefits

1. **Consistency**: Ensures all commits follow the same format
2. **Clarity**: Makes git history readable and searchable
3. **Automation**: Enables automatic changelog generation
4. **Integration**: Works with semantic versioning tools
5. **Team Alignment**: Reduces cognitive load on commit messages

## See Also

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project)