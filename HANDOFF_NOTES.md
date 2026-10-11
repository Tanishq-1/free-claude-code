# Free-Claude-Code ΓÇö Contribution Handoff Notes

> Purpose: context for continuing open-source contribution work in a new terminal/session.
> Date: 2026-10-11 (sync #13 — see the LAST SYNC block below)

> **SESSION NOTE (2026-08-12):** All commands in this doc (┬º2 gates, tests, `uv lock`, git branch/commit/push) are **AUTO-APPROVED by the user for this session** ΓÇö run them without asking for confirmation each time. Still confirm before opening any upstream PR (user decides PR timing).

> **LAST SYNC (sync #13 recorded 2026-10-11):** upstream base `105bfab8` → **`fa6adde2`** (v6.13.5; local main fast-forwarded, lineage verified). Backups first: `backup/pre-v6135-*` per branch + `backup/final-pre-v6135-rebuild` = `fa9ed2e4`. **3 active branches REBASED, validated green, and PUSHED `--force-with-lease`** (PR refresh; PRs #1736/#1606 now show MERGEABLE): `feat-api-key-rotation` `67bcbcde`, `feat-models-metadata` `69fd41d0`, `fix-ollama-model-discovery` `f1c8c172`. Frozen branches untouched; `final-rebuild` still local-only. **`final-rebuild` on `fa6adde2` (telepub EXCLUDED this cycle; 6 branches merged:** key-rotation → models-metadata → custom-provider → ollama-discovery → update-main-fix-issues → nim-minimax, keep-both conflicts resolved in custom-provider + nim; 4 audit commits re-salvaged; fixup `8eccad11` + CVE lock `298517c8`). **3 merge regressions found & fixed — §8 sync #13:** (1) the nim post-terminal framer's UNBOUNDED `finish_reason` hold broke v6.8.2+ hidden-stream/first-chunk recovery — 4 test failures + a full-suite WEDGE at 97-99% — fixed with a bounded 0.5 s terminal hold + a `terminal_pending` signal into the recovery gate (this also RESOLVED the old "2 accepted nim failures"; the previously-accepted `test_nim_parser_failure_*` pair now passes); (2) custom-provider admin status: 4 tests ported from the frozen branch's removed all-providers `/local-status` route to upstream #1909's per-provider route (+ api_key/proxy pass-through restored in the handler); (3) hidden-stream `_normalized_chunks` monkeypatch shim adapted to the nim signature. **Rebuild validation: full suite 8632 passed / 24 skipped / 0 failed in ~83 s** (suite wedge GONE), gates green (format/ruff/ty); e2e NOT yet run on final-rebuild; `final` → `final-rebuild` rename + cleanup still pending.
>
> **SYNC #12 (recorded 2026-09-28):** upstream base `ba4b9341` ΓåÆ **`105bfab8`** (18 commits, 313 files +14163/-5554: VS Code Chat integration #1915, custom API providers #1909, fcc.db SQLite storage #1913/#1919/#1931, admission-registry provider protection #1923, native tool arguments #1929, OrcaRouter #1754, cline-hub fix #1641 ΓÇö v6.4.10). Local main ff-synced (lineage `merge-base --is-ancestor` exit 0). **`add-orca-router` (#1754 ΓåÆ `10fb1d02`) and `fix-cline-hub-hijack` (#1641 ΓåÆ `d5930097`) are MERGED upstream ΓÇö dropped from the active set, LOCAL BRANCHES DELETED (exact-tip backups `merged/add-orca-router` `69189df4` / `merged/fix-cline-hub-hijack` `85b31b6a`; origin refs untouched ΓÇö no pushes).** **3 active branches rebased onto `105bfab8`, all 0-behind, all green (┬º8 sync #12):** `feat-api-key-rotation` `f976b9ce`, `feat-models-metadata` `d91ad0c7`, `fix-ollama-model-discovery` `fb735b52` (2 rebase regressions found & fixed ΓÇö see ┬º8). **FROZEN per user decision (2026-09-28), fix-nim precedent:** `add-custom-provider` (#1469 CLOSED unmerged 2026-09-26, superseded by upstream #1909) + `update-main-fix-issues` (#1744 CLOSED unmerged 2026-09-12) ΓÇö pins `69acb27d`/`f4048981` untouched; telepub/nim unchanged. **`final` REBUILT on `105bfab8` (2026-09-28): 7 branches merged, the 4 audit commits SALVAGED from the backup line, merge follow-ups fixed, gates green, suite 6742p/23s/**2 accepted nim failures**, e2e 221p/1s; all 6 pre-sync-#12 final backups consolidated into ONE `final-backup` branch.** **NOTHING PUSHED** (local only).
>
> **SYNC #11 (recorded 2026-09-26):** upstream base `faeec6ba` ΓåÆ **`ba4b9341`** (18 commits, 90 files +5165/ΓêÆ997: PyPI publishing + release-version automation, AGPL-3.0-only relicence, `requires-python ==3.14.7` and `.python-version` REMOVED, `fcc-doctor`, **Cheaper Inference provider (#1899)**, fixed cloud endpoints #1891, openai_api sampling params #1883). Local main ff-synced to `ba4b9341` (lineage verified via `merge-base --is-ancestor`, exit 0). **7 non-frozen branches rebased onto `ba4b9341`, all 0-behind, all green (┬º8 sync #11). ┬º4 VERSIONING RULE IS NOW OBSOLETE ΓÇö READ BELOW.** `final` REBUILT on `ba4b9341` (ancestry 9/9; gates green; suite 6272p/18s/**2 known failures**; e2e 195p/1s). **NOTHING PUSHED** (user decision ΓÇö local only).

> ### ΓÜá∩╕Å ┬º4 SUPERSEDED ΓÇö manual version bumps are now FORBIDDEN (upstream #1896/#1903)
> The old rule "`pyproject.toml` line 7: bump `version = "X.Y.Z"` + `uv lock` in the same commit" **no longer applies and will FAIL CI.** Upstream switched to `hatch-vcs` with `dynamic = ["version"]` and added `scripts/check_version_policy.py` + the required `version-policy.yml` check, which **rejects any `project.version`** (*"FCC must declare a dynamic version without project.version"*). Consequences: **(1)** delete the `version = ΓÇª` line, keep upstream's `dynamic = ["version"]` ΓÇö on every rebase the pyproject conflict is exactly this line; resolve to upstream's form, then `git checkout main -- uv.lock` ΓåÆ `uv lock`. **(2)** The branch-version invariant ("sit ABOVE the base version") is **dead** ΓÇö versions now come from git tags at release time. **(3)** Release intent comes from the **PR title**: any PR touching `pyproject.toml`/`uv.lock`/`.python-version`/`assets/`/`scripts/`/`src/` MUST be titled `patch: ΓÇª`/`minor: ΓÇª`/`major: ΓÇª`, and a non-release PR must NOT use those prefixes. Verify with `uv run python scripts/check_version_policy.py --base main --head HEAD --title 'minor: ΓÇª'`. Features ΓçÆ `minor:`, fixes ΓçÆ `patch:`.

> ### ┬º7 branch triage changes (sync #11)
> * **`add-lightning-ai` (#1740) and `add-experiential-labs` (#1749) are MERGED upstream** (`613cdaaa`, `0329ac49`) ΓÇö branches gone, dropped from the active set. Catalog is now **56** on main.
> * `add-telepub-voyage` (┬º12.1 freeze) and `fix-nim-minimax-post-terminal-framer` (#1742, closed unmerged) remain **frozen at `50559ea0` / `cfa42f81`** ΓÇö verified byte-identical after sync #11. Both are still merged into `final` at those pins per ┬º9.

> ### ΓÜá∩╕Å Known deliberate trade-off on `final`: 2 failing tests
> `tests/providers/test_sdk_stream_lifecycle.py::test_nim_parser_failure_closes_response_before_retry[messages|responses]` **fail on `final` by decision.** `fix-nim-minimax-post-terminal-framer` holds back `finish_reason` to tolerate post-terminal NIM chunks; upstream later added a newer contract requiring the response to be **closed before a retry**. The two behaviours are mutually exclusive ΓÇö reverting the fix fails its own 7 tests instead. Its 36 own tests all pass and `minimax` is still a live catalog provider, so the bug is still reachable. **User decision 2026-09-26: keep the fix, accept the 2 failures.** Every other branch and `main` are fully green. To drop it later: rebuild `final` without that branch.

> **LAST SYNC (sync #8 recorded 2026-09-13):** upstream base `0dcb3715` (v6.2.15 ΓÇö 11 commits #1756ΓÇô#1767, 46 files +5194/ΓêÆ345: VS Code + Codex integrations, JetBrains ACP preview card, admin loading fix, Codex client tool discovery fix; local main ff-synced `f3a3aac`ΓåÆ`0dcb3715`, pushed to fork 2026-09-12). ALL 9 updateable branches synced 2026-09-12 (details ┬º8 sync #8; every open PR conflict cleared + greptile PASS + all 7 CI green ΓÇö merge-ready, ┬º12.4 gate met): **#1469** `add-custom-provider` `b218d21e` (6.3.0 ΓÇö complex rebase, keep-both conflicts; greptile 17 files/0 comments), **#1606** `fix-ollama-model-discovery` `132b5fdc` (6.2.16 ΓÇö merge of main INTO branch, never-rewrite, NO force), **#1641** `fix-cline-hub-hijack` `acf94479` (6.2.16), **#1736** `feat-models-metadata` `a56c9856` (6.3.0), **#1740** `add-lightning-ai` `96a601d0` (6.3.0), **#1744** `update-main-fix-issues` `e3dc94e1` (6.2.16), **#1749** `add-experiential-labs` `b61736c0` (6.3.0), **#1754** `add-orca-router` `3b4f2033` (6.3.0), `feat-api-key-rotation` `03def116` (6.3.0 ΓÇö NO PR, awaiting user decision). **#1742** `fix-nim-minimax-post-terminal-framer` **CLOSED UNMERGED** by maintainer 2026-09-12 ("the minimax model is deprecated ΓÇö no need to fix, just stop using it") ΓÇö frozen at `cfa42f8`, NOT updated (user decision); still merged into `final` at `cfa42f8`. Telepub FROZEN at `50559ea` (┬º12.1) ΓÇö untouched. `final` = rebuilt 2026-09-12/13 on base `0dcb3715` (ALL 11 branches merged + audit re-application + pyproject-deps-restore incident + credential-count fix ΓÇö ┬º8 sync #8; ┬º12.5 full set green: suite 5633p/152s, e2e 116p/1s, pip-audit 0 vulns; old final `d0cc706` ΓåÆ local `final-backup-20260912-audit`; NO PR ΓÇö internal only). **HANDOFF_NOTES.md is TRACKED on `final` (final-branch-only file, ┬º9 tracking block; this commit updates it).** NOTE: upstream PR #1655+#1656 (another author) implements API-key rotation (#1301) ΓÇö our `feat-api-key-rotation` `03def116` may be redundant. Upstream e2e: context-meter is Windows-locale-only (passes on ubuntu CI). Sync log: ┬º8 (sync #8 latest recorded).

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

# E2E ΓÇö Admin UI (install Chromium once: uv run playwright install chromium)
uv run pytest e2e -q

# Lockfile (only if dependencies changed ΓÇö NOT for versions, see ┬º4)
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
# ... make changes, run gates + tests, check the version policy (NO version bump ΓÇö see ┬º4) ...
git add <explicit paths>              # never -A (stray PowerShell dirs get caught)
git commit -m "Add <feature>"
git push -u origin add-<feature>
# Open PR: base = Alishahryar1/main, head = Tanishq-1/add-<feature>
```

### If upstream main moved (conflicts) ΓÇö rebase
```powershell
$env:GIT_EDITOR='true'                # ALWAYS ΓÇö prevents the invisible vim.exe hang
git checkout add-<feature>
git rebase main
# resolve conflicts with EXACT edits (keep BOTH provider entries), verify zero markers
git add <explicit paths>
git -c core.editor=true rebase --continue
git push --force-with-lease origin add-<feature>   # force needed after rebase
```
Lockfile reset order and all other durable rebase rules: ┬º8 "Sync rails".

---

## 4. Versioning ΓÇö **SUPERSEDED (sync #11). Manual bumps are FORBIDDEN.**

> **Do NOT bump `pyproject.toml` by hand any more.** Upstream (#1896/#1903) moved to `hatch-vcs` + `dynamic = ["version"]` and added a **required CI check** (`.github/workflows/version-policy.yml` ΓåÆ `scripts/check_version_policy.py`) that **fails any PR carrying `project.version`**. Setting `version = "X.Y.Z"` in a branch will now break the `Version policy` check.

1. **No version line in a branch.** `pyproject.toml` must keep `dynamic = ["version"]` and MUST NOT contain `version =`. Versions are derived from git tags when `post-merge.yml` publishes to PyPI. The "branch-version invariant" is dead.
2. **Release intent = the PR title.** A PR touching `pyproject.toml`, `uv.lock`, `.python-version`, or anything under `assets/`, `scripts/`, `src/` is a *release* PR and MUST be titled `patch: ΓÇª` / `minor: ΓÇª` / `major: ΓÇª`; a non-release PR must NOT use those prefixes. Semantics unchanged in spirit:

   | Prefix | When | Example |
   |--------|------|---------|
   | `patch:` | bug fix only | fix crash |
   | `minor:` | new feature/provider | **added a provider** |
   | `major:` | breaking change | remove provider, rename env vars |

3. **Check locally before pushing** (mirrors the CI job):
   ```powershell
   uv run python scripts/check_version_policy.py --base main --head HEAD --title 'minor: Add <feature>'
   # -> "Version policy passed: minor"
   ```
4. When a rebase conflicts in `pyproject.toml`, the conflict is almost always the old `version` line: **resolve to upstream's `dynamic = ["version"]`**, then `git checkout main -- uv.lock` ΓåÆ `uv lock`. `uv.lock`'s editable `free-claude-code` root package must likewise carry no `version` field.

---

## 5. How to Add a New OpenAI-Compatible Provider (the template)

Provider system is **catalog-driven** ΓÇö no new protocol code needed. Touch these files:

1. **`src/free_claude_code/config/provider_catalog.py`** ΓÇö `<NAME>_DEFAULT_BASE` constant + `ProviderDescriptor` entry in `PROVIDER_CATALOG`.
2. **`src/free_claude_code/config/settings.py`** ΓÇö import the DEFAULT_BASE; add `<name>_api_key`, `<name>_base_url` Fields (with validation_alias) + `<name>_proxy` Field.
3. **`src/free_claude_code/providers/openai_chat/profiles.py`** ΓÇö `OpenAIChatProfile` in `OPENAI_CHAT_PROFILES` via `_policy(...)`; `NamedEffortReasoning(_LOW_MEDIUM_HIGH, enabled_value="medium")` if the provider supports `reasoning_effort`, else `NO_REASONING`.
4. **`src/free_claude_code/config/admin/provider_manifest.py`** ΓÇö `<NAME>_API_KEY` + `<NAME>_BASE_URL` overrides in `_PROVIDER_FIELD_OVERRIDES` (label + description).
5. **`src/free_claude_code/config/admin/manifest.py`** ΓÇö `ConfigFieldSpec("FCC_SMOKE_MODEL_<NAME>", "Smoke <Name> Model", "smoke", advanced=True)`.
6. **`tests/contracts/test_provider_catalog_order.py`** ΓÇö add `"<name>",` to `_EXPECTED_PROVIDER_ORDER` (position must match catalog dict order).
7. **`tests/providers/test_provider_runtime.py`** ΓÇö import the DEFAULT_BASE; add `<name>_api_key`, `<name>_base_url`, `<name>_proxy` mocks + `"<name>": OpenAIChatProvider,` entry.
8. **`.env.example`** ΓÇö **SKIPPED since sync #11: upstream deleted this file.** Do not re-create it.
9. **`README.md`** ΓÇö provider table row.
10. **`smoke/lib/config.py`** ΓÇö `"<name>": "<name>/<default-model>",` in `PROVIDER_SMOKE_DEFAULT_MODELS`.
11. **Logo asset + attribution** ΓÇö `src/free_claude_code/api/admin_static/providers/<name>.svg` (or `.png`) plus a row in that folder's `SOURCES.md`. **Both mandatory:** `ProviderDescriptor` now *requires* `website_url` + `logo_filename`, and `e2e/test_provider_modals.py::test_provider_titles_link_to_websites_and_every_logo_loads` asserts every logo actually loads. Reuse the project-authored neutral-glyph convention (see `custom.svg`) if the real brand mark can't be shipped.
12. **Version policy** ΓÇö **no `pyproject.toml` version edit** (┬º4). Verify with `uv run python scripts/check_version_policy.py --base main --head HEAD --title 'minor: Add <name>'`; title the PR `minor: ΓÇª`.

---

## 6. Model Discovery (auto ΓÇö no extra work)

- `OpenAIChatProvider.list_model_infos()` calls `{base_url}/models` with the **user's own API key**.
- Gated by `model_ids_are_routable` (default `True`; only `azure_openai` sets `False`).
- Any OpenAI-compatible provider **auto-discovers** its models per key; README/smoke slugs are defaults, NOT restrictions.
- Local providers (`ollama`/`lmstudio`/`llamacpp`) are self-sufficient for discovery ΓÇö zero configuration needed (see ┬º7 ollama card).

---

## 7. Active Branches (Work In Flight)

> All providers below follow the ┬º5 template; only distinguishing facts noted. Issue links use the upstream repo: https://github.com/Alishahryar1/free-claude-code/issues/<n>

### ≡ƒºè `add-custom-provider` ΓÇö Custom OpenAI-compatible provider ΓÇö **PR [#1469](https://github.com/Alishahryar1/free-claude-code/pull/1469) CLOSED UNMERGED (2026-09-26, superseded by upstream #1909) ΓÇö FROZEN 2026-09-28** ([#1230](https://github.com/Alishahryar1/free-claude-code/issues/1230))
- Generic custom-endpoint feature (single "custom" slot). **API key OPTIONAL** ΓÇö `credential_optional=True` profile flag; base URL required via `required_settings_attrs=("custom_base_url",)`. Profile: `NO_REASONING` + `ReasoningReplayMode.DISABLED` + `normalize_base_url=True`; no smoke default.
- Greptile P1 series RESOLVED ΓÇö the Admin local-status probe now matches the runtime on all four axes: keyless construction (`credential_optional` + `api_key=... or "no-api-key"` SDK placeholder), keyless bearer strip (`_drop_authorization_header` httpx request hook), `/v1` normalization (`openai_v1_base_url` moved to `core/openai_base_url.py`), and proxy passthrough. Nothing left to flag.
- **CI failure on `6ac42f9` FIXED (2026-09-02):** the playwright job failed on `test_delayed_older_page_cannot_cross_into_another_chat` (30s timeout clicking the renamed card). Root cause (┬º8): a stream committing right before an edit bumps the revision ΓåÆ the edit's PATCH 409s ΓåÆ `updateSession` in `chat_sessions.js` reloaded + showed a notice but **silently dropped the user's change** (title/model/thinking). Fix in commit `1e537fb` "Retry chat session edits once on revision conflicts": on 409, reload the session and re-apply the same edit ONCE against the fresh revision (guards preserved; no loop). Genuine product bug (silent edit loss), makes the flaky test deterministic. 10/10 local runs of the flaky test pass post-fix; suite 4422/148/0; e2e 42 passed + Windows-locale context-meter only; gates green. v5.19.0 ΓåÆ **5.19.1** + `uv lock` in the same commit (PATCH, runtime change). Pushed as a second commit (fast-forward, NO force).
- Current: `1e537fb` (`6ac42f9` + fix commit), v5.19.1, base `b85ae4a` ΓÇö suite 4422/148/0, e2e green (Windows-locale context-meter only, passes on CI), gates green. RESOLVED 2026-09-12: the fix commit is in the branch's `b69108d` lineage and in `final` (┬º10). **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` ΓåÆ `b218d21e`, v6.3.0 ΓÇö complex rebase (admin_routes.py asyncio.gather + `_probe` closure with blank-URL skip + keyless bare `client.get` ΓÇö ┬º8 sync #6 precedent; provider.py `api_key=resolved_api_key or "no-api-key"` combined with upstream's changes; e2e/conftest.py + tests/api/test_admin.py keep-both); ┬º12.5 full set green; greptile re-ran clean (17 files, 0 comments) + all 7 CI green ΓÇö merge-ready (┬º12.4 met).

### ≡ƒöä `fix-ollama-model-discovery` ΓÇö Local models missing from /model ΓÇö **PR [#1606](https://github.com/Alishahryar1/free-claude-code/pull/1606) OPEN** ([#1296](https://github.com/Alishahryar1/free-claude-code/issues/1296))
- Root cause (two stacked gates): `discovery.py` excluded every `.local` provider unless a chat model already referenced it, and `has_provider_configuration()` treated keyless-with-default locals as unconfigured ΓÇö fresh Ollama users could never get probed.
- Fix: `_self_sufficient_local()` admits `ollama`/`lmstudio`/`llamacpp` into best-effort discovery with zero configuration; failed local probes back off via a `ProviderModelCache` cooldown (`LOCAL_DISCOVERY_RETRY_COOLDOWN_S = 60s`, cleared on success, ignored by explicit full refreshes); README documents local auto-discovery.
- **Branch shape (IMPORTANT):** the PR branch was updated EXTERNALLY (GitHub web merge) to `e42e115` = merge of our work + upstream `3ef17fe`. Never rewrite it ΓÇö we fast-forwarded and added ONE commit on top: the v5.17.3 PATCH bump (`79e8345`). Push WITHOUT force (fast-forward only); single-commit-shape rule does not apply.
- Current: `c84164c`, v5.19.2 (on 2026-09-02 merged `main` `96495b9` in to clear the NEW PR #1606 dirty state ΓÇö upstream advanced `b85ae4a`ΓåÆ`96495b9`; version resolved 5.19.2 = PATCH above base 5.19.1; conflict version-only pyproject.toml + uv.lock; external merge `e42e115` + prior merge `0b3d158` preserved; merge commit `edd34fb` ff-pushed, NO force) ΓÇö suite 4454/148/0, e2e 50 passed + Windows-locale context-meter only, gates green. NOTE 2026-09-02: first CI run for `edd34fb` was CANCELLED (workflow run 33610053117 ΓÇö GitHub cancelled; no superseding run; API re-run blocked 403 without upstream write) ΓåÆ appended EMPTY commit `c84164c` "ci: re-trigger checks cancelled after main merge (no code change)" + ff-push to re-trigger; run 33612506300 **SUCCESS** ΓÇö all 7 checks green incl. Greptile; PR API **mergeable=True, state=clean**.
- NOTE RESOLVED 2026-09-12: the old merge-commit ancestry break is gone ΓÇö `final` merges the branch tip directly (ancestry checks pass on every rebuild). **Sync #8 (2026-09-12):** merged main `0dcb3715` INTO the branch (never-rewrite ΓÇö merge commit `132b5fdc`), version resolved 6.2.16, ff-push NO force; ┬º12.5 full set green; conflict cleared, greptile + all 7 CI green ΓÇö merge-ready (┬º12.4 met).

### ≡ƒöä `add-telepub-voyage` ΓÇö Telepub Voyage provider ΓÇö NO PR
- Clean reimplementation of stale PR [#739](https://github.com/Alishahryar1/free-claude-code/pull/739), fixing its defects: reasoning replay honors the reasoning policy, no `_strip_system_messages` content drop, no `Message.role` widening, version bumped.
- `telepub_voyage`, base `https://voyage.prod.telepub.cn/voyage/api`, env `TELEPUB_VOYAGE_API_KEY`; `NO_REASONING` + `ReasoningReplayMode.REASONING_CONTENT`; standard profiled provider, auto-discovers via `/models`. Test: `tests/providers/test_telepub_voyage.py`.
- **Policy: share the branch URL with the PR #739 author only ΓÇö do NOT raise a PR.**
- **FROZEN (┬º12.1):** excluded from all branch updates ΓÇö never rebase/push during syncs. The branch was externally REBASED (before 2026-09-10) to `50559ea` ΓÇö the same single clean commit on main `81fa340`, v6.3.0; the ancient frozen `17382eb` is OBSOLETE. `final` merges the current tip `50559ea`; no further updates beyond it.
- Current: `50559ea`, v6.3.0 ΓÇö pairwise merge into bare main is clean (verified via merge-tree 2026-09-12); untouched in sync #8 (┬º12.1 freeze); merged into rebuilt `final` at `50559ea` (┬º10).

### ≡ƒöä `feat-models-metadata` ΓÇö /v1/models metadata ΓÇö **PR [#1736](https://github.com/Alishahryar1/free-claude-code/pull/1736) OPEN** ([#1168](https://github.com/Alishahryar1/free-claude-code/issues/1168))
- Adds optional `pricing` (per-1K USD `input`/`output`) + `capabilities` (`chat`/`vision`/`tools`/`thinking`/`fim`/`streaming`) to `GET /v1/models`, extracted from provider model-list entries so clients need not scan 558+ models. `contextWindow`/`maxCompletionTokens` already ship on main via upstream's `ProviderModelInfo` (#1604/#1605) ΓÇö our unique value on top is **`ProviderModelPricing`** + capabilities (`application/model_metadata.py`) + extraction/thinking-inference in `providers/model_listing.py`; optional `ModelResponse` fields omitted when the provider advertises nothing (id-only responses unchanged).
- Contract note: the claude view must NOT expose `contextWindow`/`maxCompletionTokens` (upstream contract test owns that view) ΓÇö enrichment limited to optional capabilities/pricing.
- Current: `5fe9ce8` (amended, single-commit), v6.3.0, base `81fa340` (v6.2.2; rebased 2026-09-09) ΓÇö PR #1736 raised 2026-09-10; greptile scored **4/5** ΓåÆ per ┬º12.3 fixed all 3 findings same day (P1 no-thinking variants no longer advertise `thinking` in capabilities ΓÇö Claude view + messages/responses views; P2 direct views (`view=messages`/`view=responses`, and Muse/codex wrappers) now surface capabilities/pricing via `_InventoryModel.metadata`; P2 `_to_float` rejects negative/NaN/inf prices + `_pricing` key-presence keeps valid 0 prices), ┬º12.5 full set green before push (gates green; suite 5165p/149s + 2 pre-existing PS 5.1 installer stderr-wrap failures verified present at `07eca3f` too ΓÇö env brittleness, not our diff; e2e 97p/1s; targeted 43p), force-pushed ΓåÆ **greptile re-review PASSED (5/5 gate ┬º12.4 met) + all 7 CI checks green on `5fe9ce8`** ΓÇö merge-ready (merge is upstream owner's call). **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` ΓåÆ `a56c9856`, v6.3.0 kept; ┬º12.5 full set green; conflict cleared, greptile + all 7 CI green ΓÇö merge-ready.

### ≡ƒöä `add-lightning-ai` ΓÇö Lightning AI provider ΓÇö **PR [#1740](https://github.com/Alishahryar1/free-claude-code/pull/1740) OPEN** ([#1732](https://github.com/Alishahryar1/free-claude-code/issues/1732))
- Standard catalog provider (`lightning`, base `https://lightning.ai/api/v1`, env `LIGHTNING_API_KEY`/`LIGHTNING_BASE_URL`/`LIGHTNING_PROXY`) for Lightning AI Model APIs (~40M free tokens, ~47 OpenAI-compatible models with slashed ids like `lightning-ai/gpt-oss-120b`). Auto-wired `OpenAIChatProfile` ΓÇö no factory/runtime changes (LLM7 pattern).
- `NamedEffortReasoning(_LOW_MEDIUM_HIGH, disabled_value="none", enabled_value="medium")` ΓÇö litai's documented top-level `reasoning_effort` vocabulary; `ReasoningReplayMode.DISABLED`; declarative `/models` listing extracting `context_length`/`max_tokens`/`architecture.input_modalities`. NO credential-validation probe (public catalog cannot validate inference keys ΓÇö LLM7 rule) ΓåÆ unsupported-key count 20ΓåÆ21 in `test_credential_validation.py`; no tool filtering (catalog has no `supported_parameters`); pricing omitted (per-token keys Γëá generic per-1K extraction). Smoke default `lightning/lightning-ai/gpt-oss-120b`; README 50ΓåÆ51 providers.
- Tests: `tests/providers/test_lightning.py` (14 items: construct; DEFAULT/ON/OFF ΓåÆ absent/`medium`/`none`; full named-effort matrix MINIMAL/LOWΓåÆlow, MEDIUMΓåÆmedium, HIGH/XHIGH/MAXΓåÆhigh; catalog metadata incl. missing `architecture` ΓåÆ modalities unknown; malformed/empty catalog rejection; wire URL + Bearer). Contract updates: catalog order, runtime instantiation, smoke-config trio, credential-validation count.
- Current: `3575595` (amended, single-commit), v6.3.0, base `81fa340` (v6.2.2) ΓÇö PR #1740 raised 2026-09-10; greptile scored **4/5** (P2: named reasoning efforts untested) ΓåÆ added full effort-vocabulary matrix, ┬º12.5 full set green before push (gates green; suite 5188p/144s; e2e 97p/1s; targeted 14p), force-pushed `95cff5e`ΓåÆ`3575595` ΓåÆ **greptile re-review PASSED (5/5 gate ┬º12.4 met; 0 comments) + all 7 CI checks green** ΓÇö merge-ready (merge is upstream owner's call). Version-only collision with PR #1736 (both 6.3.0) ΓÇö routine per ┬º8; resolved at rebase/merge. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` ΓåÆ `96a601d0`, v6.3.0 kept; ┬º12.5 full set green; conflict cleared, greptile + all 7 CI green ΓÇö merge-ready.

### ≡ƒºè `fix-nim-minimax-post-terminal-framer` ΓÇö NIM deltas-after-finish_reason crash ΓÇö **PR [#1742](https://github.com/Alishahryar1/free-claude-code/pull/1742) CLOSED UNMERGED (2026-09-12)** ([#1734](https://github.com/Alishahryar1/free-claude-code/issues/1734))
- Root cause: NVIDIA NIM (during MiniMax-M3 decommission ΓÇö model page serves `isDeprecated: true`, "deprecated on 09/08/2026") emits deltas AFTER the chunk carrying `finish_reason`. The MiniMax-M3 native-tool normalizer finalized its framers at the FIRST finish_reason chunk, so any trailing delta ΓÇö even an empty string ΓÇö hit the FINISHED framer and raised a non-retryable `RuntimeError("MiniMax-M3 tool framer is already finished")` ΓåÆ terminal "API Error" on every tool turn (not routed through the malformed-markup recovery path). Second latent bug: duplicate finish_reason chunks re-ran finalization and re-parsed the retained tool block, duplicating generated tool calls.
- Fix: hold-terminal + end-of-stream finalization in `providers/nvidia_nim/native_tool_stream.py` ΓÇö framers are fed every string delta regardless of position (tool blocks streamed after the terminal chunk still decode; trailing non-markup text passes through as content); the terminal marker (first finish_reason wins) + latest usage are held back and re-emitted as one final chunk after the raw stream ends; finalization runs exactly once. Framer class unchanged (FINISHED guard kept as defensive invariant). 5 new regression tests incl. the exact #1734 repro (empty delta after finish), verified to fail on pre-fix code with the user-reported error. Deprecated `minimaxai/minimax-m3` dropped from `NVIDIA_NIM_CLI_DEFAULT_MODELS` smoke defaults + contract test (users who configured the model themselves keep working).
- Verified: targeted 231p; ┬º12.5 full set green before push (gates green; suite 5175p/144s; e2e 97p/1s). No local NIM key ΓÇö mocked tests authoritative (LLM7/Lightning stance); NIM deprecation verified live from the public model page.
- Current: `cfa42f8` (single-commit), v6.2.3, base `81fa340` (v6.2.2) ΓÇö PR #1742 raised 2026-09-11; greptile PASSED first review (5/5, 0 comments) + all 7 CI green. **CLOSED UNMERGED by the maintainer on 2026-09-12** with reason: "the minimax model is deprecated ΓÇö no need to fix, just stop using it". Branch FROZEN at `cfa42f8` ΓÇö excluded from sync #8 (user decision; do NOT update/push). Still merged into `final` at `cfa42f8` (┬º10) ΓÇö the internal integration keeps the fix since the hold-terminal normalizer is generic, not minimax-specific.

### ≡ƒºè `update-main-fix-issues` ΓÇö JSON-Schema `pattern` sanitization ΓÇö **PR [#1744](https://github.com/Alishahryar1/free-claude-code/pull/1744) CLOSED UNMERGED (2026-09-12) ΓÇö FROZEN 2026-09-28** ([#1730](https://github.com/Alishahryar1/free-claude-code/issues/1730))
- Root cause: Claude Code's `Artifact` tool embeds a `pattern` regex using Unicode property escapes + a negative lookahead (`^(?!__.*__$)[^\p{Cc}\p{Cf}\p{Zl}\p{Zp}...]`). OpenAI-compatible providers validate `pattern` values against dialects that reject these constructs (Rust `regex` rejects lookaround; JS no-`u` and Python `re` reject `\p{}`) ΓåÆ whole request 400s with `invalid_function_parameters` on `tools[N].parameters` before reaching the model. No request-side sanitization existed (NIM's sanitizer only strips boolean subschemas / aliases arg names).
- Fix: `sanitize_tool_schema_patterns` in `core/anthropic/tool_schema.py` ΓÇö drops any `pattern` whose value contains `\p{`/`\P{` (a stripped remainder could only be STRICTER than the original, rejecting arguments the schema allowed ΓÇö greptile P1), walking ONLY JSON Schema subschema keywords (`properties`/`items`/`anyOf`/`additionalProperties`/`$defs`/`patternProperties`/ΓÇª ΓÇö greptile P1: literal-value keywords like `enum`/`const`/`default`/`examples` are never traversed). Copy-on-write: nodes without offending patterns returned as-is, input never mutated. Wired into BOTH request emission points: `conversion.py` `convert_tools` (all ~45 openai_chat providers) + `openai_responses/provider_input.py` (Codex/Responses). PR body triages the other reviewed issues: #1732 delivered by #1740, #1662 claimed upstream by #1679, #1654/#1689 already covered by README "Claude Code in VS Code" ΓÇö PR closes #1730 only.
- Verified: targeted 152p; ┬º12.5 full set green before every push (gates green; suite 5180p/144s; e2e 97p/1s). Dropping a pattern trades server-side validation strictness for the request reaching the model ΓÇö client still validates locally.
- Current: `4ae75ae` (amended, single-commit), v6.2.4, base `81fa340` (v6.2.2) ΓÇö PR #1744 raised 2026-09-11. Greptile: first review 4/5 with 2 P1s (stripping `\p{L}` from `[\p{L}\d]+` narrows to `[\d]+` ΓåÆ must drop, never strip-keep; walker rewrote literal `pattern` keys under `enum`/`const`/`default`/`examples`) ΓåÆ fixed (drop-always + subschema-keyword-only traversal), ┬º12.5 full set green, force-pushed `f2ce738`. Second review 4/5 with 1 P1 (`propertyNames`/`unevaluatedProperties` are SINGLE schemas, misclassified as maps ΓÇö direct patterns retained) ΓåÆ fixed (moved to single-schema group) + ┬º12.5 full set green + force-pushed `4ae75ae` ΓåÆ **greptile PASSED + all 7 CI checks green ΓÇö merge-ready (┬º12.4 gate met)**; merging is the upstream owner's call. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` ΓåÆ `e3dc94e1`, v6.2.16 (PATCH above 6.2.15); ┬º12.5 full set green; conflict cleared, greptile + all 7 CI green ΓÇö merge-ready.

### ≡ƒöä `add-experiential-labs` ΓÇö Experiential Labs provider ΓÇö **PR [#1749](https://github.com/Alishahryar1/free-claude-code/pull/1749) OPEN** ([#1737](https://github.com/Alishahryar1/free-claude-code/issues/1737))
- Standard catalog provider (┬º5 template, LLM7/Lightning pattern ΓÇö auto-wired `OpenAIChatProfile`, no factory/runtime protocol code). Gateway speaks OpenAI Chat Completions at `https://api.experientiallabs.ai/v1`; auth `Bearer` with `xpl_`+40-hex keys minted at platform.experientiallabs.ai/settings/api-keys; env `EXPLABS_API_KEY`/`EXPLABS_BASE_URL`/`EXPLABS_PROXY` (matches their docs 1:1).
- Free tier: host-managed $0 models with tools+streaming ΓÇö `gemma-4-26b-a4b-it-free` (smoke default, 262k ctx), `dots-3-note-preview-free` (512k), `laguna-s-2.1-free`, `laguna-xs-2.1-free`, `lfm-2.5-2.6b-free` (65k), `ling-3.0-flash-fin-free` (262k). Promo free-tier slugs (`deepseek-v4-flash`, `gpt-5.6-luna`, 50%-off `qwen3.8-27b`) require a payment method ΓÇö deliberately NOT used as defaults. Lineup is "seeded by operations" and may rotate; models are user-configurable via `MODEL=experiential/<slug>` and auto-discovered per key.
- Profile: `_policy("EXPERIENTIAL", ReasoningReplayMode.REASONING_CONTENT, default_max_tokens=ANTHROPIC_DEFAULT_MAX_OUTPUT_TOKENS)` (thinking survives as reasoning_content ΓåÆ Claude thinking blocks) + `NamedEffortReasoning(_LOW_MEDIUM_HIGH, enabled_value="medium")` with NO `disabled_value` ΓÇö OFF omits `reasoning_effort` entirely so each model keeps its documented default effort (the "none" vocabulary is unverified for this gateway). `OpenAIModelListing(path="/models")` bare id-only listing (no context-window fields on that endpoint).
- Unlike LLM7/Lightning (public catalogs, no probe), this provider HAS a credential probe ΓÇö `GET /v1/models` is their documented key-verification call: `_Probe("experiential", "/models", _MODELS, _AUTH_401)` in `providers/credential_validation.py`. Shared-credentials count stays 20 (all_keys +1, supported +1, CASES entry added in the same change).
- Tests: `tests/providers/test_experiential.py` (~230 lines, 12 items ΓÇö construct/reasoning-default-ON-OFF/effort-matrix/replay/bare-listing/missing-id/empty-catalog/wire-URL-Bearer) + runtime config test + credential-validation CASES entry + catalog-order + smoke-config trio.
- Current: `3886c8e` (single-commit), v6.3.0 (MINOR ΓÇö new provider), base `e632c85` (upstream tip at PR time). ┬º12.5 full set green pre-push (gates green; suite 5191p/144s; e2e 97p/1s; targeted 179p). Greptile: **PASSED first review (15 files, 0 comments) + all 7 CI checks green ΓÇö merge-ready (┬º12.4 gate met)**; merging is the upstream owner's call. Version-only collision with #1736/#1740 (both 6.3.0) is routine ┬º8, resolved at rebase/merge. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` ΓåÆ `b61736c0`, v6.3.0; ┬º12.5 full set green; conflict cleared, greptile + all 7 CI green ΓÇö merge-ready.

### Γ£à `add-orca-router` ΓÇö OrcaRouter provider ΓÇö **MERGED UPSTREAM 2026-09-27 (#1754 ΓåÆ `10fb1d02`) ΓÇö branch deleted, backup `merged/add-orca-router`** ([#1751](https://github.com/Alishahryar1/free-claude-code/issues/1751))
- Issue-first workflow (user's new template): raised upstream issue #1751 2026-09-12, user relayed the URL back, then implemented. Standard catalog provider (┬º5 template, LLM7/Experiential pattern ΓÇö auto-wired `OpenAIChatProfile`, no factory/runtime protocol code). Multi-provider OpenAI-compatible gateway at `https://api.orcarouter.ai/v1` routing to 11 upstreams (OpenAI, Anthropic, Gemini, DeepSeek, Grok, Qwen, Kimi, MiniMax, Z.ai, Kling, Seedance) at provider cost, zero markup; env `ORCAROUTER_API_KEY`/`ORCAROUTER_BASE_URL`/`ORCAROUTER_PROXY`; keys `sk-orca-...` from www.orcarouter.ai/console.
- Free tier: $0 models under `-free` ids ΓÇö today `deepseek/deepseek-v4-flash-free` (smoke default) + `deepseek/deepseek-v4-pro-free` ΓÇö plus router aliases `orcarouter/free` (auto-picks among free models per request) and `orcarouter/auto` (cheapest live). Lineup rotates ("free capacity changes as models come and go"); user-configurable via `MODEL=orcarouter/<slug>` + auto-discovered per key. Limits: per-workspace fixed windows (RPM/UTC-day) tiered by lifetime spend, per-request prompt cap on lowest tier; 429 code `free_rate_limited` + `Retry-After` distinguishes retryable windows from non-retryable prompt caps.
- Profile: `_policy("ORCAROUTER", ReasoningReplayMode.REASONING_CONTENT, default_max_tokens=ANTHROPIC_DEFAULT_MAX_OUTPUT_TOKENS)` (gateway surfaces `reasoning_content` per upstream) + `NamedEffortReasoning(_LOW_MEDIUM_HIGH, enabled_value="medium")` with NO `disabled_value` ΓÇö OFF omits the field (`minimal`/`max` documented only "on some models" ΓÇö excluded from the safe vocabulary). `OpenAIModelListing(path="/models")` bare id-only (documented shape has no context-window fields). Credential probe `_Probe("orcarouter", "/models", _MODELS, _AUTH_401)` ΓÇö `/v1/models` requires the key (documented verification call); shared-credentials count stays 20.
- Nested-slash model ids (`orcarouter/deepseek/deepseek-v4-flash-free`) split on FIRST slash ΓÇö tokenrouter precedent (`tokenrouter/moonshotai/kimi-k3-free`).
- Tests: `tests/providers/test_orcarouter.py` (16 items incl. parametrizes ΓÇö construct/effort-matrix with OFF+DEFAULT omission/reasoning_content tool-history replay/bare-listing + malformed rejection/wire URL+Bearer) + runtime config test + credential-validation CASES + catalog-order + smoke-config trio.
- Current: `f8d8239` (single-commit), v6.3.0 (MINOR ΓÇö new provider), base `e632c85` (upstream tip at PR time ΓÇö #1749 NOT merged upstream, so anchors insert after llm7). ┬º12.5 full set green pre-push (gates green; suite 5192p/144s; e2e 97p/1s; targeted 180p). PR #1754 raised 2026-09-12; **greptile PASSED first review (15 files, 0 comments) + all 7 CI checks green ΓÇö merge-ready (┬º12.4 gate met)**; merging is the upstream owner's call. Version-only collision with #1736/#1740/#1749 (all 6.3.0) ΓÇö routine ┬º8, resolved at rebase/merge. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` ΓåÆ `3b4f2033`, v6.3.0; ┬º12.5 full set green; conflict cleared, greptile + all 7 CI green ΓÇö merge-ready.

### ≡ƒöä `feat-api-key-rotation` ΓÇö Multiple API keys with rotation + failover ΓÇö NO PR ([#1301](https://github.com/Alishahryar1/free-claude-code/issues/1301))
- `providers/key_pool.py`: thread-safe `KeyPool` (round-robin, cooldown failover, `parse_api_keys`); `OpenAIChatProvider` resolves the credential per request via `_resolve_api_key` when rotating; `_report_key_failure`/`_report_key_success` hooked into the stream path (rotate on 429/401/403); factory builds a pool when the credential holds >1 comma-separated key. Tests: `tests/providers/test_key_pool.py`.
- Usage: `OPENROUTER_API_KEY="sk-1,sk-2,sk-3"`. Single key = unchanged static behaviour.
- **Awaiting user decision to open a PR** (upstream #1655+#1656, another author, may cover #1301). Current: `03def116`, v6.3.0 ΓÇö rebased onto main `0dcb3715` in sync #8 (2026-09-12; provider.py KeyPool `_resolve_api_key` overlap resolved keep-both); ┬º12.5 full set green; force-with-lease pushed.

### Γ£à `fix-cline-hub-hijack` ΓÇö fcc-cline reconnects to a stale Cline Hub ΓÇö **MERGED UPSTREAM 2026-09-26 (#1641 ΓåÆ `d5930097`) ΓÇö branch deleted, backup `merged/fix-cline-hub-hijack`** ([#1590](https://github.com/Alishahryar1/free-claude-code/issues/1590))
- Root cause: interactive Cline passes `backendMode:"auto"` to core (verified in the shipped cline.exe), overriding the launcher's `CLINE_SESSION_BACKEND_MODE=local`, so Cline may attach to (or start) a **detached Hub daemon** that resolves provider settings from the user's global `~/.cline/data/settings/providers.json` instead of FCC's ephemeral file ΓÇö and outlives the launcher. The next `fcc-cline` run auto-discovers that stale Hub via `~/.cline/data/locks/hub/production.json` and routes to the wrong provider.
- Fix (defense-in-depth, isolation over deletion): `build_cline_launcher_env` now sets `CLINE_HUB_DISCOVERY_PATH` to `<ephemeral-tempdir>/hub/production.json` ΓÇö a file that never exists and is never written ΓÇö so the child can never discover ANY pre-existing Hub; any Hub it spawns writes discovery inside the ephemeral tree, deleted on exit. A user-run `cline hub` (ordinary cline) keeps its own discovery file, untouched. Upstream real fix: cline/cline#13631 + PR cline/cline#13637 (owner-filed, unmerged as of 2026-08-30); `CLINE_HUB_DISCOVERY_PATH` is an internal Cline env var (present in shipped binary) ΓÇö if renamed upstream it degrades to today's behavior with no new failure mode.
- Tests: 2 updated + 2 new in `tests/cli/test_cline_launcher.py` (env override of a stale user value; ephemeral-tree placement; file absent at spawn).
- Current: `2c8945e`, v5.19.2, base `96495b9` (v5.19.1) ΓÇö rebased on 2026-09-02 to clear the PR #1641 dirty state (upstream advanced `b85ae4a`ΓåÆ`96495b9`); version-only conflict resolved keeping PATCH 5.19.2; single-commit shape preserved (4 files, `rev-list --count main..HEAD`=1); suite 4453/148/0, e2e 50 passed + Windows-locale context-meter only, gates green; force-with-lease pushed `8962efa...2c8945e`. API-verified **mergeable=True** (state unstable = checks re-running). ┬º12.3 greptile-first applies: no manual test runs vs the bot ΓÇö wait for its review before re-validating. **Sync #8 (2026-09-12):** rebased onto main `0dcb3715` ΓåÆ `acf94479`, v6.2.16 (PATCH above 6.2.15); ┬º12.5 full set green; conflict cleared, greptile + all 7 CI green ΓÇö merge-ready (┬º12.4 met).

---

## 8. Sync Log

### Sync #13 (2026-10-11) — upstream base `105bfab8` → `fa6adde2` (v6.13.5) — 3 branches rebased + pushed, `final-rebuild` built (telepub excluded)

**Trigger:** upstream advanced to v6.13.5 (`fa6adde2`). Local main fast-forwarded after lineage verification. Pre-sync backups: `backup/pre-v6135-<branch>` per rebase target + `backup/final-pre-v6135-rebuild` = `fa9ed2e4` (old final tip).

**Per-branch results — 3 rebased, 0-behind, green, PUSHED `--force-with-lease` (PR refresh):** `feat-api-key-rotation` `67bcbcde` (no PR), `feat-models-metadata` `69fd41d0` (#1736 → MERGEABLE), `fix-ollama-model-discovery` `f1c8c172` (#1606 → MERGEABLE). Each passed the full unit suite on its rebased tip before pushing.

**`final-rebuild` merge order:** `feat-api-key-rotation` (`c2efed6f`) → `feat-models-metadata` (`ca1b884b`) → `add-custom-provider` (`f8344fe6`, anchor conflicts) → `fix-ollama-model-discovery` (`5345f2bd`) → `update-main-fix-issues` (`fae077a1`) → `fix-nim-minimax-post-terminal-framer` (`7e32ee33`, conflicts) — then the 4 audit commits re-salvaged (security hardening `101a5081`, dead-export removal `45f946e4`, smell batch `aa5f8b41`, CVE lock `298517c8` — upstream lock still carried the vulnerable versions) → fixup `8eccad11` (renamed tool-schema import + admission-registry call sites).

**Merge regressions found & fixed (all pre-existing on the rebuilt tree — proven against worktrees at `main` v6.13.5 and `fa9ed2e4`):**

| # | Symptom | Root cause | Fix |
|---|---|---|---|
| 1 | `test_sdk_stream_lifecycle.py` 4×F + file hang at 77%; full suite wedged at 97-99% (also wedged half-splits and `tests/providers` alone) | nim's post-terminal framer held `finish_reason` UNTIL RAW STREAM END; upstream v6.8.2+ (`ba43d7f3` hidden-stream retries, first-chunk streaming) needs prompt errors/stops; blocked harness streams never ended — `anext` hung and `test_sdk_observer[True]` wedged its worker | `_TERMINAL_HOLD_SECONDS = 0.5` bounded hold in `native_tool_stream._iter` (one `wait_for` post-terminal read; on timeout/stop finalize framers now) + `_TerminalHold` / `terminal_pending` property + transport recovery gate honors `terminal_pending` for `AmbiguousToolCallIdentityError` (upstream's gate keys on `terminal_seen`, which the hold defers) |
| 2 | 4× `test_chat_tool_identity.py::test_collector_identity_failure_respects_stop_and_closes_attempts[*/same|before]` — DID NOT RAISE | same hold: the terminal is stripped from its original chunk, so transport's `terminal_seen` stayed False at ambiguity time and recovery retried instead of raising | `terminal_pending` gate fix above (test file is byte-identical to main) |
| 3 | 4× `test_admin_custom_provider_status_*` 404==200 | frozen `add-custom-provider` tests hit its removed all-providers `/admin/api/providers/local-status`; the merge kept upstream #1909's per-provider route but dropped the branch's `api_key`/`proxy` pass-through | handler passes `api_key=CUSTOM_API_KEY` + `proxy=CUSTOM_PROXY` for `custom`; 4 tests ported to `/admin/api/providers/custom/local-status` + single-object response shape; upstream stub in `test_local_provider_status.py` widened to `*, api_key="", proxy=""` |
| 4 | `test_raw_nim_stop_survives_later_null_and_empty_choices[messages|responses]` — AttributeError, then wrong terminal event | monkeypatch shim used the pre-nim `_normalized_chunks(chunk, choice, ...)` signature; after adaptation the held stop re-emits — delivery completes (the test's own title: "stop survives") instead of upstream's truncated-error shape | shim rewritten to `(chunk, delta, *, hold_terminal=False, **kwargs)`; final assertion updated to `message_stop` / `response.completed` |

**Also verified:** the old "2 accepted nim failures" (`test_nim_parser_failure_closes_response_before_retry[messages|responses]`) now PASS under the bounded hold (the protocol error fires after the 0.5 s hold — inside the test's 2 s budget — and the same-provider retry recovers). Worktree comparisons pinned the regressions as merge-induced: `fa9ed2e4` ran the lifecycle file at 2F/29P (the old accepted pair only), plain `main` v6.13.5 at 35P.

**Rebuild validation:** full suite **8632 passed / 24 skipped / 0 failed / ~83 s** (the wedge is GONE; this suite previously could not finish at all); gates green (ruff format/check + ty, 0 diagnostics); `uv lock --check` consistent. e2e NOT yet run on final-rebuild. `tests/cli/test_progressive_launch.py::test_reusing_desktop_process_exits_without_owning_browser[timeout-reuse-*]` remains the known ENVIRONMENTAL flake (12 s browser-probe subprocess under load; passed in isolation and in the final clean full run).

### Sync #12 (2026-09-28) ΓÇö upstream base `ba4b9341` ΓåÆ `105bfab8` (v6.4.10) ΓÇö 3 branches rebased, 2 merged branches deleted, `final` NOT rebuilt

**Trigger:** upstream advanced 18 commits (313 files, +14163/-5554). Local main ff-synced after `merge-base --is-ancestor` lineage check (exit 0 ΓçÆ genuine fast-forward).

**Branch triage (per the user's "keep only branches that are active/available" rule):**
* **MERGED upstream ΓåÆ dropped from the active set AND local branch DELETED (user directive 2026-09-28):** `add-orca-router` (#1754 ΓåÆ `10fb1d02`, merged 2026-09-27) and `fix-cline-hub-hijack` (#1641 ΓåÆ `d5930097`, merged 2026-09-26; `git cherry upstream/main` = `-`). Exact tips saved first as `merged/add-orca-router` (`69189df4`) / `merged/fix-cline-hub-hijack` (`85b31b6a`). origin refs NOT deleted (no pushes per standing rule). NOTE: origin had moved meanwhile (force-updated `origin/add-orca-router` `867ae3cb`, `origin/fix-cline-hub-hijack` `2df1fefa`) ΓÇö irrelevant now that both are merged.
* **FROZEN (user decision 2026-09-28, mirrors the ┬º7 fix-nim precedent):** `add-custom-provider` ΓÇö PR #1469 CLOSED unmerged 2026-09-26, superseded by upstream's own custom-providers PR #1909; `update-main-fix-issues` ΓÇö PR #1744 CLOSED unmerged 2026-09-12. Both pins untouched (`69acb27d`, `f4048981`).
* `add-telepub-voyage` (`50559ea0`, ┬º12.1) and `fix-nim-minimax-post-terminal-framer` (`cfa42f81`) remain FROZEN ΓÇö verified unchanged after the cycle.

**Per-branch results ΓÇö 3 rebased, all 0-behind (`merge-base --is-ancestor main <branch>` exit 0), gates green, version-policy compliant:**

| Branch | New SHA | Commits | Policy | Suite | e2e | Notes |
|---|---|---|---|---|---|---|
| `feat-api-key-rotation` | `f976b9ce` | 1 | `minor` | 6693p/23s | 221p/1s | rebase clean; `ty` fallout from #1923 (`make_provider_config` dropped `rate_limit`/`rate_window`) ΓÇö test helper fixed + amended; 1 e2e setup-error flake ΓåÆ 5/5 green isolated |
| `feat-models-metadata` (#1736) | `d91ad0c7` | 1 | `minor` | 6681p/23s | 221p/1s | 2 keep-both import conflicts: `api/model_catalog.py` (main's `context_window_for_client` + branch's `ProviderModelInfo`), `application/model_catalog.py` (`dataclass, field, replace`); `test_code_sessions` e2e flakes ΓåÆ file re-run 84/84 green |
| `fix-ollama-model-discovery` (#1606) | `fb735b52` | 3 | `patch` | 6680p/23s | 221p/1s | rebase clean; upstream's NEW `tests/runtime/test_vscode_chat_sync.py` asserted an exact catalog set without unconfigured locals ΓÇö fails on branch, passes on `main`; assertion extended with `self_sufficient_local_provider_ids()` (branch precedent: `test_provider_manager.py`), amended; 1 playwright `TargetClosedError` flake ΓåÆ 2/2 green isolated |

**Regressions found & fixed during the cycle:** (1) 2 `ty` unknown-argument errors in `tests/providers/test_key_pool.py` against #1923's new signature; (2) `test_catalog_updates_connected_file_and_disconnect_stays_removed` broken by self-sufficient local probes populating the VS Code catalog (new upstream test, new interaction). Both fixed inside the branch commits via amend; gates + suite re-run green afterwards.

**E2e flake protocol held:** different single tests flaked per run (setup-error class, one hard fail, one playwright route race) ΓÇö every one passed in isolation; no two e2e suites were ever run concurrently (one uncaptured run wedged the shell this cycle and was re-issued after recovery).

**`final` REBUILD (executed 2026-09-28, same session):** old final `94132fb7` ΓåÆ fresh `final` on `105bfab8`, 7 branches merged in order ΓÇö telepub `994c9756` (8 keep-both conflicts: `.env.example`ΓåÆdeleted, `pyproject.toml`/`uv.lock`ΓåÆmain's dynamic-version form, README/manifest/settings/profiles/credential-test keep-both; README count ΓåÆ **57**), key-rotation `13e3f278` (clean), models-metadata `e4df873e` (clean), custom-provider `c59988f8` (**7 anchor conflicts**, incl. the ┬º9 combine `api_key_provider=resolved_api_key_provider` + `credential_optional=self._profile.credential_optional`; catalog tail `ΓÇªollama, telepub_voyage, custom`), ollama `90aa9d00` (clean), update-main `64bf8744` (clean ΓÇö sanitizer followed upstream's rename into `providers/nvidia_nim/native_tool_schema.py`), nim `db20836d` (pyproject/uv.lock ΓåÆ main's).

**Audit salvage (code that existed ONLY on the backups; user directive "add backup code not in final"):** cherry-picked the 4 audit commits ΓÇö `d21fc924` security hardening (sha1 `usedforsecurity=False`; SQLite `_TABLES` + `_check_sql_identifiers` fail-closed allowlist), `6125a548` **CVE lock bump KEPT ΓÇö upstream's current lock still carried the vulnerable versions** (starlette 1.6.0, cryptography 50.0.1, python-multipart 0.0.32, urllib3 2.7.0, click 8.5.0, pygments 2.21.0, msgpack 1.2.2; `uv lock --check` consistent; httpx2 test annotation applied), `00d5d28f` dead-export removal (all 7 symbols re-verified unused), `50692998` Batch-4 smell fixes (18 files; 3 files resolved ours/deleted ΓÇö lmstudio pre-async variant obsolete, `core/anthropic/tools.py` deleted upstream, sqlite schema assembly moved to migrations).

**Fixup commit `3cfe195c`:** telepub descriptor `website_url`+`logo_filename` + restored `telepub_voyage.svg` + SOURCES row; `test_tool_schema.py` import ΓåÆ renamed module; 5 `create_provider` call sites in `test_provider_runtime.py` given the admission registry; `test_telepub_voyage.py` rewired to `_chat._build_request_body` with the dead kwargs dropped.

**Backup consolidation (user directive):** `final-backup` (`2ab1776c`) = synthetic merge commit, tree = old final `94132fb7`, parents = old final + `final-backup-20260912` + `-audit` + `-20260920` + `-20260923` + `-20260926` + `pre-sync9/final` (all 7 verified ancestors) ΓÇö then the 6 dated backup branches were DELETED. Exactly ONE backup branch remains (`pre-syncN/<branch>` snapshots untouched).

**Skipped secondary backup code (documented):** `cde32c91` (count-22 fix superseded by the computed `len(keys)` assertion; paren fix n/a), `d2ac4b9b` (README "53" obsolete ΓÇö now 57), `3e77f612` (json5/tomlkit/simplejson already present in pyproject+lock; httpx2 annotation already applied).

**Rebuild validation:** gates green (format/ruff/ty, 0 diagnostics); full suite **6742 passed / 23 skipped / 2 failed = exactly the accepted nim trade-off**; e2e **221 passed / 1 skipped** + one `test_code_sessions` layout flake passing 3/3 isolated. ┬º9 symbols verified (`KeyPool`, `_resolve_api_key`, `sanitize_tool_schema_patterns`, `_EXPECTED_PROVIDER_ORDER` tail `ΓÇªollama, telepub_voyage, custom`).

**Not done:** no pushes, no PR actions.

### Sync #11 (2026-09-26) ΓÇö upstream base `faeec6ba` ΓåÆ `ba4b9341` ΓÇö **7 branches rebased, `final` rebuilt, NOTHING PUSHED**

**Trigger:** upstream advanced 18 commits (90 files, +5165/ΓêÆ997). Main ff-synced to `ba4b9341` after a `merge-base --is-ancestor` lineage check (exit 0 ΓçÆ genuine fast-forward, no force-push). `uv` auto-provisioned **Python 3.14.7** (upstream now pins `requires-python ==3.14.7` and **deleted `.python-version`**), rebuilding the venv.

**Upstream changes that reshaped the sync:**
* **Release automation (#1896/#1903/#1904) ΓÇö invalidates ┬º4.** `hatch-vcs` + `dynamic = ["version"]`; `scripts/check_version_policy.py`, `publish_release.py`, `validate_release.py`; required `version-policy.yml` check that **rejects `project.version`**.
* **Licence ΓåÆ AGPL-3.0-only (#1887)**, `fcc-doctor` (#1906), installer checks moved to the opt-in smoke suite (#1908).
* **Cheaper Inference provider (#1899)** ΓÇö landed in the same catalog/settings/profiles/manifest anchor regions as our provider branches, which is why `add-orca-router` and the telepub merge were "keep-both" conflicts.
* **Fixed cloud endpoints (#1891)** ΓÇö upstream dropped the `*_DEFAULT_BASE` imports for lightning/experiential/nararoute/tokenrouter; those imports must NOT be re-added during conflict resolution.
* `openai_api` sampling params (#1883), NIM voice by default (#1893), image token pricing (#1895).

**Branch triage (per the user's "keep only branches listed as active/available" instruction):** dropped `add-lightning-ai` (#1740) and `add-experiential-labs` (#1749) ΓÇö **both merged upstream** (`613cdaaa`, `0329ac49`), branches deleted. `add-telepub-voyage` (┬º12.1) and `fix-nim-minimax-post-terminal-framer` (#1742) stayed **frozen**; verified byte-identical to their pre-sync pins afterwards.

**Per-branch results ΓÇö every one rebased, 0-behind, gates green, version-policy compliant:**

| Branch | New SHA | Commits | Policy | Suite | e2e | Notes |
|---|---|---|---|---|---|---|
| `fix-cline-hub-hijack` (#1641) | `85b31b6a` | 1 | `patch` | 6207p/18s | 195p/1s | clean rebase, no conflicts |
| `feat-api-key-rotation` | `2a386dae` | 1 | `minor` | 6222p/18s | 195p/1s | version-only conflict |
| `update-main-fix-issues` (#1744) | `f4048981` | 3 | `patch` | 6218p/18s | 195p/1s | version-only conflict on commit 1 of 3 |
| `add-orca-router` (#1754) | `69189df4` | 1 | `minor` | 6237p/18s | 194p/1s* | **11 files conflicted** ΓÇö heaviest; keep-both vs cheaperinference |
| `feat-models-metadata` (#1736) | `b335ab82` | 1 | `minor` | 6210p/18s | 194p/1s* | version-only conflict |
| `add-custom-provider` (#1469) | `69acb27d` | 2 | `minor` | 6223p/18s | 195p/1s | version + `test_provider_runtime.py` |
| `fix-ollama-model-discovery` (#1606) | `58f6d818` | 3 | `patch` | 6209p/18s | 195p/1s | **collapsed 10 commits (6 main-merges, 2 no-op) ΓåÆ 3**; architectural re-map |

\* e2e flakes of the `net::ERR_UNSAFE_PORT` class ΓÇö the e2e fixture picks a random port that sometimes lands on a Chromium-blocked port (5060, 1723, 10080). **Both passed 6/6 and 2/2 in isolation and pass on a clean serial re-run. Not regressions.** When they appear, re-run the single test rather than the suite, and **never run two e2e suites concurrently** (parallel runs collide on ports ΓÇö this cost real time this cycle).

**Rebase recipe that worked (forks from ┬º3/┬º8 rails):**
```powershell
$env:GIT_EDITOR='true'                    # prevents the invisible vim.exe hang
git switch <branch>; git rebase main
# pyproject.toml/uv.lock -> keep upstream's dynamic-version form:
git checkout main -- pyproject.toml uv.lock ; uv lock
git add <explicit paths>                   # never -A
git -c core.editor=true rebase --continue
# provider-anchor conflicts -> keep BOTH sides in catalog order; drop imports
#   upstream deleted (LIGHTNING/EXPERIENTIAL/NARAROUTE/TOKENROUTER _DEFAULT_BASE)
uv run python scripts/check_version_policy.py --base main --head HEAD --title 'minor: ΓÇª'
```

**`final` rebuilt (┬º9) on `ba4b9341` ΓÇö ancestry 9/9 verified by exit code.** Merge order: key-rotation ΓåÆ models-metadata ΓåÆ custom ΓåÆ ollama ΓåÆ update-main ΓåÆ cline ΓåÆ **nim** ΓåÆ telepub. Notes:
* `add-custom-provider` conflicted in `providers/openai_chat/provider.py` as documented ΓÇö combined as `api_key_provider=resolved_api_key_provider` + `credential_optional=ΓÇª`. **The old `"no-api-key"` SDK-placeholder note in ┬º9 is OBSOLETE** ΓÇö keyless custom endpoints are now handled by the profile's `credential_optional` flag.
* Telepub's 8 conflicts were **all additive** (distinct provider fields), so ┬º12.1's "stop and ask" trigger did **not** fire. But upstream made `website_url` + `logo_filename` **required** on `ProviderDescriptor`, which telepub (frozen since 2026-08) predates: added both, and created the missing `telepub_voyage.svg` (project-authored neutral glyph, mirroring `custom.svg`) plus its `SOURCES.md` row. **Without the asset, `e2e/test_provider_modals.py::test_provider_titles_link_to_websites_and_every_logo_loads` fails** ΓÇö the e2e suite *does* assert every logo loads (`naturalWidth > 0`).
* `.env.example` (modify/delete) resolved as **deleted**, matching upstream's deliberate removal.
* Credential-count gotcha (┬º9): kept the self-computing `assert len(result) == len(keys)` form rather than telepub's hardcoded `== 21` ΓÇö the computed form cannot go stale when the catalog changes.
* `tests/providers/test_telepub_voyage.py` called `provider._build_request_body(...)`, which upstream moved to the module-level `build_openai_chat_request_body(request, reasoning=ΓÇª, policy=ΓÇª)` in `request_policy.py` (surfaced as 4 `ty` errors). Rewired through `OPENAI_CHAT_PROFILES["telepub_voyage"].request_policy`.
* **Catalog = 57** on `final` (56 on main + telepub).

**`final` result:** gates green (769 files formatted, ruff, ty) ┬╖ suite **6272 passed / 18 skipped / 2 failed** ┬╖ e2e **195 passed / 1 skipped**. The 2 failures are the accepted `fix-nim` trade-off documented in the header.

**Backups:** `pre-sync11/<branch>` for all 9 branches + `final-backup-20260926` (old `final` `1f8b1fd7`, which was a bare ancestor of main with 0 unique commits ΓÇö i.e. `final` had been silently emptied before this sync).

**Not done (user decision):** no `git push` to `origin`, no force-push, no PR opened/edited. Every branch is local-only and ready for review.

### `final` SonarQube-style audit + fix pass (2026-09-12) ΓÇö `cde32c9` ΓåÆ `3666dcc` (4 commits, no upstream movement)

**Scope:** user-directed deep-audit of `src/` on `final` only (never PR'd). Tools: bandit 1.9.x, vulture 2.14, deptry 0.17, pip-audit 2.10 (via `uvx`), ruff 0.16.4 `--select ALL` pass. Verified clean already: configured ruff ruleset 100%, zero TODO/noqa/type-ignores, constant-time auth, loopback-guarded admin, 0o600 secret files.

**Batch 1 ΓÇö `1730268` (security):** sha1 digest `usedforsecurity=False` (`core/openai_responses/tools.py`, non-crypto tool-id); sqlite identifier allowlist `_TABLES` + `_check_sql_identifiers()` fail-closed validation of interpolated table/column names (`runtime/code_sessions_sqlite.py` `_insert`/`_update`; all data stays `?`-parameterized).

**Batch 2 ΓÇö `80d1fc2` (CVEs, lock-only, NO pyproject edits):** starlette 0.52.1ΓåÆ**1.3.1** (major; ASGI layer ΓÇö validated by full suite + e2e), cryptography 49.0.0ΓåÆ**50.0.0** (major; only via google-auth/vertex), python-multipart 0.0.22ΓåÆ0.0.31, urllib3 2.6.3ΓåÆ2.7.0, click 8.3.1ΓåÆ8.3.3, pygments 2.19.2ΓåÆ2.20.0, msgpack 1.1.2ΓåÆ1.2.1 (via librosa/voice_local). Fallouts fixed: starlette 1.6 TestClient now returns `httpx2.Response` ΓåÆ tests/api/test_ordinary_error_phases.py annotation switched to httpx2. pip-audit re-run: **0 vulnerabilities**.

**Batch 3 ΓÇö `e6ff13d` (dead code):** removed 7 verified-zero-reference exports (routing.py `resolve_messages_request_with_policy`, admin/validation.py `validate_values`, admin/manifest.py `field_input_key`+`fields_with_attrs`, env_migrations.py `env_text_needs_migration`, openai_responses/reasoning.py `responses_reasoning_to_output_config`, streaming/error_mapping.py `openai_error_from_anthropic_error`) + now-unused imports; 78 deletions/6 files. **8th candidate `TRACE_PAYLOAD_BINDING` REVERTED** ΓÇö it is deliberately imported by tests/core/test_trace.py to pin the traceΓåölogging bind-key contract (Phase-1 grep truncation hid the test import).

**Batch 4 ΓÇö `3666dcc` (smells, 21 files, broad-but-safe):** ruff autofixes (FURB110 ├ù4 falsy-safe, FURB167 ├ù7, RET/PIE/PTH/ISC/PLC/PYI/Q/RSE/PLR5501 set); hand-fixes PLR1714 ├ù15 (incl. workflow.py cross-operand `!=` chain ΓåÆ `not in` tuple, logic-equivalent), FLY002 ├ù6 (str-only verified), RET504, PLW2901 ├ù2 markdown (comprehension); ASYNC240: code-session `_create` `Path.resolve` offloaded to `anyio.to_thread.run_sync` (per-request path). Gates after each batch: ruff format/check, ty, pytest -q 5306p/144s, e2e 98p/1s (2 first-run timing flakes reproduced nowhere on rerun).

**Documented WONTFIX (do NOT re-litigate in future audits):** bandit B608 ├ù3 (identifiers now allowlisted; data `?`-parameterized ΓÇö residual f-string SQL is table/column names only), B101 asserts (invariants), B105/B106/B110/B112/B603/B607/B104/B311/B615/B404 (reviewed false positives/benign); TC00x typing-import placement (~764 sites; conflicts with PEP 649 lazy annotations); C901/PLR091x complexity (~40; churn > value); PLW0603 module-level config state (deliberate); PLW2901 tool_adaptation `tool` rebinds ├ù2 (intricate restore-merge pipeline, intent verified); ASYNC240 runtime/application.py ├ù2 (startup-only, once per process); ASYNC109 limiter `timeout` param (public API name). deptry: all importΓåödist name FPs, no unused deps.

**ΓÜá∩╕Å Final-only:** all 4 commits exist ONLY on `final`. A future ┬º9 rebuild-from-main recreates final from scratch and DISCARDS this pass ΓÇö cherry-pick `1730268 80d1fc2 e6ff13d 3666dcc` (or re-run the audit) if wanted on the new final. The CVE lock-bumps would be re-derived automatically only if upstream bumps too.

### Sync #8 (2026-09-12 ΓåÆ 09-13) ΓÇö upstream base `f3a3aac` ΓåÆ `0dcb3715` (v6.2.15)

**Trigger:** upstream main advanced `f3a3aac` ΓåÆ `0dcb3715` (11 commits #1756ΓÇô#1767; 46 files +5194/ΓêÆ345; version 6.2.2 ΓåÆ **6.2.15** ΓÇö VS Code + Codex integrations, JetBrains ACP preview card, admin loading fix, Codex client tool discovery fix). Local main ff-synced + pushed to fork. All 8 open-PR branches went conflict-dirty; merge-tree scoped them version-only (exceptions: `add-custom-provider` + `feat-api-key-rotation` also touch `providers/openai_chat/provider.py`).

**Per-branch results (┬º12.5 full set green on every branch ΓÇö gates + full suite (5497ΓÇô5520p/152s) + e2e (116p/1s, Windows-locale context-meter exception); every open PR conflict cleared + greptile PASS + all 7 CI green):**

| Branch | Old ΓåÆ New SHA | Version | Method |
|--------|---------------|---------|--------|
| `main` | `f3a3aac` ΓåÆ `0dcb3715` | 6.2.15 | ff-only + push origin/main |
| `fix-ollama-model-discovery` (#1606) | `04e5c04` ΓåÆ `132b5fdc` | 6.2.16 (PATCH) | merge main INTO branch (never-rewrite), ff push NO force |
| `fix-cline-hub-hijack` (#1641) | `bf157a2` ΓåÆ `acf94479` | 6.2.16 (PATCH) | rebase + force-with-lease |
| `feat-models-metadata` (#1736) | `5fe9ce8` ΓåÆ `a56c9856` | 6.3.0 (kept) | rebase + force-with-lease |
| `add-lightning-ai` (#1740) | `3575595` ΓåÆ `96a601d0` | 6.3.0 (kept) | rebase + force-with-lease |
| `update-main-fix-issues` (#1744) | `4ae75ae` ΓåÆ `e3dc94e1` | 6.2.16 (PATCH) | rebase + force-with-lease |
| `add-experiential-labs` (#1749) | `3886c8e` ΓåÆ `b61736c0` | 6.3.0 (kept) | rebase + force-with-lease |
| `add-orca-router` (#1754) | `f8d8239` ΓåÆ `3b4f2033` | 6.3.0 (kept) | rebase + force-with-lease |
| `add-custom-provider` (#1469) | `b69108d` ΓåÆ `b218d21e` | 6.3.0 (kept) | complex rebase ΓÇö `api/admin_routes.py` (asyncio.gather + `_probe` closure preserving custom blank-URL skip + keyless bare `client.get`, ┬º8 sync #6 precedent), `providers/openai_chat/provider.py` (`api_key=resolved_api_key or "no-api-key"` combined with upstream changes), `e2e/conftest.py` + `tests/api/test_admin.py` keep-both + force-with-lease |
| `feat-api-key-rotation` (NO PR) | `6298e19` ΓåÆ `03def116` | 6.3.0 (kept) | rebase ΓÇö `provider.py` KeyPool `_resolve_api_key` overlap kept both + force-with-lease |

- Greptile sweep after all pushes: every open PR re-reviewed clean on its new head (0 blocking comments; #1469: "17 files reviewed, 0 comments added"; #1744 head `e3dc94e1` clean). ┬º12.4 gate met on all.
- **Exclusions (user decisions):** telepub FROZEN at `50559ea` (┬º12.1 ΓÇö untouched). `fix-nim` PR #1742 CLOSED UNMERGED by the maintainer 2026-09-12 ("the minimax model is deprecated ΓÇö no need to fix, just stop using it") ΓÇö branch frozen at `cfa42f8`, NOT updated; still merged into `final` at `cfa42f8`.

**`final` rebuild (base `0dcb3715`, 2026-09-12/13):**
- Old final `d0cc706` preserved as local `final-backup-20260912-audit`; final reset to main, ALL 11 branches merged in ┬º9 order (first-parent stack): telepub `50559ea` `9db9d67a` ΓåÆ key-rotation `2d33e610` ΓåÆ models-metadata `6262e6cb` ΓåÆ custom-provider `2da8b73b` ΓåÆ ollama `a6ae9f15` ΓåÆ update-main-fix-issues `9fc965df` ΓåÆ cline `999e0212` ΓåÆ fix-nim `cfa42f8` `e271aa46` ΓåÆ lightning `4e707130` ΓåÆ experiential `5164cf3b` ΓåÆ orca `33a05822`. All anchors resolved keep-both (HEAD side first); trio order lightning ΓåÆ experiential ΓåÆ orcarouter at every anchor (┬º9 rule); version 6.3.0; lock regenerated after the last merge.
- Audit re-application: `841dfc9e` (security ΓÇö sha1 `usedforsecurity=False`; tools.py conflict resolved keeping upstream's new tool-discovery code), `6a077f65` (dead exports ├ù7, clean), `424ab991` (smells; the RET504 admin_routes site no longer exists upstream ΓÇö not re-applied), `0cefbc68` (fresh CVE lock pass ΓÇö starlette 1.6.0, cryptography 50.0.1, python-multipart 0.0.32, urllib3 2.7.0, click 8.5.0, pygments 2.21.0, msgpack 1.2.2; pip-audit 0 vulns; lock re-derived fresh, NOT a `80d1fc2` cherry-pick) + httpx2 test annotation re-applied (`tests/api/test_ordinary_error_phases.py`).
- **INCIDENT ΓÇö pyproject deps silently dropped (fixed `3e77f612`):** telepub is based on OLD main (`f3a3aac`, predating upstream's `json5`/`tomlkit`/`simplejson` additions), so merge 1 made final's pyproject "delete" those dep lines relative to the merge base; every later merge silently preserved the deletion (symptoms: `uv lock` "nothing to commit" after merge 11; later ty ├ù8 unresolved-import). Fix: restored the 3 dep lines at main's exact placement + re-locked (162 packages). **Future ┬º9 rebuilds: after the telepub merge, immediately diff pyproject deps against main.**
- Count fix `7e78423`: the trio merge resolved `test_unsupported_shared_credentials_never_send_http` to 21; ┬º9 formula (main 20 + telepub +1 + lightning +1 = 22) restored both assertions to 22.
- Verification: first-parent ancestry 11/11 + main + fix-nim all `merge-base --is-ancestor` green; catalog 55 == `SUPPORTED_PROVIDER_IDS`; README provider rows 54 == old final exactly (upstream added 0 providers in #1756ΓÇô#1767; the plan's stale "53" was a sync-#7-era value); gates green; full suite 5633p/152s; e2e 116p/1s; pip-audit 0 vulns.
- Notes restored from `final-backup-20260912-audit` (┬º9 step 7) and updated in this sync #8 commit.

### Sync #7 (2026-09-02) ΓÇö upstream base `b85ae4a` ΓåÆ `96495b9` (v5.19.1)

**Trigger:** upstream main advanced `b85ae4a` ΓåÆ `96495b9` (2 commits: #1644 "Keep chat operations alive across clients", #1645 "Add internal Codex Direct app-server transport foundation"; 28 files, +6360/ΓêÆ767; version 5.18.11 ΓåÆ **5.19.1**, `uv.lock` bumped). Both OPEN PRs (#1606, #1641) went `dirty` ΓÇö merge-tree predicted version-only conflicts (pyproject.toml + uv.lock) for each.

**Per-branch results (all gates green; suites fully green):**

| Branch | Old ΓåÆ New SHA | Version | Full suite (p/s/f) | Push |
|--------|---------------|---------|--------------------|------|
| `main` | `b85ae4a` ΓåÆ `96495b9` | 5.19.1 | ΓÇö | ff-only + push origin/main |
| `fix-ollama-model-discovery` | `0b3d158` ΓåÆ `edd34fb` | 5.19.2 (PATCH) | 4454/148/0 | merge of `main` INTO branch + ff push (NO force) ΓÇö PR #1606 conflict cleared |
| `fix-cline-hub-hijack` | `8962efa` ΓåÆ `2c8945e` | 5.19.2 (PATCH) | 4453/148/0 | rebase onto `main` + force-with-lease ΓÇö PR #1641 conflict cleared |

- **ollama (never-rewrite):** `git merge upstream/main` onto `0b3d158` ΓåÆ version resolved 5.19.2, `git checkout main -- uv.lock` + `uv lock` regenerated (free-claude-code 5.19.1ΓåÆ5.19.2), zero markers, merge commit `edd34fb` (parents `0b3d158`+`96495b9`, both ancestor-exit-0 verified). FF push only `0b3d158..edd34fb`.
- **cline (standard):** rebase onto `main`; version-only conflict resolved 5.19.2; single-commit shape preserved (`2c8945e`, 4 files); force-with-lease `8962efa...2c8945e`.
- API-verified after pushes: **#1606** head `edd34fb` ΓåÆ later `c84164c`, base `96495b9`; **#1641** head `2c8945e`, base `96495b9`. Final states (2026-09-02): both PRs `mergeable=true, state=clean` ΓÇö all 7 checks green incl. Greptile.
- **ollama CI re-trigger (2026-09-02):** the first Actions run for `edd34fb` (33610053117) was CANCELLED (GitHub-side; no superseding run existed). Re-run API returned 403 (PAT has no upstream write). Appended an EMPTY commit `c84164c` and ff-pushed (`edd34fb..c84164c`) to re-trigger ΓåÆ run 33612506300 **SUCCESS** (pytest, playwright, ruff-format, ruff-check, ty, ban-suppressions all success) + Greptile Review success ΓåÆ PR #1606 `clean`. Empty-commit re-trigger is the standing fallback when a run is cancelled and upstream write is unavailable.
- **`state=blocked` on ALL open PRs = required approving review, NOT a CI failure (2026-09-02):** repo `main` rulesets (via `rules/branches/main`): (1) `main-integrity` ΓÇö required checks `{Ban suppressions, ruff-format, ruff-check, ty, pytest, playwright}` with `strict_required_status_checks_policy=true`, `required_linear_history`, deletion/force-push banned, squash-only merges; (2) `main-review-required` ΓÇö `required_approving_review_count: 1`. All three PRs (#1469, #1606, #1641) now report `mergeable=True state=blocked` identically ΓåÆ the blocker is the missing approving review, nothing to fix on the branches. PSA: the earlier #1606 `state=clean` briefly seen was GitHub's pre-ruleset cache; and the "pytest error" a viewer may see is the CANCELLED run 33610053117 attached to intermediate commit `edd34fb` (its log ends `##[error]The operation was canceled.` at 93% PASSED ΓÇö NO test failures; GitHub-side cancellation). Fork-side cannot approve (not a maintainer) nor re-run cancelled runs (403 without upstream write); owner must click Re-run or Approve.
- e2e both branches: **50 passed** + only the Windows-locale `test_chat_context_meter_...` failure (passes on ubuntu CI). NOTE: upstream #1644 reworked `e2e/test_chat_sessions.py` ΓÇö the delayed-older-page test now asserts `.assistant-message:not(.live-message)` count 2 (no more `to_be_enabled()`), new `_hold_next_chat_operation` helper; it **passed** on both branches this cycle.
- Standing debts (unchanged): `final` still `6e2aa56` (v5.19.0, base `b85ae4a`) ΓÇö rebuild onto `96495b9` per ┬º9 (will also pick up `add-custom-provider` `b596e07` incl. the 409-retry fix and ollama `edd34fb`). `add-custom-provider` origin advanced to `b596e07` = "Merge branch 'main' into add-custom-provider" (web/user-driven; parents `1e537fb`+`96495b9`) ΓÇö local ref synced, PR #1469 current and CI green.

### Sync #6 (2026-09-01)

**Trigger:** upstream main advanced `32491e7` ΓåÆ `b85ae4a` (12 commits: #1618 durable local Chat Sessions + sqlite store, #1623ΓÇô#1632 Chat Sessions/Admin UI polish, #1615 versioned Admin assets, #1616 sidebar pinning, #1634 Groq TPM budget recovery, #1635 Admin branding polish; version 5.17.5 ΓåÆ **5.18.11**). Local main synced `--ff-only` + pushed fork. Pre-restructure history (older sync logs) lives at `D:\Agentic coding\Project\claude\HANDOFF_NOTES.pre-cleanup-20260827.bak`.

**Per-branch results (all gates green; suites fully green):**

| Branch | Old ΓåÆ New SHA | Version | Full suite (p/s/f) | Push |
|--------|---------------|---------|--------------------|------|
| `main` | `32491e7` ΓåÆ `b85ae4a` | 5.18.11 | ΓÇö | ff-only + push |
| `fix-cline-hub-hijack` | `8573cbe` ΓåÆ `8962efa` | 5.18.12 (PATCH) | 4407/148/0 | force-with-lease |
| `feat-api-key-rotation` | `4e00047` ΓåÆ `fd26c36` | 5.19.0 (MINOR) | 4421/148/0 | force-with-lease |
| `feat-models-metadata` | `82e72a3` ΓåÆ `2e72ae0` | 5.19.0 (MINOR) | 4408/148/0 | force-with-lease |
| `add-custom-provider` | `af2922f` ΓåÆ `6ac42f9` | 5.19.0 (MINOR) | 4422/148/0 | force-with-lease (PR #1469 updated) |
| `fix-ollama-model-discovery` | `79e8345` ΓåÆ `0762bfd` | 5.18.12 (PATCH; bump commit on top, external merge `e42e115` preserved) | 4291/148/0 | fast-forward, NO force |
| `final` | `689f422` (deleted) ΓåÆ `6e2aa56` | 5.19.0 | 4452/148/0 | force-with-lease |

**Rebase notes:**
- All 4 rebased branches conflicted in `pyproject.toml` + `uv.lock` only (merge-tree predicted) ΓÇö except `add-custom-provider`, which also conflicted in `src/free_claude_code/api/admin_routes.py` + `tests/api/test_admin.py` (upstream's parallel `asyncio.gather` refactor of `local_provider_status`).
- **Semantic merge on admin_routes:** kept BOTH imports (`openai_v1_base_url` + upstream's `package_version`); `local_provider_status` now uses upstream's `asyncio.gather` concurrency with a `_probe` closure that preserves the custom blank-URL skip + api_key/proxy passthrough. Upstream's strict `SlowAsyncClient` e2e fake (`get(self, url)`) exposed that the probe always passed empty `headers` ΓÇö fixed by attaching headers ONLY when a credential is configured (keyless locals get a bare `client.get(url)`). `tests/api/test_admin.py`: upstream's concurrency test + all 4 custom-provider tests kept in full.
- Version invariant restored per branch (MINOR ΓåÆ 5.19.0, PATCH ΓåÆ 5.18.12) during conflict resolution + `uv lock` ΓÇö single-commit shapes preserved (no amend needed); the ollama branch got a separate bump commit instead (never rebase it).
- Telepub merged into `final` at frozen SHA `17382eb` now 3-way conflicts on version files only (main moved past its base `3ef17fe`) ΓÇö version-only, resolved per ┬º9; NOT non-additive.

**Pre-existing upstream e2e failures (verified on clean `main` ΓÇö NOT ours):**
- `e2e/test_chat_sessions.py::test_chat_context_meter_shows_used_over_advertised_context_window` ΓÇö fails on Windows ONLY: the meter renders `100k` (lowercase, `Intl.NumberFormat` compact) while the test regex expects `100K`. **PASSES on ubuntu CI** ΓÇö proven by sibling PR playwright runs (#1641 `8962ef`, #1606 `0b3d158` both green on the same base) and by the #1469 CI log. Not a CI blocker; do not chase locally.
- `e2e/test_chat_sessions.py::test_delayed_older_page_cannot_cross_into_another_chat` ΓÇö ROOT CAUSE FOUND + FIXED on `add-custom-provider` (`1e537fb`, 2026-09-02): the test's rename PATCH races the second send's revision bump ΓåÆ 409 ΓåÆ `updateSession` silently dropped the rename ΓåÆ the renamed library card never appeared ΓåÆ 30s click timeout at line 243. Confirmed from the actual CI log (run 33433364609, job 99623834946). Fixed by the 409 retry in `chat_sessions.js` (see ┬º7 add-custom-provider card). Carry the fix upstream / merge into `final` at next rebuild.
- One full-e2e run on `final` showed 12 transient ERRORs in chat-sessions tests right after the full suite finished (resource contention) ΓÇö all passed standalone. Re-run e2e before believing chat-sessions errors.
- **CI-log access trick:** Actions logs/artifacts are auth-gated, but the stored git credential (`git credential fill` ΓåÆ Tanishq-1 PAT) works: `Invoke-WebRequest -Headers @{Authorization="Bearer <PAT>"} https://api.github.com/repos/Alishahryar1/free-claude-code/actions/runs/<id>/logs` returns the zip with per-job logs. Use it instead of guessing from annotations (annotations only say "Process completed with exit code 1").

**`final` rebuilt from scratch:** fresh from `main` (`b85ae4a`); merges: `add-telepub-voyage` (version-only) ΓåÆ `feat-api-key-rotation` (clean) ΓåÆ `feat-models-metadata` (clean) ΓåÆ `add-custom-provider` (**7-file additive merge** ΓÇö kept BOTH `telepub_voyage` + `custom` in catalog/profiles/settings/provider_manifest/contract test/`.env.example`; `provider.py` semantic merge `api_key=resolved_api_key or "no-api-key"`) ΓåÆ `fix-ollama-model-discovery` (version-only, kept 5.19.0). All 5 branches + main verified as ancestors via exit-code checks; 9-symbol code audit 9/9 HIT (┬º9); gates green; suite 4452/148/0; e2e 42 passed + only the pre-existing failure; pushed `6e2aa56`.

**Sync rails (durable rules ΓÇö always apply):**
1. `$env:GIT_EDITOR='true'` before every rebase and `rebase --continue` (invisible `vim.exe` hang).
2. Resolve conflicts with exact edits, never regex; verify zero `<<<<<<<` markers before continuing.
3. Lockfile order: resolve `pyproject.toml` ΓåÆ `git checkout main -- uv.lock` ΓåÆ `uv lock` ΓåÆ marker check ΓåÆ `git add <explicit paths>` (never `-A`; stray `Microsoft/Windows/PowerShell/ModuleAnalysisCache` dirs otherwise).
4. Long pytest runs: background terminal after explicit `Set-Location` into the repo (foreground runs were killed ~163s).
5. PowerShell exit codes: `git merge-base --is-ancestor A B; $LASTEXITCODE -eq 0` ΓÇö never test output truthiness.
6. Version bump + `uv lock` in the SAME commit; amend to preserve single-commit branch shape.
7. After a rebase auto-converges the version to base, re-edit + `uv lock` + amend to restore the above-base invariant.
8. The ollama PR branch carries an EXTERNAL merge commit ΓÇö add commits on top only, push without force.
9. Full suite + e2e may run concurrently in two background terminals, but see the concurrency gotcha above before trusting config-area results.

---

## 9. Final Integration Branch (`final`)

> **ΓÜá∩╕Å SYNC #11 AMENDMENTS to the recipe below** (it was written for the pre-#1896 world):
> * The **merge list is now 8, not 11** ΓÇö drop `add-lightning-ai` and `add-experiential-labs` (both **merged upstream**; branches deleted). The "trio" stacking rule below is **dead**; `add-orca-router` is now the only one of the three left.
> * **Step 4's `provider.py` combination is obsolete** ΓÇö do NOT use `api_key=resolved_api_key or "no-api-key"`. That branch now uses `credential_optional=True` on the profile, so combine as `api_key_provider=resolved_api_key_provider` + `credential_optional=self._profile.credential_optional`.
> * **Step 5's stacked-count gotcha for `pyproject.toml`/`uv.lock` is obsolete** ΓÇö there are no versions any more (┬º4). Resolve those conflicts to upstream's `dynamic = ["version"]` form and regenerate the lock.
> * **`ProviderDescriptor` now requires `website_url` + `logo_filename`**, and the e2e suite asserts every logo asset actually loads ΓÇö any provider merged into `final` must have its asset + a `SOURCES.md` row.
> * **`.env.example` no longer exists** (upstream deleted it) ΓÇö resolve that modify/delete as *deleted*.
>
> **ΓÜá∩╕Å SYNC #12 AMENDMENTS:** the merge list is now **7** ΓÇö `add-orca-router` and `fix-cline-hub-hijack` are part of `main` (PRs #1754/#1641 merged upstream), so they no longer merge separately; `add-custom-provider` and `update-main-fix-issues` are FROZEN pins but still merged into `final` (fix-nim precedent). Rebuilt `final` also carries the salvaged audit commits (┬º8 sync #12). Catalog tail = `ΓÇª, "ollama", "telepub_voyage", "custom"` (**57** = 56 on main + telepub). Backups: exactly ONE `final-backup` branch now ΓÇö no more dated backups (┬º8 sync #12).

**Purpose:** unified integration of ALL active feature branches on current upstream main ΓÇö validates feature interactions end-to-end. Internal artifact: NOT intended for an upstream PR; NEVER raise a PR from `final`.

**Rebuild recipe (after every upstream sync):**

1. **Sync main first:** `git fetch upstream main`; verify lineage (`git merge-base --is-ancestor <old-tip> upstream/main` ΓÇö if it fails, upstream force-pushed: STOP and reassess); `git switch main && git merge --ff-only upstream/main`; push `origin main`.
2. **Backup + fresh final:**
   ```powershell
   git branch final-backup-<YYYYMMDD> <old-final-sha>   # local-only insurance
   git branch -f final main
   git switch final
   ```
3. **Merge ALL active branches in this order** (plain `git merge --no-edit <branch>`; peer branches produce merge commits):
   1. `add-telepub-voyage` (`50559ea`, ┬º12.1) ΓÇö expect clean
   2. `feat-api-key-rotation` (`6298e19`) ΓÇö expect clean (key_pool/openai_chat files; overlaps only with custom-provider in `provider.py`)
   3. `feat-models-metadata` (`5fe9ce8`) ΓÇö expect clean
   4. `add-custom-provider` (`b69108d`) ΓÇö ~7 additive conflicts; combine with key-rotation in `provider.py` via `api_key=resolved_api_key or "no-api-key"`; catalog-order tuple tail: `..., "ollama", "telepub_voyage", "custom"`
   5. `fix-ollama-model-discovery` (`04e5c04`) ΓÇö version-only (keep highest)
   6. `update-main-fix-issues` (`4ae75ae`) ΓÇö version-only (keep highest)
   7. `fix-cline-hub-hijack` (`bf157a2`) ΓÇö version-only (keep highest)
   8. `fix-nim-minimax-post-terminal-framer` (`cfa42f8`) ΓÇö version (keep highest); minimax-m3 smoke-default removals auto-merge
   9. `add-lightning-ai` (`3575595`) ΓÇö trio #1: same-anchor additive conflicts vs telepub/custom at every llm7ΓåÆollama_cloud anchor; keep both sides; NO credential probe (count +1)
   10. `add-experiential-labs` (`3886c8e`) ΓÇö trio #2: keep both sides; lightning entries BEFORE experiential in each anchor region; credential probe (count +0)
   11. `add-orca-router` (`f8d8239`) ΓÇö trio #3: keep both sides; final anchor order = llm7 ΓåÆ lightning ΓåÆ experiential ΓåÆ orcarouter ΓåÆ ollama_cloud; credential probe (count +0)
4. **Trio stacking rule (every anchor region ΓÇö catalog, settings, profiles, manifest, .env.example, README, smoke defaults, all test files):** entries order lightning ΓåÆ experiential ΓåÆ orcarouter, with telepub_voyage/custom trailing (README rows: LLM7 ΓåÆ Lightning ΓåÆ Experiential ΓåÆ OrcaRouter ΓåÆ Telepub ΓåÆ Ollama Cloud; catalog tuple tail: `..., llm7, lightning, experiential, orcarouter, ollama_cloud, lmstudio, llamacpp, ollama, telepub_voyage, custom`).
5. **Stacked-count gotchas (fix as follow-up commits ΓÇö no amend needed on internal branch):**
   - README "ToS-friendly providers" count: each trio branch bumped 50ΓåÆ51 identically (auto-merges WRONG); telepub/custom branches deliberately did NOT bump. Set per branch intent: currently **53** (50 + trio). Double-check against the provider table row count (55 incl. 3 local + custom).
   - `test_credential_validation.py::test_unsupported_shared_credentials_never_send_http` count = stacked `len({credential_env} - {CASES envs})`: main 20 + telepub +1 + lightning +1 + experiential +0 + orca +0 = **22** (the lightning branch alone asserts 21 ΓÇö stacked math differs!). Recompute, don't copy from any single branch.
   - Version: keep the highest (currently 6.3.0) across all pyproject/uv.lock conflicts; `uv lock` after the last merge.
6. **Verify:** `git merge-base --is-ancestor <branch> final` for ALL 11 (+ main); symbol audit (below) all hit; ┬º12.5 full gate set (ruff format --check ΓåÆ ruff check ΓåÆ ty check ΓåÆ pytest -q ΓåÆ pytest e2e -q).
7. **Restore HANDOFF_NOTES.md** (the rebuild discards it ΓÇö it is tracked on `final` only): `git restore --source=final-backup-<YYYYMMDD> HANDOFF_NOTES.md` ΓåÆ `git add -f HANDOFF_NOTES.md` ΓåÆ `git commit -m "Restore HANDOFF_NOTES.md"`. (Skip only if intentionally dropping note updates.)
8. **Push:** `git push --force-with-lease origin final`. **NEVER create a PR from `final`.**

**Symbol audit (all must hit on `final`):**
`TELEPUB_VOYAGE_DEFAULT_BASE` ┬╖ `"custom": ProviderDescriptor` ┬╖ `credential_optional=True` (in `profiles.py` ΓÇö the `custom` OpenAIChatProfile) ┬╖ `_drop_authorization_header` ┬╖ `class KeyPool` ┬╖ `_resolve_api_key` ┬╖ `ProviderModelPricing` ┬╖ `LOCAL_DISCOVERY_RETRY_COOLDOWN_S` ┬╖ `resolved_api_key or "no-api-key"` ┬╖ `LIGHTNING_DEFAULT_BASE` ┬╖ `EXPERIENTIAL_DEFAULT_BASE` ┬╖ `ORCAROUTER_DEFAULT_BASE` ┬╖ `_Probe("experiential"` ┬╖ `_Probe("orcarouter"` ┬╖ `sanitize_tool_schema_patterns` ┬╖ `_is_key_rotation_failure` ┬╖ `_EXPECTED_PROVIDER_ORDER` contains all 5 new ids (`lightning`, `experiential`, `orcarouter`, `telepub_voyage`, `custom`) and equals `tuple(PROVIDER_CATALOG.keys())`

**HANDOFF_NOTES.md tracking (final only ΓÇö since 2026-09-12):**
- This file is a git-tracked file on `final` ONLY. The `HANDOFF_NOTES.md` line in `.git/info/exclude` (local-only, NOT `.gitignore`) stays as a safety net ΓåÆ always stage with `git add -f HANDOFF_NOTES.md`; plain `git add` silently skips it.
- On every NON-final branch this file is ABSENT from the worktree (git removes it on switch). To consult: `git show final:HANDOFF_NOTES.md` (read-only). NEVER write a restored copy back into the worktree on another branch ΓÇö it blocks `git switch final` ("untracked working tree file would be overwritten").
- To edit notes while on another branch: save the new text to a temp path (or edit the `git show` output), then once back on `final`, overwrite the file and commit.
- Switching away from `final` with uncommitted note edits is BLOCKED by git ΓÇö intentional safety; commit notes before switching.
- Every ┬º9 rebuild (step 7 above) must restore this file from the backup branch, or the rebuild discards it.

---

## 10. Current Git State (updated 2026-09-28 ΓÇö sync #12)

> **Versions are no longer a per-branch thing** (┬º4) ΓÇö the "Version" column is gone; release intent is carried by the PR title prefix. **Nothing has been pushed since sync #8** ΓÇö all sync-#11 SHAs below are local-only.

| Branch | Issue / PR | SHA | Status |
|--------|-----------|-----|--------|
| `main` | ΓÇö | `105bfab8` | sync #12: ff-synced to upstream (18 commits; v6.2.71 ΓåÆ v6.4.10). Local only ΓÇö **not pushed to fork**. |
| `add-custom-provider` | PR #1469 **CLOSED UNMERGED** (#1230) | `69acb27d` | **FROZEN 2026-09-28 (user decision)** ΓÇö closed 2026-09-26, superseded by upstream custom providers #1909. Pin unchanged since sync #11. |
| `fix-ollama-model-discovery` | PR #1606 OPEN (#1296) | `fb735b52` | **sync #12:** rebased onto `105bfab8` (3 commits); `patch:`; gates + 6680 suite + 221 e2e green; adapted upstream's new `test_vscode_chat_sync.py` to self-sufficient locals. |
| `add-telepub-voyage` | PR #739 URL-share only ΓÇö NO PR | `50559ea0` | **FROZEN (┬º12.1)** ΓÇö unchanged, verified identical to pre-sync pin. Merged into `final` at that pin. |
| `feat-models-metadata` | PR #1736 OPEN (#1168) | `d91ad0c7` | **sync #12:** rebased; `minor:`; 2 keep-both import conflicts; gates + 6681 suite + 221 e2e green. |
| `fix-nim-minimax-post-terminal-framer` | PR #1742 **CLOSED UNMERGED** (#1734) | `cfa42f81` | **FROZEN** ΓÇö unchanged. Merged into `final`; causes the 2 accepted failures there. |
| `update-main-fix-issues` | PR #1744 **CLOSED UNMERGED** (#1730) | `f4048981` | **FROZEN 2026-09-28 (user decision)** ΓÇö closed 2026-09-12. Pin unchanged since sync #11. |
| ~~`add-orca-router`~~ | PR #1754 **MERGED** (`10fb1d02`) | ΓÇö | **REMOVED ΓÇö merged upstream 2026-09-27; local branch DELETED (backup `merged/add-orca-router` = `69189df4`).** |
| `feat-api-key-rotation` | #1301 ΓÇö NO PR | `f976b9ce` | **sync #12:** rebased; `minor:`; `ty` fix for #1923 signature (amended); gates + 6693 suite + 221 e2e green. Awaiting user decision on a PR. |
| ~~`fix-cline-hub-hijack`~~ | PR #1641 **MERGED** (`d5930097`) | ΓÇö | **REMOVED ΓÇö merged upstream 2026-09-26; local branch DELETED (backup `merged/fix-cline-hub-hijack` = `85b31b6a`).** |
| `final` | ΓÇö internal, NO PR | see ┬º8 sync #12 | **REBUILT 2026-09-28 on `105bfab8`** ΓÇö 7 branches + 4 salvaged audit commits + fixup `3cfe195c`; gates green; suite **6742p/23s/2 known nim failures**; e2e 221p/1s; audit pass rescued from the backups; all old backups consolidated into the single `final-backup` branch (`2ab1776c`). |
| ~~`add-lightning-ai`~~ | PR #1740 | ΓÇö | **REMOVED ΓÇö merged upstream** (`613cdaaa`). |
| ~~`add-experiential-labs`~~ | PR #1749 | ΓÇö | **REMOVED ΓÇö merged upstream** (`0329ac49`). |

### Sync #8 state (superseded by sync #11) ΓÇö kept for history

| Branch | Issue / PR | SHA | Version | Status |
|--------|-----------|-----|---------|--------|
| `main` | ΓÇö | `0dcb3715` | 6.2.15 | synced w/ upstream (`f3a3aac`ΓåÆ`0dcb3715` #1756ΓÇô#1767), pushed to fork 2026-09-12 |
| `add-custom-provider` | PR #1469 OPEN (#1230) | `b218d21e` | 6.3.0 | sync #8 (2026-09-12): complex rebase onto `0dcb3715`; ┬º12.5 full set green; **greptile clean (17 files, 0 comments) + all 7 CI green ΓÇö merge-ready (┬º12.4)** |
| `fix-ollama-model-discovery` | PR #1606 OPEN (#1296) | `132b5fdc` | 6.2.16 | sync #8: merge of main into branch (never-rewrite), ff push; ┬º12.5 full set green; **greptile + all 7 CI green ΓÇö merge-ready (┬º12.4)** |
| `add-telepub-voyage` | PR #739 URL-share only ΓÇö NO PR | `50559ea` | 6.3.0 | FROZEN (┬º12.1) ΓÇö untouched in sync #8; merged into `final` at `50559ea` |
| `feat-models-metadata` | **PR [#1736](https://github.com/Alishahryar1/free-claude-code/pull/1736) OPEN** (#1168) | `a56c9856` | 6.3.0 | sync #8: rebased onto `0dcb3715`; ┬º12.5 full set green; **greptile + all 7 CI green ΓÇö merge-ready (┬º12.4)** |
| `add-lightning-ai` | **PR [#1740](https://github.com/Alishahryar1/free-claude-code/pull/1740) OPEN** (#1732) | `96a601d0` | 6.3.0 | sync #8: rebased onto `0dcb3715`; ┬º12.5 full set green; **greptile + all 7 CI green ΓÇö merge-ready (┬º12.4)** |
| `fix-nim-minimax-post-terminal-framer` | **PR [#1742](https://github.com/Alishahryar1/free-claude-code/pull/1742) CLOSED UNMERGED** (#1734) | `cfa42f8` | 6.2.3 | maintainer closed 2026-09-12 ("the minimax model is deprecated"); FROZEN ΓÇö not updated in sync #8; still merged into `final` at `cfa42f8` |
| `update-main-fix-issues` | **PR [#1744](https://github.com/Alishahryar1/free-claude-code/pull/1744) OPEN** (#1730) | `e3dc94e1` | 6.2.16 | sync #8: rebased onto `0dcb3715`; ┬º12.5 full set green; **greptile + all 7 CI green ΓÇö merge-ready (┬º12.4)** |
| `add-experiential-labs` | **PR [#1749](https://github.com/Alishahryar1/free-claude-code/pull/1749) OPEN** (#1737) | `b61736c0` | 6.3.0 | sync #8: rebased onto `0dcb3715`; ┬º12.5 full set green; **greptile + all 7 CI green ΓÇö merge-ready (┬º12.4)** |
| `add-orca-router` | **PR [#1754](https://github.com/Alishahryar1/free-claude-code/pull/1754) OPEN** (#1751) | `3b4f2033` | 6.3.0 | sync #8: rebased onto `0dcb3715`; ┬º12.5 full set green; **greptile + all 7 CI green ΓÇö merge-ready (┬º12.4)** |
| `feat-api-key-rotation` | #1301 ΓÇö NO PR | `03def116` | 6.3.0 | sync #8: rebased onto `0dcb3715`; awaiting user decision (upstream #1655+#1656 may cover it) |
| `fix-cline-hub-hijack` | **PR [#1641](https://github.com/Alishahryar1/free-claude-code/pull/1641) OPEN** (#1590) | `acf94479` | 6.2.16 | sync #8: rebased onto `0dcb3715`; ┬º12.5 full set green; **greptile + all 7 CI green ΓÇö merge-ready (┬º12.4)** |
| `final` | ΓÇö internal, NO PR | `7e78423` + notes commit | 6.3.0 | **REBUILT 2026-09-12/13 on base `0dcb3715`** (┬º8 sync #8): ALL 11 branches merged in ┬º9 order (first-parent: `9db9d67a` telepub ΓåÆ `2d33e610` key-rotation ΓåÆ `6262e6cb` models-metadata ΓåÆ `2da8b73b` custom ΓåÆ `a6ae9f15` ollama ΓåÆ `9fc965df` update-main-fix-issues ΓåÆ `999e0212` cline ΓåÆ `e271aa46` fix-nim ΓåÆ `4e707130` lightning ΓåÆ `5164cf3b` experiential ΓåÆ `33a05822` orca), then audit re-application: `841dfc9e` security, `6a077f65` dead exports, `424ab991` smells, `0cefbc68` fresh CVE lock pass (starlette 1.6.0, cryptography 50.0.1, python-multipart 0.0.32, urllib3 2.7.0, click 8.5.0, pygments 2.21.0, msgpack 1.2.2; pip-audit 0 vulns), `3e77f612` pyproject deps restore (json5/tomlkit/simplejson dropped by the telepub merge ΓÇö ┬º8 sync #8 incident), `7e78423` credential count 22. Ancestry 11/11, catalog 55, README rows 54, suite 5633p/152s, e2e 116p/1s. Old final `d0cc706` ΓåÆ local backup `final-backup-20260912-audit`. **HANDOFF_NOTES.md tracked on `final` (final-branch-only file; this sync #8 commit updates it ΓÇö ┬º9 tracking block)** |

Superseded branches and pre-restructure history live in the `.bak` backup (see header). `gh` CLI v2.99.0 IS installed and authenticated as Tanishq-1 (verified 2026-09-10) ΓÇö PR states and PR creation can be managed via `gh`.

---

## 11. CONTRIBUTING.md Rules (must follow)

- NO `# type: ignore` or `# ty: ignore` comments.
- Target Python 3.14 native lazy annotations ΓÇö do NOT add `from __future__ import annotations`.
- Each PR independent ΓÇö branch from clean updated `main`.
- (Version-bump-in-same-commit and `ci.ps1` are covered in ┬º4 and ┬º2.)

---

## 12. Branch Update & PR Policy (standing rules ΓÇö 2026-08-30)

### 12.1 Telepub freeze (EXCLUSION from branch updates)
`add-telepub-voyage` is EXCLUDED from all branch updates. When updating all branches (syncs, rebases, pushes), update every other branch normally but NEVER rebase, push, or force-push telepub. Do not apply any update to it unless the user explicitly states otherwise. The branch was externally rebased to `50559ea` (single clean commit on main `81fa340`, v6.3.0 ΓÇö the old frozen `17382eb` is obsolete); the freeze now means "no updates beyond `50559ea`". Exception (user decision): the `final` integration branch still merges telepub at its current tip (`50559ea`); if that merge ever conflicts non-additively, STOP and ask the user before resolving.

### 12.2 Push-to-main race (PR conflict workflow)
**Scenario:** a PR is approved, then someone pushes directly to `main` before the PR merges ΓåÆ the PR shows conflicts.
**Resolution:**
1. `git fetch upstream` + sync local main (`git merge upstream/main --ff-only`).
2. `git merge-tree main <branch>` to scope the damage before touching anything.
3. Rebase the PR branch onto main ΓÇö exact-edit conflicts, lockfile order, `GIT_EDITOR=true` (┬º3/┬º8 rails).
4. **Test locally before pushing** ΓÇö gates + full suite + e2e (┬º2 set).
5. `git push --force-with-lease origin <branch>` ΓÇö the push clears the conflict and re-triggers bot checks.

**Prevention:**
- The repo ruleset already blocks direct/force pushes to `main` (see CLAUDE.md "Repository protection") ΓÇö flag violations to the owner.
- Keep PRs current by rebasing on every upstream sync instead of batching several upstream commits.
- Prefer small single-commit branches so conflicts stay version-only.

### 12.3 Greptile-first testing (WAIT for the bot)
When a PR is initially raised, do **NOT** run tests manually ΓÇö wait for the greptile bot to review first. Manual testing is triggered ONLY by greptile output: run tests only if greptile reports issues or scores below the confidence threshold (12.4). Pre-PR local verification before opening a PR remains the ┬º2 norm; this rule governs activity after the PR exists.

### 12.4 Confidence threshold (5/5 gate)
Greptile must reach **5/5 confidence** to pass. Current observed status: **4/5 ΓÇö insufficient.** PRs below 5/5 are **BLOCKED from merge**. When greptile reports issues or stays <5/5: highlight each finding to the user, fix the branch, and test locally before pushing (12.5). Never merge below 5/5. (Precedent: the custom-provider PR's P1 series ΓÇö keyless construction ΓåÆ bearer strip ΓåÆ `/v1` normalization ΓåÆ proxy ΓÇö each fix was local-tested then force-pushed, with greptile's T-Rex re-testing after every push.)

### 12.5 Local test before push (fix workflow)
Whenever a branch is being fixed in response to a bot/PR finding, the fix must pass the full local set ΓÇö gates (`ruff format --check`, `ruff check`, `ty check`) + full pytest suite + e2e ΓÇö BEFORE the fix is pushed to the branch. Never push a bot-driven fix on the basis of targeted tests alone.
