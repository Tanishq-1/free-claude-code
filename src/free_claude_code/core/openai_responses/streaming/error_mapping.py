"""Responses stream error mapping."""

from typing import Any


def replay_unsafe_function_call_error() -> dict[str, Any]:
    return {
        "message": (
            "Upstream function_call arguments were not a valid JSON object; "
            "refusing to emit replay-unsafe Responses output."
        ),
        "type": "api_error",
        "param": None,
        "code": None,
    }
