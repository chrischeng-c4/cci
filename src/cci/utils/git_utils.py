"""Git utility functions for CCI."""

from pathlib import Path

from git import InvalidGitRepositoryError, Repo


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


def get_git_root(path: Path) -> Path | None:
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


def get_current_branch(path: Path) -> str | None:
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


def get_remote_url(path: Path, remote_name: str = "origin") -> str | None:
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


def get_commit_hash(path: Path, short: bool = True) -> str | None:
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
            if repo.working_dir and item.a_path:
                modified.append(Path(repo.working_dir) / item.a_path)

        # Get unstaged files
        for item in repo.index.diff(None):
            if repo.working_dir and item.a_path:
                file_path = Path(repo.working_dir) / item.a_path
                if file_path not in modified:
                    modified.append(file_path)

        # Get untracked files
        if repo.working_dir:
            for filename in repo.untracked_files:
                modified.append(Path(repo.working_dir) / filename)

        return modified
    except InvalidGitRepositoryError:
        return []


def get_git_status(path: Path) -> dict[str, list[str]]:
    """Get detailed git status information.

    Args:
        path: Path inside the repository

    Returns:
        Dictionary with status categories as keys and file lists as values
    """
    return get_git_status_detailed(path)


def get_git_status_string(path: Path) -> str | None:
    """Get git status output as string.

    Args:
        path: Path inside the repository

    Returns:
        Git status output or None if not in a repo
    """
    try:
        repo = Repo(path, search_parent_directories=True)
        status: str = repo.git.status("--short")
        return status
    except InvalidGitRepositoryError:
        return None


def get_git_status_detailed(path: Path) -> dict[str, list[str]]:
    """Get detailed git status information.

    Args:
        path: Path inside the repository

    Returns:
        Dictionary with status categories as keys and file lists as values
    """
    try:
        repo = Repo(path, search_parent_directories=True)
        status: dict[str, list[str]] = {
            "staged": [],
            "modified": [],
            "untracked": [],
            "deleted": [],
        }

        # Use git status porcelain format which is more reliable
        status_output = repo.git.status("--porcelain")

        for line in status_output.splitlines():
            if not line:
                continue

            # Parse git status porcelain format
            # First character is index status, second is working tree status
            index_status = line[0] if len(line) > 0 else ' '
            worktree_status = line[1] if len(line) > 1 else ' '
            filename = line[3:] if len(line) > 3 else ''

            # Handle staged changes (index status)
            if index_status in ['A', 'M', 'D', 'R', 'C']:
                if index_status == 'D':
                    status["deleted"].append(filename)
                else:
                    status["staged"].append(filename)

            # Handle unstaged changes (working tree status)
            if worktree_status in ['M', 'D']:
                if worktree_status == 'D':
                    if filename not in status["deleted"]:
                        status["deleted"].append(filename)
                else:
                    status["modified"].append(filename)

            # Handle untracked files
            if index_status == '?' and worktree_status == '?':
                status["untracked"].append(filename)

        return status
    except InvalidGitRepositoryError:
        return {"staged": [], "modified": [], "untracked": [], "deleted": []}


def init_git_repo(path: Path, initial_branch: str = "main") -> bool:
    """Initialize a new git repository.

    Args:
        path: Path where to initialize the repository
        initial_branch: Name of the initial branch

    Returns:
        True if initialization was successful
    """
    try:
        Repo.init(path, initial_branch=initial_branch)
        return True
    except Exception:
        return False
