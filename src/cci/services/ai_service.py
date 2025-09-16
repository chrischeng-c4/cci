"""AI service abstraction layer for CCI."""

import os
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class AIProviderType(str, Enum):
    """Supported AI provider types."""

    CLAUDE_CODE = "claude-code"  # Default - native Claude Code integration
    ANTHROPIC = "anthropic"      # Standalone Anthropic API
    OPENAI = "openai"            # OpenAI API
    LOCAL = "local"              # Local model


class MessageRole(str, Enum):
    """Message roles for AI conversation."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AIMessage(BaseModel):
    """Represents a message in an AI conversation."""

    role: MessageRole = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The content of the message")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AIResponse(BaseModel):
    """Response from an AI service."""

    content: str = Field(..., description="The AI's response content")
    model: str | None = Field(None, description="The model used for the response")
    usage: dict[str, Any] = Field(default_factory=dict, description="Usage statistics")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional response metadata"
    )


class AIConfig(BaseModel):
    """Configuration for AI services."""

    provider: AIProviderType = Field(
        AIProviderType.CLAUDE_CODE, description="AI provider to use (default: Claude Code)"
    )
    model: str = Field("claude-code", description="Model to use (managed by Claude Code)")
    api_key: str | None = Field(None, description="API key (not needed for Claude Code)")
    api_key_env: str = Field(
        "ANTHROPIC_API_KEY", description="Environment variable for API key (legacy)"
    )
    base_url: str | None = Field(None, description="Base URL for API (for custom endpoints)")
    max_tokens: int = Field(4000, description="Maximum tokens for responses")
    temperature: float = Field(0.7, description="Temperature for response generation")
    timeout: int = Field(60, description="Request timeout in seconds")

    def get_api_key(self) -> str | None:
        """Get the API key from config or environment."""
        if self.api_key:
            return self.api_key
        return os.getenv(self.api_key_env)


class AIService(ABC):
    """Abstract base class for AI services."""

    def __init__(self, config: AIConfig) -> None:
        """Initialize the AI service with configuration.

        Args:
            config: AI service configuration
        """
        self.config = config

    @abstractmethod
    async def generate_response(
        self,
        messages: list[AIMessage],
        system_prompt: str | None = None,
        **kwargs: Any
    ) -> AIResponse:
        """Generate a response from the AI service.

        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            **kwargs: Additional parameters for the AI service

        Returns:
            AI response

        Raises:
            AIServiceError: If the service request fails
        """
        pass

    @abstractmethod
    async def validate_connection(self) -> bool:
        """Validate that the AI service is accessible.

        Returns:
            True if the service is accessible, False otherwise
        """
        pass

    def create_user_message(self, content: str, **metadata: Any) -> AIMessage:
        """Create a user message.

        Args:
            content: Message content
            **metadata: Additional metadata

        Returns:
            AIMessage instance
        """
        return AIMessage(role=MessageRole.USER, content=content, metadata=metadata)

    def create_system_message(self, content: str, **metadata: Any) -> AIMessage:
        """Create a system message.

        Args:
            content: Message content
            **metadata: Additional metadata

        Returns:
            AIMessage instance
        """
        return AIMessage(role=MessageRole.SYSTEM, content=content, metadata=metadata)


class AIServiceError(Exception):
    """Base exception for AI service errors."""

    def __init__(
        self,
        message: str,
        provider: str | None = None,
        original_error: Exception | None = None,
    ) -> None:
        """Initialize the error.

        Args:
            message: Error message
            provider: AI provider name
            original_error: Original exception that caused this error
        """
        super().__init__(message)
        self.provider = provider
        self.original_error = original_error


class AIServiceConnectionError(AIServiceError):
    """Exception raised when AI service connection fails."""
    pass


class AIServiceRateLimitError(AIServiceError):
    """Exception raised when AI service rate limit is exceeded."""
    pass


class AIServiceAuthenticationError(AIServiceError):
    """Exception raised when AI service authentication fails."""
    pass


class AIServiceFactory:
    """Factory for creating AI service instances."""

    _services: dict[AIProviderType, type[AIService]] = {}

    @classmethod
    def register_service(cls, provider: AIProviderType, service_class: type[AIService]) -> None:
        """Register an AI service implementation.

        Args:
            provider: Provider type
            service_class: Service class to register
        """
        cls._services[provider] = service_class

    @classmethod
    def create_service(cls, config: AIConfig) -> AIService:
        """Create an AI service instance.

        Args:
            config: AI service configuration

        Returns:
            AI service instance

        Raises:
            ValueError: If provider is not supported
        """
        if config.provider not in cls._services:
            raise ValueError(f"Unsupported AI provider: {config.provider}")

        service_class = cls._services[config.provider]
        return service_class(config)

    @classmethod
    def get_available_providers(cls) -> list[AIProviderType]:
        """Get list of available providers.

        Returns:
            List of available provider types
        """
        return list(cls._services.keys())


class ContextFile(BaseModel):
    """Represents a file to be included in AI context."""

    path: Path = Field(..., description="Path to the file")
    content: str = Field(..., description="File content")
    language: str | None = Field(None, description="Programming language")
    truncated: bool = Field(False, description="Whether content was truncated")
    max_lines: int | None = Field(None, description="Maximum lines included")


class PromptContext(BaseModel):
    """Context information for AI prompts."""

    project_path: Path | None = Field(None, description="Project root path")
    files: list[ContextFile] = Field(default_factory=list, description="Files included in context")
    working_directory: Path | None = Field(None, description="Current working directory")
    git_branch: str | None = Field(None, description="Current git branch")
    git_status: str | None = Field(None, description="Git status output")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional context metadata"
    )

    def get_context_summary(self) -> str:
        """Get a summary of the context.

        Returns:
            Context summary string
        """
        summary_parts = []

        if self.project_path:
            summary_parts.append(f"Project: {self.project_path.name}")

        if self.files:
            summary_parts.append(f"Files: {len(self.files)}")

        if self.git_branch:
            summary_parts.append(f"Branch: {self.git_branch}")

        return " | ".join(summary_parts) if summary_parts else "No context"

    def get_total_content_size(self) -> int:
        """Get total size of all file contents.

        Returns:
            Total content size in characters
        """
        return sum(len(file.content) for file in self.files)


def create_ai_service(config: AIConfig) -> AIService:
    """Create an AI service instance.

    Args:
        config: AI service configuration

    Returns:
        AI service instance
    """
    return AIServiceFactory.create_service(config)
