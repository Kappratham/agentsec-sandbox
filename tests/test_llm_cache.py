from pathlib import Path
from unittest.mock import Mock

from agentsec.llm.base import OpenAICompatibleBackend
from agentsec.llm.models import LLMRequest, Message
from agentsec.settings import Settings


def _backend(tmp_path: Path, client: Mock) -> OpenAICompatibleBackend:
    settings = Settings(
        _env_file=None,
        LLM_CACHE_PATH=tmp_path / "cache.sqlite3",
        LLM_CACHE_ENABLED=True,
    )
    return OpenAICompatibleBackend(
        client=client,
        model="test-model",
        settings=settings,
        cache_namespace="test",
    )


def test_cache_reuses_matching_response(tmp_path: Path) -> None:
    client = Mock()
    client.chat.completions.create.return_value = Mock(
        model="test-model",
        choices=[Mock(message=Mock(content="answer", tool_calls=None), finish_reason="stop")],
        usage=Mock(prompt_tokens=4, completion_tokens=2),
    )
    backend = _backend(tmp_path, client)
    request = LLMRequest(messages=[Message(role="user", content="hello")])

    first = backend.complete(request)
    second = backend.complete(request)

    assert first.content == "answer"
    assert first.cache_hit is False
    assert second.cache_hit is True
    client.chat.completions.create.assert_called_once()


def test_measurement_request_bypasses_cache(tmp_path: Path) -> None:
    client = Mock()
    client.chat.completions.create.return_value = Mock(
        model="test-model",
        choices=[Mock(message=Mock(content="answer", tool_calls=None), finish_reason="stop")],
        usage=None,
    )
    backend = _backend(tmp_path, client)
    request = LLMRequest(messages=[Message(role="user", content="hello")], use_cache=False)

    backend.complete(request)
    backend.complete(request)

    assert client.chat.completions.create.call_count == 2
