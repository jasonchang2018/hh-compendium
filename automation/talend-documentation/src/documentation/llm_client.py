"""
LLM client abstraction for the automated AI documentation enrichment stage
(ai_enrich_documentation.py).

Kept as a thin interface (rather than calling Anthropic directly from
ai_enrich_documentation.py) so the provider can be swapped later without
touching prompt-construction or pipeline logic. One concrete implementation
today: Claude via the Anthropic API.

Local to src/documentation/ only — not imported by src/talend/ or src/qlik/,
matching this repo's "no shared library code between the scripts" precedent
(see CLAUDE.md).
"""

from __future__ import annotations

import logging
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Send a prompt and return the model's text response."""
        raise NotImplementedError


class AnthropicProvider(LLMProvider):
    """
    Claude implementation.

    Model string: set in config/llm.yaml. Verify the current identifier
    against https://docs.claude.com before running against real jobs —
    model names/versions are updated over time and the default below may be
    stale by the time you run this.
    """

    DEFAULT_MODEL = "claude-sonnet-5"  # verify against docs.claude.com before use
    MAX_RETRIES = 3
    RETRY_BACKOFF_SECONDS = 5

    def __init__(self, model: str | None = None, max_tokens: int = 4096, temperature: float = 0.2):
        try:
            import anthropic
        except ImportError as e:
            raise ImportError(
                "The 'anthropic' package is required. Install with: uv sync"
            ) from e

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise OSError(
                "ANTHROPIC_API_KEY environment variable is not set. "
                "Store it in your secrets manager or a gitignored .env file — never in config/llm.yaml."
            )

        self._client = anthropic.Anthropic(api_key=api_key)
        self.model = model or self.DEFAULT_MODEL
        self.max_tokens = max_tokens
        self.temperature = temperature  # low: doc generation from facts, not creative writing

    # Client-error status codes that will fail identically on every retry
    # (bad request, auth, permissions, not found, unprocessable) — fail fast
    # instead of burning MAX_RETRIES * backoff on a deterministic failure.
    NON_RETRYABLE_STATUS_CODES = frozenset({400, 401, 403, 404, 422})

    def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        import anthropic

        last_error = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response = self._client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )
            except anthropic.APIStatusError as e:
                if e.status_code in self.NON_RETRYABLE_STATUS_CODES:
                    raise RuntimeError(
                        f"Claude API call failed with non-retryable status {e.status_code}: {e}"
                    ) from e
                last_error = e
                logger.warning(f"Claude API call failed (attempt {attempt}/{self.MAX_RETRIES}): {e}")
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.RETRY_BACKOFF_SECONDS * attempt)
                continue
            except anthropic.APIConnectionError as e:
                last_error = e
                logger.warning(f"Claude API call failed (attempt {attempt}/{self.MAX_RETRIES}): {e}")
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.RETRY_BACKOFF_SECONDS * attempt)
                continue

            if response.stop_reason == "max_tokens":
                raise RuntimeError(
                    "Claude response was truncated (stop_reason=max_tokens) — raise "
                    "max_tokens in config/llm.yaml rather than write a partial document."
                )

            text_parts = [block.text for block in response.content if block.type == "text"]
            if not text_parts:
                raise RuntimeError(
                    f"Claude response contained no text content (stop_reason={response.stop_reason})."
                )

            return LLMResponse(
                text="\n".join(text_parts),
                model=self.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
            )

        raise RuntimeError(f"Claude API call failed after {self.MAX_RETRIES} attempts") from last_error


def get_provider(config: dict, model_override: str | None = None) -> LLMProvider:
    """
    Factory. Reads config['llm'] (as loaded from config/llm.yaml) and returns
    the configured provider. Only 'anthropic' is implemented today; branch
    structure is here so adding a second provider later doesn't require
    touching callers.
    """
    llm_cfg = config.get("llm", {})
    provider_name = llm_cfg.get("provider", "anthropic")

    if provider_name == "anthropic":
        return AnthropicProvider(
            model=model_override or llm_cfg.get("model"),
            max_tokens=llm_cfg.get("max_tokens", 4096),
            temperature=llm_cfg.get("temperature", 0.2),
        )

    raise ValueError(f"Unknown or unimplemented LLM provider: {provider_name}")
