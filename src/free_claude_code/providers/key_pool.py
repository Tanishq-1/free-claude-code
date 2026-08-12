"""Rotating API-key pool with cooldown-based failover.

Supports issue #1301: multiple API keys per provider with automatic rotation
and failover. A pool holds one or more keys for a single provider, hands them
out round-robin, and temporarily sidelining a key that upstream rejects with a
rate-limit / quota / auth failure. Sidelined keys rejoin the rotation after a
cooldown so recovered keys are used again automatically.

A single-key pool behaves exactly like the previous static-key behaviour: the
same key is returned every time and failure reporting is a no-op.
"""

import threading
import time
from collections.abc import Callable

# Default seconds a failed key stays out of rotation before retry.
DEFAULT_KEY_COOLDOWN_SECONDS = 60.0


class KeyPool:
    """Thread-safe round-robin pool of API keys with cooldown failover."""

    def __init__(
        self,
        keys: list[str],
        *,
        cooldown_seconds: float = DEFAULT_KEY_COOLDOWN_SECONDS,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        clean = [key.strip() for key in keys if key and key.strip()]
        if not clean:
            raise ValueError("KeyPool requires at least one non-empty API key.")
        self._keys = tuple(clean)
        self._cooldown = cooldown_seconds
        self._clock = clock
        self._lock = threading.Lock()
        self._next_index = 0
        # key -> monotonic time at which it becomes eligible again.
        self._cooldown_until: dict[str, float] = {}
        # The key most recently handed out, used to attribute failures.
        self._last_served: str = self._keys[0]

    @property
    def size(self) -> int:
        """Return the number of keys in the pool."""
        return len(self._keys)

    @property
    def is_single(self) -> bool:
        """Return whether the pool holds exactly one key (no rotation)."""
        return len(self._keys) == 1

    def current_key(self) -> str:
        """Return the next eligible key, rotating round-robin.

        Keys in cooldown are skipped. If every key is in cooldown, the key
        whose cooldown expires soonest is returned so requests keep flowing
        (the upstream call may still fail, but the pool never deadlocks).
        """
        with self._lock:
            now = self._clock()
            count = len(self._keys)
            for offset in range(count):
                index = (self._next_index + offset) % count
                key = self._keys[index]
                if self._cooldown_until.get(key, 0.0) <= now:
                    self._next_index = (index + 1) % count
                    self._last_served = key
                    return key
            # All keys cooling down: serve the one that recovers soonest.
            key = min(self._keys, key=lambda k: self._cooldown_until.get(k, 0.0))
            self._last_served = key
            return key

    def report_failure(self, key: str | None = None) -> None:
        """Sidelining a key after an upstream rate-limit/quota/auth failure.

        Defaults to the most recently served key. Single-key pools ignore
        failure reports so behaviour is unchanged from a static key.
        """
        if self.is_single:
            return
        target = key or self._last_served
        with self._lock:
            self._cooldown_until[target] = self._clock() + self._cooldown

    def report_success(self, key: str | None = None) -> None:
        """Mark a key healthy, clearing any pending cooldown immediately."""
        target = key or self._last_served
        with self._lock:
            self._cooldown_until.pop(target, None)

    def available_count(self) -> int:
        """Return how many keys are currently eligible (not in cooldown)."""
        now = self._clock()
        return sum(1 for key in self._keys if self._cooldown_until.get(key, 0.0) <= now)


def parse_api_keys(raw: str) -> list[str]:
    """Split a comma-separated API-key setting into individual keys.

    Accepts a single key (no comma) or several keys separated by commas,
    ignoring blank entries and surrounding whitespace.
    """
    return [part.strip() for part in raw.split(",") if part.strip()]
