"""Directory browser screen for CCI."""

from pathlib import Path
from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DirectoryTree, Footer, Header, Label, Static


class DirectoryBrowserScreen(Screen):
    """Screen for browsing directories and files."""

    CSS = """
    DirectoryBrowserScreen {
        background: $surface;
    }

    #browser-header {
        height: 1;
        background: $primary;
        color: $text;
        padding: 0 1;
    }

    #tree-container {
        width: 100%;
        height: 1fr;
        border: solid $primary;
    }

    DirectoryTree {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    #info-panel {
        height: 3;
        background: $panel;
        padding: 0 1;
        border-top: solid $primary;
    }

    #button-bar {
        height: 3;
        background: $panel;
        align: center middle;
    }

    Button {
        margin: 0 1;
    }

    .info-label {
        color: $text-muted;
    }

    .info-value {
        color: $text;
    }
    """

    BINDINGS = [
        Binding("enter", "open_item", "Open", priority=True),
        Binding("backspace", "go_up", "Parent Directory"),
        Binding("f5", "refresh", "Refresh"),
        Binding("h", "toggle_hidden", "Toggle Hidden"),
        Binding("escape", "close", "Close"),
        Binding("q", "quit", "Quit"),
        Binding("?", "show_help", "Help"),
    ]

    def __init__(
        self,
        directory_path: Path,
        show_hidden: bool = False,
        name: Optional[str] = None,
    ) -> None:
        """Initialize the directory browser screen.

        Args:
            directory_path: Path to the directory to browse
            show_hidden: Whether to show hidden files
            name: Optional name for the screen
        """
        super().__init__(name=name)
        self.directory_path = directory_path.resolve()
        self.show_hidden = show_hidden
        self.directory_tree: Optional[DirectoryTree] = None
        self.selected_path: Optional[Path] = None

    def compose(self) -> ComposeResult:
        """Compose the directory browser UI."""
        yield Header()

        with Vertical():
            # Directory info header
            yield Label(
                f"📁 {self.directory_path}",
                id="browser-header"
            )

            # Directory tree container
            with Container(id="tree-container"):
                self.directory_tree = DirectoryTree(
                    self.directory_path,
                    show_root=True,
                    show_guides=True,
                )
                # Set show_hidden after creation
                if hasattr(self.directory_tree, 'show_hidden'):
                    self.directory_tree.show_hidden = self.show_hidden
                yield self.directory_tree

            # Info panel showing selected item details
            with Horizontal(id="info-panel"):
                yield Static(self._get_info_text(), id="info-text")

            # Button bar for actions
            with Horizontal(id="button-bar"):
                yield Button("Open (Enter)", variant="primary", id="open-btn")
                yield Button("Parent (Backspace)", variant="default", id="parent-btn")
                yield Button("Refresh (F5)", variant="default", id="refresh-btn")
                yield Button("Toggle Hidden (H)", variant="default", id="hidden-btn")
                yield Button("Close (Esc)", variant="default", id="close-btn")

        yield Footer()

    def _get_info_text(self) -> str:
        """Get information about the selected item."""
        if not self.selected_path:
            return "Select a file or directory to see details"

        try:
            path = Path(self.selected_path)
            if not path.exists():
                return "Path does not exist"

            if path.is_file():
                size = path.stat().st_size
                size_str = self._format_size(size)
                return f"File: {path.name} | Size: {size_str}"
            elif path.is_dir():
                try:
                    item_count = len(list(path.iterdir()))
                    return f"Directory: {path.name} | Items: {item_count}"
                except PermissionError:
                    return f"Directory: {path.name} | Permission denied"
            else:
                return f"Special: {path.name}"
        except Exception as e:
            return f"Error: {e}"

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.title = "CCI - Directory Browser"
        self.sub_title = str(self.directory_path)

        # Focus the directory tree
        if self.directory_tree:
            self.directory_tree.focus()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection in the directory tree."""
        self.selected_path = Path(event.path)
        self.query_one("#info-text", Static).update(self._get_info_text())

        # Open the file in the file viewer
        from cci.tui.screens.file_viewer import FileViewerScreen
        self.app.push_screen(FileViewerScreen(self.selected_path))

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        """Handle directory selection in the directory tree."""
        self.selected_path = Path(event.path)
        self.query_one("#info-text", Static).update(self._get_info_text())

    @on(Button.Pressed, "#open-btn")
    def on_open_button(self) -> None:
        """Handle open button press."""
        self.action_open_item()

    @on(Button.Pressed, "#parent-btn")
    def on_parent_button(self) -> None:
        """Handle parent directory button press."""
        self.action_go_up()

    @on(Button.Pressed, "#refresh-btn")
    def on_refresh_button(self) -> None:
        """Handle refresh button press."""
        self.action_refresh()

    @on(Button.Pressed, "#hidden-btn")
    def on_hidden_button(self) -> None:
        """Handle toggle hidden button press."""
        self.action_toggle_hidden()

    @on(Button.Pressed, "#close-btn")
    def on_close_button(self) -> None:
        """Handle close button press."""
        self.action_close()

    def action_open_item(self) -> None:
        """Open the selected item."""
        if not self.selected_path:
            self.notify("No item selected", severity="warning")
            return

        path = Path(self.selected_path)
        if path.is_file():
            # Open file in viewer
            from cci.tui.screens.file_viewer import FileViewerScreen
            self.app.push_screen(FileViewerScreen(path))
        elif path.is_dir():
            # Expand/collapse directory in tree
            if self.directory_tree:
                # Find the node and toggle it
                node = self.directory_tree.get_node_by_id(str(path))
                if node:
                    if node.is_expanded:
                        node.collapse()
                    else:
                        node.expand()
        else:
            self.notify(f"Cannot open {path.name}", severity="warning")

    def action_go_up(self) -> None:
        """Navigate to parent directory."""
        parent = self.directory_path.parent
        if parent != self.directory_path:
            # Create a new browser for the parent directory
            self.app.push_screen(DirectoryBrowserScreen(parent, self.show_hidden))
        else:
            self.notify("Already at root directory", severity="information")

    def action_refresh(self) -> None:
        """Refresh the directory tree."""
        if self.directory_tree:
            # Reload the tree
            self.directory_tree.reload()
            self.notify("Directory tree refreshed", severity="information")

    def action_toggle_hidden(self) -> None:
        """Toggle showing hidden files."""
        self.show_hidden = not self.show_hidden

        if self.directory_tree and hasattr(self.directory_tree, 'show_hidden'):
            self.directory_tree.show_hidden = self.show_hidden

        status = "shown" if self.show_hidden else "hidden"
        self.notify(f"Hidden files {status}", severity="information")

        # Refresh to apply the change
        self.action_refresh()

    def action_close(self) -> None:
        """Close the directory browser."""
        self.dismiss()

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_show_help(self) -> None:
        """Show help information."""
        help_text = """
Directory Browser Help:
• Enter: Open file/expand directory
• Backspace: Go to parent directory
• F5: Refresh directory tree
• H: Toggle hidden files
• Arrow keys: Navigate
• Space: Expand/collapse directory
• Esc: Close browser
• Q: Quit application
• ?: Show this help
        """.strip()
        self.notify(help_text, severity="information", timeout=10)