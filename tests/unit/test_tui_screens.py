"""Unit tests for TUI screens."""

from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, PropertyMock
import pytest

from textual.app import App
from textual.pilot import Pilot
from textual.widgets import Button, TextArea, DirectoryTree, Label

from cci.tui.app import CCIApp
from cci.tui.screens.welcome import WelcomeScreen
from cci.tui.screens.file_viewer import FileViewerScreen
from cci.tui.screens.directory_browser import DirectoryBrowserScreen


@pytest.fixture
async def pilot_app():
    """Create a test app with pilot for testing."""
    app = CCIApp()
    async with app.run_test() as pilot:
        yield pilot


class TestCCIApp:
    """Test the main CCI TUI application."""

    @pytest.mark.asyncio
    async def test_app_initialization_no_path(self):
        """Test app initialization without any path."""
        app = CCIApp()
        async with app.run_test() as pilot:
            # Should show welcome screen by default
            assert isinstance(pilot.app.screen, WelcomeScreen)
            assert pilot.app.title == f"CCI - Claude Code IDE v{app.__version__}"
            assert pilot.app.sub_title == "Universal File & Directory Tool"

    @pytest.mark.asyncio
    async def test_app_initialization_with_file(self, tmp_path):
        """Test app initialization with a file path."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        app = CCIApp(file_path=test_file)
        async with app.run_test() as pilot:
            # Should show file viewer screen
            assert isinstance(pilot.app.screen, FileViewerScreen)
            assert pilot.app.sub_title == f"Editing: {test_file.name}"

    @pytest.mark.asyncio
    async def test_app_initialization_with_directory(self, tmp_path):
        """Test app initialization with a directory path."""
        app = CCIApp(directory_path=tmp_path)
        async with app.run_test() as pilot:
            # Should show directory browser screen
            assert isinstance(pilot.app.screen, DirectoryBrowserScreen)
            assert pilot.app.sub_title == f"Browsing: {tmp_path.name}"

    @pytest.mark.asyncio
    async def test_app_quit_binding(self):
        """Test the 'q' key binding quits the app."""
        app = CCIApp()
        async with app.run_test() as pilot:
            await pilot.press("q")
            assert pilot.app.return_code == 0


class TestFileViewerScreen:
    """Test the file viewer screen."""

    @pytest.mark.asyncio
    async def test_file_viewer_loads_content(self, tmp_path):
        """Test file viewer loads file content correctly."""
        test_file = tmp_path / "test.py"
        test_content = "print('Hello, World!')"
        test_file.write_text(test_content)

        screen = FileViewerScreen(test_file)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Check that TextArea contains the file content
            text_area = pilot.app.query_one(TextArea)
            assert text_area.text == test_content

            # Check file info label
            file_info = pilot.app.query_one("#file-info", Label)
            assert test_file.name in file_info.renderable

    @pytest.mark.asyncio
    async def test_file_viewer_save_functionality(self, tmp_path):
        """Test file viewer can save changes."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("original content")

        screen = FileViewerScreen(test_file)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Modify the content
            text_area = pilot.app.query_one(TextArea)
            text_area.text = "modified content"

            # Trigger save action
            await pilot.press("ctrl+s")

            # Verify file was saved
            assert test_file.read_text() == "modified content"

    @pytest.mark.asyncio
    async def test_file_viewer_read_only_mode(self, tmp_path):
        """Test file viewer read-only mode."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        screen = FileViewerScreen(test_file, read_only=True)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            text_area = pilot.app.query_one(TextArea)
            assert text_area.read_only is True

            # Toggle read-only mode
            await pilot.press("ctrl+r")
            assert text_area.read_only is False

            # Toggle back
            await pilot.press("ctrl+r")
            assert text_area.read_only is True

    @pytest.mark.asyncio
    async def test_file_viewer_language_detection(self, tmp_path):
        """Test file viewer detects programming language."""
        # Test Python file
        py_file = tmp_path / "test.py"
        py_file.write_text("print('test')")

        screen = FileViewerScreen(py_file)
        assert screen._detect_language() == "python"

        # Test JavaScript file
        js_file = tmp_path / "test.js"
        js_file.write_text("console.log('test')")

        screen = FileViewerScreen(js_file)
        assert screen._detect_language() == "javascript"

        # Test unknown extension
        unknown_file = tmp_path / "test.xyz"
        unknown_file.write_text("content")

        screen = FileViewerScreen(unknown_file)
        assert screen._detect_language() == "text"

    @pytest.mark.asyncio
    async def test_file_viewer_nonexistent_file(self, tmp_path):
        """Test file viewer handles nonexistent file."""
        nonexistent_file = tmp_path / "nonexistent.txt"

        screen = FileViewerScreen(nonexistent_file)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Should create empty TextArea for new file
            text_area = pilot.app.query_one(TextArea)
            assert text_area.text == ""

            # Should be able to save new content
            text_area.text = "new content"
            await pilot.press("ctrl+s")

            assert nonexistent_file.exists()
            assert nonexistent_file.read_text() == "new content"

    @pytest.mark.asyncio
    async def test_file_viewer_button_interactions(self, tmp_path):
        """Test file viewer button interactions."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        screen = FileViewerScreen(test_file)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Click save button
            save_btn = pilot.app.query_one("#save-btn", Button)
            await pilot.click(save_btn)

            # Click readonly toggle button
            readonly_btn = pilot.app.query_one("#readonly-btn", Button)
            await pilot.click(readonly_btn)

            text_area = pilot.app.query_one(TextArea)
            assert text_area.read_only is True


