# Installation

## Prerequisites

- Python 3.12 or higher
- Git
- A Unix-like operating system (macOS, Linux)

## Install UV

CCI uses UV for package management. Install it first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or using pip:

```bash
pip install uv
```

## Clone Repository

```bash
git clone https://github.com/example/cci.git
cd cci
```

## Install Dependencies

### For Users

```bash
# Install CCI and its dependencies
uv sync
```

### For Developers

```bash
# Install with development dependencies
uv sync --all-extras
```

### For Documentation

```bash
# Install with documentation dependencies
uv sync --extra docs
```

## Verify Installation

```bash
# Check version
uv run cci --version

# Run help
uv run cci --help
```

## System-wide Installation

To install CCI system-wide:

```bash
# Build the package
uv build

# Install with pip
pip install dist/cci-*.whl
```

Then you can use `cci` directly:

```bash
cci --version
```

## Troubleshooting

### Python Version

Ensure you have Python 3.12+:

```bash
python --version
```

### UV Issues

If UV isn't working, try:

```bash
# Clear UV cache
uv cache clean

# Reinstall
uv sync --refresh
```

### Permission Errors

On macOS/Linux, you might need to add UV to your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Next Steps

- Follow the [Quick Start](quickstart.md) guide
- Configure CCI with [Configuration](configuration.md)
- Learn about [Project Management](../user-guide/projects.md)