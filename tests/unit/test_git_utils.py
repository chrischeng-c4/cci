"""Tests for git utility functions."""

from unittest.mock import MagicMock, patch

from git import InvalidGitRepositoryError, Repo

from cci.utils.git_utils import (
    get_commit_hash,
    get_current_branch,
    get_git_root,
    get_git_status,
    get_remote_url,
    has_uncommitted_changes,
    init_git_repo,
    is_git_repo,
    list_modified_files,
)


class TestIsGitRepo:
    """Tests for is_git_repo function."""

    def test_valid_git_repo(self, tmp_path):
        """Test detecting a valid git repository."""
        Repo.init(tmp_path)

        result = is_git_repo(tmp_path)
        assert result is True

    def test_invalid_git_repo(self, tmp_path):
        """Test detecting an invalid git repository."""
        result = is_git_repo(tmp_path)
        assert result is False

    @patch('cci.utils.git_utils.Repo')
    def test_git_repo_exception(self, mock_repo, tmp_path):
        """Test handling exception in git repo detection."""
        mock_repo.side_effect = InvalidGitRepositoryError("Not a git repo")

        result = is_git_repo(tmp_path)
        assert result is False


class TestGetGitRoot:
    """Tests for get_git_root function."""

    def test_get_root_from_repo(self, tmp_path):
        """Test getting root from repository."""
        Repo.init(tmp_path)
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        result = get_git_root(subdir)
        assert result == tmp_path

    def test_get_root_no_repo(self, tmp_path):
        """Test getting root when not in repository."""
        result = get_git_root(tmp_path)
        assert result is None

    @patch('cci.utils.git_utils.Repo')
    def test_get_root_exception(self, mock_repo, tmp_path):
        """Test handling exception when getting root."""
        mock_repo.side_effect = InvalidGitRepositoryError("Not a git repo")

        result = get_git_root(tmp_path)
        assert result is None


class TestGetCurrentBranch:
    """Tests for get_current_branch function."""

    def test_get_branch_name(self, tmp_path):
        """Test getting current branch name."""
        repo = Repo.init(tmp_path, initial_branch="main")
        # Need to make an initial commit for branch to exist
        (tmp_path / "file.txt").write_text("content")
        repo.index.add(["file.txt"])
        repo.index.commit("Initial commit")

        result = get_current_branch(tmp_path)
        assert result == "main"

    def test_get_branch_no_repo(self, tmp_path):
        """Test getting branch when not in repository."""
        result = get_current_branch(tmp_path)
        assert result is None

    @patch('cci.utils.git_utils.Repo')
    def test_get_branch_detached_head(self, mock_repo, tmp_path):
        """Test getting branch with detached HEAD."""
        mock_git_repo = MagicMock()
        mock_git_repo.head.is_detached = True
        mock_repo.return_value = mock_git_repo

        result = get_current_branch(tmp_path)
        assert result is None

    @patch('cci.utils.git_utils.Repo')
    def test_get_branch_exception(self, mock_repo, tmp_path):
        """Test handling exception when getting branch."""
        mock_repo.side_effect = InvalidGitRepositoryError("Not a git repo")

        result = get_current_branch(tmp_path)
        assert result is None


class TestHasUncommittedChanges:
    """Tests for has_uncommitted_changes function."""

    def test_clean_repo(self, tmp_path):
        """Test repository with no uncommitted changes."""
        repo = Repo.init(tmp_path)
        (tmp_path / "file.txt").write_text("content")
        repo.index.add(["file.txt"])
        repo.index.commit("Initial commit")

        result = has_uncommitted_changes(tmp_path)
        assert result is False

    def test_dirty_repo(self, tmp_path):
        """Test repository with uncommitted changes."""
        repo = Repo.init(tmp_path)
        (tmp_path / "file.txt").write_text("content")
        repo.index.add(["file.txt"])
        repo.index.commit("Initial commit")

        # Modify file
        (tmp_path / "file.txt").write_text("modified content")

        result = has_uncommitted_changes(tmp_path)
        assert result is True

    def test_untracked_files(self, tmp_path):
        """Test repository with untracked files."""
        repo = Repo.init(tmp_path)
        (tmp_path / "file.txt").write_text("content")
        repo.index.add(["file.txt"])
        repo.index.commit("Initial commit")

        # Add untracked file
        (tmp_path / "untracked.txt").write_text("untracked")

        result = has_uncommitted_changes(tmp_path)
        assert result is True

    def test_no_repo(self, tmp_path):
        """Test when not in repository."""
        result = has_uncommitted_changes(tmp_path)
        assert result is False


