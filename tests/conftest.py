"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest

from cci.core.registry import ProjectRegistry


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_config_dir(temp_dir):
    """Create a temporary config directory."""
    config_dir = temp_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


@pytest.fixture
def test_registry(temp_config_dir):
    """Create a test project registry."""
    return ProjectRegistry(config_dir=temp_config_dir)


@pytest.fixture
def sample_project_dir(temp_dir):
    """Create a sample project directory with git."""
    project_dir = temp_dir / "sample_project"
    project_dir.mkdir(parents=True, exist_ok=True)

    # Initialize git repo
    import subprocess
    subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)

    # Create some files
    (project_dir / "README.md").write_text("# Sample Project")
    (project_dir / "main.py").write_text("print('Hello, World!')")

    return project_dir
