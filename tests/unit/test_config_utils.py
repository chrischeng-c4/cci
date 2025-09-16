"""Tests for configuration utility functions."""

import tomllib
from pathlib import Path
from unittest.mock import patch

import pytest
import tomli_w
from pydantic import BaseModel, ValidationError

from cci.utils.config_utils import (
    create_default_config,
    get_default_config_path,
    get_project_config_path,
    load_config,
    load_project_config,
    merge_configs,
    save_config,
    validate_config,
)


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_valid_config(self, tmp_path):
        """Test loading a valid TOML config file."""
        config_file = tmp_path / "config.toml"
        config_data = {
            "ui": {"theme": "dark"},
            "git": {"default_branch": "main"}
        }

        with open(config_file, "wb") as f:
            tomli_w.dump(config_data, f)

        result = load_config(config_file)
        assert result == config_data

    def test_load_nonexistent_config(self, tmp_path):
        """Test loading a nonexistent config file."""
        config_file = tmp_path / "nonexistent.toml"

        with pytest.raises(FileNotFoundError):
            load_config(config_file)

    def test_load_invalid_toml(self, tmp_path):
        """Test loading an invalid TOML file."""
        config_file = tmp_path / "invalid.toml"
        config_file.write_text("invalid toml content [[[")

        with pytest.raises(tomllib.TOMLDecodeError):
            load_config(config_file)


class TestSaveConfig:
    """Tests for save_config function."""

    def test_save_config(self, tmp_path):
        """Test saving a config to file."""
        config_file = tmp_path / "config.toml"
        config_data = {
            "ui": {"theme": "dark"},
            "git": {"default_branch": "main"}
        }

        save_config(config_file, config_data)

        assert config_file.exists()
        loaded_data = load_config(config_file)
        assert loaded_data == config_data

    def test_save_config_creates_parent_dirs(self, tmp_path):
        """Test that saving creates parent directories."""
        config_file = tmp_path / "subdir" / "config.toml"
        config_data = {"test": "value"}

        save_config(config_file, config_data)

        assert config_file.exists()
        loaded_data = load_config(config_file)
        assert loaded_data == config_data

    def test_save_config_with_none_values(self, tmp_path):
        """Test saving config with None values."""
        config_file = tmp_path / "config.toml"
        config_data = {
            "ui": {"theme": "dark", "disabled_feature": None},
            "git": None,
            "values": [1, None, 3]
        }

        save_config(config_file, config_data)

        loaded_data = load_config(config_file)
        # None values should be filtered out
        expected = {
            "ui": {"theme": "dark"},
            "values": [1, 3]
        }
        assert loaded_data == expected


class TestMergeConfigs:
    """Tests for merge_configs function."""

    def test_merge_simple_configs(self):
        """Test merging simple configurations."""
        config1 = {"a": 1, "b": 2}
        config2 = {"b": 3, "c": 4}

        result = merge_configs(config1, config2)
        expected = {"a": 1, "b": 3, "c": 4}
        assert result == expected

    def test_merge_nested_configs(self):
        """Test merging nested configurations."""
        config1 = {
            "ui": {"theme": "light", "font_size": 12},
            "git": {"default_branch": "main"}
        }
        config2 = {
            "ui": {"theme": "dark", "show_line_numbers": True},
            "performance": {"cache_enabled": True}
        }

        result = merge_configs(config1, config2)
        expected = {
            "ui": {"theme": "dark", "font_size": 12, "show_line_numbers": True},
            "git": {"default_branch": "main"},
            "performance": {"cache_enabled": True}
        }
        assert result == expected

    def test_merge_multiple_configs(self):
        """Test merging multiple configurations."""
        config1 = {"a": 1}
        config2 = {"b": 2}
        config3 = {"c": 3}

        result = merge_configs(config1, config2, config3)
        expected = {"a": 1, "b": 2, "c": 3}
        assert result == expected

    def test_merge_empty_configs(self):
        """Test merging empty configurations."""
        result = merge_configs({}, {"a": 1}, {})
        expected = {"a": 1}
        assert result == expected


class TestValidateConfig:
    """Tests for validate_config function."""

    def test_validate_valid_config(self):
        """Test validating a valid configuration."""
        class TestModel(BaseModel):
            name: str
            age: int

        config = {"name": "test", "age": 25}

        result = validate_config(config, TestModel)
        assert isinstance(result, TestModel)
        assert result.name == "test"
        assert result.age == 25

    def test_validate_invalid_config(self):
        """Test validating an invalid configuration."""
        class TestModel(BaseModel):
            name: str
            age: int

        config = {"name": "test", "age": "not_a_number"}

        with pytest.raises(ValidationError):
            validate_config(config, TestModel)

    def test_validate_missing_fields(self):
        """Test validating configuration with missing required fields."""
        class TestModel(BaseModel):
            name: str
            age: int

        config = {"name": "test"}  # Missing 'age'

        with pytest.raises(ValidationError):
            validate_config(config, TestModel)


