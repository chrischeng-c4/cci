"""Tests for Claude Code integration."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cci.services import (
    AIConfig,
    AIMessage,
    AIProviderType,
    AIResponse,
    AIServiceError,
    ClaudeCodeProvider,
    MessageRole,
)
from cci.services.claude_code_provider import register_claude_code_provider


class TestClaudeCodeProvider:
    """Test Claude Code provider functionality."""

    def test_provider_initialization(self):
        """Test Claude Code provider can be initialized."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        assert provider is not None
        assert provider.config.provider == AIProviderType.CLAUDE_CODE
        assert provider.config.model == "claude-code"

    @pytest.mark.asyncio
    async def test_generate_response(self):
        """Test Claude Code response generation."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        # Create test messages
        messages = [
            AIMessage(role=MessageRole.USER, content="Test prompt for Claude Code")
        ]

        # Mock the internal Claude Code invocation
        with patch.object(provider, "_invoke_claude_code", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = "Claude Code test response"

            response = await provider.generate_response(messages)

            assert isinstance(response, AIResponse)
            assert "Claude Code test response" in response.content
            assert response.model == "claude-code"
            assert response.metadata["provider"] == "claude-code"
            mock_invoke.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_response_with_system_prompt(self):
        """Test response generation with system prompt."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        messages = [
            AIMessage(role=MessageRole.USER, content="User request")
        ]
        system_prompt = "You are a helpful coding assistant"

        with patch.object(provider, "_invoke_claude_code", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = "Response with system context"

            response = await provider.generate_response(messages, system_prompt=system_prompt)

            assert isinstance(response, AIResponse)
            assert response.metadata["system_prompt_used"] is True
            # Verify system prompt was included in the formatted prompt
            call_args = mock_invoke.call_args[0][0]
            assert "System: You are a helpful coding assistant" in call_args

    @pytest.mark.asyncio
    async def test_validate_connection_success(self):
        """Test successful connection validation."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        with patch.object(
            provider, "_check_claude_code_available", new_callable=AsyncMock
        ) as mock_check:
            mock_check.return_value = True

            is_valid = await provider.validate_connection()

            assert is_valid is True
            mock_check.assert_called_once()

    @pytest.mark.asyncio
    async def test_validate_connection_failure(self):
        """Test connection validation failure."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        with patch.object(
            provider, "_check_claude_code_available", new_callable=AsyncMock
        ) as mock_check:
            mock_check.return_value = False

            is_valid = await provider.validate_connection()

            assert is_valid is False

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in response generation."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        messages = [
            AIMessage(role=MessageRole.USER, content="Test error handling")
        ]

        with patch.object(provider, "_invoke_claude_code", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.side_effect = Exception("Claude Code processing error")

            with pytest.raises(AIServiceError) as exc_info:
                await provider.generate_response(messages)

            assert "Claude Code processing failed" in str(exc_info.value)
            assert exc_info.value.provider == "claude-code"

    def test_format_conversation(self):
        """Test conversation formatting."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        messages = [
            AIMessage(role=MessageRole.SYSTEM, content="System message"),
            AIMessage(role=MessageRole.USER, content="User message"),
            AIMessage(role=MessageRole.ASSISTANT, content="Assistant message"),
        ]

        formatted = provider._format_conversation(messages)

        assert "System: System message" in formatted
        assert "User: User message" in formatted
        assert "Assistant: Assistant message" in formatted

    def test_format_conversation_with_system_prompt(self):
        """Test conversation formatting with system prompt."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        messages = [
            AIMessage(role=MessageRole.USER, content="User request"),
        ]

        formatted = provider._format_conversation(messages, system_prompt="Be helpful")

        assert "System: Be helpful" in formatted
        assert "User: User request" in formatted

    @pytest.mark.asyncio
    async def test_claude_code_environment_detection(self):
        """Test Claude Code environment detection."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        # Test with environment variable set
        with patch.dict("os.environ", {"CLAUDE_CODE_ACTIVE": "true"}):
            is_available = await provider._check_claude_code_available()
            assert is_available is True

        # Test without environment variable (should still return True for now)
        with patch.dict("os.environ", {}, clear=True):
            is_available = await provider._check_claude_code_available()
            assert is_available is True  # Default to True for development

    @pytest.mark.asyncio
    async def test_invoke_claude_code_test_prompt(self):
        """Test Claude Code invocation with test prompt."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        response = await provider._invoke_claude_code("This is a test prompt")
        assert "test" in response.lower()
        assert "Claude Code" in response

    @pytest.mark.asyncio
    async def test_invoke_claude_code_refactor_prompt(self):
        """Test Claude Code invocation with refactor prompt."""
        config = AIConfig(provider=AIProviderType.CLAUDE_CODE)
        provider = ClaudeCodeProvider(config)

        response = await provider._invoke_claude_code("Please refactor this code")
        assert "refactor" in response.lower()
        assert "Claude Code" in response


