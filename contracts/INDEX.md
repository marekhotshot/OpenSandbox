# Contracts Index

Status: canonical
Convention: each contract under `contracts/` carries a top-of-file `Status:` line.
Source: `contracts/operational-memory-convergence-program.md` §3.2

Status values used here: `canonical`, `wave`, `reservoir`, `placeholder`, `noise`.

## Canonical

- [README.md](README.md)
- [backlog.md](backlog.md)
- [operational-memory-convergence-program.md](operational-memory-convergence-program.md)

### Inference and authority
- [inference-authority-layer.md](inference-authority-layer.md)
- [control-plane-agent-settings-parity.md](control-plane-agent-settings-parity.md)
- [runpod-heavy-lane-profile.md](runpod-heavy-lane-profile.md)

### Orchestrator runtime, runs, and persistence
- [orchestrator-run-progress-surface.md](orchestrator-run-progress-surface.md)
- [run-persistence-observability.md](run-persistence-observability.md)
- [run-logs-and-sidebar-events.md](run-logs-and-sidebar-events.md)
- [runtime-profile-workspace-shape.md](runtime-profile-workspace-shape.md)
- [runtime-idle-merkle-roots.md](runtime-idle-merkle-roots.md)
- [prod-dev-orchestrator-runtime-freshness.md](prod-dev-orchestrator-runtime-freshness.md)
- [amof-debug-live-controlplane-access.md](amof-debug-live-controlplane-access.md)

### Plan, execute, planner, worker
- [plan-execute-runner-bootstrap.md](plan-execute-runner-bootstrap.md)
- [plan-execute-budget-parity.md](plan-execute-budget-parity.md)
- [planner-repo-path-grounding.md](planner-repo-path-grounding.md)
- [planner-file-entrypoint-grounding.md](planner-file-entrypoint-grounding.md)
- [planner-visible-text-grounding.md](planner-visible-text-grounding.md)
- [worker-directory-contract-grounding.md](worker-directory-contract-grounding.md)
- [worker-no-progress-retry-stop.md](worker-no-progress-retry-stop.md)
- [scratch-artifact-pending-review.md](scratch-artifact-pending-review.md)

### Arena, MCP, screens, environments
- [arena-threading-and-reportback.md](arena-threading-and-reportback.md)
- [mcp-chat-e2e.md](mcp-chat-e2e.md)
- [screen-v1-operator-environment.md](screen-v1-operator-environment.md)
- [environments-error-ui.md](environments-error-ui.md)
- [platform-dashboard-auth-env.md](platform-dashboard-auth-env.md)
- [tools-page-shell.md](tools-page-shell.md)

### Release
- [release-builds-live-status-parity.md](release-builds-live-status-parity.md)
- [release-build-run-summary-query.md](release-build-run-summary-query.md)
- [release-ui-queue-state-surface.md](release-ui-queue-state-surface.md)
- [release-runtime-validation-gate.md](release-runtime-validation-gate.md)

### Build (generated lane)
- [generated-build-contract.md](generated-build-contract.md)
- [generated-build-contract.schema.json](generated-build-contract.schema.json)
- [generated-build-runtime-detector-matrix.md](generated-build-runtime-detector-matrix.md)
- [generated-build-admission-policy.md](generated-build-admission-policy.md)
- [generated-build-admission-policy.schema.json](generated-build-admission-policy.schema.json)
- [generated-build-candidate-write-contract.md](generated-build-candidate-write-contract.md)
- [generated-build-candidate-write-backend-boundary.md](generated-build-candidate-write-backend-boundary.md)
- [generated-build-candidate-promotion-operator-ui.md](generated-build-candidate-promotion-operator-ui.md)
- [generated-build-release-admission-preview.md](generated-build-release-admission-preview.md)
- [generated-build-release-admission-preview.schema.json](generated-build-release-admission-preview.schema.json)
- [generated-build-candidate-write-request.schema.json](generated-build-candidate-write-request.schema.json)
- [generated-build-candidate-write-result.schema.json](generated-build-candidate-write-result.schema.json)
- [examples/generated-build-contract-python-fastapi.example.json](examples/generated-build-contract-python-fastapi.example.json)
- [examples/generated-build-contract-node-express.example.json](examples/generated-build-contract-node-express.example.json)
- [examples/generated-build-contract-go-stdlib.example.json](examples/generated-build-contract-go-stdlib.example.json)
- [examples/generated-build-contract-polyglot-refused.example.json](examples/generated-build-contract-polyglot-refused.example.json)
- [examples/generated-build-admission-candidate-only.example.json](examples/generated-build-admission-candidate-only.example.json)
- [examples/generated-build-admission-existing-build-refused.example.json](examples/generated-build-admission-existing-build-refused.example.json)
- [examples/generated-build-admission-deploy-admitted.example.json](examples/generated-build-admission-deploy-admitted.example.json)
- [examples/generated-build-candidate-write-request.example.json](examples/generated-build-candidate-write-request.example.json)
- [examples/generated-build-candidate-write-result.example.json](examples/generated-build-candidate-write-result.example.json)
- [examples/generated-build-candidate-write-refused.example.json](examples/generated-build-candidate-write-refused.example.json)
- [examples/generated-build-release-admission-candidate-only.example.json](examples/generated-build-release-admission-candidate-only.example.json)
- [examples/generated-build-release-admission-preview-admitted.example.json](examples/generated-build-release-admission-preview-admitted.example.json)
- [examples/generated-build-release-admission-refused.example.json](examples/generated-build-release-admission-refused.example.json)

### Boundary
- [opensandbox-first-boundary.md](opensandbox-first-boundary.md)

## Wave (consolidation, in-flight)

- [consolidation-wave-1-topology-freeze.md](consolidation-wave-1-topology-freeze.md)
- [consolidation-wave-2-journal-archive-reconciliation.md](consolidation-wave-2-journal-archive-reconciliation.md)
- [consolidation-wave-3-learnings-and-doc-promotion.md](consolidation-wave-3-learnings-and-doc-promotion.md)
- [consolidation-wave-4-runtime-bearing-surface-review.md](consolidation-wave-4-runtime-bearing-surface-review.md)
- [consolidation-wave-5-repo-and-release-reconciliation.md](consolidation-wave-5-repo-and-release-reconciliation.md)
- [consolidation-wave-6-dev-derivation-and-validation.md](consolidation-wave-6-dev-derivation-and-validation.md)

## Reservoir (preserved, do not act on)

- [clean-start-target-topology.md](clean-start-target-topology.md) — superseded by current topology in `docs/status/amof-master-status.md`
- [demo-microsaas-flow.md](demo-microsaas-flow.md) — original "Status: SUPERSEDED" already in body
- [director-demo-prompt.md](director-demo-prompt.md) — demo-era prompt
- [uc-amov-dev-rollout-foundation.md](uc-amov-dev-rollout-foundation.md) — superseded by `uc-amof.hotshot.sk` rollout in `docs/status/amof-master-status.md`
- [ultra-plan-3-history-retention.md](ultra-plan-3-history-retention.md) — older retention groundwork

## Placeholder

(none)

## Noise

(none)
