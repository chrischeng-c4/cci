"""Tests for Anthropic provider."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from cci.services import (
    AIConfig,
    AIMessage,
    AIProviderType,
    AIServiceAuthenticationError,
    MessageRole,
)
from cci.services.anthropic_provider import AnthropicProvider


class TestAnthropicProvider:
    """Test Anthropic provider implementation."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return AIConfig(
            provider=AIProviderType.ANTHROPIC,
            model="claude-3-sonnet-20240229",
            api_key="test-key",
            max_tokens=1000,
            temperature=0.5,
        )

    def test_init_without_api_key(self):
        """Test initialization without API key fails."""
        config = AIConfig(provider=AIProviderType.ANTHROPIC)

        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(AIServiceAuthenticationError):
                AnthropicProvider(config)

    @patch("cci.services.anthropic_provider.AsyncAnthropic")
    def test_init_with_api_key(self, mock_anthropic, config):
        """Test initialization with API key."""
        provider = AnthropicProvider(config)

        assert provider.config == config
        mock_anthropic.assert_called_once_with(
            api_key="test-key",
            base_url=None,
            timeout=60,
        )

    @pytest.mark.asyncio
    @patch("cci.services.anthropic_provider.AsyncAnthropic")
    async def test_generate_response(self, mock_anthropic, config):
        """Test generating response."""
        # Setup mock
        mock_client = AsyncMock()
        mock_anthropic.return_value = mock_client

        mock_message = Mock()
        mock_message.id = "test-id"
        mock_message.model = "claude-3-sonnet-20240229"
        mock_message.role = "assistant"
        mock_message.content = [Mock(text="Hello world")]
        mock_message.usage = Mock(input_tokens=10, output_tokens=5)
        mock_message.stop_reason = "end_turn"

        mock_client.messages.create.return_value = mock_message

        # Create provider and test
        provider = AnthropicProvider(config)
        messages = [AIMessage(role=MessageRole.USER, content="Hello")]

        response = await provider.generate_response(messages)

        # Verify response
        assert response.content == "Hello world"
        assert response.model == "claude-3-sonnet-20240229"
        assert response.usage["input_tokens"] == 10
        assert response.usage["output_tokens"] == 5
        assert response.usage["total_tokens"] == 15
        assert response.metadata["id"] == "test-id"
        assert response.metadata["role"] == "assistant"
        assert response.metadata["stop_reason"] == "end_turn"

        # Verify API call
        mock_client.messages.create.assert_called_once_with(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=1000,
            temperature=0.5,
        )

    @pytest.mark.asyncio
    @patch("cci.services.anthropic_provider.AsyncAnthropic")
    async def test_generate_response_with_system_prompt(self, mock_anthropic, config):
        """Test generating response with system prompt."""
        # Setup mock
        mock_client = AsyncMock()
        mock_anthropic.return_value = mock_client

        mock_message = Mock()
        mock_message.id = "test-id"
        mock_message.model = "claude-3-sonnet-20240229"
        mock_message.role = "assistant"
        mock_message.content = [Mock(text="Response")]
        mock_message.usage = Mock(input_tokens=10, output_tokens=5)

        mock_client.messages.create.return_value = mock_message

        # Create provider and test
        provider = AnthropicProvider(config)
        messages = [AIMessage(role=MessageRole.USER, content="Hello")]
        system_prompt = "You are a helpful assistant."

        await provider.generate_response(messages, system_prompt=system_prompt)

        # Verify system prompt was included
        mock_client.messages.create.assert_called_once_with(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=1000,
            temperature=0.5,
            system="You are a helpful assistant.",
        )

    @pytest.mark.asyncio
    @patch("cci.services.anthropic_provider.AsyncAnthropic")
    async def test_generate_response_with_system_message(self, mock_anthropic, config):
        """Test generating response with system message in conversation."""
        # Setup mock
        mock_client = AsyncMock()
        mock_anthropic.return_value = mock_client

        mock_message = Mock()
        mock_message.content = [Mock(text="Response")]
        mock_message.model = "claude-3-sonnet-20240229"
        mock_message.id = "test-id"
        mock_message.role = "assistant"
        mock_message.usage = Mock(input_tokens=10, output_tokens=5)

        mock_client.messages.create.return_value = mock_message

        # Create provider and test
        provider = AnthropicProvider(config)
        messages = [
            AIMessage(role=MessageRole.SYSTEM, content="Be helpful"),
            AIMessage(role=MessageRole.USER, content="Hello"),
        ]

        await provider.generate_response(messages)

        # Verify system message was converted to system parameter
        mock_client.messages.create.assert_called_once_with(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=1000,
            temperature=0.5,
            system="Be helpful",
        )

    @pytest.mark.asyncio
    @patch("cci.services.anthropic_provider.AsyncAnthropic")
    async def test_generate_response_authentication_error(self, mock_anthropic, config):
        """Test handling authentication errors."""
        from anthropic import AuthenticationError

        from cci.services import AIServiceAuthenticationError

        # Setup mock
        mock_client = AsyncMock()
        mock_anthropic.return_value = mock_client

        # Create a mock response for the error
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.request = Mock()
        mock_response.headers = {}

        mock_client.messages.create.side_effect = AuthenticationError(
            message="Invalid API key",
            response=mock_response,
            body={"error": {"message": "Invalid API key", "type": "authentication_error"}}
        )

        # Create provider and test
        provider = AnthropicProvider(config)
        messages = [AIMessage(role=MessageRole.USER, content="Hello")]

        with pytest.raises(AIServiceAuthenticationError) as exc_info:
            await provider.generate_response(messages)

        assert "Anthropic authentication failed" in str(exc_info.value)
        assert exc_info.value.provider == "anthropic"

    @pytest.mark.asyncio
    @patch("cci.services.anthropic_provider.AsyncAnthropic")
    async def test_generate_response_rate_limit_error(self, mock_anthropic, config):
        """Test handling rate limit errors."""
        from anthropic import RateLimitError

        from cci.services import AIServiceRateLimitError

        # Setup mock
        mock_client = AsyncMock()
        mock_anthropic.return_value = mock_client

        # Create a mock response for the error
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.request = Mock()
        mock_response.headers = {}

        mock_client.messages.create.side_effect = RateLimitError(
            message="Rate limit exceeded",
            response=mock_response,
            body={"error": {"message": "Rate limit exceeded", "type": "rate_limit_error"}}
        )

        # Create provider and test
        provider = AnthropicProvider(config)
        messages = [AIMessage(role=MessageRole.USER, content="Hello")]

        with pytest.raises(AIServiceRateLimitError) as exc_info:
            await provider.generate_response(messages)

        assert "Anthropic rate limit exceeded" in str(exc_info.value)

    @pytest.mark.asyncio
    @patch("cci.services.anthropic_provider.AsyncAnthropic")
    async def test_generate_response_connection_error(self, mock_anthropic, config):
        """Test handling connection errors."""
        from anthropic import APIConnectionError

        from cci.services import AIServiceConnectionError

        # Setup mock
        mock_client = AsyncMock()
        mock_anthropic.return_value = mock_client

        # Create a mock request for the error
        mock_request = Mock()

        mock_client.messages.create.side_effect = APIConnectionError(
            message="Connection failed",
            request=mock_request
        )

        # Create provider and test
        provider = AnthropicProvider(config)
        messages = [AIMessage(role=MessageRole.USER, content="Hello")]

        with pytest.raises(AIServiceConnectionError) as exc_info:
            await provider.generate_response(messages)

        assert "Failed to connect to Anthropic API" in str(exc_info.value)

    @pytest.mark.asyncio
    @patch("cci.services.anthropic_provider.AsyncAnthropic")
    async def test_validate_connection_success(self, mock_anthropic, config):
        """Test successful connection validation."""
        # Setup mock
        mock_client = AsyncMock()
        mock_anthropic.return_value = mock_client

        mock_message = Mock()
        mock_message.content = [Mock(text="Hi")]
        mock_client.messages.create.return_value = mock_message

        # Create provider and test
        provider = AnthropicProvider(config)
        result = await provider.validate_connection()

        assert result is True
        mock_client.messages.create.assert_called_once()

    @pytest.mark.asyncio
    @patch("cci.services.anthropic_provider.AsyncAnthropic")
    async def test_validate_connection_failure(self, mock_anthropic, config):
        """Test failed connection validation."""
        # Setup mock
        mock_client = AsyncMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("Connection failed")

        # Create provider and test
        provider = AnthropicProvider(config)
        result = await provider.validate_connection()

        assert result is False

    def test_get_available_models(self):
        """Test getting available models."""
        models = AnthropicProvider.get_available_models()

        assert isinstance(models, list)
        assert len(models) > 0
        assert "claude-3-5-sonnet-20241022" in models
        assert "claude-3-opus-20240229" in models

    def test_get_default_model(self):
        """Test getting default model."""
        default = AnthropicProvider.get_default_model()
        assert default == "claude-3-5-sonnet-20241022"
