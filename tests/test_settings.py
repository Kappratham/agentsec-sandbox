from pathlib import Path

import pytest
from pydantic import ValidationError

from agentsec.settings import Settings


def test_groq_is_default_and_uses_current_model() -> None:
    settings = Settings(_env_file=None)
    assert settings.llm_backend == "groq"
    assert settings.provider_model == "openai/gpt-oss-120b"
    assert settings.groq_api_key.get_secret_value() == ""


def test_ollama_endpoint_must_be_local() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, OLLAMA_BASE_URL="https://example.com/v1")


def test_cache_path_uses_pathlib() -> None:
    settings = Settings(_env_file=None)
    assert isinstance(settings.llm_cache_path, Path)
