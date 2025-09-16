"""Tests for configuration management."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from cci.config import (
    CCIConfig,
    ConfigManager,
    create_default_ai_config,
    get_ai_config,
    get_config_manager,
)
from cci.services import AIConfig, AIProviderType


class TestCCIConfig:
    """Test CCI configuration model."""

    def test_default_config(self):
        """Test default configuration."""
        config = CCIConfig()

        assert config.ai.provider == AIProviderType.CLAUDE_CODE
        assert config.ui.theme == "monokai"
        assert config.git.default_branch == "main"
        assert config.performance.max_workers == 4

    def test_from_dict(self):
        """Test creating config from dictionary."""
        config_dict = {
            "ai": {
                "provider": "anthropic",
                "model": "claude-3-opus-20240229",
                "max_tokens": 2000,
            },
            "ui": {
                "theme": "dark",
                "editor_mode": "vim",
            },
            "performance": {
                "max_workers": 8,
            }
        }

        config = CCIConfig.from_dict(config_dict)

        assert config.ai.provider == AIProviderType.ANTHROPIC
        assert config.ai.model == "claude-3-opus-20240229"
        assert config.ai.max_tokens == 2000
        assert config.ui.theme == "dark"
        assert config.ui.editor_mode == "vim"
        assert config.performance.max_workers == 8

    def test_from_dict_empty(self):
        """Test creating config from empty dictionary."""
        config = CCIConfig.from_dict({})

        # Should use defaults
        assert config.ai.provider == AIProviderType.CLAUDE_CODE
        assert config.ui.theme == "monokai"

    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = CCIConfig()
        config_dict = config.to_dict()

        assert "ai" in config_dict
        assert "ui" in config_dict
        assert "git" in config_dict
        assert "performance" in config_dict

        assert config_dict["ai"]["provider"] == "claude-code"
        assert config_dict["ui"]["theme"] == "monokai"


class TestConfigManager:
    """Test configuration manager."""

    @pytest.fixture
    def temp_project(self, tmp_path):
        """Create temporary project directory."""
        project = tmp_path / "test_project"
        project.mkdir()
        return project

    def test_init_no_project(self):
        """Test initialization without project path."""
        manager = ConfigManager()
        assert manager.project_path is None
        assert manager._config is None

    def test_init_with_project(self, temp_project):
        """Test initialization with project path."""
        manager = ConfigManager(temp_project)
        assert manager.project_path == temp_project

    @patch('cci.config.load_project_config')
    def test_load_config_project(self, mock_load, temp_project):
        """Test loading project configuration."""
        mock_load.return_value = {
            "ai": {"model": "claude-3-opus-20240229"}
        }

        manager = ConfigManager(temp_project)
        config = manager.load_config()

        assert config.ai.model == "claude-3-opus-20240229"
        mock_load.assert_called_once_with(temp_project)

    @patch('cci.utils.config_utils.load_config')
    @patch('cci.config.get_default_config_path')
    def test_load_config_global(self, mock_get_path, mock_load):
        """Test loading global configuration."""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_get_path.return_value = mock_path

        mock_load.return_value = {
            "ui": {"theme": "dark"}
        }

        manager = ConfigManager()
        config = manager.load_config()

        assert config.ui.theme == "dark"
        mock_load.assert_called_once_with(mock_path)

    @patch('cci.config.load_project_config')
    def test_load_config_empty(self, mock_load, temp_project):
        """Test loading with empty configuration."""
        mock_load.return_value = {}

        manager = ConfigManager(temp_project)

        with patch.object(manager, 'create_default_config') as mock_create:
            manager.load_config()

            # Should create default config when empty
            mock_create.assert_called_once()

    @patch('cci.utils.config_utils.save_config')
    def test_save_config(self, mock_save, temp_project):
        """Test saving configuration."""
        manager = ConfigManager(temp_project)
        config = CCIConfig()

        manager.save_config(config)

        mock_save.assert_called_once()
        # Check that config was converted to dict
        call_args = mock_save.call_args[0]
        assert isinstance(call_args[1], dict)

    def test_get_config(self, temp_project):
        """Test getting current configuration."""
        manager = ConfigManager(temp_project)

        with patch.object(manager, 'load_config') as mock_load:
            mock_config = CCIConfig()
            mock_load.return_value = mock_config

            config = manager.get_config()

            assert config == mock_config
            mock_load.assert_called_once()

    @patch('cci.config.create_default_config')
    def test_create_default_config_global(self, mock_create):
        """Test creating default global configuration."""
        manager = ConfigManager()
        manager.create_default_config()

        mock_create.assert_called_once()

    @patch('cci.utils.config_utils.save_config')
    @patch('cci.utils.config_utils.get_project_config_path')
    def test_create_default_config_project(self, mock_get_path, mock_save, temp_project):
        """Test creating default project configuration."""
        mock_path = temp_project / ".cci" / "config.toml"
        mock_get_path.return_value = mock_path

        manager = ConfigManager(temp_project)
        manager.create_default_config()

        mock_save.assert_called_once()
        call_args = mock_save.call_args[0]
        assert call_args[0] == mock_path
        assert "ai" in call_args[1]

    def test_update_ai_config(self, temp_project):
        """Test updating AI configuration."""
        manager = ConfigManager(temp_project)

        with patch.object(manager, 'get_config') as mock_get:
            with patch.object(manager, 'save_config') as mock_save:
                mock_config = CCIConfig()
                mock_get.return_value = mock_config

                manager.update_ai_config(model="claude-3-opus-20240229", temperature=0.9)

                # Should update the AI config
                assert mock_config.ai.model == "claude-3-opus-20240229"
                assert mock_config.ai.temperature == 0.9
                mock_save.assert_called_once_with(mock_config)

    def test_update_ai_config_provider(self, temp_project):
        """Test updating AI provider."""
        manager = ConfigManager(temp_project)

        with patch.object(manager, 'get_config') as mock_get:
            with patch.object(manager, 'save_config'):
                mock_config = CCIConfig()
                mock_get.return_value = mock_config

                manager.update_ai_config(provider="anthropic")

                assert mock_config.ai.provider == AIProviderType.ANTHROPIC

    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    def test_validate_ai_config_valid(self, temp_project):
        """Test validating AI configuration with valid key."""
        manager = ConfigManager(temp_project)

        with patch.object(manager, 'get_config') as mock_get:
            mock_config = CCIConfig()
            mock_get.return_value = mock_config

            result = manager.validate_ai_config()

            assert result is True

    def test_validate_ai_config_invalid(self, temp_project):
        """Test validating AI configuration without key."""
        manager = ConfigManager(temp_project)

        with patch.dict('os.environ', {}, clear=True):
            with patch.object(manager, 'get_config') as mock_get:
                mock_config = CCIConfig()
                mock_get.return_value = mock_config

                result = manager.validate_ai_config()

                assert result is False

    def test_get_ai_config(self, temp_project):
        """Test getting AI configuration."""
        manager = ConfigManager(temp_project)

        with patch.object(manager, 'get_config') as mock_get:
            mock_config = CCIConfig()
            mock_get.return_value = mock_config

            ai_config = manager.get_ai_config()

            assert ai_config == mock_config.ai


def test_get_config_manager():
    """Test get_config_manager helper."""
    manager = get_config_manager()
    assert isinstance(manager, ConfigManager)
    assert manager.project_path is None

    project_path = Path("/test")
    manager = get_config_manager(project_path)
    assert manager.project_path == project_path


def test_get_ai_config():
    """Test get_ai_config helper."""
    with patch('cci.config.get_config_manager') as mock_get_manager:
        mock_manager = Mock()
        mock_ai_config = AIConfig()
        mock_manager.get_ai_config.return_value = mock_ai_config
        mock_get_manager.return_value = mock_manager

        result = get_ai_config(Path("/test"))

        assert result == mock_ai_config
        mock_get_manager.assert_called_once_with(Path("/test"))
        mock_manager.get_ai_config.assert_called_once()


def test_create_default_ai_config():
    """Test creating default AI configuration."""
    config = create_default_ai_config()

    assert isinstance(config, AIConfig)
    assert config.provider == AIProviderType.CLAUDE_CODE
    assert config.model == "claude-code"
    assert config.api_key_env == "ANTHROPIC_API_KEY"  # Still uses this for backward compatibility
    assert config.max_tokens == 4000
    assert config.temperature == 0.7
