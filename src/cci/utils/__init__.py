"""Utility functions for CCI."""

from cci.utils.file_utils import (
    read_file_safe,
    write_file_safe,
    get_file_encoding,
    format_file_size,
)
from cci.utils.git_utils import (
    is_git_repo,
    get_git_root,
    get_current_branch,
    has_uncommitted_changes,
)
from cci.utils.config_utils import (
    load_config,
    save_config,
    merge_configs,
    validate_config,
)

__all__ = [
    # File utilities
    "read_file_safe",
    "write_file_safe",
    "get_file_encoding",
    "format_file_size",
    # Git utilities
    "is_git_repo",
    "get_git_root",
    "get_current_branch",
    "has_uncommitted_changes",
    # Config utilities
    "load_config",
    "save_config",
    "merge_configs",
    "validate_config",
]