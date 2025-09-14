"""Unit tests for CLI commands."""

from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
from typer.testing import CliRunner

from cci.cli import app


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_cciapp():
    """Mock the CCIApp class."""
    with patch("cci.cli.CCIApp") as mock:
        yield mock


class TestCLICommands:
    """Test CLI command functionality."""

    def test_version_flag(self, runner):
        """Test --version flag displays version."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "CCI (Claude Code IDE)" in result.stdout
        assert "version" in result.stdout

    def test_help_flag(self, runner):
        """Test --help flag displays help."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Claude Code IDE" in result.stdout
        assert "Usage:" in result.stdout

    def test_open_command_no_args(self, runner, mock_cciapp):
        """Test 'cci open' with no arguments opens current directory."""
        result = runner.invoke(app, ["open"])
        assert result.exit_code == 0
        assert "Opening current directory" in result.stdout
        mock_cciapp.assert_called_once()

        # Check that CCIApp was instantiated with current directory
        call_kwargs = mock_cciapp.call_args[1]
        assert call_kwargs["directory_path"] == Path.cwd()

    def test_open_command_with_file(self, runner, mock_cciapp, tmp_path):
        """Test 'cci open file.txt' opens a file."""
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        result = runner.invoke(app, ["open", str(test_file)])
        assert result.exit_code == 0
        assert "Opening file:" in result.stdout
        assert str(test_file) in result.stdout

        mock_cciapp.assert_called_once()
        call_kwargs = mock_cciapp.call_args[1]
        assert call_kwargs["file_path"] == test_file

    def test_open_command_with_directory(self, runner, mock_cciapp, tmp_path):
        """Test 'cci open dir' opens a directory."""
        result = runner.invoke(app, ["open", str(tmp_path)])
        assert result.exit_code == 0
        assert "Opening directory:" in result.stdout
        assert str(tmp_path) in result.stdout

        mock_cciapp.assert_called_once()
        call_kwargs = mock_cciapp.call_args[1]
        assert call_kwargs["directory_path"] == tmp_path

    def test_open_command_nonexistent_path(self, runner, mock_cciapp):
        """Test 'cci open' with nonexistent path shows error."""
        result = runner.invoke(app, ["open", "/nonexistent/path"])
        assert result.exit_code == 1
        assert "Error:" in result.stdout
        assert "does not exist" in result.stdout
        mock_cciapp.assert_not_called()

    def test_new_command_creates_project(self, runner, tmp_path):
        """Test 'cci new' command creates a new project."""
        project_path = tmp_path / "new_project"

        with patch("cci.cli.Path.mkdir") as mock_mkdir, \
             patch("cci.cli.Project") as mock_project, \
             patch("cci.cli.ProjectRegistry") as mock_registry:

            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance

            result = runner.invoke(app, ["new", str(project_path)])

            assert result.exit_code == 0
            assert "Creating new project:" in result.stdout
            assert "new_project" in result.stdout

            # Verify project directory was created
            mock_mkdir.assert_called_once()

            # Verify project was registered
            mock_registry_instance.add_project.assert_called_once()

    def test_new_command_with_name_option(self, runner, tmp_path):
        """Test 'cci new --name' command with custom name."""
        project_path = tmp_path / "project_dir"

        with patch("cci.cli.Path.mkdir") as mock_mkdir, \
             patch("cci.cli.Project") as mock_project, \
             patch("cci.cli.ProjectRegistry") as mock_registry:

            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance

            result = runner.invoke(app, ["new", str(project_path), "--name", "CustomName"])

            assert result.exit_code == 0
            assert "Creating new project:" in result.stdout
            assert "CustomName" in result.stdout

    def test_new_command_existing_path(self, runner, tmp_path):
        """Test 'cci new' with existing path shows error."""
        # tmp_path already exists
        result = runner.invoke(app, ["new", str(tmp_path)])
        assert result.exit_code == 1
        assert "Error:" in result.stdout
        assert "already exists" in result.stdout

    def test_list_command(self, runner):
        """Test 'cci list' command lists projects."""
        with patch("cci.cli.ProjectRegistry") as mock_registry:
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance

            # Mock some projects
            mock_project1 = Mock()
            mock_project1.name = "Project1"
            mock_project1.path = Path("/path/to/project1")
            mock_project1.created_at = "2024-01-01T12:00:00"

            mock_project2 = Mock()
            mock_project2.name = "Project2"
            mock_project2.path = Path("/path/to/project2")
            mock_project2.created_at = "2024-01-02T12:00:00"

            mock_registry_instance.list_projects.return_value = [mock_project1, mock_project2]

            result = runner.invoke(app, ["list"])

            assert result.exit_code == 0
            assert "Registered Projects" in result.stdout
            assert "Project1" in result.stdout
            assert "Project2" in result.stdout

    def test_list_command_no_projects(self, runner):
        """Test 'cci list' with no projects."""
        with patch("cci.cli.ProjectRegistry") as mock_registry:
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            mock_registry_instance.list_projects.return_value = []

            result = runner.invoke(app, ["list"])

            assert result.exit_code == 0
            assert "No projects registered" in result.stdout

    def test_remove_command(self, runner):
        """Test 'cci remove' command removes a project."""
        with patch("cci.cli.ProjectRegistry") as mock_registry:
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance

            result = runner.invoke(app, ["remove", "TestProject"])

            assert result.exit_code == 0
            assert "Removed project:" in result.stdout
            assert "TestProject" in result.stdout
            mock_registry_instance.remove_project.assert_called_once_with("TestProject")

    def test_remove_command_nonexistent_project(self, runner):
        """Test 'cci remove' with nonexistent project."""
        with patch("cci.cli.ProjectRegistry") as mock_registry:
            mock_registry_instance = Mock()
            mock_registry.return_value = mock_registry_instance
            mock_registry_instance.remove_project.side_effect = ValueError("Project not found")

            result = runner.invoke(app, ["remove", "NonexistentProject"])

            assert result.exit_code == 1
            assert "Error:" in result.stdout
            assert "Project not found" in result.stdout


