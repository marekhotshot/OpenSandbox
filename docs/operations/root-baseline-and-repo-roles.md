# Root Baseline And Repo Roles

Status: canonical
Date: 2026-04-26

## Operational Rule

Root `origin/main` is the only valid root workspace baseline.

`main-helper` is a retired legacy cleanup branch. It MUST NOT be used
to start new work, derive new AMOF platform changes, or decide runtime
truth.

The root workspace is a wrapper/config/audit/orchestration shell. It
is not product implementation truth.

## Repo Role Classification

| Surface | Role | Current truth |
|---|---|---|
| root workspace `/home/hotshot/work/amof-platform` | `wrapper_config_audit_shell` | Holds workspace config, wrappers, contracts, audit receipts, and ignored external repo checkouts. Not product implementation truth. |
| `repos/amof` | `canonical_active` | Canonical AMOF backend/CLI/runtime source. Runtime imports must resolve here. |
| `repos/amof-ui` | `canonical_active` | Canonical AMOF Control Center frontend source. |
| `repos/gmd-app` | `active_supporting` | Active supporting ecosystem app/source truth for the current `gmd` golden-flow/generated-build work. Not AMOF platform implementation. |
| `repos/opensandbox` | `inactive_member` | This path resolves to the root workspace checkout. It is an ecosystem member, but it is not in the current AMOF execution path and is not canonical implementation truth. |
| `_lanes/*` | `historical_reference` | Historical/recovery reference material only. Do not run or import directly. |
| `.amof-worktrees/*` | `historical_reference` unless an explicit active ticket targets it | Managed worktree area. With `active_ticket: null`, no worktree here is active. |

## Baseline Rule For Future Work

1. AMOF backend/CLI/runtime changes go to `repos/amof`.
2. AMOF UI changes go to `repos/amof-ui`.
3. Root changes are limited to wrapper/config/audit/orchestration shell.
4. `main-helper` is not a valid baseline for new work.
5. If root work is needed, branch from clean root `origin/main` or a
   clean published UP10 branch, not from `main-helper`.

## Why Not OpenSandbox As Execution Truth?

The root Git remote is `OpenSandbox`, and `.amof/state.json` lists
`repos/opensandbox` as a workspace member. In this checkout, however,
`repos/opensandbox` resolves to the root repository itself, and current
runtime/import surfaces resolve to `repos/amof` and `repos/amof-ui`.

Therefore OpenSandbox/root is an orchestration shell and ecosystem
member, not canonical AMOF execution truth.

## Published Clean Branches From UP10

The root `main-helper` branch has known secret-scanning ancestry and
was not used for publication. Clean branches were published from clean
OpenSandbox ancestry:

- `feat/UP10-root-wrapper-guardrails`
- `feat/UP10-visible-dirty-state-classification-v2`
- `feat/UP10-root-contracts-audit-batch`
- `feat/UP10-root-implementation-dirt-archive`

These should be merged or superseded into root `origin/main`; then
`main-helper` can be deleted locally and ignored as historical.

## Acceptance Checks

- `amof doctor` reports canonical AMOF import source under
  `repos/amof/scripts/amof`.
- `repos/amof-ui` is clean on `main`.
- root workspace is clean or has only explicitly scoped wrapper/config/audit
  changes.
- no task starts from `main-helper`.
