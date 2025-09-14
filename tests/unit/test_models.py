"""Tests for data models."""

from datetime import datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from cci.models.project import Project, ProjectConfig


class TestProjectModel:
    """Test the Project model."""

    def test_create_project_minimal(self, temp_dir):
        """Test creating a project with minimal fields."""
        project = Project(
            name="test_project",
            path=temp_dir / "test",
        )
        assert project.name == "test_project"
        assert project.path == (temp_dir / "test").resolve()
        assert project.worktree_count == 0
        assert project.git_remote is None
        assert project.description is None
        assert isinstance(project.last_opened, datetime)
        assert isinstance(project.created_at, datetime)

    def test_create_project_full(self, temp_dir):
        """Test creating a project with all fields."""
        now = datetime.now()
        project = Project(
            name="test_project",
            path=temp_dir / "test",
            last_opened=now,
            created_at=now,
            worktree_count=3,
            git_remote="https://github.com/user/repo.git",
            description="Test project description",
        )
        assert project.name == "test_project"
        assert project.path == (temp_dir / "test").resolve()
        assert project.worktree_count == 3
        assert project.git_remote == "https://github.com/user/repo.git"
        assert project.description == "Test project description"
        assert project.last_opened == now
        assert project.created_at == now

    def test_project_path_validation(self):
        """Test that project path is resolved to absolute."""
        project = Project(
            name="test",
            path=Path("./relative/path"),
        )
        assert project.path.is_absolute()

    def test_project_name_validation(self):
        """Test project name validation."""
        # Empty name should fail
        with pytest.raises(ValidationError):
            Project(name="", path=Path("/tmp/test"))

        # Whitespace-only name should fail
        with pytest.raises(ValidationError):
            Project(name="   ", path=Path("/tmp/test"))

        # Name with whitespace should be stripped
        project = Project(name="  test  ", path=Path("/tmp/test"))
        assert project.name == "test"

    def test_update_last_opened(self, temp_dir):
        """Test updating the last opened timestamp."""
        project = Project(
            name="test",
            path=temp_dir,
        )
        original_time = project.last_opened

        # Small delay to ensure time difference
        import time
        time.sleep(0.01)

        project.update_last_opened()
        assert project.last_opened > original_time

    def test_is_git_repo(self, temp_dir):
        """Test git repository detection."""
        project = Project(name="test", path=temp_dir)

        # Should not be a git repo initially
        assert not project.is_git_repo()

        # Create .git directory
        (temp_dir / ".git").mkdir()
        assert project.is_git_repo()


class TestProjectConfig:
    """Test the ProjectConfig model."""

    def test_create_config_minimal(self):
        """Test creating config with minimal fields."""
        config = ProjectConfig(name="test_project")
        assert config.name == "test_project"
        assert config.description == ""
        assert config.worktree_path == ".cci/worktrees"

    def test_create_config_full(self):
        """Test creating config with all fields."""
        config = ProjectConfig(
            name="test_project",
            description="A test project",
            worktree_path="custom/worktrees",
        )
        assert config.name == "test_project"
        assert config.description == "A test project"
        assert config.worktree_path == "custom/worktrees"

    def test_prompt_config_defaults(self):
        """Test prompt configuration defaults."""
        config = ProjectConfig(name="test")
        assert config.prompt.max_context_files == 20
        assert config.prompt.include_patterns == ["*.py", "*.md"]
        assert config.prompt.exclude_patterns == ["__pycache__", "*.pyc"]

    def test_workflow_config_defaults(self):
        """Test workflow configuration defaults."""
        config = ProjectConfig(name="test")
        assert config.workflow.auto_commit is False
        assert config.workflow.require_tests is True
        assert config.workflow.require_review is True

    def test_custom_prompt_config(self):
        """Test custom prompt configuration."""
        config = ProjectConfig(
            name="test",
            prompt=ProjectConfig.PromptConfig(
                max_context_files=50,
                include_patterns=["*.rs", "*.toml"],
                exclude_patterns=["target", "*.lock"],
            ),
        )
        assert config.prompt.max_context_files == 50
        assert config.prompt.include_patterns == ["*.rs", "*.toml"]
        assert config.prompt.exclude_patterns == ["target", "*.lock"]