"""Tests for AI service abstraction."""

from pathlib import Path
from unittest.mock import patch

import pytest

from cci.services import (
    AIConfig,
    AIMessage,
    AIProviderType,
    AIResponse,
    AIService,
    AIServiceError,
    AIServiceFactory,
    ContextFile,
    MessageRole,
    PromptContext,
    create_ai_service,
)


class TestAIConfig:
    """Test AI configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = AIConfig()
        assert config.provider == AIProviderType.CLAUDE_CODE
        assert config.model == "claude-code"
        assert config.api_key_env == "ANTHROPIC_API_KEY"
        assert config.max_tokens == 4000
        assert config.temperature == 0.7
        assert config.timeout == 60

    def test_get_api_key_from_config(self):
        """Test getting API key from config."""
        config = AIConfig(api_key="test-key")
        assert config.get_api_key() == "test-key"

    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "env-key"})
    def test_get_api_key_from_env(self):
        """Test getting API key from environment."""
        config = AIConfig()
        assert config.get_api_key() == "env-key"

    @patch.dict("os.environ", {"CUSTOM_KEY": "custom-key"})
    def test_get_api_key_custom_env(self):
        """Test getting API key from custom environment variable."""
        config = AIConfig(api_key_env="CUSTOM_KEY")
        assert config.get_api_key() == "custom-key"

    def test_get_api_key_none(self):
        """Test getting API key when not set."""
        config = AIConfig()
        with patch.dict("os.environ", {}, clear=True):
            assert config.get_api_key() is None


class TestAIMessage:
    """Test AI message model."""

    def test_create_user_message(self):
        """Test creating user message."""
        message = AIMessage(
            role=MessageRole.USER,
            content="Hello",
            metadata={"source": "test"}
        )
        assert message.role == MessageRole.USER
        assert message.content == "Hello"
        assert message.metadata["source"] == "test"

    def test_create_assistant_message(self):
        """Test creating assistant message."""
        message = AIMessage(
            role=MessageRole.ASSISTANT,
            content="Hi there!"
        )
        assert message.role == MessageRole.ASSISTANT
        assert message.content == "Hi there!"
        assert message.metadata == {}


class TestAIResponse:
    """Test AI response model."""

    def test_create_response(self):
        """Test creating AI response."""
        response = AIResponse(
            content="Hello world",
            model="test-model",
            usage={"tokens": 10},
            metadata={"id": "test"}
        )
        assert response.content == "Hello world"
        assert response.model == "test-model"
        assert response.usage["tokens"] == 10
        assert response.metadata["id"] == "test"


class TestContextFile:
    """Test context file model."""

    def test_create_context_file(self):
        """Test creating context file."""
        file = ContextFile(
            path=Path("test.py"),
            content="print('hello')",
            language="python",
            truncated=False
        )
        assert file.path == Path("test.py")
        assert file.content == "print('hello')"
        assert file.language == "python"
        assert not file.truncated


class TestPromptContext:
    """Test prompt context model."""

    def test_create_context(self):
        """Test creating prompt context."""
        context = PromptContext(
            project_path=Path("/test/project"),
            files=[
                ContextFile(path=Path("main.py"), content="# main", language="python"),
                ContextFile(path=Path("README.md"), content="# Project", language="markdown"),
            ],
            git_branch="main",
            git_status="M main.py",
        )
        assert context.project_path == Path("/test/project")
        assert len(context.files) == 2
        assert context.git_branch == "main"
        assert context.git_status == "M main.py"

    def test_context_summary(self):
        """Test context summary generation."""
        context = PromptContext(
            project_path=Path("/test/myproject"),
            files=[ContextFile(path=Path("test.py"), content="test", language="python")],
            git_branch="feature",
        )
        summary = context.get_context_summary()
        assert "Project: myproject" in summary
        assert "Files: 1" in summary
        assert "Branch: feature" in summary

    def test_total_content_size(self):
        """Test total content size calculation."""
        context = PromptContext(
            files=[
                ContextFile(path=Path("a.py"), content="hello", language="python"),  # 5 chars
                ContextFile(path=Path("b.py"), content="world!", language="python"),  # 6 chars
            ]
        )
        assert context.get_total_content_size() == 11


class MockAIService(AIService):
    """Mock AI service for testing."""

    async def generate_response(self, messages, system_prompt=None, **kwargs):
        """Mock response generation."""
        content = "Mock response"
        if messages and messages[0].content:
            content = f"Echo: {messages[0].content}"

        return AIResponse(
            content=content,
            model="mock-model",
            usage={"tokens": 10},
            metadata={"mock": True}
        )

    async def validate_connection(self):
        """Mock connection validation."""
        return True


class TestAIServiceFactory:
    """Test AI service factory."""

    def test_register_service(self):
        """Test registering a service."""
        # Register mock service
        AIServiceFactory.register_service(AIProviderType.LOCAL, MockAIService)

        # Check it's registered
        available = AIServiceFactory.get_available_providers()
        assert AIProviderType.LOCAL in available

    def test_create_service(self):
        """Test creating a service."""
        # Register mock service
        AIServiceFactory.register_service(AIProviderType.LOCAL, MockAIService)

        # Create service
        config = AIConfig(provider=AIProviderType.LOCAL)
        service = AIServiceFactory.create_service(config)

        assert isinstance(service, MockAIService)
        assert service.config == config

    def test_create_service_unknown_provider(self):
        """Test creating service with unknown provider."""
        # Create a valid config and then modify it to have an unregistered provider
        config = AIConfig(provider=AIProviderType.LOCAL)  # Use a valid enum value

        # Clear the factory's registered services to simulate unknown provider
        original_services = AIServiceFactory._services.copy()
        AIServiceFactory._services = {}

        try:
            with pytest.raises(ValueError, match="Unsupported AI provider"):
                AIServiceFactory.create_service(config)
        finally:
            # Restore original services
            AIServiceFactory._services = original_services


class TestAIService:
    """Test AI service base class."""

    @pytest.fixture
    def service(self):
        """Create mock AI service."""
        config = AIConfig()
        return MockAIService(config)

    @pytest.mark.asyncio
    async def test_generate_response(self, service):
        """Test generating response."""
        messages = [AIMessage(role=MessageRole.USER, content="Hello")]
        response = await service.generate_response(messages)

        assert response.content == "Echo: Hello"
        assert response.model == "mock-model"
        assert response.usage["tokens"] == 10

    @pytest.mark.asyncio
    async def test_validate_connection(self, service):
        """Test connection validation."""
        result = await service.validate_connection()
        assert result is True

    def test_create_user_message(self, service):
        """Test creating user message."""
        message = service.create_user_message("test", source="unit-test")
        assert message.role == MessageRole.USER
        assert message.content == "test"
        assert message.metadata["source"] == "unit-test"

    def test_create_system_message(self, service):
        """Test creating system message."""
        message = service.create_system_message("system prompt")
        assert message.role == MessageRole.SYSTEM
        assert message.content == "system prompt"


def test_create_ai_service():
    """Test create_ai_service helper function."""
    # Register mock service first
    AIServiceFactory.register_service(AIProviderType.LOCAL, MockAIService)

    config = AIConfig(provider=AIProviderType.LOCAL)
    service = create_ai_service(config)

    assert isinstance(service, MockAIService)
    assert service.config == config


class TestAIServiceErrors:
    """Test AI service error classes."""

    def test_ai_service_error(self):
        """Test base AI service error."""
        error = AIServiceError("Test error", provider="test")
        assert str(error) == "Test error"
        assert error.provider == "test"
        assert error.original_error is None

    def test_ai_service_error_with_original(self):
        """Test AI service error with original exception."""
        original = ValueError("Original error")
        error = AIServiceError("Test error", provider="test", original_error=original)

        assert str(error) == "Test error"
        assert error.provider == "test"
        assert error.original_error == original
