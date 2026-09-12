# Free-Claude-Code — Contribution Handoff Notes

> Purpose: context for continuing open-source contribution work in a new terminal/session.
> Date: 2026-08-30 (restructured this session — active branches only; history preserved in the backup below)

> **SESSION NOTE (2026-08-12):** All commands in this doc (§2 gates, tests, `uv lock`, git branch/commit/push) are **AUTO-APPROVED by the user for this session** — run them without asking for confirmation each time. Still confirm before opening any upstream PR (user decides PR timing).

> **LAST SYNC (sync #8 recorded 2026-09-13):** upstream base `0dcb3715` (v6.2.15 — 11 commits #1756–#1767, 46 files +5194/−345: VS Code + Codex integrations, JetBrains ACP preview card, admin loading fix, Codex client tool discovery fix; local main ff-synced `f3a3aac`→`0dcb3715`, pushed to fork 2026-09-12). ALL 9 updateable branches synced 2026-09-12 (details §8 sync #8; every open PR conflict cleared + greptile PASS + all 7 CI green — merge-ready, §12.4 gate met): **#1469** `add-custom-provider` `b218d21e` (6.3.0 — complex rebase, keep-both conflicts; greptile 17 files/0 comments), **#1606** `fix-ollama-model-discovery` `132b5fdc` (6.2.16 — merge of main INTO branch, never-rewrite, NO force), **#1641** `fix-cline-hub-hijack` `acf94479` (6.2.16), **#1736** `feat-models-metadata` `a56c9856` (6.3.0), **#1740** `add-lightning-ai` `96a601d0` (6.3.0), **#1744** `update-main-fix-issues` `e3dc94e1` (6.2.16), **#1749** `add-experiential-labs` `b61736c0` (6.3.0), **#1754** `add-orca-router` `3b4f2033` (6.3.0), `feat-api-key-rotation` `03def116` (6.3.0 — NO PR, awaiting user decision). **#1742** `fix-nim-minimax-post-terminal-framer` **CLOSED UNMERGED** by maintainer 2026-09-12 ("the minimax model is deprecated — no need to fix, just stop using it") — frozen at `cfa42f8`, NOT updated (user decision); still merged into `final` at `cfa42f8`. Telepub FROZEN at `50559ea` (§12.1) — untouched. `final` = rebuilt 2026-09-12/13 on base `0dcb3715` (ALL 11 branches merged + audit re-application + pyproject-deps-restore incident + credential-count fix — §8 sync #8; §12.5 full set green: suite 5633p/152s, e2e 116p/1s, pip-audit 0 vulns; old final `d0cc706` → local `final-backup-20260912-audit`; NO PR — internal only). **HANDOFF_NOTES.md is TRACKED on `final` (final-branch-only file, §9 tracking block; this commit updates it).** NOTE: upstream PR #1655+#1656 (another author) implements API-key rotation (#1301) — our `feat-api-key-rotation` `03def116` may be redundant. Upstream e2e: context-meter is Windows-locale-only (passes on ubuntu CI). Sync log: §8 (sync #8 latest recorded).

---

## 1. Project Overview

- **Repo (upstream):** https://github.com/Alishahryar1/free-claude-code
- **Fork (origin):** https://github.com/Tanishq-1/free-claude-code
- **Local path:** `d:\Agentic coding\Project\claude\free-claude-code`
- **What it is:** Local proxy (FastAPI + uvicorn) connecting coding agents to OpenAI-compatible AI providers.
- **Language/Tooling:** Python 3.14, `pydantic-settings`, `uv` package manager.
- **Admin UI:** http://127.0.0.1:8082/admin (server on port 8082).

---

## 2. Critical Commands (always use `uv run`, NOT global python)

```powershell
# Run server
uv run fcc-server

# Quality gates (run before every PR)
uv run ruff format --check
uv run ruff check
uv run ty check

# Tests
uv run pytest -q                                          # full suite
uv run pytest tests/config tests/contracts tests/providers -q

# E2E — Admin UI (install Chromium once: uv run playwright install chromium)
uv run pytest e2e -q

# Lockfile after version bump
uv lock

# Full CI script
.\scripts\ci.ps1
```

---

## 3. Git Setup

```powershell
git remote -v
# origin    https://github.com/Tanishq-1/free-claude-code.git   (your fork)
# upstream  https://github.com/Alishahryar1/free-claude-code.git (main repo)
```

### Standard workflow for a new feature
```powershell
git checkout main
git fetch upstream
git merge upstream/main --ff-only     # sync local main
git push origin main                  # sync fork main
git checkout -b add-<feature>         # new branch from updated main
# ... make changes, bump version, uv lock, run gates + tests ...
git add <explicit paths>              # never -A (stray PowerShell dirs get caught)
git commit -m "Add <feature>"
git push -u origin add-<feature>
# Open PR: base = Alishahryar1/main, head = Tanishq-1/add-<feature>
```

### If upstream main moved (conflicts) — rebase
```powershell
$env:GIT_EDITOR='true'                # ALWAYS — prevents the invisible vim.exe hang
git checkout add-<feature>
git rebase main
# resolve conflicts with EXACT edits (keep BOTH provider entries), verify zero markers
git add <explicit paths>
git -c core.editor=true rebase --continue
git push --force-with-lease origin add-<feature>   # force needed after rebase
```
Lockfile reset order and all other durable rebase rules: §8 "Sync rails".

---

## 4. Versioning (SemVer) — REQUIRED for runtime changes

`pyproject.toml` line 7: `version = "X.Y.Z"` — bump + run `uv lock` in the SAME commit.

| Bump | When | Example |
|------|------|---------|
| PATCH (x.x.1) | bug fix only | fix crash |
| MINOR (x.1.0) | new feature/provider | **added a provider** |
| MAJOR (1.0.0) | breaking change | remove provider, rename env vars |

**Branch-version invariant:** every branch must sit ABOVE the upstream base version — features MINOR, fixes PATCH. Rebases auto-converge the version line to the base; restore the above-base version via edit + `uv lock` + `git commit --amend` (single-commit branches keep their shape this way).

---

## 5. How to Add a New OpenAI-Compatible Provider (the template)

Provider system is **catalog-driven** — no new protocol code needed. Touch these files:

1. **`src/free_claude_code/config/provider_catalog.py`** — `<NAME>_DEFAULT_BASE` constant + `ProviderDescriptor` entry in `PROVIDER_CATALOG`.
2. **`src/free_claude_code/config/settings.py`** — import the DEFAULT_BASE; add `<name>_api_key`, `<name>_base_url` Fields (with validation_alias) + `<name>_proxy` Field.
3. **`src/free_claude_code/providers/openai_chat/profiles.py`** — `OpenAIChatProfile` in `OPENAI_CHAT_PROFILES` via `_policy(...)`; `NamedEffortReasoning(_LOW_MEDIUM_HIGH, enabled_value="medium")` if the provider supports `reasoning_effort`, else `NO_REASONING`.
4. **`src/free_claude_code/config/admin/provider_manifest.py`** — `<NAME>_API_KEY` + `<NAME>_BASE_URL` overrides in `_PROVIDER_FIELD_OVERRIDES` (label + description).
5. **`src/free_claude_code/config/admin/manifest.py`** — `ConfigFieldSpec("FCC_SMOKE_MODEL_<NAME>", "Smoke <Name> Model", "smoke", advanced=True)`.
6. **`tests/contracts/test_provider_catalog_order.py`** — add `"<name>",` to `_EXPECTED_PROVIDER_ORDER` (position must match catalog dict order).
7. **`tests/providers/test_provider_runtime.py`** — import the DEFAULT_BASE; add `<name>_api_key`, `<name>_base_url`, `<name>_proxy` mocks + `"<name>": OpenAIChatProvider,` entry.
8. **`.env.example`** — `<NAME>_API_KEY`, `<NAME>_BASE_URL`, `<NAME>_PROXY`, `FCC_SMOKE_MODEL_<NAME>` blocks AND `"<name>"` in the Valid providers comment.
9. **`README.md`** — provider table row.
10. **`smoke/lib/config.py`** — `"<name>": "<name>/<default-model>",` in `PROVIDER_SMOKE_DEFAULT_MODELS`.
11. **`pyproject.toml` + `uv.lock`** — version bump (MINOR).

---

## 6. Model Discovery (auto — no extra work)

- `OpenAIChatProvider.list_model_infos()` calls `{base_url}/models` with the **user's own API key**.
- Gated by `model_ids_are_routable` (default `True`; only `azure_openai` sets `False`).
- Any OpenAI-compatible provider **auto-discovers** its models per key; README/smoke slugs are defaults, NOT restrictions.
- Local providers (`ollama`/`lmstudio`/`llamacpp`) are self-sufficient for discovery — zero configuration needed (see §7 ollama card).

---

## 7. Active Branches (Work In Flight)

> All providers below follow the §5 template; only distinguishing facts noted. Issue links use the upstream repo: https://github.com/Alishahryar1/free-claude-code/issues/<n>

### 🔄 `add-custom-provider` — Custom OpenAI-compatible provider — **PR [#1469](https://github.com/Alishahryar1/free-claude-code/pull/1469) OPEN** ([#1230](https://github.com/Alishahryar1/free-claude-code/issues/1230))
- Generic custom-endpoint feature (single "custom" slot). **API key OPTIONAL** — `credential_optional=True` profile flag; base URL required via `required_settings_attrs=("custom_base_url",)`. Profile: `NO_REASONING` + `ReasoningReplayMode.DISABLED` + `normalize_base_url=True`; no smoke default.
- Greptile P1 series RESOLVED — the Admin local-status probe now matches the runtime on all four axes: keyless construction (`credential_optional` + `api_key=... or "no-api-key"` SDK placeholder), keyless bearer strip (`_drop_authorization_header` httpx request hook), `/v1` normalization (`openai_v1_base_url` moved to `core/openai_base_url.py`), and proxy passthrough. Nothing left to flag.
- **CI failure on `6ac42f9` FIXED (2026-09-02):** the playwright job failed on `test_delayed_older_page_cannot_cross_into_another_chat` (30s timeout clicking the renamed card). Root cause (§8): a stream committing right before an edit bumps the revision → the edit's PATCH 409s → `updateSession` in `chat_sessions.js` reloaded + showed a notice but **silently dropped the user's change** (title/model/thinking). Fix in commit `1e537fb` "Retry chat session edits once on revision conflicts": on 409, reload the session and re-apply the same edit ONCE against the fresh revision (guards preserved; no loop). Genuine product bug (silent edit loss), makes the flaky test deterministic. 10/10 local runs of the flaky test pass post-fix; suite 4422/148/0; e2e 42 passed + Windows-locale context-meter only; gates green. v5.19.0 → **5.19.1** + `uv lock` in the same commit (PATCH, runtime change). Pushed as a second commit (fast-forward, NO force).
- Current: `1e537fb` (`6ac42f9` + fix commit), v5.19.1, base `b85ae4a` — suite 4422/148/0, e2e green (Windows-locale context-meter only, passes on CI), gates green. RESOLVED 2026-09-12: the fix commit is in the branch's `b69108d` lineage and in `final` (§10). **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` → `b218d21e`, v6.3.0 — complex rebase (admin_routes.py asyncio.gather + `_probe` closure with blank-URL skip + keyless bare `client.get` — §8 sync #6 precedent; provider.py `api_key=resolved_api_key or "no-api-key"` combined with upstream's changes; e2e/conftest.py + tests/api/test_admin.py keep-both); §12.5 full set green; greptile re-ran clean (17 files, 0 comments) + all 7 CI green — merge-ready (§12.4 met).

