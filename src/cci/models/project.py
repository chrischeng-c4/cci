"""Project data models."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Project(BaseModel):
    """Represents a project in CCI."""

    name: str = Field(..., description="Project name")
    path: Path = Field(..., description="Absolute path to project directory")
    last_opened: datetime = Field(default_factory=datetime.now, description="Last opened timestamp")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    worktree_count: int = Field(default=0, description="Number of active worktrees")
    git_remote: Optional[str] = Field(None, description="Primary git remote URL")
    description: Optional[str] = Field(None, description="Project description")

    @field_validator("path")
    @classmethod
    def validate_path(cls, v: Path) -> Path:
        """Ensure path is absolute."""
        return v.resolve()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name is not empty."""
        if not v.strip():
            raise ValueError("Project name cannot be empty")
        return v.strip()

    def update_last_opened(self) -> None:
        """Update the last opened timestamp."""
        self.last_opened = datetime.now()

    def is_git_repo(self) -> bool:
        """Check if the project is a git repository."""
        git_dir = self.path / ".git"
        return git_dir.exists()

    model_config = {
        "json_encoders": {
            Path: str,
            datetime: lambda v: v.isoformat(),
        }
    }


class ProjectConfig(BaseModel):
    """Project-specific configuration."""

    name: str = Field(..., description="Project name")
    description: str = Field("", description="Project description")
    worktree_path: str = Field(".cci/worktrees", description="Path for worktrees")

    class PromptConfig(BaseModel):
        """Prompt processing configuration."""

        max_context_files: int = Field(20, description="Maximum files to include in context")
        include_patterns: list[str] = Field(
            default_factory=lambda: ["*.py", "*.md"],
            description="File patterns to include",
        )
        exclude_patterns: list[str] = Field(
            default_factory=lambda: ["__pycache__", "*.pyc"],
            description="File patterns to exclude",
        )

    class WorkflowConfig(BaseModel):
        """Workflow configuration."""

        auto_commit: bool = Field(False, description="Automatically commit changes")
        require_tests: bool = Field(True, description="Require tests for patches")
        require_review: bool = Field(True, description="Require review before applying")

    prompt: PromptConfig = Field(default_factory=PromptConfig)
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)