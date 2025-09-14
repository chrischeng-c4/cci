"""File utility functions for CCI."""

import chardet
from pathlib import Path
from typing import Optional, Tuple


def read_file_safe(file_path: Path, encoding: Optional[str] = None) -> Tuple[str, str]:
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

    return encoding_map.get(encoding, encoding)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            if unit == "B":
                return f"{size_bytes} {unit}"
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"