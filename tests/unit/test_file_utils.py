"""Tests for file utility functions."""

from unittest.mock import patch

import pytest

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


class TestReadFileSafe:
    """Tests for read_file_safe function."""

    def test_read_existing_file(self, tmp_path):
        """Test reading an existing file."""
        test_file = tmp_path / "test.txt"
        content = "Hello, World!"
        test_file.write_text(content, encoding="utf-8")

        result_content, result_encoding = read_file_safe(test_file)
        assert result_content == content
        assert result_encoding == "utf-8"

    def test_read_with_explicit_encoding(self, tmp_path):
        """Test reading with explicit encoding."""
        test_file = tmp_path / "test.txt"
        content = "Hello, World!"
        test_file.write_text(content, encoding="latin-1")

        result_content, result_encoding = read_file_safe(test_file, encoding="latin-1")
        assert result_content == content
        assert result_encoding == "latin-1"

    def test_read_nonexistent_file(self, tmp_path):
        """Test reading a nonexistent file."""
        test_file = tmp_path / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            read_file_safe(test_file)

    def test_read_with_fallback_encoding(self, tmp_path):
        """Test reading with fallback to latin-1."""
        test_file = tmp_path / "test.txt"
        # Write binary data that's not valid UTF-8
        test_file.write_bytes(b'\x80\x81\x82')

        with patch('cci.utils.file_utils.get_file_encoding', return_value='utf-8'):
            result_content, result_encoding = read_file_safe(test_file)
            assert result_encoding == "latin-1"


class TestWriteFileSafe:
    """Tests for write_file_safe function."""

    def test_write_to_new_file(self, tmp_path):
        """Test writing to a new file."""
        test_file = tmp_path / "test.txt"
        content = "Hello, World!"

        write_file_safe(test_file, content)

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8") == content

    def test_write_creates_parent_dirs(self, tmp_path):
        """Test that parent directories are created."""
        test_file = tmp_path / "subdir" / "test.txt"
        content = "Hello, World!"

        write_file_safe(test_file, content)

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8") == content

    def test_write_with_custom_encoding(self, tmp_path):
        """Test writing with custom encoding."""
        test_file = tmp_path / "test.txt"
        content = "Hello, World!"

        write_file_safe(test_file, content, encoding="latin-1")

        assert test_file.exists()
        assert test_file.read_text(encoding="latin-1") == content


class TestGetFileEncoding:
    """Tests for get_file_encoding function."""

    def test_detect_utf8(self, tmp_path):
        """Test detecting UTF-8 encoding."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!", encoding="utf-8")

        encoding = get_file_encoding(test_file)
        assert encoding == "utf-8"

    def test_detect_nonexistent_file(self, tmp_path):
        """Test detecting encoding of nonexistent file."""
        test_file = tmp_path / "nonexistent.txt"

        encoding = get_file_encoding(test_file)
        assert encoding == "utf-8"  # Default

    def test_detect_empty_file(self, tmp_path):
        """Test detecting encoding of empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.touch()

        encoding = get_file_encoding(test_file)
        assert encoding == "utf-8"  # Default for empty files

    def test_encoding_mapping(self, tmp_path):
        """Test encoding alias mapping."""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b"Hello")

        with patch('chardet.detect', return_value={'encoding': 'ascii'}):
            encoding = get_file_encoding(test_file)
            assert encoding == "utf-8"  # ASCII maps to UTF-8


class TestFormatFileSize:
    """Tests for format_file_size function."""

    def test_bytes(self):
        """Test formatting bytes."""
        assert format_file_size(100) == "100 B"

    def test_kilobytes(self):
        """Test formatting kilobytes."""
        assert format_file_size(1536) == "1.5 KB"

    def test_megabytes(self):
        """Test formatting megabytes."""
        assert format_file_size(1572864) == "1.5 MB"

    def test_gigabytes(self):
        """Test formatting gigabytes."""
        assert format_file_size(1610612736) == "1.5 GB"

    def test_zero_bytes(self):
        """Test formatting zero bytes."""
        assert format_file_size(0) == "0 B"


class TestGetFileInfo:
    """Tests for get_file_info function."""

    def test_get_info_for_file(self, tmp_path):
        """Test getting info for a file."""
        test_file = tmp_path / "test.txt"
        content = "Hello, World!"
        test_file.write_text(content, encoding="utf-8")

        info = get_file_info(test_file)

        assert info["name"] == "test.txt"
        assert info["size"] == "13 B"
        assert info["size_bytes"] == "13"
        assert info["is_file"] == "True"
        assert info["is_dir"] == "False"
        assert info["suffix"] == ".txt"
        assert info["encoding"] == "utf-8"

    def test_get_info_for_directory(self, tmp_path):
        """Test getting info for a directory."""
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        info = get_file_info(test_dir)

        assert info["name"] == "testdir"
        assert info["is_file"] == "False"
        assert info["is_dir"] == "True"
        assert info["suffix"] == ""
        assert info["encoding"] == "N/A"

    def test_get_info_nonexistent_file(self, tmp_path):
        """Test getting info for nonexistent file."""
        test_file = tmp_path / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            get_file_info(test_file)


