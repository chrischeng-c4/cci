# Quick Start

Get up and running with CCI in 5 minutes!

## Launch CCI

The simplest way to start:

```bash
uv run cci
```

This opens the welcome screen where you can manage all your projects.

## Your First Project

### 1. Create a New Project

```bash
uv run cci new ~/my-awesome-project --name "My Awesome Project"
```

This will:
- Create the project directory
- Initialize a git repository
- Register the project in CCI
- Create project configuration

### 2. View Your Projects

```bash
uv run cci list
```

Output:
```
📁 My Awesome Project
   Path: /Users/you/my-awesome-project
   Last opened: 2025-09-13 14:30
```

### 3. Open the Project

```bash
uv run cci open ~/my-awesome-project
```

Or just launch CCI and select from the welcome screen:

```bash
uv run cci
```

## Welcome Screen Navigation

When you launch CCI without arguments, you'll see:

```
┌────────────────────────────────────┐
│  ██████╗ ██████╗██╗                │
│ ██╔════╝██╔════╝██║   Claude Code  │
│ ██║     ██║     ██║   IDE v0.1.0   │
│ ╚██████╗╚██████╗██║                │
├────────────────────────────────────┤
│  Recent Projects                    │
│  ─────────────────                  │
│  📁 My Awesome Project              │
│     ~/my-awesome-project            │
│     Last opened: 2 minutes ago      │
│                                     │
│  [N]ew  [O]pen  [Q]uit  [?]Help    │
└────────────────────────────────────┘
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `N` | Create new project |
| `O` | Open existing project |
| `R` | Remove selected project |
| `Enter` | Open selected project |
| `↑/↓` | Navigate projects |
| `Q` | Quit |
| `?` | Show help |

## Project Configuration

Each project has a `.cci/config.toml` file:

```toml
[project]
name = "My Awesome Project"
description = "A great project"
worktree_path = ".cci/worktrees"

[prompt]
max_context_files = 20
include_patterns = ["*.py", "*.md"]
exclude_patterns = ["__pycache__", "*.pyc"]

[workflow]
auto_commit = false
require_tests = true
require_review = true
```

## Coming Soon: AI Workflows

Soon you'll be able to:

```bash
# Generate code from prompts
cci prompt "Add user authentication"

# Review generated patches
cci patch review

# Apply approved changes
cci patch apply
```

## Tips

1. **Use Tab Completion**: CCI supports shell completion for commands
2. **Rich Output**: All commands use rich formatting for beautiful output
3. **Project Registry**: Projects are stored in `~/.config/cci/projects.toml`
4. **Git Integration**: CCI works best with git repositories

## Next Steps

- Learn about [Project Management](../user-guide/projects.md)
- Understand [Configuration](configuration.md)
- Explore the [User Guide](../user-guide/overview.md)

## Getting Help

```bash
# Command help
uv run cci --help
uv run cci new --help

# In TUI
Press ? for help
```