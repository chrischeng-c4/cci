"""Welcome screen for CCI."""


from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, ListItem, ListView, Static

from cci import __version__
from cci.core.registry import ProjectRegistry


class ProjectListItem(ListItem):
    """Custom list item for projects."""

    def __init__(self, name: str, path: str, last_opened: str, worktrees: int):
        """Initialize a project list item."""
        super().__init__()
        self.project_name = name
        self.project_path = path
        self.last_opened = last_opened
        self.worktrees = worktrees

    def compose(self) -> ComposeResult:
        """Compose the project item."""
        with Vertical():
            yield Label(f"📁 {self.project_name}", classes="project-name")
            yield Label(f"   {self.project_path}", classes="project-path")
            yield Label(
                f"   Last opened: {self.last_opened} | {self.worktrees} worktrees",
                classes="project-meta",
            )


class WelcomeScreen(Screen[None]):
    """Welcome screen showing project list and options."""

    CSS = """
    WelcomeScreen {
        align: center middle;
    }

    .welcome-container {
        width: 80;
        height: 40;
        border: solid $primary;
        background: $panel;
    }

    .logo {
        text-align: center;
        padding: 1;
        color: $primary;
        text-style: bold;
    }

    .tagline {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    .section-title {
        text-style: bold;
        color: $primary;
        margin: 1 0;
    }

    .project-list {
        height: 15;
        margin: 1;
        border: solid $border;
        background: $background;
    }

    .project-name {
        color: $success;
        text-style: bold;
    }

    .project-path {
        color: $text;
    }

    .project-meta {
        color: $text-muted;
    }

    .actions {
        margin: 1;
        align: center middle;
    }

    .action-button {
        margin: 0 1;
    }

    .empty-state {
        text-align: center;
        color: $text-muted;
        margin: 3;
    }

    .shortcuts {
        margin: 1;
        color: $text-muted;
    }
    """

    BINDINGS = [
        Binding("n", "new_project", "New Project"),
        Binding("o", "open_project", "Open Project"),
        Binding("r", "remove_project", "Remove Project"),
        Binding("enter", "select_project", "Open Selected"),
        Binding("s", "settings", "Settings"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the welcome screen."""
        yield Header()

        with Container(classes="welcome-container"):
            # Logo and tagline
            yield Static(self._get_logo(), classes="logo")
            yield Label(f"Universal File & Directory Tool - v{__version__}", classes="tagline")

            # Recent items section
            yield Label("Recent Items", classes="section-title")

            # Try to load projects from registry (if it exists)
            try:
                registry = ProjectRegistry()
                projects = registry.list_projects()

                if projects:
                    items = []
                    for project in projects[:5]:  # Show only 5 most recent
                        item = ProjectListItem(
                            name=project.name,
                            path=str(project.path),
                            last_opened=project.last_opened.strftime("%Y-%m-%d %H:%M"),
                            worktrees=project.worktree_count,
                        )
                        items.append(item)
                    yield ListView(*items, classes="project-list", id="project-list")
                else:
                    yield Static(
                        (
                            "Welcome to CCI!\n\nUse CCI to open any file or directory:\n"
                            "  cci file.txt\n  cci ~/Documents\n  cci ."
                        ),
                        classes="empty-state",
                    )
            except Exception:
                # Registry doesn't exist or can't be loaded - that's fine
                yield Static(
                    (
                        "Welcome to CCI!\n\nUse CCI to open any file or directory:\n"
                        "  cci file.txt\n  cci ~/Documents\n  cci ."
                    ),
                    classes="empty-state",
                )

            # Quick actions
            yield Label("Quick Actions", classes="section-title")
            with Horizontal(classes="actions"):
                yield Button("New [N]", variant="primary", id="new-btn", classes="action-button")
                yield Button("Open [O]", variant="default", id="open-btn", classes="action-button")
                yield Button(
                    "Settings [S]", variant="default", id="settings-btn", classes="action-button"
                )

            # Keyboard shortcuts
            yield Static(
                "[Enter] Open selected | [N] New | [O] Open | [R] Remove | [S] Settings | [Q] Quit",
                classes="shortcuts",
            )

        yield Footer()

    def _get_logo(self) -> str:
        """Get the ASCII art logo."""
        return """
 ██████╗ ██████╗██╗
██╔════╝██╔════╝██║
██║     ██║     ██║   Claude Code IDE
██║     ██║     ██║
╚██████╗╚██████╗██║
 ╚═════╝ ╚═════╝╚═╝
"""

    def action_new_project(self) -> None:
        """Create a new project."""
        # TODO: Show new project dialog
        self.app.bell()

    def action_open_project(self) -> None:
        """Open an existing project."""
        # TODO: Show file picker dialog
        self.app.bell()

    def action_remove_project(self) -> None:
        """Remove selected project from registry."""
        # TODO: Get selected project and confirm removal
        self.app.bell()

    def action_select_project(self) -> None:
        """Open the selected project."""
        list_view = self.query_one("#project-list", ListView)
        if list_view.highlighted_child:
            # TODO: Open the selected project
            self.app.bell()

    def action_settings(self) -> None:
        """Open settings screen."""
        # TODO: Show settings screen
        self.app.bell()

    @on(Button.Pressed, "#new-btn")
    def on_new_button(self) -> None:
        """Handle new button press."""
        self.action_new_project()

    @on(Button.Pressed, "#open-btn")
    def on_open_button(self) -> None:
        """Handle open button press."""
        self.action_open_project()

    @on(Button.Pressed, "#settings-btn")
    def on_settings_button(self) -> None:
        """Handle settings button press."""
        self.action_settings()
