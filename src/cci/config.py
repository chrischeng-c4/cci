"""Configuration management for CCI."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

from cci.services import AIConfig, AIProviderType
from cci.utils.config_utils import (
    create_default_config,
    get_default_config_path,
    get_project_config_path,
    load_project_config,
)


class UIConfig(BaseModel):
    """UI configuration."""

    theme: str = Field("monokai", description="UI theme")
    editor_mode: str = Field("normal", description="Editor mode (normal, vim)")
    show_line_numbers: bool = Field(True, description="Show line numbers in editor")
    syntax_highlighting: bool = Field(True, description="Enable syntax highlighting")


class GitConfig(BaseModel):
    """Git configuration."""

    default_branch: str = Field("main", description="Default git branch")
    auto_fetch: bool = Field(False, description="Automatically fetch updates")
    signing_key: str | None = Field(None, description="GPG signing key")


class PerformanceConfig(BaseModel):
    """Performance configuration."""

    max_workers: int = Field(4, description="Maximum worker threads")
    cache_enabled: bool = Field(True, description="Enable caching")
    cache_size_mb: int = Field(100, description="Cache size in MB")

    @field_validator("max_workers")
    @classmethod
    def validate_max_workers(cls, v: int) -> int:
        """Validate max workers is positive."""
        if v <= 0:
            raise ValueError("max_workers must be positive")
        return v

    @field_validator("cache_size_mb")
    @classmethod
    def validate_cache_size(cls, v: int) -> int:
        """Validate cache size is positive."""
        if v <= 0:
            raise ValueError("cache_size_mb must be positive")
        return v


class CCIConfig(BaseModel):
    """Main CCI configuration."""

    ai: AIConfig = Field(default_factory=lambda: AIConfig())  # type: ignore[call-arg]
    ui: UIConfig = Field(default_factory=lambda: UIConfig())  # type: ignore[call-arg]
    git: GitConfig = Field(default_factory=lambda: GitConfig())  # type: ignore[call-arg]
    performance: PerformanceConfig = Field(default_factory=lambda: PerformanceConfig())  # type: ignore[call-arg]

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> "CCIConfig":
        """Create configuration from dictionary.

        Args:
            config_dict: Configuration dictionary

        Returns:
            CCIConfig instance
        """
        # Handle AI config specially to convert provider string to enum
        ai_config = config_dict.get("ai", {})
        if "provider" in ai_config and isinstance(ai_config["provider"], str):
            ai_config["provider"] = AIProviderType(ai_config["provider"])

        return cls(
            ai=AIConfig(**ai_config),
            ui=UIConfig(**config_dict.get("ui", {})),
            git=GitConfig(**config_dict.get("git", {})),
            performance=PerformanceConfig(**config_dict.get("performance", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary.

        Returns:
            Configuration dictionary
        """
        return {
            "ai": self.ai.model_dump(),
            "ui": self.ui.model_dump(),
            "git": self.git.model_dump(),
            "performance": self.performance.model_dump(),
        }


class ConfigManager:
    """Configuration manager for CCI."""

    def __init__(self, project_path: Path | None = None) -> None:
        """Initialize configuration manager.

        Args:
            project_path: Optional project path for project-specific config
        """
        self.project_path = project_path
        self._config: CCIConfig | None = None

    def load_config(self, force_reload: bool = False) -> CCIConfig:
        """Load configuration.

        Args:
            force_reload: Force reload configuration from disk

        Returns:
            Loaded configuration
        """
        if self._config is None or force_reload:
            if self.project_path:
                config_dict = load_project_config(self.project_path)
            else:
                global_config_path = get_default_config_path()
                if global_config_path.exists():
                    from cci.utils.config_utils import load_config
                    config_dict = load_config(global_config_path)
                else:
                    config_dict = {}

            # Fill in defaults if config is empty or missing keys
            if not config_dict:
                self.create_default_config()
                config_dict = load_project_config(self.project_path) if self.project_path else {}

            self._config = CCIConfig.from_dict(config_dict)

        return self._config

    def save_config(self, config: CCIConfig | None = None) -> None:
        """Save configuration to disk.

        Args:
            config: Configuration to save. If None, saves current config.
        """
        if config is None:
            config = self.get_config()

        from cci.utils.config_utils import save_config

        config_dict = config.to_dict()

        if self.project_path:
            config_path = get_project_config_path(self.project_path)
        else:
            config_path = get_default_config_path()

        save_config(config_path, config_dict)
        self._config = config

    def get_config(self) -> CCIConfig:
        """Get current configuration.

        Returns:
            Current configuration
        """
        return self.load_config()

    def create_default_config(self) -> None:
        """Create default configuration file."""
        if self.project_path:
            config_path = get_project_config_path(self.project_path)
            # Create project-specific defaults
            default_config = {
                "ai": {
                    "provider": "claude-code",
                    "model": "claude-code",
                    "api_key_env": "ANTHROPIC_API_KEY",
                    "max_tokens": 4000,
                    "temperature": 0.7,
                    "timeout": 60,
                },
            }
            from cci.utils.config_utils import save_config
            save_config(config_path, default_config)
        else:
            create_default_config()

    def update_ai_config(self, **kwargs: Any) -> None:
        """Update AI configuration.

        Args:
            **kwargs: AI configuration parameters to update
        """
        config = self.get_config()
        ai_dict = config.ai.model_dump()
        ai_dict.update(kwargs)

        # Convert provider string to enum if needed
        if "provider" in kwargs and isinstance(kwargs["provider"], str):
            ai_dict["provider"] = AIProviderType(kwargs["provider"])

        config.ai = AIConfig(**ai_dict)
        self.save_config(config)

    def validate_ai_config(self) -> bool:
        """Validate AI configuration.

        Returns:
            True if AI configuration is valid, False otherwise
        """
        try:
            config = self.get_config()
            api_key = config.ai.get_api_key()
            return api_key is not None
        except Exception:
            return False

    def get_ai_config(self) -> AIConfig:
        """Get AI configuration.

        Returns:
            AI configuration
        """
        return self.get_config().ai


def get_config_manager(project_path: Path | None = None) -> ConfigManager:
    """Get a configuration manager instance.

    Args:
        project_path: Optional project path

    Returns:
        ConfigManager instance
    """
    return ConfigManager(project_path)


def get_ai_config(project_path: Path | None = None) -> AIConfig:
    """Get AI configuration for a project.

    Args:
        project_path: Optional project path

    Returns:
        AI configuration
    """
    config_manager = get_config_manager(project_path)
    return config_manager.get_ai_config()


def create_default_ai_config() -> AIConfig:
    """Create default AI configuration.

    Returns:
        Default AI configuration
    """
    return AIConfig(
        provider=AIProviderType.CLAUDE_CODE,
        model="claude-code",
        api_key=None,
        api_key_env="ANTHROPIC_API_KEY",
        base_url=None,
        max_tokens=4000,
        temperature=0.7,
        timeout=60,
    )
