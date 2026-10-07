"""Environment-backed application settings."""

from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from process environment and an optional local ``.env`` file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    groq_api_key: SecretStr = Field(default=SecretStr(""), alias="GROQ_API_KEY")
    groq_model: str = Field(default="openai/gpt-oss-120b", alias="GROQ_MODEL")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")
    llm_backend: Literal["groq", "ollama"] = Field(default="groq", alias="LLM_BACKEND")
    llm_temperature: float = Field(default=0.0, ge=0.0, le=2.0, alias="LLM_TEMPERATURE")
    llm_timeout_seconds: float = Field(default=60.0, gt=0, alias="LLM_TIMEOUT_SECONDS")
    llm_rate_limit_retries: int = Field(default=4, ge=0, le=10, alias="LLM_RATE_LIMIT_RETRIES")
    llm_cache_enabled: bool = Field(default=True, alias="LLM_CACHE_ENABLED")
    llm_cache_path: Path = Field(
        default=Path(".agentsec") / "cache.sqlite3", alias="LLM_CACHE_PATH"
    )

    @field_validator("ollama_base_url")
    @classmethod
    def ollama_must_be_local(cls, value: str) -> str:
        """Prevent configuration from pointing the Ollama backend at a remote host."""

        from urllib.parse import urlparse

        host = urlparse(value).hostname
        if host not in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("OLLAMA_BASE_URL must point to localhost")
        return value.rstrip("/")

    @property
    def provider_model(self) -> str:
        """Return the selected provider's configured model name."""

        return self.groq_model if self.llm_backend == "groq" else self.ollama_model

    @property
    def provider_base_url(self) -> str:
        """Return the selected provider endpoint."""

        if self.llm_backend == "groq":
            return "https://api.groq.com/openai/v1"
        return (
            self.ollama_base_url
            if self.ollama_base_url.endswith("/v1")
            else f"{self.ollama_base_url}/v1"
        )
