"""File viewer and editor screen for CCI."""

from pathlib import Path
from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, TextArea
from rich.syntax import Syntax
from rich.console import Console
from rich.text import Text


class FileViewerScreen(Screen):
    """Screen for viewing and editing files."""

    CSS = """
    FileViewerScreen {
        background: $surface;
    }

    #file-info {
        height: 1;
        background: $primary;
        color: $text;
        padding: 0 1;
    }

    #editor-container {
        width: 100%;
        height: 1fr;
    }

    TextArea {
        width: 100%;
        height: 100%;
    }

    #status-bar {
        height: 1;
        background: $panel;
        color: $text-muted;
        padding: 0 1;
    }

    #button-bar {
        height: 3;
        background: $panel;
        align: center middle;
    }

    Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+s", "save", "Save", priority=True),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+r", "toggle_readonly", "Toggle Read-only"),
        Binding("escape", "close", "Close"),
        Binding("f1", "show_help", "Help"),
    ]

    def __init__(
        self,
        file_path: Path,
        read_only: bool = False,
        name: Optional[str] = None,
    ) -> None:
        """Initialize the file viewer screen.

        Args:
            file_path: Path to the file to view/edit
            read_only: Whether to open in read-only mode
            name: Optional name for the screen
        """
        super().__init__(name=name)
        self.file_path = file_path.resolve()
        self.read_only = read_only
        self.modified = False
        self.original_content = ""
        self.text_area: Optional[TextArea] = None

    def compose(self) -> ComposeResult:
        """Compose the file viewer UI."""
        yield Header()

        with Vertical():
            # File info bar
            yield Label(
                f"📄 {self.file_path.name} - {self.file_path.parent}",
                id="file-info"
            )

            # Editor container
            with Container(id="editor-container"):
                # Load file content
                content = self._load_file_content()
                self.original_content = content

                # Create text area with content
                self.text_area = TextArea(
                    content,
                    language=self._detect_language(),
                    theme="monokai",
                    show_line_numbers=True,
                    tab_behavior="indent",
                    read_only=self.read_only,
                )
                yield self.text_area

            # Status bar
            yield Label(
                self._get_status_text(),
                id="status-bar"
            )

            # Button bar for actions
            with Horizontal(id="button-bar"):
                yield Button("Save (Ctrl+S)", variant="primary", id="save-btn")
                yield Button("Toggle Read-only (Ctrl+R)", variant="default", id="readonly-btn")
                yield Button("Close (Esc)", variant="default", id="close-btn")

        yield Footer()

    def _load_file_content(self) -> str:
        """Load content from the file."""
        try:
            if self.file_path.exists():
                # Try to read with UTF-8 first, fallback to latin-1
                try:
                    return self.file_path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    return self.file_path.read_text(encoding="latin-1")
            else:
                # New file
                return ""
        except Exception as e:
            self.notify(f"Error loading file: {e}", severity="error")
            return f"# Error loading file\n\n{e}"

    def _detect_language(self) -> str:
        """Detect the programming language based on file extension."""
        ext_to_lang = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "jsx",
            ".tsx": "tsx",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".cs": "csharp",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".r": "r",
            ".R": "r",
            ".sql": "sql",
            ".sh": "bash",
            ".bash": "bash",
            ".zsh": "bash",
            ".fish": "fish",
            ".ps1": "powershell",
            ".yml": "yaml",
            ".yaml": "yaml",
            ".toml": "toml",
            ".json": "json",
            ".xml": "xml",
            ".html": "html",
            ".htm": "html",
            ".css": "css",
            ".scss": "scss",
            ".sass": "sass",
            ".less": "less",
            ".md": "markdown",
            ".markdown": "markdown",
            ".rst": "rst",
            ".tex": "latex",
            ".dockerfile": "dockerfile",
            ".Dockerfile": "dockerfile",
            ".makefile": "makefile",
            ".Makefile": "makefile",
            ".cmake": "cmake",
            ".vim": "vim",
            ".lua": "lua",
            ".pl": "perl",
            ".jl": "julia",
            ".m": "matlab",
            ".dart": "dart",
            ".elm": "elm",
            ".clj": "clojure",
            ".ex": "elixir",
            ".exs": "elixir",
            ".erl": "erlang",
            ".hrl": "erlang",
            ".fs": "fsharp",
            ".fsx": "fsharp",
            ".ml": "ocaml",
            ".mli": "ocaml",
            ".pas": "pascal",
            ".pp": "pascal",
            ".hs": "haskell",
            ".lhs": "haskell",
            ".nim": "nim",
            ".nims": "nim",
            ".zig": "zig",
            ".v": "v",
            ".sv": "systemverilog",
            ".svh": "systemverilog",
            ".vhd": "vhdl",
            ".vhdl": "vhdl",
        }

        suffix = self.file_path.suffix.lower()

        # Special case for files without extension
        if not suffix and self.file_path.name.lower() in ["dockerfile", "makefile", "cmakefile"]:
            return self.file_path.name.lower()

        return ext_to_lang.get(suffix, "text")

    def _get_status_text(self) -> str:
        """Get the status bar text."""
        mode = "Read-only" if self.read_only else "Edit"
        modified_indicator = " • Modified" if self.modified else ""

        if self.text_area:
            cursor = self.text_area.cursor_location
            line = cursor[0] + 1
            col = cursor[1] + 1
            position = f"Line {line}, Col {col}"
        else:
            position = ""

        return f"{mode}{modified_indicator} | {position}"

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.title = f"CCI - {self.file_path.name}"
        self.sub_title = str(self.file_path.parent)

        # Focus the text area
        if self.text_area:
            self.text_area.focus()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle text area content changes."""
        if self.text_area and not self.read_only:
            current_content = self.text_area.text
            self.modified = current_content != self.original_content
            self.query_one("#status-bar", Label).update(self._get_status_text())

    @on(Button.Pressed, "#save-btn")
    def on_save_button(self) -> None:
        """Handle save button press."""
        self.action_save()

    @on(Button.Pressed, "#readonly-btn")
    def on_readonly_button(self) -> None:
        """Handle read-only toggle button press."""
        self.action_toggle_readonly()

    @on(Button.Pressed, "#close-btn")
    def on_close_button(self) -> None:
        """Handle close button press."""
        self.action_close()

    def action_save(self) -> None:
        """Save the file."""
        if self.read_only:
            self.notify("Cannot save in read-only mode", severity="warning")
            return

        if not self.text_area:
            return

        if not self.modified:
            self.notify("No changes to save", severity="information")
            return

        try:
            content = self.text_area.text

            # Create parent directories if they don't exist
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the file
            self.file_path.write_text(content, encoding="utf-8")

            # Update state
            self.original_content = content
            self.modified = False
            self.query_one("#status-bar", Label).update(self._get_status_text())

            self.notify(f"Saved {self.file_path.name}", severity="information")
        except Exception as e:
            self.notify(f"Error saving file: {e}", severity="error")

    def action_toggle_readonly(self) -> None:
        """Toggle read-only mode."""
        self.read_only = not self.read_only

        if self.text_area:
            self.text_area.read_only = self.read_only

        self.query_one("#status-bar", Label).update(self._get_status_text())

        mode = "read-only" if self.read_only else "edit"
        self.notify(f"Switched to {mode} mode", severity="information")

    def action_close(self) -> None:
        """Close the file viewer."""
        if self.modified:
            # TODO: Show confirmation dialog
            self.notify("Unsaved changes! Press Ctrl+S to save or Esc again to force close", severity="warning")
            # For now, just dismiss to go back
            self.dismiss()
        else:
            self.dismiss()

    def action_show_help(self) -> None:
        """Show help information."""
        help_text = """
File Viewer Help:
• Ctrl+S: Save file
• Ctrl+R: Toggle read-only mode
• Ctrl+Q: Quit application
• Esc: Close file viewer
• F1: Show this help
        """.strip()
        self.notify(help_text, severity="information", timeout=10)

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()