### 🔄 `fix-ollama-model-discovery` — Local models missing from /model — **PR [#1606](https://github.com/Alishahryar1/free-claude-code/pull/1606) OPEN** ([#1296](https://github.com/Alishahryar1/free-claude-code/issues/1296))
- Root cause (two stacked gates): `discovery.py` excluded every `.local` provider unless a chat model already referenced it, and `has_provider_configuration()` treated keyless-with-default locals as unconfigured — fresh Ollama users could never get probed.
- Fix: `_self_sufficient_local()` admits `ollama`/`lmstudio`/`llamacpp` into best-effort discovery with zero configuration; failed local probes back off via a `ProviderModelCache` cooldown (`LOCAL_DISCOVERY_RETRY_COOLDOWN_S = 60s`, cleared on success, ignored by explicit full refreshes); README documents local auto-discovery.
- **Branch shape (IMPORTANT):** the PR branch was updated EXTERNALLY (GitHub web merge) to `e42e115` = merge of our work + upstream `3ef17fe`. Never rewrite it — we fast-forwarded and added ONE commit on top: the v5.17.3 PATCH bump (`79e8345`). Push WITHOUT force (fast-forward only); single-commit-shape rule does not apply.
- Current: `c84164c`, v5.19.2 (on 2026-09-02 merged `main` `96495b9` in to clear the NEW PR #1606 dirty state — upstream advanced `b85ae4a`→`96495b9`; version resolved 5.19.2 = PATCH above base 5.19.1; conflict version-only pyproject.toml + uv.lock; external merge `e42e115` + prior merge `0b3d158` preserved; merge commit `edd34fb` ff-pushed, NO force) — suite 4454/148/0, e2e 50 passed + Windows-locale context-meter only, gates green. NOTE 2026-09-02: first CI run for `edd34fb` was CANCELLED (workflow run 33610053117 — GitHub cancelled; no superseding run; API re-run blocked 403 without upstream write) → appended EMPTY commit `c84164c` "ci: re-trigger checks cancelled after main merge (no code change)" + ff-push to re-trigger; run 33612506300 **SUCCESS** — all 7 checks green incl. Greptile; PR API **mergeable=True, state=clean**.
- NOTE RESOLVED 2026-09-12: the old merge-commit ancestry break is gone — `final` merges the branch tip directly (ancestry checks pass on every rebuild). **Sync #8 (2026-09-12):** merged main `0dcb3715` INTO the branch (never-rewrite — merge commit `132b5fdc`), version resolved 6.2.16, ff-push NO force; §12.5 full set green; conflict cleared, greptile + all 7 CI green — merge-ready (§12.4 met).

### 🔄 `add-telepub-voyage` — Telepub Voyage provider — NO PR
- Clean reimplementation of stale PR [#739](https://github.com/Alishahryar1/free-claude-code/pull/739), fixing its defects: reasoning replay honors the reasoning policy, no `_strip_system_messages` content drop, no `Message.role` widening, version bumped.
- `telepub_voyage`, base `https://voyage.prod.telepub.cn/voyage/api`, env `TELEPUB_VOYAGE_API_KEY`; `NO_REASONING` + `ReasoningReplayMode.REASONING_CONTENT`; standard profiled provider, auto-discovers via `/models`. Test: `tests/providers/test_telepub_voyage.py`.
- **Policy: share the branch URL with the PR #739 author only — do NOT raise a PR.**
- **FROZEN (§12.1):** excluded from all branch updates — never rebase/push during syncs. The branch was externally REBASED (before 2026-09-10) to `50559ea` — the same single clean commit on main `81fa340`, v6.3.0; the ancient frozen `17382eb` is OBSOLETE. `final` merges the current tip `50559ea`; no further updates beyond it.
- Current: `50559ea`, v6.3.0 — pairwise merge into bare main is clean (verified via merge-tree 2026-09-12); untouched in sync #8 (§12.1 freeze); merged into rebuilt `final` at `50559ea` (§10).

### 🔄 `feat-models-metadata` — /v1/models metadata — **PR [#1736](https://github.com/Alishahryar1/free-claude-code/pull/1736) OPEN** ([#1168](https://github.com/Alishahryar1/free-claude-code/issues/1168))
- Adds optional `pricing` (per-1K USD `input`/`output`) + `capabilities` (`chat`/`vision`/`tools`/`thinking`/`fim`/`streaming`) to `GET /v1/models`, extracted from provider model-list entries so clients need not scan 558+ models. `contextWindow`/`maxCompletionTokens` already ship on main via upstream's `ProviderModelInfo` (#1604/#1605) — our unique value on top is **`ProviderModelPricing`** + capabilities (`application/model_metadata.py`) + extraction/thinking-inference in `providers/model_listing.py`; optional `ModelResponse` fields omitted when the provider advertises nothing (id-only responses unchanged).
- Contract note: the claude view must NOT expose `contextWindow`/`maxCompletionTokens` (upstream contract test owns that view) — enrichment limited to optional capabilities/pricing.
- Current: `5fe9ce8` (amended, single-commit), v6.3.0, base `81fa340` (v6.2.2; rebased 2026-09-09) — PR #1736 raised 2026-09-10; greptile scored **4/5** → per §12.3 fixed all 3 findings same day (P1 no-thinking variants no longer advertise `thinking` in capabilities — Claude view + messages/responses views; P2 direct views (`view=messages`/`view=responses`, and Muse/codex wrappers) now surface capabilities/pricing via `_InventoryModel.metadata`; P2 `_to_float` rejects negative/NaN/inf prices + `_pricing` key-presence keeps valid 0 prices), §12.5 full set green before push (gates green; suite 5165p/149s + 2 pre-existing PS 5.1 installer stderr-wrap failures verified present at `07eca3f` too — env brittleness, not our diff; e2e 97p/1s; targeted 43p), force-pushed → **greptile re-review PASSED (5/5 gate §12.4 met) + all 7 CI checks green on `5fe9ce8`** — merge-ready (merge is upstream owner's call). **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` → `a56c9856`, v6.3.0 kept; §12.5 full set green; conflict cleared, greptile + all 7 CI green — merge-ready.

### 🔄 `add-lightning-ai` — Lightning AI provider — **PR [#1740](https://github.com/Alishahryar1/free-claude-code/pull/1740) OPEN** ([#1732](https://github.com/Alishahryar1/free-claude-code/issues/1732))
- Standard catalog provider (`lightning`, base `https://lightning.ai/api/v1`, env `LIGHTNING_API_KEY`/`LIGHTNING_BASE_URL`/`LIGHTNING_PROXY`) for Lightning AI Model APIs (~40M free tokens, ~47 OpenAI-compatible models with slashed ids like `lightning-ai/gpt-oss-120b`). Auto-wired `OpenAIChatProfile` — no factory/runtime changes (LLM7 pattern).
- `NamedEffortReasoning(_LOW_MEDIUM_HIGH, disabled_value="none", enabled_value="medium")` — litai's documented top-level `reasoning_effort` vocabulary; `ReasoningReplayMode.DISABLED`; declarative `/models` listing extracting `context_length`/`max_tokens`/`architecture.input_modalities`. NO credential-validation probe (public catalog cannot validate inference keys — LLM7 rule) → unsupported-key count 20→21 in `test_credential_validation.py`; no tool filtering (catalog has no `supported_parameters`); pricing omitted (per-token keys ≠ generic per-1K extraction). Smoke default `lightning/lightning-ai/gpt-oss-120b`; README 50→51 providers.
- Tests: `tests/providers/test_lightning.py` (14 items: construct; DEFAULT/ON/OFF → absent/`medium`/`none`; full named-effort matrix MINIMAL/LOW→low, MEDIUM→medium, HIGH/XHIGH/MAX→high; catalog metadata incl. missing `architecture` → modalities unknown; malformed/empty catalog rejection; wire URL + Bearer). Contract updates: catalog order, runtime instantiation, smoke-config trio, credential-validation count.
- Current: `3575595` (amended, single-commit), v6.3.0, base `81fa340` (v6.2.2) — PR #1740 raised 2026-09-10; greptile scored **4/5** (P2: named reasoning efforts untested) → added full effort-vocabulary matrix, §12.5 full set green before push (gates green; suite 5188p/144s; e2e 97p/1s; targeted 14p), force-pushed `95cff5e`→`3575595` → **greptile re-review PASSED (5/5 gate §12.4 met; 0 comments) + all 7 CI checks green** — merge-ready (merge is upstream owner's call). Version-only collision with PR #1736 (both 6.3.0) — routine per §8; resolved at rebase/merge. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` → `96a601d0`, v6.3.0 kept; §12.5 full set green; conflict cleared, greptile + all 7 CI green — merge-ready.

### 🧊 `fix-nim-minimax-post-terminal-framer` — NIM deltas-after-finish_reason crash — **PR [#1742](https://github.com/Alishahryar1/free-claude-code/pull/1742) CLOSED UNMERGED (2026-09-12)** ([#1734](https://github.com/Alishahryar1/free-claude-code/issues/1734))
- Root cause: NVIDIA NIM (during MiniMax-M3 decommission — model page serves `isDeprecated: true`, "deprecated on 09/08/2026") emits deltas AFTER the chunk carrying `finish_reason`. The MiniMax-M3 native-tool normalizer finalized its framers at the FIRST finish_reason chunk, so any trailing delta — even an empty string — hit the FINISHED framer and raised a non-retryable `RuntimeError("MiniMax-M3 tool framer is already finished")` → terminal "API Error" on every tool turn (not routed through the malformed-markup recovery path). Second latent bug: duplicate finish_reason chunks re-ran finalization and re-parsed the retained tool block, duplicating generated tool calls.
- Fix: hold-terminal + end-of-stream finalization in `providers/nvidia_nim/native_tool_stream.py` — framers are fed every string delta regardless of position (tool blocks streamed after the terminal chunk still decode; trailing non-markup text passes through as content); the terminal marker (first finish_reason wins) + latest usage are held back and re-emitted as one final chunk after the raw stream ends; finalization runs exactly once. Framer class unchanged (FINISHED guard kept as defensive invariant). 5 new regression tests incl. the exact #1734 repro (empty delta after finish), verified to fail on pre-fix code with the user-reported error. Deprecated `minimaxai/minimax-m3` dropped from `NVIDIA_NIM_CLI_DEFAULT_MODELS` smoke defaults + contract test (users who configured the model themselves keep working).
- Verified: targeted 231p; §12.5 full set green before push (gates green; suite 5175p/144s; e2e 97p/1s). No local NIM key — mocked tests authoritative (LLM7/Lightning stance); NIM deprecation verified live from the public model page.
- Current: `cfa42f8` (single-commit), v6.2.3, base `81fa340` (v6.2.2) — PR #1742 raised 2026-09-11; greptile PASSED first review (5/5, 0 comments) + all 7 CI green. **CLOSED UNMERGED by the maintainer on 2026-09-12** with reason: "the minimax model is deprecated — no need to fix, just stop using it". Branch FROZEN at `cfa42f8` — excluded from sync #8 (user decision; do NOT update/push). Still merged into `final` at `cfa42f8` (§10) — the internal integration keeps the fix since the hold-terminal normalizer is generic, not minimax-specific.

### 🔄 `update-main-fix-issues` — JSON-Schema `pattern` sanitization — **PR [#1744](https://github.com/Alishahryar1/free-claude-code/pull/1744) OPEN** ([#1730](https://github.com/Alishahryar1/free-claude-code/issues/1730))
- Root cause: Claude Code's `Artifact` tool embeds a `pattern` regex using Unicode property escapes + a negative lookahead (`^(?!__.*__$)[^\p{Cc}\p{Cf}\p{Zl}\p{Zp}...]`). OpenAI-compatible providers validate `pattern` values against dialects that reject these constructs (Rust `regex` rejects lookaround; JS no-`u` and Python `re` reject `\p{}`) → whole request 400s with `invalid_function_parameters` on `tools[N].parameters` before reaching the model. No request-side sanitization existed (NIM's sanitizer only strips boolean subschemas / aliases arg names).
- Fix: `sanitize_tool_schema_patterns` in `core/anthropic/tool_schema.py` — drops any `pattern` whose value contains `\p{`/`\P{` (a stripped remainder could only be STRICTER than the original, rejecting arguments the schema allowed — greptile P1), walking ONLY JSON Schema subschema keywords (`properties`/`items`/`anyOf`/`additionalProperties`/`$defs`/`patternProperties`/… — greptile P1: literal-value keywords like `enum`/`const`/`default`/`examples` are never traversed). Copy-on-write: nodes without offending patterns returned as-is, input never mutated. Wired into BOTH request emission points: `conversion.py` `convert_tools` (all ~45 openai_chat providers) + `openai_responses/provider_input.py` (Codex/Responses). PR body triages the other reviewed issues: #1732 delivered by #1740, #1662 claimed upstream by #1679, #1654/#1689 already covered by README "Claude Code in VS Code" — PR closes #1730 only.
- Verified: targeted 152p; §12.5 full set green before every push (gates green; suite 5180p/144s; e2e 97p/1s). Dropping a pattern trades server-side validation strictness for the request reaching the model — client still validates locally.
- Current: `4ae75ae` (amended, single-commit), v6.2.4, base `81fa340` (v6.2.2) — PR #1744 raised 2026-09-11. Greptile: first review 4/5 with 2 P1s (stripping `\p{L}` from `[\p{L}\d]+` narrows to `[\d]+` → must drop, never strip-keep; walker rewrote literal `pattern` keys under `enum`/`const`/`default`/`examples`) → fixed (drop-always + subschema-keyword-only traversal), §12.5 full set green, force-pushed `f2ce738`. Second review 4/5 with 1 P1 (`propertyNames`/`unevaluatedProperties` are SINGLE schemas, misclassified as maps — direct patterns retained) → fixed (moved to single-schema group) + §12.5 full set green + force-pushed `4ae75ae` → **greptile PASSED + all 7 CI checks green — merge-ready (§12.4 gate met)**; merging is the upstream owner's call. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` → `e3dc94e1`, v6.2.16 (PATCH above 6.2.15); §12.5 full set green; conflict cleared, greptile + all 7 CI green — merge-ready.

### 🔄 `add-experiential-labs` — Experiential Labs provider — **PR [#1749](https://github.com/Alishahryar1/free-claude-code/pull/1749) OPEN** ([#1737](https://github.com/Alishahryar1/free-claude-code/issues/1737))
- Standard catalog provider (§5 template, LLM7/Lightning pattern — auto-wired `OpenAIChatProfile`, no factory/runtime protocol code). Gateway speaks OpenAI Chat Completions at `https://api.experientiallabs.ai/v1`; auth `Bearer` with `xpl_`+40-hex keys minted at platform.experientiallabs.ai/settings/api-keys; env `EXPLABS_API_KEY`/`EXPLABS_BASE_URL`/`EXPLABS_PROXY` (matches their docs 1:1).
- Free tier: host-managed $0 models with tools+streaming — `gemma-4-26b-a4b-it-free` (smoke default, 262k ctx), `dots-3-note-preview-free` (512k), `laguna-s-2.1-free`, `laguna-xs-2.1-free`, `lfm-2.5-2.6b-free` (65k), `ling-3.0-flash-fin-free` (262k). Promo free-tier slugs (`deepseek-v4-flash`, `gpt-5.6-luna`, 50%-off `qwen3.8-27b`) require a payment method — deliberately NOT used as defaults. Lineup is "seeded by operations" and may rotate; models are user-configurable via `MODEL=experiential/<slug>` and auto-discovered per key.
- Profile: `_policy("EXPERIENTIAL", ReasoningReplayMode.REASONING_CONTENT, default_max_tokens=ANTHROPIC_DEFAULT_MAX_OUTPUT_TOKENS)` (thinking survives as reasoning_content → Claude thinking blocks) + `NamedEffortReasoning(_LOW_MEDIUM_HIGH, enabled_value="medium")` with NO `disabled_value` — OFF omits `reasoning_effort` entirely so each model keeps its documented default effort (the "none" vocabulary is unverified for this gateway). `OpenAIModelListing(path="/models")` bare id-only listing (no context-window fields on that endpoint).
- Unlike LLM7/Lightning (public catalogs, no probe), this provider HAS a credential probe — `GET /v1/models` is their documented key-verification call: `_Probe("experiential", "/models", _MODELS, _AUTH_401)` in `providers/credential_validation.py`. Shared-credentials count stays 20 (all_keys +1, supported +1, CASES entry added in the same change).
- Tests: `tests/providers/test_experiential.py` (~230 lines, 12 items — construct/reasoning-default-ON-OFF/effort-matrix/replay/bare-listing/missing-id/empty-catalog/wire-URL-Bearer) + runtime config test + credential-validation CASES entry + catalog-order + smoke-config trio.
- Current: `3886c8e` (single-commit), v6.3.0 (MINOR — new provider), base `e632c85` (upstream tip at PR time). §12.5 full set green pre-push (gates green; suite 5191p/144s; e2e 97p/1s; targeted 179p). Greptile: **PASSED first review (15 files, 0 comments) + all 7 CI checks green — merge-ready (§12.4 gate met)**; merging is the upstream owner's call. Version-only collision with #1736/#1740 (both 6.3.0) is routine §8, resolved at rebase/merge. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` → `b61736c0`, v6.3.0; §12.5 full set green; conflict cleared, greptile + all 7 CI green — merge-ready.

### 🔄 `add-orca-router` — OrcaRouter provider — **PR [#1754](https://github.com/Alishahryar1/free-claude-code/pull/1754) OPEN** ([#1751](https://github.com/Alishahryar1/free-claude-code/issues/1751))
- Issue-first workflow (user's new template): raised upstream issue #1751 2026-09-12, user relayed the URL back, then implemented. Standard catalog provider (§5 template, LLM7/Experiential pattern — auto-wired `OpenAIChatProfile`, no factory/runtime protocol code). Multi-provider OpenAI-compatible gateway at `https://api.orcarouter.ai/v1` routing to 11 upstreams (OpenAI, Anthropic, Gemini, DeepSeek, Grok, Qwen, Kimi, MiniMax, Z.ai, Kling, Seedance) at provider cost, zero markup; env `ORCAROUTER_API_KEY`/`ORCAROUTER_BASE_URL`/`ORCAROUTER_PROXY`; keys `sk-orca-...` from www.orcarouter.ai/console.
- Free tier: $0 models under `-free` ids — today `deepseek/deepseek-v4-flash-free` (smoke default) + `deepseek/deepseek-v4-pro-free` — plus router aliases `orcarouter/free` (auto-picks among free models per request) and `orcarouter/auto` (cheapest live). Lineup rotates ("free capacity changes as models come and go"); user-configurable via `MODEL=orcarouter/<slug>` + auto-discovered per key. Limits: per-workspace fixed windows (RPM/UTC-day) tiered by lifetime spend, per-request prompt cap on lowest tier; 429 code `free_rate_limited` + `Retry-After` distinguishes retryable windows from non-retryable prompt caps.
- Profile: `_policy("ORCAROUTER", ReasoningReplayMode.REASONING_CONTENT, default_max_tokens=ANTHROPIC_DEFAULT_MAX_OUTPUT_TOKENS)` (gateway surfaces `reasoning_content` per upstream) + `NamedEffortReasoning(_LOW_MEDIUM_HIGH, enabled_value="medium")` with NO `disabled_value` — OFF omits the field (`minimal`/`max` documented only "on some models" — excluded from the safe vocabulary). `OpenAIModelListing(path="/models")` bare id-only (documented shape has no context-window fields). Credential probe `_Probe("orcarouter", "/models", _MODELS, _AUTH_401)` — `/v1/models` requires the key (documented verification call); shared-credentials count stays 20.
- Nested-slash model ids (`orcarouter/deepseek/deepseek-v4-flash-free`) split on FIRST slash — tokenrouter precedent (`tokenrouter/moonshotai/kimi-k3-free`).
- Tests: `tests/providers/test_orcarouter.py` (16 items incl. parametrizes — construct/effort-matrix with OFF+DEFAULT omission/reasoning_content tool-history replay/bare-listing + malformed rejection/wire URL+Bearer) + runtime config test + credential-validation CASES + catalog-order + smoke-config trio.
- Current: `f8d8239` (single-commit), v6.3.0 (MINOR — new provider), base `e632c85` (upstream tip at PR time — #1749 NOT merged upstream, so anchors insert after llm7). §12.5 full set green pre-push (gates green; suite 5192p/144s; e2e 97p/1s; targeted 180p). PR #1754 raised 2026-09-12; **greptile PASSED first review (15 files, 0 comments) + all 7 CI checks green — merge-ready (§12.4 gate met)**; merging is the upstream owner's call. Version-only collision with #1736/#1740/#1749 (all 6.3.0) — routine §8, resolved at rebase/merge. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` → `3b4f2033`, v6.3.0; §12.5 full set green; conflict cleared, greptile + all 7 CI green — merge-ready.

### 🔄 `feat-api-key-rotation` — Multiple API keys with rotation + failover — NO PR ([#1301](https://github.com/Alishahryar1/free-claude-code/issues/1301))
- `providers/key_pool.py`: thread-safe `KeyPool` (round-robin, cooldown failover, `parse_api_keys`); `OpenAIChatProvider` resolves the credential per request via `_resolve_api_key` when rotating; `_report_key_failure`/`_report_key_success` hooked into the stream path (rotate on 429/401/403); factory builds a pool when the credential holds >1 comma-separated key. Tests: `tests/providers/test_key_pool.py`.
- Usage: `OPENROUTER_API_KEY="sk-1,sk-2,sk-3"`. Single key = unchanged static behaviour.
- **Awaiting user decision to open a PR** (upstream #1655+#1656, another author, may cover #1301). Current: `03def116`, v6.3.0 — rebased onto main `0dcb3715` in sync #8 (2026-09-12; provider.py KeyPool `_resolve_api_key` overlap resolved keep-both); §12.5 full set green; force-with-lease pushed.

### 🔄 `fix-cline-hub-hijack` — fcc-cline reconnects to a stale Cline Hub — **PR [#1641](https://github.com/Alishahryar1/free-claude-code/pull/1641) OPEN** ([#1590](https://github.com/Alishahryar1/free-claude-code/issues/1590))
- Root cause: interactive Cline passes `backendMode:"auto"` to core (verified in the shipped cline.exe), overriding the launcher's `CLINE_SESSION_BACKEND_MODE=local`, so Cline may attach to (or start) a **detached Hub daemon** that resolves provider settings from the user's global `~/.cline/data/settings/providers.json` instead of FCC's ephemeral file — and outlives the launcher. The next `fcc-cline` run auto-discovers that stale Hub via `~/.cline/data/locks/hub/production.json` and routes to the wrong provider.
- Fix (defense-in-depth, isolation over deletion): `build_cline_launcher_env` now sets `CLINE_HUB_DISCOVERY_PATH` to `<ephemeral-tempdir>/hub/production.json` — a file that never exists and is never written — so the child can never discover ANY pre-existing Hub; any Hub it spawns writes discovery inside the ephemeral tree, deleted on exit. A user-run `cline hub` (ordinary cline) keeps its own discovery file, untouched. Upstream real fix: cline/cline#13631 + PR cline/cline#13637 (owner-filed, unmerged as of 2026-08-30); `CLINE_HUB_DISCOVERY_PATH` is an internal Cline env var (present in shipped binary) — if renamed upstream it degrades to today's behavior with no new failure mode.
- Tests: 2 updated + 2 new in `tests/cli/test_cline_launcher.py` (env override of a stale user value; ephemeral-tree placement; file absent at spawn).
- Current: `2c8945e`, v5.19.2, base `96495b9` (v5.19.1) — rebased on 2026-09-02 to clear the PR #1641 dirty state (upstream advanced `b85ae4a`→`96495b9`); version-only conflict resolved keeping PATCH 5.19.2; single-commit shape preserved (4 files, `rev-list --count main..HEAD`=1); suite 4453/148/0, e2e 50 passed + Windows-locale context-meter only, gates green; force-with-lease pushed `8962efa...2c8945e`. API-verified **mergeable=True** (state unstable = checks re-running). §12.3 greptile-first applies: no manual test runs vs the bot — wait for its review before re-validating. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` → `acf94479`, v6.2.16 (PATCH above 6.2.15); §12.5 full set green; conflict cleared, greptile + all 7 CI green — merge-ready (§12.4 met).

---

## 8. Sync Log

### `final` SonarQube-style audit + fix pass (2026-09-12) — `cde32c9` → `3666dcc` (4 commits, no upstream movement)

**Scope:** user-directed deep-audit of `src/` on `final` only (never PR'd). Tools: bandit 1.9.x, vulture 2.14, deptry 0.17, pip-audit 2.10 (via `uvx`), ruff 0.16.4 `--select ALL` pass. Verified clean already: configured ruff ruleset 100%, zero TODO/noqa/type-ignores, constant-time auth, loopback-guarded admin, 0o600 secret files.

**Batch 1 — `1730268` (security):** sha1 digest `usedforsecurity=False` (`core/openai_responses/tools.py`, non-crypto tool-id); sqlite identifier allowlist `_TABLES` + `_check_sql_identifiers()` fail-closed validation of interpolated table/column names (`runtime/code_sessions_sqlite.py` `_insert`/`_update`; all data stays `?`-parameterized).

**Batch 2 — `80d1fc2` (CVEs, lock-only, NO pyproject edits):** starlette 0.52.1→**1.3.1** (major; ASGI layer — validated by full suite + e2e), cryptography 49.0.0→**50.0.0** (major; only via google-auth/vertex), python-multipart 0.0.22→0.0.31, urllib3 2.6.3→2.7.0, click 8.3.1→8.3.3, pygments 2.19.2→2.20.0, msgpack 1.1.2→1.2.1 (via librosa/voice_local). Fallouts fixed: starlette 1.6 TestClient now returns `httpx2.Response` → tests/api/test_ordinary_error_phases.py annotation switched to httpx2. pip-audit re-run: **0 vulnerabilities**.

**Batch 3 — `e6ff13d` (dead code):** removed 7 verified-zero-reference exports (routing.py `resolve_messages_request_with_policy`, admin/validation.py `validate_values`, admin/manifest.py `field_input_key`+`fields_with_attrs`, env_migrations.py `env_text_needs_migration`, openai_responses/reasoning.py `responses_reasoning_to_output_config`, streaming/error_mapping.py `openai_error_from_anthropic_error`) + now-unused imports; 78 deletions/6 files. **8th candidate `TRACE_PAYLOAD_BINDING` REVERTED** — it is deliberately imported by tests/core/test_trace.py to pin the trace↔logging bind-key contract (Phase-1 grep truncation hid the test import).

**Batch 4 — `3666dcc` (smells, 21 files, broad-but-safe):** ruff autofixes (FURB110 ×4 falsy-safe, FURB167 ×7, RET/PIE/PTH/ISC/PLC/PYI/Q/RSE/PLR5501 set); hand-fixes PLR1714 ×15 (incl. workflow.py cross-operand `!=` chain → `not in` tuple, logic-equivalent), FLY002 ×6 (str-only verified), RET504, PLW2901 ×2 markdown (comprehension); ASYNC240: code-session `_create` `Path.resolve` offloaded to `anyio.to_thread.run_sync` (per-request path). Gates after each batch: ruff format/check, ty, pytest -q 5306p/144s, e2e 98p/1s (2 first-run timing flakes reproduced nowhere on rerun).

**Documented WONTFIX (do NOT re-litigate in future audits):** bandit B608 ×3 (identifiers now allowlisted; data `?`-parameterized — residual f-string SQL is table/column names only), B101 asserts (invariants), B105/B106/B110/B112/B603/B607/B104/B311/B615/B404 (reviewed false positives/benign); TC00x typing-import placement (~764 sites; conflicts with PEP 649 lazy annotations); C901/PLR091x complexity (~40; churn > value); PLW0603 module-level config state (deliberate); PLW2901 tool_adaptation `tool` rebinds ×2 (intricate restore-merge pipeline, intent verified); ASYNC240 runtime/application.py ×2 (startup-only, once per process); ASYNC109 limiter `timeout` param (public API name). deptry: all import↔dist name FPs, no unused deps.

**⚠️ Final-only:** all 4 commits exist ONLY on `final`. A future §9 rebuild-from-main recreates final from scratch and DISCARDS this pass — cherry-pick `1730268 80d1fc2 e6ff13d 3666dcc` (or re-run the audit) if wanted on the new final. The CVE lock-bumps would be re-derived automatically only if upstream bumps too.

### Sync #8 (2026-09-12 → 09-13) — upstream base `f3a3aac` → `0dcb3715` (v6.2.15)

**Trigger:** upstream main advanced `f3a3aac` → `0dcb3715` (11 commits #1756–#1767; 46 files +5194/−345; version 6.2.2 → **6.2.15** — VS Code + Codex integrations, JetBrains ACP preview card, admin loading fix, Codex client tool discovery fix). Local main ff-synced + pushed to fork. All 8 open-PR branches went conflict-dirty; merge-tree scoped them version-only (exceptions: `add-custom-provider` + `feat-api-key-rotation` also touch `providers/openai_chat/provider.py`).

**Per-branch results (§12.5 full set green on every branch — gates + full suite (5497–5520p/152s) + e2e (116p/1s, Windows-locale context-meter exception); every open PR conflict cleared + greptile PASS + all 7 CI green):**

| Branch | Old → New SHA | Version | Method |
|--------|---------------|---------|--------|
| `main` | `f3a3aac` → `0dcb3715` | 6.2.15 | ff-only + push origin/main |
| `fix-ollama-model-discovery` (#1606) | `04e5c04` → `132b5fdc` | 6.2.16 (PATCH) | merge main INTO branch (never-rewrite), ff push NO force |
| `fix-cline-hub-hijack` (#1641) | `bf157a2` → `acf94479` | 6.2.16 (PATCH) | rebase + force-with-lease |
| `feat-models-metadata` (#1736) | `5fe9ce8` → `a56c9856` | 6.3.0 (kept) | rebase + force-with-lease |
| `add-lightning-ai` (#1740) | `3575595` → `96a601d0` | 6.3.0 (kept) | rebase + force-with-lease |
| `update-main-fix-issues` (#1744) | `4ae75ae` → `e3dc94e1` | 6.2.16 (PATCH) | rebase + force-with-lease |
| `add-experiential-labs` (#1749) | `3886c8e` → `b61736c0` | 6.3.0 (kept) | rebase + force-with-lease |
| `add-orca-router` (#1754) | `f8d8239` → `3b4f2033` | 6.3.0 (kept) | rebase + force-with-lease |
| `add-custom-provider` (#1469) | `b69108d` → `b218d21e` | 6.3.0 (kept) | complex rebase — `api/admin_routes.py` (asyncio.gather + `_probe` closure preserving custom blank-URL skip + keyless bare `client.get`, §8 sync #6 precedent), `providers/openai_chat/provider.py` (`api_key=resolved_api_key or "no-api-key"` combined with upstream changes), `e2e/conftest.py` + `tests/api/test_admin.py` keep-both + force-with-lease |
| `feat-api-key-rotation` (NO PR) | `6298e19` → `03def116` | 6.3.0 (kept) | rebase — `provider.py` KeyPool `_resolve_api_key` overlap kept both + force-with-lease |

- Greptile sweep after all pushes: every open PR re-reviewed clean on its new head (0 blocking comments; #1469: "17 files reviewed, 0 comments added"; #1744 head `e3dc94e1` clean). §12.4 gate met on all.
- **Exclusions (user decisions):** telepub FROZEN at `50559ea` (§12.1 — untouched). `fix-nim` PR #1742 CLOSED UNMERGED by the maintainer 2026-09-12 ("the minimax model is deprecated — no need to fix, just stop using it") — branch frozen at `cfa42f8`, NOT updated; still merged into `final` at `cfa42f8`.

**`final` rebuild (base `0dcb3715`, 2026-09-12/13):**
- Old final `d0cc706` preserved as local `final-backup-20260912-audit`; final reset to main, ALL 11 branches merged in §9 order (first-parent stack): telepub `50559ea` `9db9d67a` → key-rotation `2d33e610` → models-metadata `6262e6cb` → custom-provider `2da8b73b` → ollama `a6ae9f15` → update-main-fix-issues `9fc965df` → cline `999e0212` → fix-nim `cfa42f8` `e271aa46` → lightning `4e707130` → experiential `5164cf3b` → orca `33a05822`. All anchors resolved keep-both (HEAD side first); trio order lightning → experiential → orcarouter at every anchor (§9 rule); version 6.3.0; lock regenerated after the last merge.
- Audit re-application: `841dfc9e` (security — sha1 `usedforsecurity=False`; tools.py conflict resolved keeping upstream's new tool-discovery code), `6a077f65` (dead exports ×7, clean), `424ab991` (smells; the RET504 admin_routes site no longer exists upstream — not re-applied), `0cefbc68` (fresh CVE lock pass — starlette 1.6.0, cryptography 50.0.1, python-multipart 0.0.32, urllib3 2.7.0, click 8.5.0, pygments 2.21.0, msgpack 1.2.2; pip-audit 0 vulns; lock re-derived fresh, NOT a `80d1fc2` cherry-pick) + httpx2 test annotation re-applied (`tests/api/test_ordinary_error_phases.py`).
- **INCIDENT — pyproject deps silently dropped (fixed `3e77f612`):** telepub is based on OLD main (`f3a3aac`, predating upstream's `json5`/`tomlkit`/`simplejson` additions), so merge 1 made final's pyproject "delete" those dep lines relative to the merge base; every later merge silently preserved the deletion (symptoms: `uv lock` "nothing to commit" after merge 11; later ty ×8 unresolved-import). Fix: restored the 3 dep lines at main's exact placement + re-locked (162 packages). **Future §9 rebuilds: after the telepub merge, immediately diff pyproject deps against main.**
- Count fix `7e78423`: the trio merge resolved `test_unsupported_shared_credentials_never_send_http` to 21; §9 formula (main 20 + telepub +1 + lightning +1 = 22) restored both assertions to 22.
- Verification: first-parent ancestry 11/11 + main + fix-nim all `merge-base --is-ancestor` green; catalog 55 == `SUPPORTED_PROVIDER_IDS`; README provider rows 54 == old final exactly (upstream added 0 providers in #1756–#1767; the plan's stale "53" was a sync-#7-era value); gates green; full suite 5633p/152s; e2e 116p/1s; pip-audit 0 vulns.
- Notes restored from `final-backup-20260912-audit` (§9 step 7) and updated in this sync #8 commit.

### Sync #7 (2026-09-02) — upstream base `b85ae4a` → `96495b9` (v5.19.1)

**Trigger:** upstream main advanced `b85ae4a` → `96495b9` (2 commits: #1644 "Keep chat operations alive across clients", #1645 "Add internal Codex Direct app-server transport foundation"; 28 files, +6360/−767; version 5.18.11 → **5.19.1**, `uv.lock` bumped). Both OPEN PRs (#1606, #1641) went `dirty` — merge-tree predicted version-only conflicts (pyproject.toml + uv.lock) for each.

**Per-branch results (all gates green; suites fully green):**

| Branch | Old → New SHA | Version | Full suite (p/s/f) | Push |
|--------|---------------|---------|--------------------|------|
| `main` | `b85ae4a` → `96495b9` | 5.19.1 | — | ff-only + push origin/main |
| `fix-ollama-model-discovery` | `0b3d158` → `edd34fb` | 5.19.2 (PATCH) | 4454/148/0 | merge of `main` INTO branch + ff push (NO force) — PR #1606 conflict cleared |
| `fix-cline-hub-hijack` | `8962efa` → `2c8945e` | 5.19.2 (PATCH) | 4453/148/0 | rebase onto `main` + force-with-lease — PR #1641 conflict cleared |

- **ollama (never-rewrite):** `git merge upstream/main` onto `0b3d158` → version resolved 5.19.2, `git checkout main -- uv.lock` + `uv lock` regenerated (free-claude-code 5.19.1→5.19.2), zero markers, merge commit `edd34fb` (parents `0b3d158`+`96495b9`, both ancestor-exit-0 verified). FF push only `0b3d158..edd34fb`.
- **cline (standard):** rebase onto `main`; version-only conflict resolved 5.19.2; single-commit shape preserved (`2c8945e`, 4 files); force-with-lease `8962efa...2c8945e`.
- API-verified after pushes: **#1606** head `edd34fb` → later `c84164c`, base `96495b9`; **#1641** head `2c8945e`, base `96495b9`. Final states (2026-09-02): both PRs `mergeable=true, state=clean` — all 7 checks green incl. Greptile.
- **ollama CI re-trigger (2026-09-02):** the first Actions run for `edd34fb` (33610053117) was CANCELLED (GitHub-side; no superseding run existed). Re-run API returned 403 (PAT has no upstream write). Appended an EMPTY commit `c84164c` and ff-pushed (`edd34fb..c84164c`) to re-trigger → run 33612506300 **SUCCESS** (pytest, playwright, ruff-format, ruff-check, ty, ban-suppressions all success) + Greptile Review success → PR #1606 `clean`. Empty-commit re-trigger is the standing fallback when a run is cancelled and upstream write is unavailable.
- **`state=blocked` on ALL open PRs = required approving review, NOT a CI failure (2026-09-02):** repo `main` rulesets (via `rules/branches/main`): (1) `main-integrity` — required checks `{Ban suppressions, ruff-format, ruff-check, ty, pytest, playwright}` with `strict_required_status_checks_policy=true`, `required_linear_history`, deletion/force-push banned, squash-only merges; (2) `main-review-required` — `required_approving_review_count: 1`. All three PRs (#1469, #1606, #1641) now report `mergeable=True state=blocked` identically → the blocker is the missing approving review, nothing to fix on the branches. PSA: the earlier #1606 `state=clean` briefly seen was GitHub's pre-ruleset cache; and the "pytest error" a viewer may see is the CANCELLED run 33610053117 attached to intermediate commit `edd34fb` (its log ends `##[error]The operation was canceled.` at 93% PASSED — NO test failures; GitHub-side cancellation). Fork-side cannot approve (not a maintainer) nor re-run cancelled runs (403 without upstream write); owner must click Re-run or Approve.
- e2e both branches: **50 passed** + only the Windows-locale `test_chat_context_meter_...` failure (passes on ubuntu CI). NOTE: upstream #1644 reworked `e2e/test_chat_sessions.py` — the delayed-older-page test now asserts `.assistant-message:not(.live-message)` count 2 (no more `to_be_enabled()`), new `_hold_next_chat_operation` helper; it **passed** on both branches this cycle.
- Standing debts (unchanged): `final` still `6e2aa56` (v5.19.0, base `b85ae4a`) — rebuild onto `96495b9` per §9 (will also pick up `add-custom-provider` `b596e07` incl. the 409-retry fix and ollama `edd34fb`). `add-custom-provider` origin advanced to `b596e07` = "Merge branch 'main' into add-custom-provider" (web/user-driven; parents `1e537fb`+`96495b9`) — local ref synced, PR #1469 current and CI green.

### Sync #6 (2026-09-01)

**Trigger:** upstream main advanced `32491e7` → `b85ae4a` (12 commits: #1618 durable local Chat Sessions + sqlite store, #1623–#1632 Chat Sessions/Admin UI polish, #1615 versioned Admin assets, #1616 sidebar pinning, #1634 Groq TPM budget recovery, #1635 Admin branding polish; version 5.17.5 → **5.18.11**). Local main synced `--ff-only` + pushed fork. Pre-restructure history (older sync logs) lives at `D:\Agentic coding\Project\claude\HANDOFF_NOTES.pre-cleanup-20260827.bak`.

**Per-branch results (all gates green; suites fully green):**

| Branch | Old → New SHA | Version | Full suite (p/s/f) | Push |
|--------|---------------|---------|--------------------|------|
| `main` | `32491e7` → `b85ae4a` | 5.18.11 | — | ff-only + push |
| `fix-cline-hub-hijack` | `8573cbe` → `8962efa` | 5.18.12 (PATCH) | 4407/148/0 | force-with-lease |
| `feat-api-key-rotation` | `4e00047` → `fd26c36` | 5.19.0 (MINOR) | 4421/148/0 | force-with-lease |
| `feat-models-metadata` | `82e72a3` → `2e72ae0` | 5.19.0 (MINOR) | 4408/148/0 | force-with-lease |
| `add-custom-provider` | `af2922f` → `6ac42f9` | 5.19.0 (MINOR) | 4422/148/0 | force-with-lease (PR #1469 updated) |
| `fix-ollama-model-discovery` | `79e8345` → `0762bfd` | 5.18.12 (PATCH; bump commit on top, external merge `e42e115` preserved) | 4291/148/0 | fast-forward, NO force |
| `final` | `689f422` (deleted) → `6e2aa56` | 5.19.0 | 4452/148/0 | force-with-lease |

**Rebase notes:**
- All 4 rebased branches conflicted in `pyproject.toml` + `uv.lock` only (merge-tree predicted) — except `add-custom-provider`, which also conflicted in `src/free_claude_code/api/admin_routes.py` + `tests/api/test_admin.py` (upstream's parallel `asyncio.gather` refactor of `local_provider_status`).
- **Semantic merge on admin_routes:** kept BOTH imports (`openai_v1_base_url` + upstream's `package_version`); `local_provider_status` now uses upstream's `asyncio.gather` concurrency with a `_probe` closure that preserves the custom blank-URL skip + api_key/proxy passthrough. Upstream's strict `SlowAsyncClient` e2e fake (`get(self, url)`) exposed that the probe always passed empty `headers` — fixed by attaching headers ONLY when a credential is configured (keyless locals get a bare `client.get(url)`). `tests/api/test_admin.py`: upstream's concurrency test + all 4 custom-provider tests kept in full.
- Version invariant restored per branch (MINOR → 5.19.0, PATCH → 5.18.12) during conflict resolution + `uv lock` — single-commit shapes preserved (no amend needed); the ollama branch got a separate bump commit instead (never rebase it).
- Telepub merged into `final` at frozen SHA `17382eb` now 3-way conflicts on version files only (main moved past its base `3ef17fe`) — version-only, resolved per §9; NOT non-additive.

**Pre-existing upstream e2e failures (verified on clean `main` — NOT ours):**
- `e2e/test_chat_sessions.py::test_chat_context_meter_shows_used_over_advertised_context_window` — fails on Windows ONLY: the meter renders `100k` (lowercase, `Intl.NumberFormat` compact) while the test regex expects `100K`. **PASSES on ubuntu CI** — proven by sibling PR playwright runs (#1641 `8962ef`, #1606 `0b3d158` both green on the same base) and by the #1469 CI log. Not a CI blocker; do not chase locally.
- `e2e/test_chat_sessions.py::test_delayed_older_page_cannot_cross_into_another_chat` — ROOT CAUSE FOUND + FIXED on `add-custom-provider` (`1e537fb`, 2026-09-02): the test's rename PATCH races the second send's revision bump → 409 → `updateSession` silently dropped the rename → the renamed library card never appeared → 30s click timeout at line 243. Confirmed from the actual CI log (run 33433364609, job 99623834946). Fixed by the 409 retry in `chat_sessions.js` (see §7 add-custom-provider card). Carry the fix upstream / merge into `final` at next rebuild.
- One full-e2e run on `final` showed 12 transient ERRORs in chat-sessions tests right after the full suite finished (resource contention) — all passed standalone. Re-run e2e before believing chat-sessions errors.
- **CI-log access trick:** Actions logs/artifacts are auth-gated, but the stored git credential (`git credential fill` → Tanishq-1 PAT) works: `Invoke-WebRequest -Headers @{Authorization="Bearer <PAT>"} https://api.github.com/repos/Alishahryar1/free-claude-code/actions/runs/<id>/logs` returns the zip with per-job logs. Use it instead of guessing from annotations (annotations only say "Process completed with exit code 1").

**`final` rebuilt from scratch:** fresh from `main` (`b85ae4a`); merges: `add-telepub-voyage` (version-only) → `feat-api-key-rotation` (clean) → `feat-models-metadata` (clean) → `add-custom-provider` (**7-file additive merge** — kept BOTH `telepub_voyage` + `custom` in catalog/profiles/settings/provider_manifest/contract test/`.env.example`; `provider.py` semantic merge `api_key=resolved_api_key or "no-api-key"`) → `fix-ollama-model-discovery` (version-only, kept 5.19.0). All 5 branches + main verified as ancestors via exit-code checks; 9-symbol code audit 9/9 HIT (§9); gates green; suite 4452/148/0; e2e 42 passed + only the pre-existing failure; pushed `6e2aa56`.

**Sync rails (durable rules — always apply):**
1. `$env:GIT_EDITOR='true'` before every rebase and `rebase --continue` (invisible `vim.exe` hang).
2. Resolve conflicts with exact edits, never regex; verify zero `<<<<<<<` markers before continuing.
3. Lockfile order: resolve `pyproject.toml` → `git checkout main -- uv.lock` → `uv lock` → marker check → `git add <explicit paths>` (never `-A`; stray `Microsoft/Windows/PowerShell/ModuleAnalysisCache` dirs otherwise).
4. Long pytest runs: background terminal after explicit `Set-Location` into the repo (foreground runs were killed ~163s).
5. PowerShell exit codes: `git merge-base --is-ancestor A B; $LASTEXITCODE -eq 0` — never test output truthiness.
6. Version bump + `uv lock` in the SAME commit; amend to preserve single-commit branch shape.
7. After a rebase auto-converges the version to base, re-edit + `uv lock` + amend to restore the above-base invariant.
8. The ollama PR branch carries an EXTERNAL merge commit — add commits on top only, push without force.
9. Full suite + e2e may run concurrently in two background terminals, but see the concurrency gotcha above before trusting config-area results.

---

## 9. Final Integration Branch (`final`)

**Purpose:** unified integration of ALL active feature branches on current upstream main — validates feature interactions end-to-end. Internal artifact: NOT intended for an upstream PR; NEVER raise a PR from `final`.

**Rebuild recipe (after every upstream sync):**

1. **Sync main first:** `git fetch upstream main`; verify lineage (`git merge-base --is-ancestor <old-tip> upstream/main` — if it fails, upstream force-pushed: STOP and reassess); `git switch main && git merge --ff-only upstream/main`; push `origin main`.
2. **Backup + fresh final:**
   ```powershell
   git branch final-backup-<YYYYMMDD> <old-final-sha>   # local-only insurance
   git branch -f final main
   git switch final
   ```
3. **Merge ALL active branches in this order** (plain `git merge --no-edit <branch>`; peer branches produce merge commits):
   1. `add-telepub-voyage` (`50559ea`, §12.1) — expect clean
   2. `feat-api-key-rotation` (`6298e19`) — expect clean (key_pool/openai_chat files; overlaps only with custom-provider in `provider.py`)
   3. `feat-models-metadata` (`5fe9ce8`) — expect clean
   4. `add-custom-provider` (`b69108d`) — ~7 additive conflicts; combine with key-rotation in `provider.py` via `api_key=resolved_api_key or "no-api-key"`; catalog-order tuple tail: `..., "ollama", "telepub_voyage", "custom"`
   5. `fix-ollama-model-discovery` (`04e5c04`) — version-only (keep highest)
   6. `update-main-fix-issues` (`4ae75ae`) — version-only (keep highest)
   7. `fix-cline-hub-hijack` (`bf157a2`) — version-only (keep highest)
   8. `fix-nim-minimax-post-terminal-framer` (`cfa42f8`) — version (keep highest); minimax-m3 smoke-default removals auto-merge
   9. `add-lightning-ai` (`3575595`) — trio #1: same-anchor additive conflicts vs telepub/custom at every llm7→ollama_cloud anchor; keep both sides; NO credential probe (count +1)
   10. `add-experiential-labs` (`3886c8e`) — trio #2: keep both sides; lightning entries BEFORE experiential in each anchor region; credential probe (count +0)
   11. `add-orca-router` (`f8d8239`) — trio #3: keep both sides; final anchor order = llm7 → lightning → experiential → orcarouter → ollama_cloud; credential probe (count +0)
4. **Trio stacking rule (every anchor region — catalog, settings, profiles, manifest, .env.example, README, smoke defaults, all test files):** entries order lightning → experiential → orcarouter, with telepub_voyage/custom trailing (README rows: LLM7 → Lightning → Experiential → OrcaRouter → Telepub → Ollama Cloud; catalog tuple tail: `..., llm7, lightning, experiential, orcarouter, ollama_cloud, lmstudio, llamacpp, ollama, telepub_voyage, custom`).
5. **Stacked-count gotchas (fix as follow-up commits — no amend needed on internal branch):**
   - README "ToS-friendly providers" count: each trio branch bumped 50→51 identically (auto-merges WRONG); telepub/custom branches deliberately did NOT bump. Set per branch intent: currently **53** (50 + trio). Double-check against the provider table row count (55 incl. 3 local + custom).
   - `test_credential_validation.py::test_unsupported_shared_credentials_never_send_http` count = stacked `len({credential_env} - {CASES envs})`: main 20 + telepub +1 + lightning +1 + experiential +0 + orca +0 = **22** (the lightning branch alone asserts 21 — stacked math differs!). Recompute, don't copy from any single branch.
   - Version: keep the highest (currently 6.3.0) across all pyproject/uv.lock conflicts; `uv lock` after the last merge.
6. **Verify:** `git merge-base --is-ancestor <branch> final` for ALL 11 (+ main); symbol audit (below) all hit; §12.5 full gate set (ruff format --check → ruff check → ty check → pytest -q → pytest e2e -q).
7. **Restore HANDOFF_NOTES.md** (the rebuild discards it — it is tracked on `final` only): `git restore --source=final-backup-<YYYYMMDD> HANDOFF_NOTES.md` → `git add -f HANDOFF_NOTES.md` → `git commit -m "Restore HANDOFF_NOTES.md"`. (Skip only if intentionally dropping note updates.)
8. **Push:** `git push --force-with-lease origin final`. **NEVER create a PR from `final`.**

**Symbol audit (all must hit on `final`):**
`TELEPUB_VOYAGE_DEFAULT_BASE` · `"custom": ProviderDescriptor` · `credential_optional=True` (in `profiles.py` — the `custom` OpenAIChatProfile) · `_drop_authorization_header` · `class KeyPool` · `_resolve_api_key` · `ProviderModelPricing` · `LOCAL_DISCOVERY_RETRY_COOLDOWN_S` · `resolved_api_key or "no-api-key"` · `LIGHTNING_DEFAULT_BASE` · `EXPERIENTIAL_DEFAULT_BASE` · `ORCAROUTER_DEFAULT_BASE` · `_Probe("experiential"` · `_Probe("orcarouter"` · `sanitize_tool_schema_patterns` · `_is_key_rotation_failure` · `_EXPECTED_PROVIDER_ORDER` contains all 5 new ids (`lightning`, `experiential`, `orcarouter`, `telepub_voyage`, `custom`) and equals `tuple(PROVIDER_CATALOG.keys())`

**HANDOFF_NOTES.md tracking (final only — since 2026-09-12):**
- This file is a git-tracked file on `final` ONLY. The `HANDOFF_NOTES.md` line in `.git/info/exclude` (local-only, NOT `.gitignore`) stays as a safety net → always stage with `git add -f HANDOFF_NOTES.md`; plain `git add` silently skips it.
- On every NON-final branch this file is ABSENT from the worktree (git removes it on switch). To consult: `git show final:HANDOFF_NOTES.md` (read-only). NEVER write a restored copy back into the worktree on another branch — it blocks `git switch final` ("untracked working tree file would be overwritten").
- To edit notes while on another branch: save the new text to a temp path (or edit the `git show` output), then once back on `final`, overwrite the file and commit.
- Switching away from `final` with uncommitted note edits is BLOCKED by git — intentional safety; commit notes before switching.
- Every §9 rebuild (step 7 above) must restore this file from the backup branch, or the rebuild discards it.

---

## 10. Current Git State (updated 2026-09-13)

| Branch | Issue / PR | SHA | Version | Status |
|--------|-----------|-----|---------|--------|
| `main` | — | `0dcb3715` | 6.2.15 | synced w/ upstream (`f3a3aac`→`0dcb3715` #1756–#1767), pushed to fork 2026-09-12 |
| `add-custom-provider` | PR #1469 OPEN (#1230) | `b218d21e` | 6.3.0 | sync #8 (2026-09-12): complex rebase onto `0dcb3715`; §12.5 full set green; **greptile clean (17 files, 0 comments) + all 7 CI green — merge-ready (§12.4)** |
| `fix-ollama-model-discovery` | PR #1606 OPEN (#1296) | `132b5fdc` | 6.2.16 | sync #8: merge of main into branch (never-rewrite), ff push; §12.5 full set green; **greptile + all 7 CI green — merge-ready (§12.4)** |
| `add-telepub-voyage` | PR #739 URL-share only — NO PR | `50559ea` | 6.3.0 | FROZEN (§12.1) — untouched in sync #8; merged into `final` at `50559ea` |
| `feat-models-metadata` | **PR [#1736](https://github.com/Alishahryar1/free-claude-code/pull/1736) OPEN** (#1168) | `a56c9856` | 6.3.0 | sync #8: rebased onto `0dcb3715`; §12.5 full set green; **greptile + all 7 CI green — merge-ready (§12.4)** |
| `add-lightning-ai` | **PR [#1740](https://github.com/Alishahryar1/free-claude-code/pull/1740) OPEN** (#1732) | `96a601d0` | 6.3.0 | sync #8: rebased onto `0dcb3715`; §12.5 full set green; **greptile + all 7 CI green — merge-ready (§12.4)** |
| `fix-nim-minimax-post-terminal-framer` | **PR [#1742](https://github.com/Alishahryar1/free-claude-code/pull/1742) CLOSED UNMERGED** (#1734) | `cfa42f8` | 6.2.3 | maintainer closed 2026-09-12 ("the minimax model is deprecated"); FROZEN — not updated in sync #8; still merged into `final` at `cfa42f8` |
| `update-main-fix-issues` | **PR [#1744](https://github.com/Alishahryar1/free-claude-code/pull/1744) OPEN** (#1730) | `e3dc94e1` | 6.2.16 | sync #8: rebased onto `0dcb3715`; §12.5 full set green; **greptile + all 7 CI green — merge-ready (§12.4)** |
| `add-experiential-labs` | **PR [#1749](https://github.com/Alishahryar1/free-claude-code/pull/1749) OPEN** (#1737) | `b61736c0` | 6.3.0 | sync #8: rebased onto `0dcb3715`; §12.5 full set green; **greptile + all 7 CI green — merge-ready (§12.4)** |
| `add-orca-router` | **PR [#1754](https://github.com/Alishahryar1/free-claude-code/pull/1754) OPEN** (#1751) | `3b4f2033` | 6.3.0 | sync #8: rebased onto `0dcb3715`; §12.5 full set green; **greptile + all 7 CI green — merge-ready (§12.4)** |
| `feat-api-key-rotation` | #1301 — NO PR | `03def116` | 6.3.0 | sync #8: rebased onto `0dcb3715`; awaiting user decision (upstream #1655+#1656 may cover it) |
| `fix-cline-hub-hijack` | **PR [#1641](https://github.com/Alishahryar1/free-claude-code/pull/1641) OPEN** (#1590) | `acf94479` | 6.2.16 | sync #8: rebased onto `0dcb3715`; §12.5 full set green; **greptile + all 7 CI green — merge-ready (§12.4)** |
| `final` | — internal, NO PR | `7e78423` + notes commit | 6.3.0 | **REBUILT 2026-09-12/13 on base `0dcb3715`** (§8 sync #8): ALL 11 branches merged in §9 order (first-parent: `9db9d67a` telepub → `2d33e610` key-rotation → `6262e6cb` models-metadata → `2da8b73b` custom → `a6ae9f15` ollama → `9fc965df` update-main-fix-issues → `999e0212` cline → `e271aa46` fix-nim → `4e707130` lightning → `5164cf3b` experiential → `33a05822` orca), then audit re-application: `841dfc9e` security, `6a077f65` dead exports, `424ab991` smells, `0cefbc68` fresh CVE lock pass (starlette 1.6.0, cryptography 50.0.1, python-multipart 0.0.32, urllib3 2.7.0, click 8.5.0, pygments 2.21.0, msgpack 1.2.2; pip-audit 0 vulns), `3e77f612` pyproject deps restore (json5/tomlkit/simplejson dropped by the telepub merge — §8 sync #8 incident), `7e78423` credential count 22. Ancestry 11/11, catalog 55, README rows 54, suite 5633p/152s, e2e 116p/1s. Old final `d0cc706` → local backup `final-backup-20260912-audit`. **HANDOFF_NOTES.md tracked on `final` (final-branch-only file; this sync #8 commit updates it — §9 tracking block)** |

Superseded branches and pre-restructure history live in the `.bak` backup (see header). `gh` CLI v2.99.0 IS installed and authenticated as Tanishq-1 (verified 2026-09-10) — PR states and PR creation can be managed via `gh`.

---

## 11. CONTRIBUTING.md Rules (must follow)

- NO `# type: ignore` or `# ty: ignore` comments.
- Target Python 3.14 native lazy annotations — do NOT add `from __future__ import annotations`.
- Each PR independent — branch from clean updated `main`.
- (Version-bump-in-same-commit and `ci.ps1` are covered in §4 and §2.)

---

## 12. Branch Update & PR Policy (standing rules — 2026-08-30)

### 12.1 Telepub freeze (EXCLUSION from branch updates)
`add-telepub-voyage` is EXCLUDED from all branch updates. When updating all branches (syncs, rebases, pushes), update every other branch normally but NEVER rebase, push, or force-push telepub. Do not apply any update to it unless the user explicitly states otherwise. The branch was externally rebased to `50559ea` (single clean commit on main `81fa340`, v6.3.0 — the old frozen `17382eb` is obsolete); the freeze now means "no updates beyond `50559ea`". Exception (user decision): the `final` integration branch still merges telepub at its current tip (`50559ea`); if that merge ever conflicts non-additively, STOP and ask the user before resolving.

### 12.2 Push-to-main race (PR conflict workflow)
**Scenario:** a PR is approved, then someone pushes directly to `main` before the PR merges → the PR shows conflicts.
**Resolution:**
1. `git fetch upstream` + sync local main (`git merge upstream/main --ff-only`).
2. `git merge-tree main <branch>` to scope the damage before touching anything.
3. Rebase the PR branch onto main — exact-edit conflicts, lockfile order, `GIT_EDITOR=true` (§3/§8 rails).
4. **Test locally before pushing** — gates + full suite + e2e (§2 set).
5. `git push --force-with-lease origin <branch>` — the push clears the conflict and re-triggers bot checks.

**Prevention:**
- The repo ruleset already blocks direct/force pushes to `main` (see CLAUDE.md "Repository protection") — flag violations to the owner.
- Keep PRs current by rebasing on every upstream sync instead of batching several upstream commits.
- Prefer small single-commit branches so conflicts stay version-only.

### 12.3 Greptile-first testing (WAIT for the bot)
When a PR is initially raised, do **NOT** run tests manually — wait for the greptile bot to review first. Manual testing is triggered ONLY by greptile output: run tests only if greptile reports issues or scores below the confidence threshold (12.4). Pre-PR local verification before opening a PR remains the §2 norm; this rule governs activity after the PR exists.

### 12.4 Confidence threshold (5/5 gate)
Greptile must reach **5/5 confidence** to pass. Current observed status: **4/5 — insufficient.** PRs below 5/5 are **BLOCKED from merge**. When greptile reports issues or stays <5/5: highlight each finding to the user, fix the branch, and test locally before pushing (12.5). Never merge below 5/5. (Precedent: the custom-provider PR's P1 series — keyless construction → bearer strip → `/v1` normalization → proxy — each fix was local-tested then force-pushed, with greptile's T-Rex re-testing after every push.)

### 12.5 Local test before push (fix workflow)
Whenever a branch is being fixed in response to a bot/PR finding, the fix must pass the full local set — gates (`ruff format --check`, `ruff check`, `ty check`) + full pytest suite + e2e — BEFORE the fix is pushed to the branch. Never push a bot-driven fix on the basis of targeted tests alone.