class TestGetDefaultConfigPath:
    """Tests for get_default_config_path function."""

    @patch('pathlib.Path.home')
    def test_get_default_config_path(self, mock_home):
        """Test getting default config path."""
        mock_home.return_value = Path("/home/user")

        result = get_default_config_path()
        expected = Path("/home/user/.config/cci/config.toml")
        assert result == expected


class TestGetProjectConfigPath:
    """Tests for get_project_config_path function."""

    def test_get_project_config_path(self):
        """Test getting project config path."""
        project_path = Path("/path/to/project")

        result = get_project_config_path(project_path)
        expected = Path("/path/to/project/.cci/config.toml")
        assert result == expected


class TestLoadProjectConfig:
    """Tests for load_project_config function."""

    @patch('cci.utils.config_utils.get_default_config_path')
    @patch('cci.utils.config_utils.get_project_config_path')
    @patch('cci.utils.config_utils.load_config')
    def test_load_both_configs(self, mock_load_config, mock_project_path, mock_default_path):
        """Test loading both global and project configs."""
        # Mock paths
        mock_default_path.return_value = Path("/home/user/.config/cci/config.toml")
        mock_project_path.return_value = Path("/project/.cci/config.toml")

        # Mock path existence
        with patch('pathlib.Path.exists', return_value=True):
            # Mock load_config calls
            mock_load_config.side_effect = [
                {"ui": {"theme": "light"}},  # Global config
                {"ui": {"theme": "dark"}, "git": {"default_branch": "main"}}  # Project config
            ]

            result = load_project_config(Path("/project"))

            expected = {
                "ui": {"theme": "dark"},  # Project overrides global
                "git": {"default_branch": "main"}
            }
            assert result == expected

    @patch('cci.utils.config_utils.get_default_config_path')
    @patch('cci.utils.config_utils.get_project_config_path')
    def test_load_no_configs(self, mock_project_path, mock_default_path):
        """Test loading when no configs exist."""
        # Mock paths
        mock_default_path.return_value = Path("/home/user/.config/cci/config.toml")
        mock_project_path.return_value = Path("/project/.cci/config.toml")

        # Mock path existence (both don't exist)
        with patch('pathlib.Path.exists', return_value=False):
            result = load_project_config(Path("/project"))
            assert result == {}

    @patch('cci.utils.config_utils.get_default_config_path')
    @patch('cci.utils.config_utils.get_project_config_path')
    @patch('cci.utils.config_utils.load_config')
    def test_load_with_config_errors(self, mock_load_config, mock_project_path, mock_default_path):
        """Test loading with config errors (should be ignored)."""
        # Mock paths
        mock_default_path.return_value = Path("/home/user/.config/cci/config.toml")
        mock_project_path.return_value = Path("/project/.cci/config.toml")

        # Mock path existence
        with patch('pathlib.Path.exists', return_value=True):
            # Mock load_config to raise exception
            mock_load_config.side_effect = Exception("Config error")

            result = load_project_config(Path("/project"))
            assert result == {}


class TestCreateDefaultConfig:
    """Tests for create_default_config function."""

    @patch('cci.utils.config_utils.get_default_config_path')
    @patch('cci.utils.config_utils.save_config')
    def test_create_default_config_default_path(self, mock_save_config, mock_default_path):
        """Test creating default config at default path."""
        mock_default_path.return_value = Path("/home/user/.config/cci/config.toml")

        create_default_config()

        mock_save_config.assert_called_once()
        args, _ = mock_save_config.call_args
        path, config = args

        assert path == Path("/home/user/.config/cci/config.toml")
        assert "ui" in config
        assert "git" in config
        assert "performance" in config

    @patch('cci.utils.config_utils.save_config')
    def test_create_default_config_custom_path(self, mock_save_config):
        """Test creating default config at custom path."""
        custom_path = Path("/custom/path/config.toml")

        create_default_config(custom_path)

        mock_save_config.assert_called_once()
        args, _ = mock_save_config.call_args
        path, config = args

        assert path == custom_path
        assert "ui" in config
        assert "git" in config
        assert "performance" in config

    def test_create_default_config_structure(self, tmp_path):
        """Test the structure of default config."""
        config_path = tmp_path / "config.toml"

        create_default_config(config_path)

        loaded_config = load_config(config_path)

        # Check structure
        assert "ui" in loaded_config
        assert "git" in loaded_config
        assert "performance" in loaded_config

        # Check UI defaults
        ui_config = loaded_config["ui"]
        assert ui_config["theme"] == "monokai"
        assert ui_config["editor_mode"] == "normal"
        assert ui_config["show_line_numbers"] is True
        assert ui_config["syntax_highlighting"] is True

        # Check Git defaults
        git_config = loaded_config["git"]
        assert git_config["default_branch"] == "main"
        assert git_config["auto_fetch"] is False

        # Check Performance defaults
        perf_config = loaded_config["performance"]
        assert perf_config["max_workers"] == 4
        assert perf_config["cache_enabled"] is True
        assert perf_config["cache_size_mb"] == 100
