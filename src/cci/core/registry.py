"""Project registry management."""

from datetime import datetime
from pathlib import Path
from typing import Any

from cci.models.project import Project
from cci.utils import get_remote_url, load_config, save_config


class ProjectRegistry:
    """Manages the registry of projects."""

    def __init__(self, config_dir: Path | None = None):
        """Initialize the project registry.

        Args:
            config_dir: Directory for CCI configuration. Defaults to ~/.config/cci
        """
        if config_dir is None:
            config_dir = Path.home() / ".config" / "cci"

        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.config_dir / "projects.toml"

        # Create registry file if it doesn't exist
        if not self.registry_file.exists():
            self._save_registry({"projects": {}})

    def _load_registry(self) -> dict[str, Any]:
        """Load the registry from disk."""
        try:
            return load_config(self.registry_file)
        except Exception:
            return {"projects": {}}

    def _save_registry(self, data: dict[str, Any]) -> None:
        """Save the registry to disk."""
        save_config(self.registry_file, data)

    def add_project(self, name: str, path: Path) -> Project:
        """Add a new project to the registry.

        Args:
            name: Project name
            path: Path to project directory

        Returns:
            The created Project instance
        """
        path = path.resolve()
        project = Project(
            name=name,
            path=path,
            last_opened=datetime.now(),
            created_at=datetime.now(),
            git_remote=get_remote_url(path),
            description=None,
        )

        registry = self._load_registry()
        project_data = {
            "path": str(project.path),
            "last_opened": project.last_opened.isoformat(),
            "created_at": project.created_at.isoformat(),
            "worktree_count": project.worktree_count,
        }

        # Only add optional fields if they have values
        if project.git_remote is not None:
            project_data["git_remote"] = project.git_remote
        if project.description is not None:
            project_data["description"] = project.description

        registry["projects"][name] = project_data
        self._save_registry(registry)

        return project

    def get_project(self, name: str) -> Project | None:
        """Get a project by name.

        Args:
            name: Project name

        Returns:
            Project instance or None if not found
        """
        registry = self._load_registry()
        if name not in registry["projects"]:
            return None

        data = registry["projects"][name]
        return Project(
            name=name,
            path=Path(data["path"]),
            last_opened=datetime.fromisoformat(data["last_opened"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            worktree_count=data.get("worktree_count", 0),
            git_remote=data.get("git_remote"),
            description=data.get("description"),
        )

    def list_projects(self) -> list[Project]:
        """List all registered projects.

        Returns:
            List of Project instances, sorted by last opened date
        """
        registry = self._load_registry()
        projects = []

        for name, data in registry["projects"].items():
            projects.append(
                Project(
                    name=name,
                    path=Path(data["path"]),
                    last_opened=datetime.fromisoformat(data["last_opened"]),
                    created_at=datetime.fromisoformat(data["created_at"]),
                    worktree_count=data.get("worktree_count", 0),
                    git_remote=data.get("git_remote"),
                    description=data.get("description"),
                )
            )

        # Sort by last opened, most recent first
        projects.sort(key=lambda p: p.last_opened, reverse=True)
        return projects

    def update_project(self, project: Project) -> None:
        """Update a project in the registry.

        Args:
            project: Project instance to update
        """
        registry = self._load_registry()
        if project.name in registry["projects"]:
            project_data = {
                "path": str(project.path),
                "last_opened": project.last_opened.isoformat(),
                "created_at": project.created_at.isoformat(),
                "worktree_count": project.worktree_count,
            }

            # Only add optional fields if they have values
            if project.git_remote is not None:
                project_data["git_remote"] = project.git_remote
            if project.description is not None:
                project_data["description"] = project.description

            registry["projects"][project.name] = project_data
            self._save_registry(registry)

    def remove_project(self, name: str) -> bool:
        """Remove a project from the registry.

        Args:
            name: Project name

        Returns:
            True if removed, False if not found
        """
        registry = self._load_registry()
        if name in registry["projects"]:
            del registry["projects"][name]
            self._save_registry(registry)
            return True
        return False

    def update_last_opened(self, name: str) -> None:
        """Update the last opened timestamp for a project.

        Args:
            name: Project name
        """
        project = self.get_project(name)
        if project:
            project.update_last_opened()
            self.update_project(project)
