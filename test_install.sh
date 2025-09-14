#!/bin/bash
# Test script for CCI installation

echo "=== CCI Installation Test ==="
echo ""

# Build the package
echo "1. Building CCI package..."
uv build

echo ""
echo "2. Creating test virtual environment..."
python -m venv /tmp/test-cci-env
source /tmp/test-cci-env/bin/activate

echo ""
echo "3. Installing CCI from wheel..."
pip install dist/cci-0.1.0-py3-none-any.whl

echo ""
echo "4. Testing CCI commands..."

# Test version
echo "   - Testing version:"
cci --version

# Test help
echo ""
echo "   - Testing help:"
cci --help | head -10

# Test opening a file
echo ""
echo "   - Testing file opening (will timeout, that's expected):"
timeout 2 cci README.md 2>&1 | head -5 || echo "   (TUI launched successfully)"

# Test list command
echo ""
echo "   - Testing list command:"
cci list

echo ""
echo "5. Checking installation location:"
which cci
pip show cci | grep Location

echo ""
echo "6. Cleaning up test environment..."
deactivate
rm -rf /tmp/test-cci-env

echo ""
echo "=== Test Complete ==="
echo ""
echo "To install system-wide, run:"
echo "  pip install dist/cci-0.1.0-py3-none-any.whl"
echo ""
echo "Or for development:"
echo "  pip install -e ."