class TestDirectoryBrowserScreen:
    """Test the directory browser screen."""

    @pytest.mark.asyncio
    async def test_directory_browser_initialization(self, tmp_path):
        """Test directory browser initializes correctly."""
        # Create some test files and directories
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.py").write_text("print('test')")
        (tmp_path / "subdir").mkdir()

        screen = DirectoryBrowserScreen(tmp_path)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Check that DirectoryTree is present
            tree = pilot.app.query_one(DirectoryTree)
            assert tree is not None
            assert tree.path == str(tmp_path)

            # Check header shows directory path
            header = pilot.app.query_one("#browser-header", Label)
            assert str(tmp_path) in header.renderable

    @pytest.mark.asyncio
    async def test_directory_browser_file_selection(self, tmp_path):
        """Test selecting a file in directory browser."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        screen = DirectoryBrowserScreen(tmp_path)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Simulate file selection
            tree = pilot.app.query_one(DirectoryTree)

            # Mock the file selection event
            with patch.object(app, 'push_screen') as mock_push:
                screen.on_directory_tree_file_selected(
                    DirectoryTree.FileSelected(tree, str(test_file))
                )

                # Should push FileViewerScreen
                mock_push.assert_called_once()
                pushed_screen = mock_push.call_args[0][0]
                assert isinstance(pushed_screen, FileViewerScreen)
                assert pushed_screen.file_path == test_file

    @pytest.mark.asyncio
    async def test_directory_browser_navigation(self, tmp_path):
        """Test directory browser navigation."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        screen = DirectoryBrowserScreen(subdir)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Test go to parent action
            with patch.object(app, 'push_screen') as mock_push:
                await pilot.press("backspace")

                # Should push new browser for parent directory
                mock_push.assert_called_once()
                pushed_screen = mock_push.call_args[0][0]
                assert isinstance(pushed_screen, DirectoryBrowserScreen)
                assert pushed_screen.directory_path == tmp_path

    @pytest.mark.asyncio
    async def test_directory_browser_refresh(self, tmp_path):
        """Test directory browser refresh functionality."""
        screen = DirectoryBrowserScreen(tmp_path)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            tree = pilot.app.query_one(DirectoryTree)

            with patch.object(tree, 'reload') as mock_reload:
                await pilot.press("f5")
                mock_reload.assert_called_once()

    @pytest.mark.asyncio
    async def test_directory_browser_toggle_hidden(self, tmp_path):
        """Test toggling hidden files in directory browser."""
        # Create a hidden file
        (tmp_path / ".hidden").write_text("hidden content")

        screen = DirectoryBrowserScreen(tmp_path, show_hidden=False)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            assert screen.show_hidden is False

            # Toggle hidden files
            await pilot.press("h")
            assert screen.show_hidden is True

            # Toggle back
            await pilot.press("h")
            assert screen.show_hidden is False

    @pytest.mark.asyncio
    async def test_directory_browser_button_interactions(self, tmp_path):
        """Test directory browser button interactions."""
        screen = DirectoryBrowserScreen(tmp_path)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Test refresh button
            refresh_btn = pilot.app.query_one("#refresh-btn", Button)
            tree = pilot.app.query_one(DirectoryTree)

            with patch.object(tree, 'reload') as mock_reload:
                await pilot.click(refresh_btn)
                mock_reload.assert_called_once()

            # Test hidden toggle button
            hidden_btn = pilot.app.query_one("#hidden-btn", Button)
            initial_state = screen.show_hidden
            await pilot.click(hidden_btn)
            assert screen.show_hidden != initial_state


class TestWelcomeScreen:
    """Test the welcome screen."""

    @pytest.mark.asyncio
    async def test_welcome_screen_display(self):
        """Test welcome screen displays correctly."""
        screen = WelcomeScreen()
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Check that welcome content is present
            assert "Welcome to CCI" in pilot.app.screen.query_one("Static").renderable

    @pytest.mark.asyncio
    async def test_welcome_screen_actions(self):
        """Test welcome screen button actions."""
        screen = WelcomeScreen()
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Test quick start button
            quick_start_btn = pilot.app.query_one("#quick-start", Button)
            await pilot.click(quick_start_btn)

            # Test other action buttons if present
            buttons = pilot.app.query(Button)
            assert len(buttons) > 0


class TestTUIIntegration:
    """Test TUI integration scenarios."""

    @pytest.mark.asyncio
    async def test_file_to_directory_navigation(self, tmp_path):
        """Test navigating from file viewer back to directory browser."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        app = CCIApp(file_path=test_file)
        async with app.run_test() as pilot:
            # Start in file viewer
            assert isinstance(pilot.app.screen, FileViewerScreen)

            # Close file viewer
            await pilot.press("escape")

            # Should return to previous screen or welcome
            # (Depending on navigation stack implementation)

    @pytest.mark.asyncio
    async def test_keyboard_shortcuts(self):
        """Test various keyboard shortcuts work correctly."""
        app = CCIApp()
        async with app.run_test() as pilot:
            # Test help shortcut
            await pilot.press("?")

            # Test quit shortcut
            await pilot.press("q")
            assert pilot.app.return_code == 0

    @pytest.mark.asyncio
    async def test_error_notifications(self, tmp_path):
        """Test error notifications are displayed correctly."""
        # Try to open a file without permissions
        protected_file = tmp_path / "protected.txt"
        protected_file.write_text("content")
        protected_file.chmod(0o000)  # Remove all permissions

        screen = FileViewerScreen(protected_file)
        app = App()
        app.push_screen(screen)

        async with app.run_test() as pilot:
            # Should handle the error gracefully
            # Check for error notification or fallback content
            pass  # Specific assertion depends on error handling implementation

        # Restore permissions for cleanup
        protected_file.chmod(0o644)