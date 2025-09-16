"""Prompt processing and context management for CCI."""

import logging
from pathlib import Path
from typing import Any

import chardet

from cci.config import get_ai_config, get_config_manager
from cci.services import (
    AIConfig,
    AIMessage,
    AIResponse,
    AIService,
    ContextFile,
    MessageRole,
    PromptContext,
    create_ai_service,
)
from cci.utils.file_utils import get_language_from_extension
from cci.utils.git_utils import get_current_branch, get_git_status_string

logger = logging.getLogger(__name__)


class PromptProcessor:
    """Processes prompts and manages context for AI interactions."""

    def __init__(
        self,
        project_path: Path | None = None,
        ai_config: AIConfig | None = None
    ) -> None:
        """Initialize the prompt processor.

        Args:
            project_path: Path to the project (for context gathering)
            ai_config: AI configuration to use
        """
        self.project_path = project_path.resolve() if project_path else Path.cwd()
        self.ai_config = ai_config or get_ai_config(self.project_path)
        self.ai_service: AIService | None = None

        # Load project configuration for prompt settings
        self.config_manager = get_config_manager(self.project_path)
        self.config = self.config_manager.get_config()

    async def get_ai_service(self) -> AIService:
        """Get or create the AI service instance.

        Returns:
            AI service instance

        Raises:
            AIServiceError: If AI service creation fails
        """
        if self.ai_service is None:
            self.ai_service = create_ai_service(self.ai_config)
        return self.ai_service

    def gather_context(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        max_files: int | None = None,
        max_file_size: int = 1024 * 1024,  # 1MB default
    ) -> PromptContext:
        """Gather context information from the project.

        Args:
            include_patterns: File patterns to include (e.g., ["*.py", "*.md"])
            exclude_patterns: File patterns to exclude (e.g., ["__pycache__", "*.pyc"])
            max_files: Maximum number of files to include
            max_file_size: Maximum file size in bytes

        Returns:
            PromptContext with gathered information
        """
        # Use configuration defaults if not specified
        if include_patterns is None:
            include_patterns = self.config.ai.model_dump().get(
                "include_patterns", ["*.py", "*.md", "*.txt"]
            )
        if exclude_patterns is None:
            exclude_patterns = self.config.ai.model_dump().get(
                "exclude_patterns", ["__pycache__", "*.pyc", ".git"]
            )
        if max_files is None:
            max_files = getattr(self.config.ai, 'max_context_files', 20)

        logger.debug(f"Gathering context from {self.project_path}")
        logger.debug(f"Include patterns: {include_patterns}")
        logger.debug(f"Exclude patterns: {exclude_patterns}")

        files = self._find_relevant_files(
            include_patterns, exclude_patterns, max_files, max_file_size
        )

        # Get git information
        git_branch = get_current_branch(self.project_path) if self.project_path else None
        git_status = get_git_status_string(self.project_path) if self.project_path else None

        return PromptContext(
            project_path=self.project_path,
            files=files,
            working_directory=Path.cwd(),
            git_branch=git_branch,
            git_status=git_status,
            metadata={
                "include_patterns": include_patterns,
                "exclude_patterns": exclude_patterns,
                "max_files": max_files,
                "total_files_found": len(files),
            }
        )

    def _find_relevant_files(
        self,
        include_patterns: list[str],
        exclude_patterns: list[str],
        max_files: int,
        max_file_size: int
    ) -> list[ContextFile]:
        """Find relevant files for context.

        Args:
            include_patterns: Patterns to include
            exclude_patterns: Patterns to exclude
            max_files: Maximum number of files
            max_file_size: Maximum file size

        Returns:
            List of context files
        """
        import fnmatch

        files = []
        seen_files = 0

        # Walk through project directory
        for file_path in self.project_path.rglob("*"):
            if seen_files >= max_files:
                break

            if not file_path.is_file():
                continue

            # Check size limit
            try:
                if file_path.stat().st_size > max_file_size:
                    continue
            except OSError:
                continue

            relative_path = file_path.relative_to(self.project_path)
            path_str = str(relative_path)

            # Check exclude patterns first
            if any(fnmatch.fnmatch(path_str, pattern) for pattern in exclude_patterns):
                continue

            # Check include patterns
            if not any(fnmatch.fnmatch(path_str, pattern) for pattern in include_patterns):
                continue

            # Try to read file content
            context_file = self._read_context_file(file_path)
            if context_file:
                files.append(context_file)
                seen_files += 1

        # Sort by file type relevance (source files first)
        files.sort(key=lambda f: (
            0 if f.language in ["python", "typescript", "javascript", "rust", "go"] else 1,
            f.path.name
        ))

        return files[:max_files]

    def _read_context_file(self, file_path: Path, max_lines: int = 500) -> ContextFile | None:
        """Read a file for context inclusion.

        Args:
            file_path: Path to the file
            max_lines: Maximum lines to read

        Returns:
            ContextFile if successful, None otherwise
        """
        try:
            # Detect encoding
            with open(file_path, "rb") as f:
                raw_data = f.read(8192)  # Read first 8KB for encoding detection

            encoding_info = chardet.detect(raw_data)
            encoding = encoding_info.get("encoding", "utf-8")

            if not encoding or encoding_info.get("confidence", 0) < 0.7:
                encoding = "utf-8"

            # Read file content
            with open(file_path, encoding=encoding, errors="replace") as f:
                lines = f.readlines()

            # Determine language
            language = get_language_from_extension(file_path.suffix)

            # If file is too long, truncate it
            truncated = len(lines) > max_lines
            if truncated:
                lines = lines[:max_lines]

            content = "".join(lines)

            return ContextFile(
                path=file_path.relative_to(self.project_path),
                content=content,
                language=language,
                truncated=truncated,
                max_lines=max_lines if truncated else None
            )

        except Exception as e:
            logger.warning(f"Failed to read file {file_path}: {e}")
            return None

    def create_context_prompt(self, context: PromptContext) -> str:
        """Create a prompt section with context information.

        Args:
            context: Context information

        Returns:
            Formatted context prompt
        """
        prompt_parts = []

        # Project information
        if context.project_path:
            prompt_parts.append(f"# Project: {context.project_path.name}")
            prompt_parts.append(f"Project Path: {context.project_path}")

        # Git information
        if context.git_branch:
            prompt_parts.append(f"Git Branch: {context.git_branch}")

        if context.git_status and context.git_status.strip():
            prompt_parts.append("Git Status:")
            prompt_parts.append("```")
            prompt_parts.append(context.git_status.strip())
            prompt_parts.append("```")

        # File contents
        if context.files:
            prompt_parts.append(f"\n## Project Files ({len(context.files)} files included)")

            for file in context.files:
                prompt_parts.append(f"\n### {file.path}")
                if file.language:
                    prompt_parts.append(f"```{file.language}")
                else:
                    prompt_parts.append("```")

                prompt_parts.append(file.content)
                prompt_parts.append("```")

                if file.truncated:
                    prompt_parts.append(f"[File truncated at {file.max_lines} lines]")

        return "\n".join(prompt_parts)

    async def process_prompt(
        self,
        user_prompt: str,
        include_context: bool = True,
        context_patterns: dict[str, list[str]] | None = None,
        system_prompt: str | None = None,
        **ai_kwargs: Any
    ) -> AIResponse:
        """Process a user prompt with optional context.

        Args:
            user_prompt: The user's prompt
            include_context: Whether to include project context
            context_patterns: Custom include/exclude patterns for context
            system_prompt: Optional system prompt
            **ai_kwargs: Additional arguments for AI service

        Returns:
            AI response

        Raises:
            AIServiceError: If AI service fails
        """
        ai_service = await self.get_ai_service()

        # Prepare messages
        messages = []

        # Add context if requested
        if include_context:
            context_config = context_patterns or {}
            context = self.gather_context(
                include_patterns=context_config.get("include"),
                exclude_patterns=context_config.get("exclude"),
            )

            if context.files or context.git_status:
                context_prompt = self.create_context_prompt(context)
                logger.debug(f"Including context with {len(context.files)} files")

                # Add context as part of user message or system message
                full_user_prompt = f"{context_prompt}\n\n# User Request\n{user_prompt}"
            else:
                full_user_prompt = user_prompt
        else:
            full_user_prompt = user_prompt

        messages.append(AIMessage(
            role=MessageRole.USER,
            content=full_user_prompt
        ))

        # Generate response
        logger.debug("Sending request to AI service")
        response = await ai_service.generate_response(
            messages=messages,
            system_prompt=system_prompt,
            **ai_kwargs
        )

        logger.debug(f"Received response with {len(response.content)} characters")
        return response

    async def chat(
        self,
        messages: list[AIMessage],
        system_prompt: str | None = None,
        **ai_kwargs: Any
    ) -> AIResponse:
        """Have a chat conversation with the AI service.

        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            **ai_kwargs: Additional arguments for AI service

        Returns:
            AI response

        Raises:
            AIServiceError: If AI service fails
        """
        ai_service = await self.get_ai_service()

        logger.debug(f"Starting chat with {len(messages)} messages")
        response = await ai_service.generate_response(
            messages=messages,
            system_prompt=system_prompt,
            **ai_kwargs
        )

        logger.debug(f"Chat response received with {len(response.content)} characters")
        return response

    async def validate_ai_connection(self) -> bool:
        """Validate that AI service is available.

        Returns:
            True if AI service is available, False otherwise
        """
        try:
            ai_service = await self.get_ai_service()
            return await ai_service.validate_connection()
        except Exception as e:
            logger.warning(f"AI connection validation failed: {e}")
            return False

    def create_user_message(self, content: str, **metadata: Any) -> AIMessage:
        """Create a user message.

        Args:
            content: Message content
            **metadata: Additional metadata

        Returns:
            AIMessage instance
        """
        return AIMessage(role=MessageRole.USER, content=content, metadata=metadata)

    def create_assistant_message(self, content: str, **metadata: Any) -> AIMessage:
        """Create an assistant message.

        Args:
            content: Message content
            **metadata: Additional metadata

        Returns:
            AIMessage instance
        """
        return AIMessage(role=MessageRole.ASSISTANT, content=content, metadata=metadata)


def create_prompt_processor(
    project_path: Path | None = None,
    ai_config: AIConfig | None = None
) -> PromptProcessor:
    """Create a prompt processor instance.

    Args:
        project_path: Path to project
        ai_config: AI configuration

    Returns:
        PromptProcessor instance
    """
    return PromptProcessor(project_path=project_path, ai_config=ai_config)


async def process_simple_prompt(
    prompt: str,
    project_path: Path | None = None,
    include_context: bool = True
) -> AIResponse:
    """Process a simple prompt with minimal setup.

    Args:
        prompt: User prompt
        project_path: Optional project path
        include_context: Whether to include project context

    Returns:
        AI response
    """
    processor = create_prompt_processor(project_path)
    return await processor.process_prompt(prompt, include_context=include_context)
