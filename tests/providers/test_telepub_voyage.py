"""Tests for the Telepub Voyage OpenAI-chat provider."""

from free_claude_code.config.constants import ANTHROPIC_DEFAULT_MAX_OUTPUT_TOKENS
from free_claude_code.config.provider_catalog import TELEPUB_VOYAGE_DEFAULT_BASE
from free_claude_code.core.anthropic.models import Message, MessagesRequest
from free_claude_code.providers.openai_chat import OpenAIChatProvider
from tests.providers.support import (
    REASONING_OFF,
    REASONING_ON,
    immediate_admission,
    make_provider_config,
    profiled_provider,
    reasoning_for,
)


def _provider() -> OpenAIChatProvider:
    return profiled_provider(
        "telepub_voyage",
        make_provider_config(
            api_key="test_telepub_voyage_key",
            base_url=TELEPUB_VOYAGE_DEFAULT_BASE,
            rate_limit=10,
            rate_window=60,
        ),
        admission=immediate_admission(),
    )


def test_init_uses_openai_chat_provider() -> None:
    provider = _provider()
    assert isinstance(provider, OpenAIChatProvider)
    assert provider._api_key == "test_telepub_voyage_key"
    assert provider._base_url == TELEPUB_VOYAGE_DEFAULT_BASE


def test_base_url_constant() -> None:
    assert TELEPUB_VOYAGE_DEFAULT_BASE == "https://voyage.prod.telepub.cn/voyage/api"


def test_build_request_body_openai_chat_shape() -> None:
    provider = _provider()
    request = MessagesRequest(
        model="voyage-3-large",
        max_tokens=100,
        messages=[Message(role="user", content="Hello")],
        system="System prompt",
    )

    body = provider._build_request_body(request, reasoning=reasoning_for(request))

    assert body["model"] == "voyage-3-large"
    assert body["max_tokens"] == 100
    assert body["messages"] == [
        {"role": "system", "content": "System prompt"},
        {"role": "user", "content": "Hello"},
    ]


def test_build_request_body_default_max_tokens() -> None:
    provider = _provider()
    request = MessagesRequest(
        model="m",
        messages=[Message(role="user", content="x")],
    )

    body = provider._build_request_body(request, reasoning=reasoning_for(request))

    assert body["max_tokens"] == ANTHROPIC_DEFAULT_MAX_OUTPUT_TOKENS


def test_reasoning_content_replayed_only_when_thinking_enabled() -> None:
    """Reasoning replay must honor the reasoning policy (fixes PR #739 defect).

    The original PR hard-coded ReasoningReplayMode.REASONING_CONTENT regardless of
    the thinking_enabled flag, so disabled-thinking requests still replayed prior
    reasoning upstream. The profile wires REASONING_CONTENT as the *mode* but the
    policy decides whether reasoning is actually emitted.
    """
    provider = _provider()
    request = MessagesRequest(
        model="voyage-3-large",
        messages=[Message(role="user", content="x")],
    )

    off_body = provider._build_request_body(request, reasoning=REASONING_OFF)
    on_body = provider._build_request_body(request, reasoning=REASONING_ON)

    # NO_REASONING encoder emits no reasoning_effort / thinking flag either way;
    # the request must remain a clean OpenAI chat body in both cases.
    for body in (off_body, on_body):
        assert "reasoning_effort" not in body
        assert body["messages"] == [{"role": "user", "content": "x"}]
