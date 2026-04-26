# Contracts

Status: canonical

This directory captures durable product and runtime contracts for AMOF.

Terminology guardrail for new contract work:

- keep the canonical product/system name as `AMOF`
- for new inference-boundary docs and contracts, prefer `IAL` (`Inference Authority Layer`)
- do not rename working runtime paths or historical records just to force terminology alignment

Each contract should answer:

1. What is the single source of truth?
2. What drift exists today?
3. What behavior is expected?
4. What acceptance checks prove it?

Consolidation guardrails promoted from Waves 1-2:

- prefer one explicit AMOF core edit path under `repos/*`; do not let `.amof-worktrees/*` become the hidden default for AMOF core work
- preserve first, then clean; archive old journals before removing anything from active surfaces
- treat raw journals as evidence and `docs/*` / contracts as distilled truth; do not keep important lessons trapped only in raw journal files
- do not assume unmatched untracked journals are garbage; first decide whether they are canonical new evidence, archive candidates, or unknown material that must be preserved
- treat release/version truth as one contract across tags, version files, release status, runtime claims, and docs
- treat placeholder or stale operator docs as real drift, not harmless polish debt, when they affect clone URLs, path guidance, repo roles, or live hostnames

Current contract set:

- `backlog.md`
- `demo-microsaas-flow.md`
- `environments-error-ui.md`
- `arena-threading-and-reportback.md`
- `run-logs-and-sidebar-events.md`
- `runtime-profile-workspace-shape.md`
- `platform-dashboard-auth-env.md`
- `plan-execute-runner-bootstrap.md`
- `plan-execute-budget-parity.md`
- `worker-no-progress-retry-stop.md`
- `scratch-artifact-pending-review.md`
- `planner-repo-path-grounding.md`
- `planner-file-entrypoint-grounding.md`
- `planner-visible-text-grounding.md`
- `orchestrator-run-progress-surface.md`
- `prod-dev-orchestrator-runtime-freshness.md`
- `worker-directory-contract-grounding.md`
- `release-ui-queue-state-surface.md`
- `release-builds-live-status-parity.md`
- `release-build-run-summary-query.md`
- `run-persistence-observability.md`
- `tools-page-shell.md`
- `mcp-chat-e2e.md`
- `director-demo-prompt.md`
- `director-delivery-contract.md`
- `director-gmd-dev-local-proof-action.md`
- `inference-authority-layer.md`
- `consolidation-wave-1-topology-freeze.md`
- `consolidation-wave-2-journal-archive-reconciliation.md`
- `consolidation-wave-3-learnings-and-doc-promotion.md`
- `consolidation-wave-4-runtime-bearing-surface-review.md`
- `consolidation-wave-5-repo-and-release-reconciliation.md`
- `consolidation-wave-6-dev-derivation-and-validation.md`
- `ultra-plan-3-history-retention.md`
- `opensandbox-first-boundary.md`
- `operational-memory-convergence-program.md`
