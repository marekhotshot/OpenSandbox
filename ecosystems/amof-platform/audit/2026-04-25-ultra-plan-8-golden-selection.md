# Ultra Plan 8 Golden Ecosystem Selection

Date: 2026-04-25

## Verdict

`gmd` remains the correct golden ecosystem for Ultra Plan 8, with one
important qualification: it is ready as the source and GitOps baseline,
but live delivery is blocked until Argo CD runtime access and a gmd live
URL/DNS contract are available.

## Matrix

| Ecosystem | Repo completeness | Infra chaos | Live proof chance | Reusable pattern | Reset risk | Decision |
|---|---:|---:|---:|---:|---:|---|
| `gmd` | high after sync | medium | blocked by Argo/DNS runtime | high | low | first target |
| `amof-platform` | high | high | high for control-plane proof | medium | high | delivery plane, not first target |
| `hotshot` | missing checkout | medium | medium | medium | medium-high | rollout after golden proof |
| `demo-microsaas` | missing local seed repos | high | low | low | high | retired recovery-only |

## Why `gmd`

`gmd` is the only current downstream ecosystem that is explicitly
documented as the canonical example app ecosystem. It has a single app
repo, a concrete GitOps layout, and a direct mapping to the universal
Argo CD pattern through `gmd-dev`, `gmd-test`, and `gmd-prod`.

`amof-platform` must remain the delivery plane under test. Using it as
the first downstream proof would conflate AMOF bootstrap, AMOF runtime,
and AMOF delivery.

`demo-microsaas` is retired and must not be extended as a reference
shape. `hotshot` is real product surface with protected `.env` and local
commentary data, so it is better as a second rollout target after the
pattern is proved.

## Current Proof State

Completed:

- `repos/gmd-app` cloned from `https://github.com/marekhotshot/google-microservices-demo.git`.
- `repos/gmd-app` is clean on `main` at `c9857ee54fba10486013f15ba6b31411986f530c`.
- `python3 scripts/amof.py -e gmd manifest validate --strict` passes.
- `helm lint infrastructure/gitops/gmd/chart` passes.
- `helm template gmd-dev infrastructure/gitops/gmd/chart -n gmd-dev` renders 1200 lines.

Blocked:

- Active Kubernetes context is local `k3d-amof`; it has no Argo CD
  `ApplicationSet` or `Application` CRDs.
- Cloud-dev kubeconfig file exists but exposes no usable contexts.
- No gmd public hostname, Cloudflare record, ingress, or live URL was
  proved.
- AMOF's non-demo lifecycle deploy command is still AMOF-stack-oriented,
  so a gmd Argo registration/readback path must be explicit before this
  becomes a primary delivery flow.
