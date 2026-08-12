"""KeyPool rotation and failover tests (issue #1301)."""

import pytest

from free_claude_code.providers.base import ProviderConfig
from free_claude_code.providers.key_pool import (
    DEFAULT_KEY_COOLDOWN_SECONDS,
    KeyPool,
    parse_api_keys,
)
from free_claude_code.providers.openai_chat import create_openai_chat_provider
from tests.providers.support import immediate_admission, make_provider_config


class _FakeClock:
    def __init__(self, start: float = 1000.0):
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


def test_parse_api_keys_splits_comma_separated() -> None:
    assert parse_api_keys("k1,k2,k3") == ["k1", "k2", "k3"]


def test_parse_api_keys_strips_whitespace_and_drops_empty() -> None:
    assert parse_api_keys("  k1 , , k2 ,,  ") == ["k1", "k2"]


def test_parse_api_keys_single_key() -> None:
    assert parse_api_keys("only-one") == ["only-one"]


def test_parse_api_keys_empty_returns_empty() -> None:
    assert parse_api_keys("") == []
    assert parse_api_keys("   ") == []


def test_single_key_pool_is_single_and_static() -> None:
    pool = KeyPool(["solo"])
    assert pool.is_single is True
    assert pool.size == 1
    assert pool.current_key() == "solo"
    assert pool.current_key() == "solo"


def test_round_robin_rotates_across_keys() -> None:
    pool = KeyPool(["a", "b", "c"])
    assert pool.is_single is False
    assert pool.size == 3
    assert [pool.current_key() for _ in range(6)] == ["a", "b", "c", "a", "b", "c"]


def test_report_failure_sidelines_key_and_fails_over() -> None:
    pool = KeyPool(["a", "b", "c"])
    assert pool.current_key() == "a"
    pool.report_failure()
    # "a" is now in cooldown; rotation continues from the next key.
    assert pool.current_key() == "b"
    assert pool.current_key() == "c"
    assert pool.current_key() == "b"
    assert pool.available_count() == 2


def test_report_failure_on_single_key_pool_is_noop() -> None:
    pool = KeyPool(["solo"])
    pool.report_failure()
    assert pool.current_key() == "solo"
    assert pool.available_count() == 1


def test_cooldown_expiry_restores_key() -> None:
    clock = _FakeClock()
    pool = KeyPool(["a", "b"], clock=clock)
    assert pool.current_key() == "a"
    pool.report_failure()
    assert pool.current_key() == "b"
    assert pool.available_count() == 1
    clock.advance(DEFAULT_KEY_COOLDOWN_SECONDS + 1)
    # "a" recovered; round-robin resumes including it.
    served = {pool.current_key() for _ in range(2)}
    assert served == {"a", "b"}
    assert pool.available_count() == 2


def test_report_success_clears_cooldown() -> None:
    pool = KeyPool(["a", "b"])
    assert pool.current_key() == "a"
    pool.report_failure()
    assert pool.available_count() == 1
    pool.report_success("a")
    assert pool.available_count() == 2


def test_all_keys_cooling_serves_soonest_recovering() -> None:
    clock = _FakeClock()
    pool = KeyPool(["a", "b"], clock=clock)
    pool.current_key()  # serve "a"
    pool.report_failure()  # "a" cooling until t+60
    clock.advance(10)
    pool.current_key()  # serve "b"
    pool.report_failure()  # "b" cooling until t+10+60
    assert pool.available_count() == 0
    # Both cooling: serve the one that recovers soonest ("a").
    assert pool.current_key() == "a"


def test_empty_pool_raises() -> None:
    with pytest.raises(ValueError, match="at least one"):
        KeyPool([])


def _config(api_key: str) -> ProviderConfig:
    return make_provider_config(
        api_key=api_key,
        base_url="https://provider.example/v1",
        rate_limit=100,
        rate_window=60,
    )


def test_factory_attaches_pool_for_comma_separated_keys() -> None:
    provider = create_openai_chat_provider(
        "mistral_codestral", _config("k1,k2,k3"), immediate_admission()
    )
    assert provider._key_pool is not None
    assert provider._key_pool.size == 3


def test_factory_no_pool_for_single_key() -> None:
    provider = create_openai_chat_provider(
        "mistral_codestral", _config("solo"), immediate_admission()
    )
    assert provider._key_pool is None


@pytest.mark.asyncio
async def test_resolve_api_key_rotates_with_pool() -> None:
    provider = create_openai_chat_provider(
        "mistral_codestral", _config("k1,k2"), immediate_admission()
    )
    assert await provider._resolve_api_key() == "k1"
    assert await provider._resolve_api_key() == "k2"
    assert await provider._resolve_api_key() == "k1"


@pytest.mark.asyncio
async def test_resolve_api_key_static_without_pool() -> None:
    provider = create_openai_chat_provider(
        "mistral_codestral", _config("solo"), immediate_admission()
    )
    assert await provider._resolve_api_key() == "solo"
    assert await provider._resolve_api_key() == "solo"
