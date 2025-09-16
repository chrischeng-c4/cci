"""Tests for prompt processing system."""

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from cci.core.prompt import PromptProcessor, create_prompt_processor, process_simple_prompt
from cci.services import AIConfig, AIMessage, AIResponse, ContextFile, MessageRole, PromptContext


class TestPromptProcessor:
    """Test prompt processor."""

    @pytest.fixture
    def temp_project(self, tmp_path):
        """Create temporary project structure."""
        project = tmp_path / "test_project"
        project.mkdir()

        # Create some test files
        (project / "main.py").write_text("print('Hello, world!')")
        (project / "README.md").write_text("# Test Project\n\nA test project.")
        (project / "requirements.txt").write_text("requests>=2.0.0\nclick>=8.0.0")

        # Create subdirectory
        subdir = project / "src"
        subdir.mkdir()
        (subdir / "utils.py").write_text("def helper(): pass")

        # Create files to exclude
        cache_dir = project / "__pycache__"
        cache_dir.mkdir()
        (cache_dir / "main.cpython-39.pyc").write_text("compiled")

        return project

    @pytest.fixture
    def ai_config(self):
        """Create test AI config."""
        return AIConfig(api_key="test-key")

    @pytest.fixture
    def processor(self, temp_project, ai_config):
        """Create prompt processor."""
        return PromptProcessor(temp_project, ai_config)

    def test_init(self, temp_project, ai_config):
        """Test processor initialization."""
        processor = PromptProcessor(temp_project, ai_config)

        assert processor.project_path == temp_project.resolve()
        assert processor.ai_config == ai_config
        assert processor.ai_service is None

    def test_init_default_path(self, ai_config):
        """Test processor initialization with default path."""
        with patch('pathlib.Path.cwd') as mock_cwd:
            mock_cwd.return_value = Path("/test/path")
            processor = PromptProcessor(ai_config=ai_config)

            assert processor.project_path == Path("/test/path")

    @pytest.mark.asyncio
    @patch('cci.core.prompt.create_ai_service')
    async def test_get_ai_service(self, mock_create, processor):
        """Test getting AI service."""
        mock_service = AsyncMock()
        mock_create.return_value = mock_service

        service = await processor.get_ai_service()

        assert service == mock_service
        assert processor.ai_service == mock_service
        mock_create.assert_called_once_with(processor.ai_config)

        # Second call should return cached service
        service2 = await processor.get_ai_service()
        assert service2 == mock_service
        assert mock_create.call_count == 1

    def test_gather_context_default(self, processor, temp_project):
        """Test gathering context with defaults."""
        context = processor.gather_context()

        assert context.project_path == temp_project
        assert len(context.files) > 0

        # Should include Python and Markdown files
        file_paths = [f.path for f in context.files]
        assert Path("main.py") in file_paths
        assert Path("README.md") in file_paths

        # Should not include cache files
        cache_files = [f for f in context.files if "__pycache__" in str(f.path)]
        assert len(cache_files) == 0

    def test_gather_context_patterns(self, processor):
        """Test gathering context with custom patterns."""
        context = processor.gather_context(
            include_patterns=["*.py"],
            exclude_patterns=["src/*"]
        )

        file_paths = [f.path for f in context.files]

        # Should include main.py but not utils.py (in src/)
        assert Path("main.py") in file_paths
        assert Path("src/utils.py") not in file_paths
        assert Path("README.md") not in file_paths

    def test_gather_context_max_files(self, processor):
        """Test gathering context with file limit."""
        context = processor.gather_context(max_files=1)

        assert len(context.files) == 1

    @patch('cci.core.prompt.get_current_branch')
    @patch('cci.core.prompt.get_git_status_string')
    def test_gather_context_git_info(self, mock_status, mock_branch, processor):
        """Test gathering context with git information."""
        mock_branch.return_value = "feature-branch"
        mock_status.return_value = "M main.py\nA new_file.py"

        context = processor.gather_context()

        assert context.git_branch == "feature-branch"
        assert context.git_status == "M main.py\nA new_file.py"

    def test_read_context_file(self, processor, temp_project):
        """Test reading context file."""
        test_file = temp_project / "test.py"
        test_file.write_text("# Test file\nprint('test')")

        context_file = processor._read_context_file(test_file)

        assert context_file is not None
        assert context_file.path == Path("test.py")
        assert context_file.content == "# Test file\nprint('test')"
        assert context_file.language == "python"
        assert not context_file.truncated

    def test_read_context_file_truncated(self, processor, temp_project):
        """Test reading context file with truncation."""
        test_file = temp_project / "large.py"
        lines = [f"# Line {i}\n" for i in range(1000)]  # 1000 lines
        test_file.write_text("".join(lines))

        context_file = processor._read_context_file(test_file, max_lines=100)

        assert context_file is not None
        assert context_file.truncated
        assert context_file.max_lines == 100
        assert context_file.content.count('\n') == 100

    def test_read_context_file_error(self, processor):
        """Test reading non-existent file."""
        context_file = processor._read_context_file(Path("/nonexistent/file.py"))
        assert context_file is None

    def test_create_context_prompt(self, processor, temp_project):
        """Test creating context prompt."""
        context = PromptContext(
            project_path=temp_project,
            files=[
                ContextFile(
                    path=Path("main.py"),
                    content="print('hello')",
                    language="python"
                )
            ],
            git_branch="main",
            git_status="M main.py"
        )

        prompt = processor.create_context_prompt(context)

        assert f"Project: {temp_project.name}" in prompt
        assert f"Project Path: {temp_project}" in prompt
        assert "Git Branch: main" in prompt
        assert "M main.py" in prompt
        assert "### main.py" in prompt
        assert "```python" in prompt
        assert "print('hello')" in prompt

    def test_create_context_prompt_empty(self, processor):
        """Test creating context prompt with minimal context."""
        context = PromptContext()
        prompt = processor.create_context_prompt(context)

        # Should not crash and return something
        assert isinstance(prompt, str)

    @pytest.mark.asyncio
    @patch('cci.core.prompt.create_ai_service')
    async def test_process_prompt_with_context(self, mock_create, processor):
        """Test processing prompt with context."""
        mock_service = AsyncMock()
        mock_response = AIResponse(
            content="Test response",
            model="test-model",
            usage={"tokens": 10}
        )
        mock_service.generate_response.return_value = mock_response
        mock_create.return_value = mock_service

        response = await processor.process_prompt("Test prompt", include_context=True)

        assert response == mock_response
        mock_service.generate_response.assert_called_once()

        # Check that context was included
        call_args = mock_service.generate_response.call_args
        messages = call_args[1]["messages"]
        assert len(messages) == 1
        assert "Test prompt" in messages[0].content
        # Should include some context
        assert len(messages[0].content) > len("Test prompt")

    @pytest.mark.asyncio
    @patch('cci.core.prompt.create_ai_service')
    async def test_process_prompt_without_context(self, mock_create, processor):
        """Test processing prompt without context."""
        mock_service = AsyncMock()
        mock_response = AIResponse(content="Test response", model="test")
        mock_service.generate_response.return_value = mock_response
        mock_create.return_value = mock_service

        response = await processor.process_prompt("Test prompt", include_context=False)

        assert response == mock_response

        # Check that only the prompt was sent
        call_args = mock_service.generate_response.call_args
        messages = call_args[1]["messages"]
        assert len(messages) == 1
        assert messages[0].content == "Test prompt"

    @pytest.mark.asyncio
    @patch('cci.core.prompt.create_ai_service')
    async def test_chat(self, mock_create, processor):
        """Test chat functionality."""
        mock_service = AsyncMock()
        mock_response = AIResponse(content="Chat response", model="test")
        mock_service.generate_response.return_value = mock_response
        mock_create.return_value = mock_service

        messages = [
            AIMessage(role=MessageRole.USER, content="Hello"),
            AIMessage(role=MessageRole.ASSISTANT, content="Hi there!"),
            AIMessage(role=MessageRole.USER, content="How are you?"),
        ]

        response = await processor.chat(messages, system_prompt="Be helpful")

        assert response == mock_response
        mock_service.generate_response.assert_called_once_with(
            messages=messages,
            system_prompt="Be helpful"
        )

    @pytest.mark.asyncio
    @patch('cci.core.prompt.create_ai_service')
    async def test_validate_ai_connection(self, mock_create, processor):
        """Test AI connection validation."""
        mock_service = AsyncMock()
        mock_service.validate_connection.return_value = True
        mock_create.return_value = mock_service

        result = await processor.validate_ai_connection()

        assert result is True
        mock_service.validate_connection.assert_called_once()

    @pytest.mark.asyncio
    @patch('cci.core.prompt.create_ai_service')
    async def test_validate_ai_connection_error(self, mock_create, processor):
        """Test AI connection validation with error."""
        mock_create.side_effect = Exception("Connection failed")

        result = await processor.validate_ai_connection()

        assert result is False

    def test_create_user_message(self, processor):
        """Test creating user message."""
        message = processor.create_user_message("Test", source="test")

        assert message.role == MessageRole.USER
        assert message.content == "Test"
        assert message.metadata["source"] == "test"

    def test_create_assistant_message(self, processor):
        """Test creating assistant message."""
        message = processor.create_assistant_message("Response")

        assert message.role == MessageRole.ASSISTANT
        assert message.content == "Response"


def test_create_prompt_processor():
    """Test create_prompt_processor helper."""
    with patch('cci.config.get_ai_config') as mock_get_config:
        mock_config = AIConfig()
        mock_get_config.return_value = mock_config

        processor = create_prompt_processor(Path("/test"), mock_config)

        assert isinstance(processor, PromptProcessor)
        assert processor.project_path == Path("/test").resolve()
        assert processor.ai_config == mock_config


@pytest.mark.asyncio
@patch('cci.core.prompt.create_prompt_processor')
async def test_process_simple_prompt(mock_create):
    """Test process_simple_prompt helper."""
    mock_processor = AsyncMock()
    mock_response = AIResponse(content="Simple response", model="test")
    mock_processor.process_prompt.return_value = mock_response
    mock_create.return_value = mock_processor

    response = await process_simple_prompt("Test prompt", Path("/test"), include_context=False)

    assert response == mock_response
    mock_create.assert_called_once_with(Path("/test"))
    mock_processor.process_prompt.assert_called_once_with("Test prompt", include_context=False)
