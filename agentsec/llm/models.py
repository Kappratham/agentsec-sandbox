"""Validated request and response models for the backend contract."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Message(BaseModel):
    """One chat message passed to a host-side model backend."""

    role: Literal["system", "user", "assistant", "tool"]
    content: str = ""
    name: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[dict[str, Any]] | None = None


class ToolDefinition(BaseModel):
    """OpenAI-compatible function tool schema."""

    model_config = ConfigDict(extra="allow")

    type: Literal["function"] = "function"
    function: dict[str, Any]


class LLMRequest(BaseModel):
    """Stable provider-independent input contract."""

    messages: list[Message]
    tools: list[ToolDefinition] = Field(default_factory=list)
    temperature: float = Field(default=0.0, ge=0, le=2)
    seed: int | None = None
    use_cache: bool = True


class ToolCall(BaseModel):
    """A function call requested by the model."""

    id: str
    name: str
    arguments: dict[str, Any]


class LLMResponse(BaseModel):
    """Provider-independent model output and measurement metadata."""

    content: str | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    model: str
    finish_reason: str | None = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_hit: bool = False
