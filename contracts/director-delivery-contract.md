# Director Delivery Contract

Status: canonical
Date: 2026-04-25

## Source Of Truth

Director delivery runs use one structured input envelope and one
structured result envelope. The contract is execution-oriented: it
names the ecosystem, ticket, target environment, delivery modes,
constraints, and acceptance criteria before work starts.

This contract is the Ultra Plan 8 minimum needed to make AMOF the
primary delivery plane without turning delivery into an open-ended chat
session.

## Input Envelope

The input envelope must include:

- `ecosystem`
- `ticket_id`
- `goal`
- `scope`
- `constraints`
- `target_environment`
- `build_mode`
- `deploy_mode`
- `release_intent`
- `acceptance_criteria`

Validation rules:

- `ecosystem`, `ticket_id`, `goal`, `target_environment`,
  `build_mode`, and `deploy_mode` must be non-empty strings.
- `scope.repos` must name at least one repo.
- `scope.allowed_paths` must be non-empty.
- `constraints` and `acceptance_criteria` must be non-empty arrays.
- `release_intent.type` must be explicit, even when the intent is
  `none`.
- Director must persist the exact accepted input before execution.

## Result Envelope

The result envelope must include:

- `status`
- `ecosystem`
- `ticket_id`
- `run_id`
- `stage`
- `changed_refs`
- `artifacts`
- `receipts`
- `failures`
- `next_action`

Validation rules:

- `status` is one of `pass`, `fail`, or `blocked`.
- `stage` names the last completed or failed delivery stage.
- `failures[]` entries must include `code`, `message`, `retryable`,
  and `owner`.
- `owner` is one of `director`, `operator`, or `external`.
- Director must stop before release or promotion when build, deploy,
  DNS/live verification, or final readback fails.

## Failure Semantics

- `pass`: every acceptance criterion passed and receipts are attached.
- `fail`: the contract was executable, but one or more acceptance
  criteria failed.
- `blocked`: execution cannot continue because a prerequisite is
  missing or outside AMOF's current control, such as missing kubeconfig,
  missing Argo CD CRDs, missing DNS credentials, or a disabled build
  backend.

## Acceptance Checks

A delivery run is acceptable only when the result carries receipts for:

- fresh baseline
- ticket creation or explicit ticket-bound execution
- build evidence with source refs
- deploy evidence
- DNS/live URL evidence
- release bump or explicit release no-op
- promotion or explicit promotion no-op
- final readback

## Ultra Plan 8 Initial Example

```json
{
  "ecosystem": "gmd",
  "ticket_id": "UP8-GOLDEN-GMD-001",
  "goal": "Prove one clean end-to-end AMOF delivery baseline for gmd dev.",
  "scope": {
    "repos": ["gmd-app"],
    "allowed_paths": [
      "repos/gmd-app/**",
      "infrastructure/gitops/gmd/**",
      "ecosystems/gmd/**"
    ],
    "blocked_paths": ["**/.git/**", "**/.env", "**/node_modules/**"]
  },
  "constraints": [
    "no broad cleanup",
    "no retired demo-microsaas extension",
    "ticket worktrees are execution lanes, not delivery truth",
    "Cursor remains bootstrap/debug plane"
  ],
  "target_environment": "dev",
  "build_mode": "commit_detached",
  "deploy_mode": "argocd_application",
  "release_intent": {
    "type": "patch_alpha_then_promote",
    "component": "amof-delivery-plane"
  },
  "acceptance_criteria": [
    "fresh baseline captured",
    "ticket created and bound to gmd dev",
    "build uses explicit source commit evidence",
    "Argo application is synced and healthy",
    "Cloudflare/DNS and live URL checks pass",
    "release bump and promotion receipts exist",
    "final readback matches runtime truth"
  ]
}
```