class TestGetRemoteUrl:
    """Tests for get_remote_url function."""

    @patch('cci.utils.git_utils.Repo')
    def test_get_origin_url(self, mock_repo, tmp_path):
        """Test getting origin URL."""
        mock_git_repo = MagicMock()
        mock_remote = MagicMock()
        mock_remote.url = "https://github.com/user/repo.git"
        mock_git_repo.remotes = {"origin": mock_remote}
        mock_repo.return_value = mock_git_repo

        result = get_remote_url(tmp_path)
        assert result == "https://github.com/user/repo.git"

    @patch('cci.utils.git_utils.Repo')
    def test_get_custom_remote_url(self, mock_repo, tmp_path):
        """Test getting custom remote URL."""
        mock_git_repo = MagicMock()
        mock_remote = MagicMock()
        mock_remote.url = "https://github.com/user/repo.git"
        mock_git_repo.remotes = {"upstream": mock_remote}
        mock_repo.return_value = mock_git_repo

        result = get_remote_url(tmp_path, "upstream")
        assert result == "https://github.com/user/repo.git"

    @patch('cci.utils.git_utils.Repo')
    def test_get_remote_not_found(self, mock_repo, tmp_path):
        """Test getting URL for non-existent remote."""
        mock_git_repo = MagicMock()
        mock_git_repo.remotes = {}
        mock_repo.return_value = mock_git_repo

        result = get_remote_url(tmp_path)
        assert result is None

    @patch('cci.utils.git_utils.Repo')
    def test_get_remote_exception(self, mock_repo, tmp_path):
        """Test handling exception when getting remote URL."""
        mock_repo.side_effect = InvalidGitRepositoryError("Not a git repo")

        result = get_remote_url(tmp_path)
        assert result is None


class TestGetCommitHash:
    """Tests for get_commit_hash function."""

    def test_get_short_hash(self, tmp_path):
        """Test getting short commit hash."""
        repo = Repo.init(tmp_path)
        (tmp_path / "file.txt").write_text("content")
        repo.index.add(["file.txt"])
        commit = repo.index.commit("Initial commit")

        result = get_commit_hash(tmp_path, short=True)
        assert result == commit.hexsha[:7]

    def test_get_full_hash(self, tmp_path):
        """Test getting full commit hash."""
        repo = Repo.init(tmp_path)
        (tmp_path / "file.txt").write_text("content")
        repo.index.add(["file.txt"])
        commit = repo.index.commit("Initial commit")

        result = get_commit_hash(tmp_path, short=False)
        assert result == commit.hexsha

    def test_get_hash_no_repo(self, tmp_path):
        """Test getting hash when not in repository."""
        result = get_commit_hash(tmp_path)
        assert result is None


class TestListModifiedFiles:
    """Tests for list_modified_files function."""

    def test_list_modified_files(self, tmp_path):
        """Test listing modified files."""
        repo = Repo.init(tmp_path)
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        # Initial commit
        file1.write_text("content1")
        repo.index.add(["file1.txt"])
        repo.index.commit("Initial commit")

        # Modify existing file
        file1.write_text("modified content1")

        # Add new untracked file
        file2.write_text("content2")

        result = list_modified_files(tmp_path)

        # Convert to names for easier testing
        file_names = {f.name for f in result}
        assert "file1.txt" in file_names  # Modified
        assert "file2.txt" in file_names  # Untracked

    def test_list_modified_no_repo(self, tmp_path):
        """Test listing files when not in repository."""
        result = list_modified_files(tmp_path)
        assert result == []


class TestGetGitStatus:
    """Tests for get_git_status function."""

    def test_get_status_with_changes(self, tmp_path):
        """Test getting git status with various changes."""
        repo = Repo.init(tmp_path)
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file3 = tmp_path / "file3.txt"

        # Initial commit
        file1.write_text("content1")
        repo.index.add(["file1.txt"])
        repo.index.commit("Initial commit")

        # Stage a new file
        file2.write_text("content2")
        repo.index.add(["file2.txt"])

        # Modify existing file
        file1.write_text("modified content1")

        # Add untracked file
        file3.write_text("content3")

        result = get_git_status(tmp_path)

        assert "file2.txt" in result["staged"]
        assert "file1.txt" in result["modified"]
        assert "file3.txt" in result["untracked"]

    def test_get_status_clean_repo(self, tmp_path):
        """Test getting status of clean repository."""
        repo = Repo.init(tmp_path)
        (tmp_path / "file.txt").write_text("content")
        repo.index.add(["file.txt"])
        repo.index.commit("Initial commit")

        result = get_git_status(tmp_path)

        assert result["staged"] == []
        assert result["modified"] == []
        assert result["untracked"] == []
        assert result["deleted"] == []

    def test_get_status_no_repo(self, tmp_path):
        """Test getting status when not in repository."""
        result = get_git_status(tmp_path)

        expected = {"staged": [], "modified": [], "untracked": [], "deleted": []}
        assert result == expected


class TestInitGitRepo:
    """Tests for init_git_repo function."""

    def test_init_repo_success(self, tmp_path):
        """Test successful repository initialization."""
        result = init_git_repo(tmp_path, "main")

        assert result is True
        assert (tmp_path / ".git").exists()

    def test_init_repo_default_branch(self, tmp_path):
        """Test initialization with default branch name."""
        result = init_git_repo(tmp_path)

        assert result is True
        assert (tmp_path / ".git").exists()

    @patch('cci.utils.git_utils.Repo.init')
    def test_init_repo_failure(self, mock_init, tmp_path):
        """Test failed repository initialization."""
        mock_init.side_effect = Exception("Init failed")

        result = init_git_repo(tmp_path)

        assert result is False