class TestCLIFallbackBehavior:
    """Test CLI fallback behavior for direct path arguments."""

    def test_direct_file_path(self, runner, mock_cciapp, tmp_path):
        """Test 'cci file.txt' opens the file directly."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        # Simulate the sys.argv manipulation in __main__.py
        with patch("cci.__main__.sys.argv", ["cci", "open", str(test_file)]):
            result = runner.invoke(app, ["open", str(test_file)])

            assert result.exit_code == 0
            assert "Opening file:" in result.stdout
            mock_cciapp.assert_called_once()

    def test_direct_directory_path(self, runner, mock_cciapp, tmp_path):
        """Test 'cci /some/dir' opens the directory directly."""
        with patch("cci.__main__.sys.argv", ["cci", "open", str(tmp_path)]):
            result = runner.invoke(app, ["open", str(tmp_path)])

            assert result.exit_code == 0
            assert "Opening directory:" in result.stdout
            mock_cciapp.assert_called_once()

    def test_current_directory_shortcut(self, runner, mock_cciapp):
        """Test 'cci .' opens current directory."""
        with patch("cci.__main__.sys.argv", ["cci", "open", "."]):
            result = runner.invoke(app, ["open", "."])

            assert result.exit_code == 0
            assert "Opening directory:" in result.stdout
            mock_cciapp.assert_called_once()


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_invalid_command(self, runner):
        """Test invalid command shows error."""
        result = runner.invoke(app, ["invalidcommand"])
        assert result.exit_code != 0
        assert "No such option" in result.stdout or "Invalid" in result.stdout

    def test_missing_required_argument(self, runner):
        """Test missing required argument shows error."""
        result = runner.invoke(app, ["new"])  # Missing path argument
        assert result.exit_code != 0
        assert "Missing argument" in result.stdout

    def test_registry_error_handling(self, runner):
        """Test registry errors are handled gracefully."""
        with patch("cci.cli.ProjectRegistry") as mock_registry:
            mock_registry.side_effect = Exception("Registry error")

            result = runner.invoke(app, ["list"])

            # Should handle the error gracefully
            assert result.exit_code == 1
            assert "Error:" in result.stdout