class TestEnsureDirectory:
    """Tests for ensure_directory function."""

    def test_create_new_directory(self, tmp_path):
        """Test creating a new directory."""
        test_dir = tmp_path / "newdir"

        ensure_directory(test_dir)

        assert test_dir.exists()
        assert test_dir.is_dir()

    def test_create_nested_directory(self, tmp_path):
        """Test creating nested directories."""
        test_dir = tmp_path / "level1" / "level2" / "level3"

        ensure_directory(test_dir)

        assert test_dir.exists()
        assert test_dir.is_dir()

    def test_existing_directory(self, tmp_path):
        """Test ensuring existing directory."""
        test_dir = tmp_path / "existing"
        test_dir.mkdir()

        # Should not raise an error
        ensure_directory(test_dir)

        assert test_dir.exists()
        assert test_dir.is_dir()


class TestCopyFileSafe:
    """Tests for copy_file_safe function."""

    def test_copy_file(self, tmp_path):
        """Test copying a file."""
        src = tmp_path / "source.txt"
        dst = tmp_path / "dest.txt"
        content = "Hello, World!"
        src.write_text(content, encoding="utf-8")

        result = copy_file_safe(src, dst)

        assert result is True
        assert dst.exists()
        assert dst.read_text(encoding="utf-8") == content

    def test_copy_creates_parent_dirs(self, tmp_path):
        """Test that copying creates parent directories."""
        src = tmp_path / "source.txt"
        dst = tmp_path / "subdir" / "dest.txt"
        content = "Hello, World!"
        src.write_text(content, encoding="utf-8")

        result = copy_file_safe(src, dst)

        assert result is True
        assert dst.exists()
        assert dst.read_text(encoding="utf-8") == content

    def test_copy_nonexistent_source(self, tmp_path):
        """Test copying nonexistent source."""
        src = tmp_path / "nonexistent.txt"
        dst = tmp_path / "dest.txt"

        result = copy_file_safe(src, dst)

        assert result is False
        assert not dst.exists()

    def test_copy_with_existing_dest_no_overwrite(self, tmp_path):
        """Test copying with existing destination without overwrite."""
        src = tmp_path / "source.txt"
        dst = tmp_path / "dest.txt"
        src.write_text("source content", encoding="utf-8")
        dst.write_text("dest content", encoding="utf-8")

        result = copy_file_safe(src, dst, overwrite=False)

        assert result is False
        assert dst.read_text(encoding="utf-8") == "dest content"

    def test_copy_with_existing_dest_overwrite(self, tmp_path):
        """Test copying with existing destination with overwrite."""
        src = tmp_path / "source.txt"
        dst = tmp_path / "dest.txt"
        src.write_text("source content", encoding="utf-8")
        dst.write_text("dest content", encoding="utf-8")

        result = copy_file_safe(src, dst, overwrite=True)

        assert result is True
        assert dst.read_text(encoding="utf-8") == "source content"


class TestFindFilesByPattern:
    """Tests for find_files_by_pattern function."""

    def test_find_files_recursive(self, tmp_path):
        """Test finding files recursively."""
        # Create test files
        (tmp_path / "file1.py").touch()
        (tmp_path / "file2.txt").touch()
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.py").touch()
        (subdir / "file4.txt").touch()

        result = find_files_by_pattern(tmp_path, "*.py", recursive=True)

        assert len(result) == 2
        file_names = {f.name for f in result}
        assert file_names == {"file1.py", "file3.py"}

    def test_find_files_non_recursive(self, tmp_path):
        """Test finding files non-recursively."""
        # Create test files
        (tmp_path / "file1.py").touch()
        (tmp_path / "file2.txt").touch()
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.py").touch()

        result = find_files_by_pattern(tmp_path, "*.py", recursive=False)

        assert len(result) == 1
        assert result[0].name == "file1.py"

    def test_find_files_nonexistent_directory(self, tmp_path):
        """Test finding files in nonexistent directory."""
        nonexistent = tmp_path / "nonexistent"

        result = find_files_by_pattern(nonexistent, "*.py")

        assert result == []

    def test_find_files_no_matches(self, tmp_path):
        """Test finding files with no matches."""
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()

        result = find_files_by_pattern(tmp_path, "*.py")

        assert result == []
