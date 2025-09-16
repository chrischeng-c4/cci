"""Utility functions for CCI."""

from cci.utils.config_utils import (
    load_config,
    merge_configs,
    save_config,
    validate_config,
)
from cci.utils.file_utils import (
    copy_file_safe,
    ensure_directory,
    find_files_by_pattern,
    format_file_size,
    get_file_encoding,
    get_file_info,
    read_file_safe,
    write_file_safe,
)
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

__all__ = [
    # File utilities
    "read_file_safe",
    "write_file_safe",
    "get_file_encoding",
    "format_file_size",
    "get_file_info",
    "ensure_directory",
    "copy_file_safe",
    "find_files_by_pattern",
    # Git utilities
    "is_git_repo",
    "get_git_root",
    "get_current_branch",
    "has_uncommitted_changes",
    "get_remote_url",
    "get_commit_hash",
    "list_modified_files",
    "get_git_status",
    "init_git_repo",
    # Config utilities
    "load_config",
    "save_config",
    "merge_configs",
    "validate_config",
]
