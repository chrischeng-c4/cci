# Features Ready for UAT

> This document lists features ready for User Acceptance Testing
> Updated after each feature completion

## 🎯 Currently Ready for Testing

### Project Management with Welcome Page
**Status**: 🟢 Ready for UAT
**Implemented**: 2025-09-13
**Developer**: Claude Code

#### Description
Complete project management system with a welcome page as the main entry point. Users can create, open, list, and remove projects from the registry. The welcome TUI shows recent projects and provides quick actions.

#### How to Test

##### 1. Test CLI Commands
```bash
# Check version
uv run cci --version

# View help
uv run cci --help

# List projects (should be empty initially)
uv run cci list

# Create a new project
uv run cci new ~/test-project --name "Test Project"

# List projects again (should show the new project)
uv run cci list

# Open the welcome TUI
uv run cci open

# Remove a project (doesn't delete files)
uv run cci remove "Test Project"
```

##### 2. Test Welcome TUI
```bash
# Launch the welcome screen
uv run cci

# Or directly via Python
uv run python -m cci
```

#### Test Scenarios

**Happy Path**:
1. Launch CCI without arguments → See welcome screen
2. Create a new project → Project appears in list
3. Open existing project → Project registry updates last opened
4. Remove project → Project removed from registry only

**Edge Cases**:
- Try creating project in existing directory
- Try opening non-existent path
- Try removing non-existent project
- Launch TUI with no projects registered

**Error Cases**:
- Create project without write permissions
- Open path that's a file, not directory
- Remove project with --force flag

#### Expected Behavior
- Welcome screen displays ASCII art logo
- Recent projects sorted by last opened date
- Keyboard shortcuts work (N, O, R, Q)
- Project creation initializes git repo
- Registry persists between sessions
- Clean error messages for invalid operations

#### Known Limitations
- TUI buttons currently just beep (not fully implemented)
- No project search functionality yet
- No project templates yet
- Settings screen not implemented

#### Feedback Needed
- Is the welcome screen intuitive?
- Are the CLI commands clear?
- Is the project list display helpful?
- Any missing essential features for project management?

---

## Testing Instructions Template

When features are ready, they will be listed here with:

### Feature Name
**Status**: 🟢 Ready for UAT
**Implemented**: [Date]
**Developer**: Claude Code

#### Description
Brief description of what the feature does.

#### How to Test
1. Step-by-step instructions
2. Commands to run
3. Expected outcomes

#### Test Scenarios
- **Happy Path**: Normal usage
- **Edge Cases**: Boundary conditions
- **Error Cases**: How it handles failures

#### Test Data
```bash
# Example commands or data
cci test-command
```

#### Expected Behavior
- What you should see
- How it should respond
- Performance expectations

#### Known Limitations
- Any current limitations
- Planned improvements

#### Feedback Needed
- Specific areas to focus on
- Questions for the user

---

## UAT History

### Completed UAT Sessions
_Will be populated as features are tested_

| Date | Feature | Status | Feedback | Action Taken |
|------|---------|--------|----------|--------------|
| - | - | - | - | - |

---

## How to Provide Feedback

1. **Test the feature** following the instructions
2. **Note any issues** or unexpected behavior
3. **Provide feedback** via:
   - Comments in this document
   - Create an issue in docs/ISSUES.md
   - Direct message in our session

## Quick Commands for Testing

```bash
# Check current version
cci --version

# Get help
cci --help

# Run specific test
uv run pytest tests/test_feature.py -v
```

---
*This document is your primary source for UAT-ready features*