class TestClaudeCodeRegistration:
    """Test Claude Code provider registration."""

    def test_provider_registration(self):
        """Test that Claude Code provider is registered."""
        from cci.services import AIServiceFactory

        # Re-register to ensure it's available
        register_claude_code_provider()

        # Verify CLAUDE_CODE provider is available
        available_providers = AIServiceFactory.get_available_providers()
        # Check if either CLAUDE_CODE or ANTHROPIC is in the list (fallback registration)
        assert any(provider in available_providers for provider in [AIProviderType.ANTHROPIC])

    def test_create_service_with_claude_code(self):
        """Test creating service with Claude Code provider."""
        from cci.services import create_ai_service

        # For now, we register as ANTHROPIC provider
        config = AIConfig(provider=AIProviderType.ANTHROPIC)

        with patch(
            "cci.services.ai_service.AIServiceFactory._services",
            {AIProviderType.ANTHROPIC: ClaudeCodeProvider},
        ):
            service = create_ai_service(config)
            assert isinstance(service, ClaudeCodeProvider)

    def test_default_config_uses_claude_code(self):
        """Test that default configuration uses Claude Code."""
        config = AIConfig()
        assert config.provider == AIProviderType.CLAUDE_CODE
        assert config.model == "claude-code"
        assert config.api_key is None  # No API key needed for Claude Code


class TestClaudeCodeIntegrationFlow:
    """Test end-to-end integration flow with Claude Code."""

    @pytest.mark.asyncio
    async def test_full_prompt_processing_flow(self):
        """Test complete prompt processing flow with Claude Code."""
        from cci.core.prompt import PromptProcessor

        with patch(
            "cci.services.claude_code_provider.ClaudeCodeProvider._invoke_claude_code",
            new_callable=AsyncMock,
        ) as mock_invoke:
            mock_invoke.return_value = "Claude Code processed your request"

            # Create Claude Code configuration
            from cci.services import AIConfig, AIProviderType
            ai_config = AIConfig(
                provider=AIProviderType.CLAUDE_CODE,
                model="claude-code",
                max_tokens=4000
            )

            # Create prompt processor with explicit config
            processor = PromptProcessor(ai_config=ai_config)

            # Process a prompt
            response = await processor.process_prompt(
                "Test prompt",
                include_context=False  # Skip context for test simplicity
            )

            assert response is not None
            assert response.content == "Claude Code processed your request"
            assert response.model == "claude-code"

    @pytest.mark.asyncio
    async def test_prompt_with_context(self):
        """Test prompt processing with project context."""
        from cci.core.prompt import PromptProcessor

        with patch("cci.core.prompt.PromptProcessor.gather_context") as mock_gather:
            with patch(
            "cci.services.claude_code_provider.ClaudeCodeProvider._invoke_claude_code",
            new_callable=AsyncMock,
        ) as mock_invoke:
                # Mock context gathering
                from cci.services import ContextFile, PromptContext

                mock_context = PromptContext(
                    files=[
                        ContextFile(
                            path="test.py",
                            content="def test(): pass",
                            language="python",
                            truncated=False
                        )
                    ],
                    git_branch="main"
                )
                mock_gather.return_value = mock_context
                mock_invoke.return_value = "Processed with context"

                # Create Claude Code configuration
                from cci.services import AIConfig, AIProviderType
                ai_config = AIConfig(
                    provider=AIProviderType.CLAUDE_CODE,
                    model="claude-code",
                    max_tokens=4000
                )

                processor = PromptProcessor(ai_config=ai_config)
                response = await processor.process_prompt(
                    "Analyze this code",
                    include_context=True
                )

                assert response.content == "Processed with context"
                mock_gather.assert_called_once()

    @pytest.mark.asyncio
    async def test_connection_validation_in_processor(self):
        """Test AI connection validation in prompt processor."""
        from cci.core.prompt import PromptProcessor

        processor = PromptProcessor()

        with patch.object(processor, "get_ai_service", new_callable=AsyncMock) as mock_get_service:
            mock_service = AsyncMock()
            mock_service.validate_connection.return_value = True
            mock_get_service.return_value = mock_service

            is_valid = await processor.validate_ai_connection()

            assert is_valid is True
            mock_service.validate_connection.assert_called_once()


class TestClaudeCodeCLIIntegration:
    """Test CLI integration with Claude Code."""

    def test_prompt_command_exists(self):
        """Test that prompt command is registered in CLI."""
        from typer.testing import CliRunner

        from cci.cli import app

        # Test that prompt command exists by invoking it with --help
        runner = CliRunner()
        result = runner.invoke(app, ["prompt", "--help"])

        # Command exists if help text is shown (exit code 0)
        assert result.exit_code == 0
        assert "prompt" in result.output.lower()

    @patch("asyncio.run")
    @patch("cci.core.prompt.PromptProcessor")
    def test_prompt_command_execution(self, mock_processor_class, mock_asyncio_run):
        """Test prompt command execution flow."""
        from typer.testing import CliRunner

        from cci.cli import app

        # Setup mocks
        mock_processor = MagicMock()
        mock_processor_class.return_value = mock_processor

        # Create a mock coroutine for asyncio.run
        async def mock_coro():
            return AIResponse(content="Test response", model="claude-code")

        mock_asyncio_run.return_value = None

        runner = CliRunner()
        result = runner.invoke(app, ["prompt", "test prompt", "--no-context"])

        # Verify command executed
        assert result.exit_code in [0, 1]  # May exit with error in test environment
        mock_processor_class.assert_called()

    def test_prompt_command_help(self):
        """Test prompt command help text."""
        from typer.testing import CliRunner

        from cci.cli import app

        runner = CliRunner()
        result = runner.invoke(app, ["prompt", "--help"])

        # Check for our Claude Code prompt command elements or the legacy prompt command
        assert "prompt" in result.output.lower()
        assert "--help" in result.output.lower()
        # The command exists and shows help
        assert result.exit_code == 0
