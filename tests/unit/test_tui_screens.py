"""Unit tests for TUI screens."""

from unittest.mock import patch

import pytest
from textual.app import App
from textual.widgets import Button, DirectoryTree, Label, TextArea

from cci.tui.app import CCIApp
from cci.tui.screens.directory_browser import DirectoryBrowserScreen
from cci.tui.screens.file_viewer import FileViewerScreen
from cci.tui.screens.welcome import WelcomeScreen


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
            from cci import __version__
            assert pilot.app.title == f"CCI - Claude Code IDE v{__version__}"
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

        app = CCIApp(file_path=test_file)

        async with app.run_test() as pilot:
            # Check that TextArea contains the file content
            text_area = pilot.app.screen.query_one(TextArea)
            assert text_area.text == test_content

            # Check file info label exists
            file_info = pilot.app.screen.query_one("#file-info", Label)
            assert file_info is not None

    @pytest.mark.asyncio
    async def test_file_viewer_save_functionality(self, tmp_path):
        """Test file viewer can save changes."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("original content")

        app = CCIApp(file_path=test_file)

        async with app.run_test() as pilot:
            # Get the screen and text area
            screen = pilot.app.screen
            assert isinstance(screen, FileViewerScreen)
            text_area = screen.query_one(TextArea)

            # Verify initial content
            assert text_area.text == "original content"

            # Modify the content properly by replacing the text area contents
            # This should trigger the change handlers
            text_area.replace("modified content", (0, 0), (text_area.document.line_count, 0))

            # Wait a moment for the change event to propagate
            await pilot.pause(0.1)

            # Verify the screen is marked as modified
            assert screen.modified is True

            # Trigger save action
            await pilot.press("ctrl+s")

            # Wait for save to complete
            await pilot.pause(0.1)

            # Verify file was saved
            assert test_file.read_text() == "modified content"

    @pytest.mark.asyncio
    async def test_file_viewer_read_only_mode(self, tmp_path):
        """Test file viewer read-only mode."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        # Start with read-only mode enabled
        app = CCIApp(file_path=test_file)

        async with app.run_test() as pilot:
            # Get the screen and text area
            screen = pilot.app.screen
            assert isinstance(screen, FileViewerScreen)
            text_area = screen.query_one(TextArea)

            # Initially should be in edit mode (read_only=False by default)
            assert text_area.read_only is False

            # Toggle read-only mode
            await pilot.press("ctrl+r")
            assert text_area.read_only is True

            # Toggle back to edit mode
            await pilot.press("ctrl+r")
            assert text_area.read_only is False

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

        app = CCIApp(file_path=nonexistent_file)

        async with app.run_test() as pilot:
            # Get the screen and text area
            screen = pilot.app.screen
            assert isinstance(screen, FileViewerScreen)
            text_area = screen.query_one(TextArea)

            # Should create empty TextArea for new file
            assert text_area.text == ""

            # Should be able to save new content by properly replacing text
            text_area.replace("new content", (0, 0), (text_area.document.line_count, 0))

            # Wait for the change event to propagate
            await pilot.pause(0.1)

            # Verify the screen is marked as modified
            assert screen.modified is True

            # Trigger save action
            await pilot.press("ctrl+s")

            # Wait for save to complete
            await pilot.pause(0.1)

            assert nonexistent_file.exists()
            assert nonexistent_file.read_text() == "new content"

    @pytest.mark.asyncio
    async def test_file_viewer_button_interactions(self, tmp_path):
        """Test file viewer button interactions."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        app = CCIApp(file_path=test_file)

        async with app.run_test() as pilot:
            # Click save button
            save_btn = pilot.app.screen.query_one("#save-btn", Button)
            await pilot.click(save_btn)

            # Click readonly toggle button
            readonly_btn = pilot.app.screen.query_one("#readonly-btn", Button)
            await pilot.click(readonly_btn)

            text_area = pilot.app.screen.query_one(TextArea)
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

        app = CCIApp(directory_path=tmp_path)

        async with app.run_test() as pilot:
            # Wait for the app to mount and push the DirectoryBrowserScreen
            await pilot.pause()

            # Check that DirectoryTree is present
            tree = pilot.app.screen.query_one(DirectoryTree)
            assert tree is not None
            assert str(tmp_path) in str(tree.path)

            # Check header shows directory path
            header = pilot.app.screen.query_one("#browser-header", Label)
            assert header is not None

    @pytest.mark.asyncio
    async def test_directory_browser_file_selection(self, tmp_path):
        """Test selecting a file in directory browser."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        # Use CCIApp which properly initializes the DirectoryBrowserScreen
        app = CCIApp(directory_path=tmp_path)

        async with app.run_test() as pilot:
            # Wait for screen to mount
            await pilot.pause()

            # Get the current screen (should be DirectoryBrowserScreen)
            screen = pilot.app.screen
            assert isinstance(screen, DirectoryBrowserScreen)

            # Verify the DirectoryTree exists
            tree = screen.query_one(DirectoryTree)
            assert tree is not None

            # Mock the app's push_screen method to verify file selection behavior
            with patch.object(pilot.app, 'push_screen') as mock_push:
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

        # Use CCIApp to properly initialize the screen
        app = CCIApp(directory_path=subdir)

        async with app.run_test() as pilot:
            # Wait for screen to mount
            await pilot.pause()

            # Get the current screen
            screen = pilot.app.screen
            assert isinstance(screen, DirectoryBrowserScreen)

            # Test go to parent action
            with patch.object(pilot.app, 'push_screen') as mock_push:
                await pilot.press("backspace")

                # Should push new browser for parent directory
                mock_push.assert_called_once()
                pushed_screen = mock_push.call_args[0][0]
                assert isinstance(pushed_screen, DirectoryBrowserScreen)
                assert pushed_screen.directory_path == tmp_path

    @pytest.mark.asyncio
    async def test_directory_browser_refresh(self, tmp_path):
        """Test directory browser refresh functionality."""
        # Use CCIApp to properly initialize the screen
        app = CCIApp(directory_path=tmp_path)

        async with app.run_test() as pilot:
            await pilot.pause()

            # Get the screen and verify it has a directory tree
            screen = pilot.app.screen
            assert isinstance(screen, DirectoryBrowserScreen)
            tree = screen.query_one(DirectoryTree)

            with patch.object(tree, 'reload') as mock_reload:
                await pilot.press("f5")
                mock_reload.assert_called_once()

    @pytest.mark.asyncio
    async def test_directory_browser_toggle_hidden(self, tmp_path):
        """Test toggling hidden files in directory browser."""
        # Create a hidden file
        (tmp_path / ".hidden").write_text("hidden content")

        # Use CCIApp to properly initialize the screen
        app = CCIApp(directory_path=tmp_path)

        async with app.run_test() as pilot:
            await pilot.pause()

            # Get the screen and verify its initial state
            screen = pilot.app.screen
            assert isinstance(screen, DirectoryBrowserScreen)
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
        # Use CCIApp to properly initialize the screen
        app = CCIApp(directory_path=tmp_path)

        async with app.run_test() as pilot:
            await pilot.pause()

            # Get the screen and its widgets
            screen = pilot.app.screen
            assert isinstance(screen, DirectoryBrowserScreen)

            # Test refresh button
            refresh_btn = screen.query_one("#refresh-btn", Button)
            tree = screen.query_one(DirectoryTree)

            with patch.object(tree, 'reload') as mock_reload:
                await pilot.click(refresh_btn)
                mock_reload.assert_called_once()

            # Test hidden toggle button
            hidden_btn = screen.query_one("#hidden-btn", Button)
            initial_state = screen.show_hidden
            await pilot.click(hidden_btn)
            assert screen.show_hidden != initial_state


