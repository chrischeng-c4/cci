"""Git worktree management functionality for CCI."""

import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

from git import Repo, GitCommandError
from pydantic import BaseModel, Field, validator


class WorktreeStatus(Enum):
    """Status of a git worktree."""
    ACTIVE = "active"
    LOCKED = "locked"
    PRUNABLE = "prunable"
    DETACHED = "detached"


@dataclass
class WorktreeInfo:
    """Information about a git worktree."""
    path: Path
    branch: Optional[str]
    commit: str
    status: WorktreeStatus
    is_bare: bool = False
    is_main: bool = False


class GitWorktree:
    """Manages git worktrees for a repository."""

    def __init__(self, repo_path: Path):
        """Initialize worktree manager for a repository.

        Args:
            repo_path: Path to the git repository (main worktree)
        """
        self.repo_path = repo_path.resolve()

        try:
            self.repo = Repo(self.repo_path)
        except Exception as e:
            raise ValueError(f"Invalid git repository: {repo_path}") from e

        if self.repo.bare:
            raise ValueError("Cannot manage worktrees for a bare repository")

        # Find the actual git directory (could be .git or the worktree base)
        self.git_dir = Path(self.repo.git_dir)
        self.common_dir = self._get_common_dir()

    def _get_common_dir(self) -> Path:
        """Get the common git directory for all worktrees."""
        # Check if this is already a worktree
        commondir_file = self.git_dir / "commondir"
        if commondir_file.exists():
            common_path = commondir_file.read_text().strip()
            return (self.git_dir / common_path).resolve()
        return self.git_dir

    def create_worktree(
        self,
        path: Path,
        branch: Optional[str] = None,
        new_branch: Optional[str] = None,
        force: bool = False,
        checkout: bool = True,
    ) -> WorktreeInfo:
        """Create a new git worktree.

        Args:
            path: Path where the worktree will be created
            branch: Existing branch to checkout in the worktree
            new_branch: Create and checkout a new branch
            force: Force creation even if path exists
            checkout: Whether to checkout files after creating

        Returns:
            WorktreeInfo object with details about the created worktree
        """
        path = path.resolve()

        # Check if path already exists
        if path.exists() and not force:
            raise ValueError(f"Path already exists: {path}")

        # Build the git worktree add command
        cmd = ["add"]

        if force:
            cmd.append("--force")

        if not checkout:
            cmd.append("--no-checkout")

        if new_branch:
            cmd.extend(["-b", new_branch])
            cmd.append(str(path))
        elif branch:
            cmd.append(str(path))
            cmd.append(branch)
        else:
            # Create with detached HEAD at current commit
            cmd.append(str(path))

        try:
            self.repo.git.worktree(*cmd)
        except GitCommandError as e:
            raise RuntimeError(f"Failed to create worktree: {e}") from e

        # Get info about the created worktree
        return self._get_worktree_info(path)

    def list_worktrees(self, include_main: bool = True) -> List[WorktreeInfo]:
        """List all worktrees for the repository.

        Args:
            include_main: Whether to include the main worktree in the list

        Returns:
            List of WorktreeInfo objects
        """
        try:
            # Use porcelain format for stable parsing
            output = self.repo.git.worktree("list", "--porcelain")
        except GitCommandError as e:
            raise RuntimeError(f"Failed to list worktrees: {e}") from e

        worktrees = []
        current_worktree = {}

        for line in output.strip().split("\n"):
            if not line:
                # Empty line marks end of a worktree entry
                if current_worktree:
                    info = self._parse_worktree_entry(current_worktree)
                    if include_main or not info.is_main:
                        worktrees.append(info)
                    current_worktree = {}
            else:
                # Parse the line
                if " " in line:
                    key, value = line.split(" ", 1)
                else:
                    key, value = line, ""
                current_worktree[key] = value

        # Don't forget the last entry
        if current_worktree:
            info = self._parse_worktree_entry(current_worktree)
            if include_main or not info.is_main:
                worktrees.append(info)

        return worktrees

    def _parse_worktree_entry(self, entry: Dict[str, str]) -> WorktreeInfo:
        """Parse a worktree entry from git worktree list --porcelain output."""
        path = Path(entry.get("worktree", ""))
        branch = entry.get("branch", "").replace("refs/heads/", "") if "branch" in entry else None
        commit = entry.get("HEAD", "")

        # Determine status
        status = WorktreeStatus.ACTIVE
        if "locked" in entry:
            status = WorktreeStatus.LOCKED
        elif "prunable" in entry:
            status = WorktreeStatus.PRUNABLE
        elif "detached" in entry:
            status = WorktreeStatus.DETACHED

        # Check if this is the main worktree
        is_main = path == self.repo_path

        return WorktreeInfo(
            path=path,
            branch=branch,
            commit=commit,
            status=status,
            is_bare="bare" in entry,
            is_main=is_main,
        )

    def get_worktree(self, identifier: str) -> Optional[WorktreeInfo]:
        """Get information about a specific worktree.

        Args:
            identifier: Path or branch name of the worktree

        Returns:
            WorktreeInfo object or None if not found
        """
        worktrees = self.list_worktrees()

        # Try to match by path first
        identifier_path = Path(identifier).resolve()
        for wt in worktrees:
            if wt.path == identifier_path:
                return wt

        # Try to match by branch name
        for wt in worktrees:
            if wt.branch == identifier:
                return wt

        return None

    def _get_worktree_info(self, path: Path) -> WorktreeInfo:
        """Get information about a worktree at a specific path."""
        worktrees = self.list_worktrees()
        for wt in worktrees:
            if wt.path == path:
                return wt
        raise ValueError(f"Worktree not found at path: {path}")

    def remove_worktree(self, identifier: str, force: bool = False) -> bool:
        """Remove a git worktree.

        Args:
            identifier: Path or branch name of the worktree to remove
            force: Force removal even if there are uncommitted changes

        Returns:
            True if removal was successful
        """
        worktree = self.get_worktree(identifier)
        if not worktree:
            raise ValueError(f"Worktree not found: {identifier}")

        if worktree.is_main:
            raise ValueError("Cannot remove the main worktree")

        cmd = ["remove"]
        if force:
            cmd.append("--force")
        cmd.append(str(worktree.path))

        try:
            self.repo.git.worktree(*cmd)
            return True
        except GitCommandError as e:
            raise RuntimeError(f"Failed to remove worktree: {e}") from e

    def switch_worktree(self, identifier: str) -> Path:
        """Switch to a different worktree by changing directory.

        Note: This method returns the path to switch to. The actual
        directory change must be handled by the calling code.

        Args:
            identifier: Path or branch name of the worktree

        Returns:
            Path to the worktree directory
        """
        worktree = self.get_worktree(identifier)
        if not worktree:
            raise ValueError(f"Worktree not found: {identifier}")

        if not worktree.path.exists():
            raise ValueError(f"Worktree path does not exist: {worktree.path}")

        return worktree.path

    def prune_worktrees(self, dry_run: bool = False) -> List[Path]:
        """Prune worktrees that no longer exist on disk.

        Args:
            dry_run: If True, only show what would be pruned

        Returns:
            List of paths that were (or would be) pruned
        """
        cmd = ["prune"]
        if dry_run:
            cmd.append("--dry-run")

        try:
            output = self.repo.git.worktree(*cmd, verbose=True)
        except GitCommandError as e:
            raise RuntimeError(f"Failed to prune worktrees: {e}") from e

        # Parse the output to find pruned paths
        pruned = []
        for line in output.strip().split("\n"):
            if "Removing worktree" in line or "would remove" in line:
                # Extract path from the message
                parts = line.split('"')
                if len(parts) >= 2:
                    pruned.append(Path(parts[1]))

        return pruned

    def lock_worktree(self, identifier: str, reason: Optional[str] = None) -> bool:
        """Lock a worktree to prevent automatic pruning.

        Args:
            identifier: Path or branch name of the worktree
            reason: Optional reason for locking

        Returns:
            True if locking was successful
        """
        worktree = self.get_worktree(identifier)
        if not worktree:
            raise ValueError(f"Worktree not found: {identifier}")

        cmd = ["lock"]
        if reason:
            cmd.extend(["--reason", reason])
        cmd.append(str(worktree.path))

        try:
            self.repo.git.worktree(*cmd)
            return True
        except GitCommandError as e:
            raise RuntimeError(f"Failed to lock worktree: {e}") from e

    def unlock_worktree(self, identifier: str) -> bool:
        """Unlock a previously locked worktree.

        Args:
            identifier: Path or branch name of the worktree

        Returns:
            True if unlocking was successful
        """
        worktree = self.get_worktree(identifier)
        if not worktree:
            raise ValueError(f"Worktree not found: {identifier}")

        try:
            self.repo.git.worktree("unlock", str(worktree.path))
            return True
        except GitCommandError as e:
            raise RuntimeError(f"Failed to unlock worktree: {e}") from e

    def repair_worktree(self, identifier: Optional[str] = None) -> bool:
        """Repair worktree administrative files if they've been moved.

        Args:
            identifier: Path or branch name of the worktree to repair.
                       If None, repairs all worktrees.

        Returns:
            True if repair was successful
        """
        cmd = ["repair"]

        if identifier:
            worktree = self.get_worktree(identifier)
            if not worktree:
                raise ValueError(f"Worktree not found: {identifier}")
            cmd.append(str(worktree.path))

        try:
            self.repo.git.worktree(*cmd)
            return True
        except GitCommandError as e:
            raise RuntimeError(f"Failed to repair worktree: {e}") from e


class WorktreeConfig(BaseModel):
    """Configuration for worktree management."""

    base_path: Path = Field(
        default=Path(".cci/worktrees"),
        description="Base path for creating worktrees"
    )
    auto_prune: bool = Field(
        default=True,
        description="Automatically prune stale worktrees"
    )
    default_branch_prefix: str = Field(
        default="cci/",
        description="Default prefix for worktree branches"
    )
    max_worktrees: int = Field(
        default=10,
        description="Maximum number of worktrees allowed"
    )

    @validator("base_path")
    def validate_base_path(cls, v: Path) -> Path:
        """Ensure base_path is not absolute unless it starts with home."""
        if v.is_absolute() and not str(v).startswith(str(Path.home())):
            raise ValueError("base_path must be relative or under home directory")
        return v

    class Config:
        """Pydantic config."""
        use_enum_values = True