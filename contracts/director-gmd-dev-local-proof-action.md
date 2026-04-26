# Director GMD Dev Local Proof Action

Status: canonical
Date: 2026-04-25

## Action Name

`director.gmd_dev_local_proof.v1`

CLI surface:

```bash
python3 scripts/amof.py -e gmd director-action gmd-dev-local-proof --input <contract.json>
```

Control API surface:

```text
POST /api/v1/control/ecosystems/gmd/actions/director/gmd-dev-local-proof
```

The API surface enqueues the CLI action as a tracked AMOF run with
action `director-action/gmd-dev-local-proof`.

## Scope

This action is explicitly:

- `gmd` only
- `dev` only
- local `k3d-amof` only
- Argo CD Application `gmd-dev` only
- ClusterIP frontend readback through local port-forward only

It does not create or modify cloud-dev, public DNS, test, prod, release,
promote, or UI surfaces.

## Input Contract

Required fields:

- `action`: must be `director.gmd_dev_local_proof.v1`
- `ecosystem`: must be `gmd`
- `ticket_id`
- `goal`
- `scope.repos`: must be exactly `["gmd-app"]`
- `constraints`
- `target_environment`: must be `dev`
- `build_mode`
- `deploy_mode`
- `release_intent.type`: must be `none`
- `acceptance_criteria`
- `readback.local_port`
- `artifacts.result_path`

## Result Contract

The action writes a JSON result with:

- `final_status`: `pass` or `blocked`
- `action`
- `ticket_id`
- `target_environment`
- `preflights`
- `substrate_verification`
- `deploy_result`
- `readback_result`
- `release_promote_attempted`
- `blocker`
- `failure_classification`
- `evidence`
- `acceptance_criteria_results`

## Preflight Gates

The action fails before execution when:

- `.amof/runs` is not writable
- required SDKs (`openai`, `anthropic`) are unavailable
- model ladder/provider config cannot resolve the configured provider path
- current Kubernetes context is not `k3d-amof`
- local readback port is already in use
- Argo CD ApplicationSet `gmd-environments` is missing or not dev-only
- Argo CD Application `gmd-dev` is missing, unhealthy, or unsynced
- `gmd-dev` namespace/frontend service/workload pods are missing or not ready

## Deferred Scope

- cloud-dev proof
- public DNS / Cloudflare proof
- test/prod rollout
- release/promote
- UI improvements