class TestWelcomeScreen:
    """Test the welcome screen."""

    @pytest.mark.asyncio
    async def test_welcome_screen_display(self):
        """Test welcome screen displays correctly."""
        # Use CCIApp to properly show the welcome screen
        app = CCIApp()  # No path provided should show welcome screen

        async with app.run_test() as pilot:
            await pilot.pause()

            # Verify we're on the welcome screen
            screen = pilot.app.screen
            assert isinstance(screen, WelcomeScreen)

            # Simply verify that the welcome screen has composed properly
            # We can check for basic structural elements

            # Should have at least one Label (for various text elements)
            labels = screen.query("Label")
            assert len(labels) > 0, "Welcome screen should have Label widgets"

            # Should have at least one Static (for logo or empty state)
            statics = screen.query("Static")
            assert len(statics) > 0, "Welcome screen should have Static widgets"

            # Should have buttons for actions
            buttons = screen.query("Button")
            assert len(buttons) >= 3, (
                f"Welcome screen should have at least 3 buttons, found {len(buttons)}"
            )

    @pytest.mark.asyncio
    async def test_welcome_screen_actions(self):
        """Test welcome screen button actions."""
        # Use CCIApp to properly show the welcome screen
        app = CCIApp()  # No path provided should show welcome screen

        async with app.run_test() as pilot:
            await pilot.pause()

            # Verify we're on the welcome screen
            screen = pilot.app.screen
            assert isinstance(screen, WelcomeScreen)

            # Test that action buttons are present
            buttons = screen.query(Button)
            assert len(buttons) > 0

            # Test a specific button (new-btn should exist)
            new_btn = screen.query_one("#new-btn", Button)
            assert new_btn is not None


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

        async with app.run_test():
            # Should handle the error gracefully
            # Check for error notification or fallback content
            pass  # Specific assertion depends on error handling implementation

        # Restore permissions for cleanup
        protected_file.chmod(0o644)
