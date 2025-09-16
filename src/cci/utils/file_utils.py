"""File utility functions for CCI."""

from pathlib import Path

import chardet


def read_file_safe(file_path: Path, encoding: str | None = None) -> tuple[str, str]:
    """Safely read a file with automatic encoding detection.

    Args:
        file_path: Path to the file to read
        encoding: Optional encoding to use, auto-detected if not provided

    Returns:
        Tuple of (content, encoding_used)
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if encoding:
        try:
            content = file_path.read_text(encoding=encoding)
            return content, encoding
        except UnicodeDecodeError:
            pass  # Fall through to auto-detection

    # Auto-detect encoding
    detected_encoding = get_file_encoding(file_path)

    try:
        content = file_path.read_text(encoding=detected_encoding)
        return content, detected_encoding
    except UnicodeDecodeError:
        # Fallback to latin-1 which can read any byte sequence
        content = file_path.read_text(encoding="latin-1")
        return content, "latin-1"


def write_file_safe(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    """Safely write content to a file.

    Args:
        file_path: Path to the file to write
        content: Content to write
        encoding: Encoding to use (default: utf-8)
    """
    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    file_path.write_text(content, encoding=encoding)


def get_file_encoding(file_path: Path) -> str:
    """Detect the encoding of a file.

    Args:
        file_path: Path to the file

    Returns:
        Detected encoding string
    """
    if not file_path.exists():
        return "utf-8"  # Default for new files

    # Read a sample of the file for detection
    with open(file_path, "rb") as f:
        raw_data = f.read(10000)  # Read first 10KB

    if not raw_data:
        return "utf-8"  # Empty file

    # Detect encoding
    result = chardet.detect(raw_data)
    encoding = result.get("encoding")

    # Map common encoding aliases
    encoding_map = {
        "ascii": "utf-8",  # ASCII is subset of UTF-8
        "ISO-8859-1": "latin-1",
        None: "utf-8",  # Default if detection fails
    }

    return encoding_map.get(encoding, encoding or "utf-8")


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    size: float = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def get_file_info(file_path: Path) -> dict[str, str]:
    """Get comprehensive file information.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary with file information
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    stat = file_path.stat()

    return {
        "name": file_path.name,
        "size": format_file_size(stat.st_size),
        "size_bytes": str(stat.st_size),
        "modified": str(stat.st_mtime),
        "permissions": oct(stat.st_mode)[-3:],
        "is_file": str(file_path.is_file()),
        "is_dir": str(file_path.is_dir()),
        "suffix": file_path.suffix,
        "encoding": get_file_encoding(file_path) if file_path.is_file() else "N/A",
    }


def ensure_directory(dir_path: Path) -> None:
    """Ensure a directory exists, creating it if necessary.

    Args:
        dir_path: Path to the directory
    """
    dir_path.mkdir(parents=True, exist_ok=True)


def copy_file_safe(src: Path, dst: Path, overwrite: bool = False) -> bool:
    """Safely copy a file with error handling.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing files

    Returns:
        True if copy was successful, False otherwise
    """
    import shutil

    if not src.exists():
        return False

    if dst.exists() and not overwrite:
        return False

    try:
        # Ensure destination directory exists
        dst.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file
        shutil.copy2(src, dst)
        return True
    except Exception:
        return False


def find_files_by_pattern(directory: Path, pattern: str, recursive: bool = True) -> list[Path]:
    """Find files matching a glob pattern.

    Args:
        directory: Directory to search in
        pattern: Glob pattern to match
        recursive: Whether to search recursively

    Returns:
        List of matching file paths
    """
    if not directory.exists():
        return []

    if recursive:
        return list(directory.rglob(pattern))
    else:
        return list(directory.glob(pattern))


def get_language_from_extension(extension: str) -> str | None:
    """Get programming language from file extension.

    Args:
        extension: File extension (with or without leading dot)

    Returns:
        Language name if detected, None otherwise
    """
    # Normalize extension
    if not extension:
        return None

    ext = extension.lower()
    if not ext.startswith('.'):
        ext = '.' + ext

    # Language mapping
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.hpp': 'cpp',
        '.cs': 'csharp',
        '.go': 'go',
        '.rs': 'rust',
        '.php': 'php',
        '.rb': 'ruby',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.r': 'r',
        '.m': 'matlab',
        '.pl': 'perl',
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'bash',
        '.fish': 'bash',
        '.ps1': 'powershell',
        '.sql': 'sql',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        '.xml': 'xml',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
        '.conf': 'ini',
        '.md': 'markdown',
        '.markdown': 'markdown',
        '.rst': 'rst',
        '.tex': 'latex',
        '.vim': 'vim',
        '.lua': 'lua',
        '.dockerfile': 'dockerfile',
        '.makefile': 'makefile',
        '.cmake': 'cmake',
        '.gradle': 'gradle',
        '.maven': 'maven',
        '.properties': 'properties',
        '.gitignore': 'gitignore',
        '.gitattributes': 'gitattributes',
    }

    return language_map.get(ext)
