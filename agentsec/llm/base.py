"""Backend protocol and shared cached completion implementation."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from typing import Protocol

from openai import OpenAI, RateLimitError

from agentsec.llm.models import LLMRequest, LLMResponse, ToolCall
from agentsec.settings import Settings


class LLMBackend(Protocol):
    """Provider interface used by the agent; credentials stay in this host-side object."""

    def complete(self, request: LLMRequest) -> LLMResponse:
        """Generate a response. Measurement runs should pass ``use_cache=False``."""


class OpenAICompatibleBackend:
    """OpenAI-compatible backend with SQLite response caching and rate-limit backoff."""

    def __init__(
        self,
        *,
        client: OpenAI,
        model: str,
        settings: Settings,
        cache_namespace: str,
    ) -> None:
        self._client = client
        self.model = model
        self._settings = settings
        self._cache_namespace = cache_namespace

    def complete(self, request: LLMRequest) -> LLMResponse:
        cache_key = self._cache_key(request)
        if request.use_cache and self._settings.llm_cache_enabled:
            cached = self._read_cache(cache_key)
            if cached is not None:
                return cached.model_copy(update={"cache_hit": True})

        response = self._request_with_backoff(request)
        if request.use_cache and self._settings.llm_cache_enabled:
            self._write_cache(cache_key, response)
        return response

    def _request_with_backoff(self, request: LLMRequest) -> LLMResponse:
        tools = [tool.model_dump(exclude_none=True) for tool in request.tools]
        params: dict[str, object] = {
            "model": self.model,
            "messages": [message.model_dump(exclude_none=True) for message in request.messages],
            "temperature": request.temperature,
        }
        if tools:
            params["tools"] = tools
        if request.seed is not None:
            params["seed"] = request.seed

        retries = self._settings.llm_rate_limit_retries
        for attempt in range(retries + 1):
            try:
                raw = self._client.chat.completions.create(**params)  # type: ignore[arg-type]
                choice = raw.choices[0]
                message = choice.message
                calls = [
                    ToolCall(
                        id=call.id,
                        name=call.function.name,
                        arguments=json.loads(call.function.arguments or "{}"),
                    )
                    for call in (message.tool_calls or [])
                ]
                return LLMResponse(
                    content=message.content,
                    tool_calls=calls,
                    model=raw.model or self.model,
                    finish_reason=choice.finish_reason,
                    prompt_tokens=raw.usage.prompt_tokens if raw.usage else 0,
                    completion_tokens=raw.usage.completion_tokens if raw.usage else 0,
                )
            except RateLimitError:
                if attempt >= retries:
                    raise
                time.sleep(min(2**attempt, 30))
        raise RuntimeError("Rate-limit retry loop exited unexpectedly")

    def _cache_key(self, request: LLMRequest) -> str:
        value = {
            "namespace": self._cache_namespace,
            "model": self.model,
            "messages": [message.model_dump(exclude_none=True) for message in request.messages],
            "tools": [tool.model_dump(exclude_none=True) for tool in request.tools],
            "temperature": request.temperature,
            "seed": request.seed,
        }
        serialized = json.dumps(value, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def _read_cache(self, key: str) -> LLMResponse | None:
        path = self._settings.llm_cache_path
        if not path.exists():
            return None
        with sqlite3.connect(path) as connection:
            row = connection.execute(
                "SELECT response_json FROM llm_cache WHERE cache_key = ?", (key,)
            ).fetchone()
        return LLMResponse.model_validate_json(row[0]) if row else None

    def _write_cache(self, key: str, response: LLMResponse) -> None:
        path = self._settings.llm_cache_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS llm_cache "
                "(cache_key TEXT PRIMARY KEY, response_json TEXT NOT NULL)"
            )
            connection.execute(
                "INSERT OR REPLACE INTO llm_cache(cache_key, response_json) VALUES (?, ?)",
                (key, response.model_dump_json()),
            )


def build_backend(settings: Settings | None = None) -> LLMBackend:
    """Create the configured provider client in the host process."""

    current = settings or Settings()
    client = OpenAI(
        api_key=current.groq_api_key.get_secret_value()
        if current.llm_backend == "groq"
        else "ollama-local",
        base_url=current.provider_base_url,
        timeout=current.llm_timeout_seconds,
        max_retries=0,
    )
    return OpenAICompatibleBackend(
        client=client,
        model=current.provider_model,
        settings=current,
        cache_namespace=current.llm_backend,
    )
