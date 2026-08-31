"""OpenAI-compatible provider family."""

from free_claude_code.core.openai_base_url import openai_v1_base_url
from free_claude_code.providers.admission import ProviderAdmissionController
from free_claude_code.providers.base import ProviderConfig
from free_claude_code.providers.key_pool import KeyPool, parse_api_keys

from .extra_body import (
    validate_extra_body_does_not_override_canonical_fields,
    validate_extra_body_does_not_override_reasoning_fields,
)
from .profiles import OPENAI_CHAT_PROFILES, OpenAIChatProfile, OpenAIModelListing
from .provider import OpenAIAsyncCredentialProvider, OpenAIChatProvider
from .reasoning import (
    NO_REASONING,
    ChatTemplateReasoning,
    NamedEffortReasoning,
    ReasoningObject,
)
from .reasoning_details import apply_reasoning_details_replay
from .request_policy import (
    OpenAIChatRequestPolicy,
    apply_openai_chat_body_policy,
    build_openai_chat_request_body,
)
from .stream_output import ChatStreamOutput
from .usage import usage_int


def create_openai_chat_provider(
    provider_id: str,
    config: ProviderConfig,
    admission: ProviderAdmissionController,
) -> OpenAIChatProvider:
    """Construct one profile-driven provider.

    When the configured credential holds several comma-separated API keys, a
    rotating KeyPool is attached so the provider fails over between them on
    rate-limit/auth errors (issue #1301). A single key keeps static behaviour.
    """
    profile = OPENAI_CHAT_PROFILES.get(provider_id)
    if profile is None:
        raise KeyError(f"No declarative OpenAI-chat profile for {provider_id!r}")
    keys = parse_api_keys(config.api_key or "")
    key_pool = KeyPool(keys) if len(keys) > 1 else None
    return OpenAIChatProvider(
        config,
        profile=profile,
        admission=admission,
        default_headers=(
            {"User-Agent": profile.user_agent} if profile.user_agent else None
        ),
        key_pool=key_pool,
    )


__all__ = [
    "NO_REASONING",
    "OPENAI_CHAT_PROFILES",
    "ChatStreamOutput",
    "ChatTemplateReasoning",
    "NamedEffortReasoning",
    "OpenAIAsyncCredentialProvider",
    "OpenAIChatProfile",
    "OpenAIChatProvider",
    "OpenAIChatRequestPolicy",
    "OpenAIModelListing",
    "ReasoningObject",
    "apply_openai_chat_body_policy",
    "apply_reasoning_details_replay",
    "build_openai_chat_request_body",
    "create_openai_chat_provider",
    "openai_v1_base_url",
    "usage_int",
    "validate_extra_body_does_not_override_canonical_fields",
    "validate_extra_body_does_not_override_reasoning_fields",
]
