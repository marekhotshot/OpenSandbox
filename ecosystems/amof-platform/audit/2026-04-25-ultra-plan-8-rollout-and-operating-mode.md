# Ultra Plan 8 Rollout And Operating Mode Record

Date: 2026-04-25

## Wave 4 Supporting Hardening

Only blockers directly preventing the `gmd` golden flow were handled or
classified.

Handled in this slice:

- `gmd` source repo presence: `repos/gmd-app` was cloned and verified
  clean on `main`.
- Generated sync residue: `repos/gmd-app/.amof/profile.md` was removed.
- Director contract: input and result schemas were added under
  `contracts/`, with an executable `gmd` example recorded in audit.
- Golden run result: the blocked result envelope records stage, owner,
  retryability, receipts, and next action.

Not implemented because they require runtime/operator prerequisites:

- Argo CD CRDs are missing from the active local cluster.
- The cloud-dev kubeconfig file has no usable contexts.
- No `gmd` public hostname, ingress, Cloudflare record, or live URL
  receipt exists yet.
- AMOF's current non-demo lifecycle deploy path still targets the AMOF
  stack rather than a first-class `gmd` Argo delivery path.

Excluded as unrelated polish:

- broad UI cleanup
- retired `demo-microsaas` extension
- all-ecosystem reset
- release/version cleanup beyond recording current status
- realtime/run-chat redesign

## Wave 5 Rollout Matrix

| Ecosystem | Classification | Rollout order | Rationale |
|---|---|---:|---|
| `gmd` | golden baseline | 1 | Canonical app ecosystem, one repo, concrete GitOps layout, lowest downstream ambiguity |
| `hotshot` | same pattern with minor overrides | 2 | Real product surface, but needs explicit protection for `server/.env` and commentary data before reset/deploy |
| `amof-platform` | special snowflake | 3 | AMOF is the delivery plane itself; self-delivery comes after downstream proof |
| `demo-microsaas` | retired recovery-only | excluded | Manifest is retired and uses local seed repo paths; must not become the reference path |

Rollout rule:

The program must not start `hotshot` or AMOF self-delivery until the
`gmd` result changes from `blocked` to `pass`.

## Wave 6 Operating-Mode Switch

Primary delivery does not move into AMOF yet.

Current decision: `no-go`.

Reasons:

- The `gmd` golden proof is blocked at deploy/readback.
- Argo CD runtime truth is not available from the active context.
- DNS/live URL truth for `gmd` is not defined or proved.
- AMOF does not yet expose a first-class `gmd` Argo delivery/readback
  path with receipts.

Switch criteria that remain:

- `UP8-GOLDEN-GMD-001` returns a `pass` result envelope.
- Build, deploy, DNS/live, release, promote, and readback receipts are
  visible as AMOF evidence.
- Reset-safety decisions are recorded before any hard reset.
- At least one post-golden target is ready with known overrides.
- Failed delivery runs produce structured failure envelopes without
  transcript archaeology.

What remains in Cursor until the switch:

- bootstrap and emergency repair
- focused code edits opened by AMOF tickets/runs
- runtime debugging when AMOF evidence identifies the failing stage
- architectural review and operator approval

Cursor must not be treated as the long-term primary coordinator for the
build, deploy, DNS, release, promote, and readback chain.
