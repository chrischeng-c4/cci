"""Configuration utility functions for CCI."""

import toml
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, ValidationError


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from a TOML file.

    Args:
        config_path: Path to the TOML configuration file

    Returns:
        Dictionary containing configuration data

    Raises:
        FileNotFoundError: If config file doesn't exist
        toml.TomlDecodeError: If config file is invalid TOML
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        return toml.load(f)


def save_config(config_path: Path, config: Dict[str, Any]) -> None:
    """Save configuration to a TOML file.

    Args:
        config_path: Path where to save the configuration
        config: Configuration dictionary to save
    """
    # Create parent directories if they don't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Filter out None values for TOML compatibility
    cleaned_config = _clean_config_for_toml(config)

    with open(config_path, "w") as f:
        toml.dump(cleaned_config, f)


def _clean_config_for_toml(config: Any) -> Any:
    """Recursively remove None values from config for TOML compatibility.

    Args:
        config: Configuration data to clean

    Returns:
        Cleaned configuration data
    """
    if isinstance(config, dict):
        return {k: _clean_config_for_toml(v) for k, v in config.items() if v is not None}
    elif isinstance(config, list):
        return [_clean_config_for_toml(item) for item in config if item is not None]
    else:
        return config


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple configuration dictionaries.

    Later configs override earlier ones.

    Args:
        *configs: Configuration dictionaries to merge

    Returns:
        Merged configuration dictionary
    """
    result = {}
    for config in configs:
        result = _deep_merge(result, config)
    return result


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries.

    Args:
        base: Base dictionary
        override: Dictionary with values to override

    Returns:
        Merged dictionary
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def validate_config(config: Dict[str, Any], model: type[BaseModel]) -> BaseModel:
    """Validate configuration against a Pydantic model.

    Args:
        config: Configuration dictionary to validate
        model: Pydantic model class to validate against

    Returns:
        Validated model instance

    Raises:
        ValidationError: If configuration is invalid
    """
    return model(**config)


def get_default_config_path() -> Path:
    """Get the default configuration file path.

    Returns:
        Path to the default config file (~/.config/cci/config.toml)
    """
    return Path.home() / ".config" / "cci" / "config.toml"


def get_project_config_path(project_path: Path) -> Path:
    """Get the project-specific configuration file path.

    Args:
        project_path: Path to the project directory

    Returns:
        Path to the project config file (.cci/config.toml)
    """
    return project_path / ".cci" / "config.toml"


def load_project_config(project_path: Path) -> Dict[str, Any]:
    """Load merged configuration for a project.

    Loads global config and merges with project-specific config.

    Args:
        project_path: Path to the project directory

    Returns:
        Merged configuration dictionary
    """
    configs = []

    # Load global config if it exists
    global_config_path = get_default_config_path()
    if global_config_path.exists():
        try:
            configs.append(load_config(global_config_path))
        except Exception:
            pass  # Ignore errors in global config

    # Load project config if it exists
    project_config_path = get_project_config_path(project_path)
    if project_config_path.exists():
        try:
            configs.append(load_config(project_config_path))
        except Exception:
            pass  # Ignore errors in project config

    # Return merged config or empty dict
    return merge_configs(*configs) if configs else {}


def create_default_config(path: Optional[Path] = None) -> None:
    """Create a default configuration file.

    Args:
        path: Path where to create the config file.
              If None, uses the default global config path.
    """
    if path is None:
        path = get_default_config_path()

    default_config = {
        "ui": {
            "theme": "monokai",
            "editor_mode": "normal",
            "show_line_numbers": True,
            "syntax_highlighting": True,
        },
        "git": {
            "default_branch": "main",
            "auto_fetch": False,
        },
        "performance": {
            "max_workers": 4,
            "cache_enabled": True,
            "cache_size_mb": 100,
        },
    }

    save_config(path, default_config)