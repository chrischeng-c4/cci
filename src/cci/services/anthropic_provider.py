"""Anthropic Claude API provider for CCI."""

import logging
from typing import Any

import anthropic
from anthropic import AsyncAnthropic
from anthropic.types import Message, MessageParam

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
    MessageRole,
)

logger = logging.getLogger(__name__)


class AnthropicProvider(AIService):
    """Anthropic Claude API provider."""

    def __init__(self, config: AIConfig) -> None:
        """Initialize the Anthropic provider.

        Args:
            config: AI service configuration

        Raises:
            AIServiceAuthenticationError: If API key is not provided
        """
        super().__init__(config)

        api_key = config.get_api_key()
        if not api_key:
            raise AIServiceAuthenticationError(
                "Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable "
                "or provide api_key in configuration.",
                provider="anthropic"
            )

        self.client = AsyncAnthropic(
            api_key=api_key,
            base_url=config.base_url,
            timeout=config.timeout,
        )

    async def generate_response(
        self,
        messages: list[AIMessage],
        system_prompt: str | None = None,
        **kwargs: Any
    ) -> AIResponse:
        """Generate a response using Anthropic's Claude API.

        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            **kwargs: Additional parameters

        Returns:
            AI response

        Raises:
            AIServiceError: If the API request fails
        """
        try:
            # Convert messages to Anthropic format
            anthropic_messages = []

            for msg in messages:
                if msg.role == MessageRole.SYSTEM:
                    # System messages are handled separately in Anthropic
                    if not system_prompt:
                        system_prompt = msg.content
                    continue

                anthropic_messages.append({
                    "role": msg.role.value,
                    "content": msg.content
                })

            # Prepare request parameters
            request_params = {
                "model": self.config.model,
                "messages": anthropic_messages,
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature,
                **kwargs
            }

            if system_prompt:
                request_params["system"] = system_prompt

            logger.debug(f"Making Anthropic API request with model: {self.config.model}")

            # Make the API request
            response: Message = await self.client.messages.create(**request_params)

            # Extract content from response
            content = ""
            if response.content:
                for block in response.content:
                    if hasattr(block, 'text'):
                        content += block.text

            # Prepare usage statistics
            usage = {}
            if hasattr(response, 'usage') and response.usage:
                usage = {
                    "input_tokens": getattr(response.usage, 'input_tokens', 0),
                    "output_tokens": getattr(response.usage, 'output_tokens', 0),
                    "total_tokens": getattr(response.usage, 'input_tokens', 0) +
                                  getattr(response.usage, 'output_tokens', 0)
                }

            return AIResponse(
                content=content,
                model=response.model,
                usage=usage,
                metadata={
                    "id": response.id,
                    "role": response.role,
                    "stop_reason": getattr(response, 'stop_reason', None)
                }
            )

        except anthropic.AuthenticationError as e:
            raise AIServiceAuthenticationError(
                f"Anthropic authentication failed: {str(e)}",
                provider="anthropic",
                original_error=e
            ) from e
        except anthropic.RateLimitError as e:
            raise AIServiceRateLimitError(
                f"Anthropic rate limit exceeded: {str(e)}",
                provider="anthropic",
                original_error=e
            ) from e
        except anthropic.APIConnectionError as e:
            raise AIServiceConnectionError(
                f"Failed to connect to Anthropic API: {str(e)}",
                provider="anthropic",
                original_error=e
            ) from e
        except Exception as e:
            raise AIServiceError(
                f"Anthropic API request failed: {str(e)}",
                provider="anthropic",
                original_error=e
            ) from e

    async def validate_connection(self) -> bool:
        """Validate connection to Anthropic API.

        Returns:
            True if connection is valid, False otherwise
        """
        try:
            # Make a simple API call to validate connection
            test_messages: list[MessageParam] = [
                {"role": "user", "content": "Hello"}
            ]

            response = await self.client.messages.create(
                model=self.config.model,
                messages=test_messages,
                max_tokens=10,
                temperature=0
            )

            return response is not None

        except Exception as e:
            logger.warning(f"Anthropic connection validation failed: {e}")
            return False

    @staticmethod
    def get_available_models() -> list[str]:
        """Get list of available Anthropic models.

        Returns:
            List of available model names
        """
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ]

    @staticmethod
    def get_default_model() -> str:
        """Get the default model for this provider.

        Returns:
            Default model name
        """
        return "claude-3-5-sonnet-20241022"


# Register the Anthropic provider with the factory
AIServiceFactory.register_service(AIProviderType.ANTHROPIC, AnthropicProvider)
