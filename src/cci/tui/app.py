"""Main TUI application for CCI."""

from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding

from cci import __version__
from cci.tui.screens.welcome import WelcomeScreen


class CCIApp(App):
    """Main CCI TUI Application."""

    CSS = """
    Screen {
        background: $surface;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("?", "help", "Help"),
    ]

    def __init__(
        self,
        file_path: Optional[Path] = None,
        directory_path: Optional[Path] = None,
        project_path: Optional[Path] = None,  # Keep for backward compatibility
    ):
        """Initialize the CCI application.

        Args:
            file_path: Path to a specific file to open
            directory_path: Path to a directory to browse
            project_path: Path to open a specific project (deprecated, use directory_path)
        """
        super().__init__()
        self.file_path = file_path
        self.directory_path = directory_path or project_path
        self.title = f"CCI - Claude Code IDE v{__version__}"

        # Update subtitle based on what we're opening
        if self.file_path:
            self.sub_title = f"Editing: {self.file_path.name}"
        elif self.directory_path:
            self.sub_title = f"Browsing: {self.directory_path.name}"
        else:
            self.sub_title = "Universal File & Directory Tool"

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        if self.file_path:
            # TODO: Open file editor/viewer screen
            self.push_screen(WelcomeScreen())  # Placeholder for now
        elif self.directory_path:
            # TODO: Open directory browser screen
            self.push_screen(WelcomeScreen())  # Placeholder for now
        else:
            # Show welcome screen with recent files/directories
            self.push_screen(WelcomeScreen())

    def action_help(self) -> None:
        """Show help screen."""
        # TODO: Implement help screen
        pass