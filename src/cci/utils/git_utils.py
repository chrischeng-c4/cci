"""Git utility functions for CCI."""

from pathlib import Path
from typing import Optional

from git import Repo, InvalidGitRepositoryError


def is_git_repo(path: Path) -> bool:
    """Check if a path is inside a git repository.

    Args:
        path: Path to check

    Returns:
        True if path is in a git repo, False otherwise
    """
    try:
        Repo(path, search_parent_directories=True)
        return True
    except InvalidGitRepositoryError:
        return False


def get_git_root(path: Path) -> Optional[Path]:
    """Get the root directory of the git repository.

    Args:
        path: Path inside the repository

    Returns:
        Path to git root or None if not in a repo
    """
    try:
        repo = Repo(path, search_parent_directories=True)
        return Path(repo.working_dir)
    except InvalidGitRepositoryError:
        return None


def get_current_branch(path: Path) -> Optional[str]:
    """Get the current git branch name.

    Args:
        path: Path inside the repository

    Returns:
        Branch name or None if not in a repo or detached HEAD
    """
    try:
        repo = Repo(path, search_parent_directories=True)
        if repo.head.is_detached:
            return None
        return repo.active_branch.name
    except (InvalidGitRepositoryError, TypeError):
        return None


def has_uncommitted_changes(path: Path) -> bool:
    """Check if the repository has uncommitted changes.

    Args:
        path: Path inside the repository

    Returns:
        True if there are uncommitted changes, False otherwise
    """
    try:
        repo = Repo(path, search_parent_directories=True)
        return repo.is_dirty(untracked_files=True)
    except InvalidGitRepositoryError:
        return False


def get_remote_url(path: Path, remote_name: str = "origin") -> Optional[str]:
    """Get the URL of a git remote.

    Args:
        path: Path inside the repository
        remote_name: Name of the remote (default: "origin")

    Returns:
        Remote URL or None if not found
    """
    try:
        repo = Repo(path, search_parent_directories=True)
        if remote_name in repo.remotes:
            remote = repo.remotes[remote_name]
            return remote.url
        return None
    except InvalidGitRepositoryError:
        return None


def get_commit_hash(path: Path, short: bool = True) -> Optional[str]:
    """Get the current commit hash.

    Args:
        path: Path inside the repository
        short: If True, return short hash (7 chars)

    Returns:
        Commit hash or None if not in a repo
    """
    try:
        repo = Repo(path, search_parent_directories=True)
        commit = repo.head.commit
        if short:
            return commit.hexsha[:7]
        return commit.hexsha
    except (InvalidGitRepositoryError, ValueError):
        return None


def list_modified_files(path: Path) -> list[Path]:
    """List all modified files in the repository.

    Args:
        path: Path inside the repository

    Returns:
        List of paths to modified files
    """
    try:
        repo = Repo(path, search_parent_directories=True)
        modified = []

        # Get staged files
        for item in repo.index.diff("HEAD"):
            modified.append(Path(repo.working_dir) / item.a_path)

        # Get unstaged files
        for item in repo.index.diff(None):
            file_path = Path(repo.working_dir) / item.a_path
            if file_path not in modified:
                modified.append(file_path)

        # Get untracked files
        for item in repo.untracked_files:
            modified.append(Path(repo.working_dir) / item)

        return modified
    except InvalidGitRepositoryError:
        return []