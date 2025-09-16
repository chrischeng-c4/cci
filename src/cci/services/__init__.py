"""External services integration for CCI."""

from .ai_service import (
    AIConfig,
    AIMessage,
    AIProviderType,
    AIResponse,
    AIService,
    AIServiceAuthenticationError,
    AIServiceConnectionError,
    AIServiceError,
    AIServiceFactory,
    AIServiceRateLimitError,
    ContextFile,
    MessageRole,
    PromptContext,
    create_ai_service,
)

# Import providers to register them
from .anthropic_provider import AnthropicProvider
from .claude_code_provider import ClaudeCodeProvider, register_claude_code_provider

# Register Claude Code provider
register_claude_code_provider()

__all__ = [
    "AIConfig",
    "AIMessage",
    "AIProviderType",
    "AIResponse",
    "AIService",
    "AIServiceError",
    "AIServiceAuthenticationError",
    "AIServiceConnectionError",
    "AIServiceRateLimitError",
    "AIServiceFactory",
    "AnthropicProvider",
    "ClaudeCodeProvider",
    "ContextFile",
    "MessageRole",
    "PromptContext",
    "create_ai_service",
]
