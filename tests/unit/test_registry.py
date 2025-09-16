"""Tests for project registry."""

from datetime import datetime

from cci.core.registry import ProjectRegistry
from cci.models.project import Project


class TestProjectRegistry:
    """Test the project registry."""

    def test_create_registry(self, temp_config_dir):
        """Test creating a new registry."""
        registry = ProjectRegistry(config_dir=temp_config_dir)
        assert registry.config_dir == temp_config_dir
        assert registry.registry_file == temp_config_dir / "projects.toml"
        assert registry.registry_file.exists()

    def test_add_project(self, test_registry, temp_dir):
        """Test adding a project to the registry."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()

        project = test_registry.add_project("test_project", project_path)

        assert project.name == "test_project"
        assert project.path == project_path.resolve()
        assert isinstance(project.last_opened, datetime)
        assert isinstance(project.created_at, datetime)

    def test_add_git_project(self, test_registry, sample_project_dir):
        """Test adding a git project to the registry."""
        project = test_registry.add_project("git_project", sample_project_dir)

        assert project.name == "git_project"
        assert project.path == sample_project_dir.resolve()
        # Note: git_remote will be None unless origin is configured

    def test_get_project(self, test_registry, temp_dir):
        """Test retrieving a project from the registry."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()

        # Add project
        added_project = test_registry.add_project("test_project", project_path)

        # Retrieve project
        retrieved_project = test_registry.get_project("test_project")

        assert retrieved_project is not None
        assert retrieved_project.name == added_project.name
        assert retrieved_project.path == added_project.path
        assert retrieved_project.last_opened == added_project.last_opened

    def test_get_nonexistent_project(self, test_registry):
        """Test retrieving a non-existent project."""
        project = test_registry.get_project("nonexistent")
        assert project is None

    def test_list_projects_empty(self, test_registry):
        """Test listing projects when registry is empty."""
        projects = test_registry.list_projects()
        assert projects == []

    def test_list_projects(self, test_registry, temp_dir):
        """Test listing multiple projects."""
        # Add multiple projects
        for i in range(3):
            project_path = temp_dir / f"project_{i}"
            project_path.mkdir()
            test_registry.add_project(f"project_{i}", project_path)

        projects = test_registry.list_projects()

        assert len(projects) == 3
        assert all(isinstance(p, Project) for p in projects)
        assert [p.name for p in projects] == ["project_2", "project_1", "project_0"]
        # Should be sorted by last_opened (most recent first)

    def test_update_project(self, test_registry, temp_dir):
        """Test updating a project in the registry."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()

        # Add project
        project = test_registry.add_project("test_project", project_path)

        # Update project
        project.description = "Updated description"
        project.worktree_count = 5
        test_registry.update_project(project)

        # Retrieve and verify
        updated_project = test_registry.get_project("test_project")
        assert updated_project.description == "Updated description"
        assert updated_project.worktree_count == 5

    def test_remove_project(self, test_registry, temp_dir):
        """Test removing a project from the registry."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()

        # Add project
        test_registry.add_project("test_project", project_path)

        # Remove project
        result = test_registry.remove_project("test_project")
        assert result is True

        # Verify it's gone
        project = test_registry.get_project("test_project")
        assert project is None

    def test_remove_nonexistent_project(self, test_registry):
        """Test removing a non-existent project."""
        result = test_registry.remove_project("nonexistent")
        assert result is False

    def test_update_last_opened(self, test_registry, temp_dir):
        """Test updating the last opened timestamp."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()

        # Add project
        test_registry.add_project("test_project", project_path)
        original_project = test_registry.get_project("test_project")
        original_time = original_project.last_opened

        # Small delay to ensure time difference
        import time
        time.sleep(0.01)

        # Update last opened
        test_registry.update_last_opened("test_project")

        # Verify
        updated_project = test_registry.get_project("test_project")
        assert updated_project.last_opened > original_time

    def test_registry_persistence(self, temp_config_dir, temp_dir):
        """Test that registry persists across instances."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()

        # Create first registry and add project
        registry1 = ProjectRegistry(config_dir=temp_config_dir)
        registry1.add_project("test_project", project_path)

        # Create second registry and verify project exists
        registry2 = ProjectRegistry(config_dir=temp_config_dir)
        project = registry2.get_project("test_project")

        assert project is not None
        assert project.name == "test_project"
        assert project.path == project_path.resolve()
