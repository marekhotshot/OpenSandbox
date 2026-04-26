# Generated Build Admission Policy

Status: canonical
Date: 2026-04-26

## Source Of Truth

The generated-build proof ladder and the generated-build admission
state are separate axes.

The proof ladder (`proposed`, `build_proven`, `runtime_proven`,
`refused`) answers:

> What evidence has AMOF observed about this generated artifact?

The admission state (`evidence_only`, `candidate_only`,
`deploy_admitted`, `refused`) answers:

> How far may AMOF use this artifact in build/deploy workflows?

Runtime proof is necessary for admission, but it is not sufficient for
deployment. A `runtime_proven` generated artifact is still
`evidence_only` until an explicit admission policy result says
otherwise.

## Status Model

### Evidence-only artifact

An artifact is **evidence-only** when it exists only as proof material.
It may be listed, inspected, audited, compared, and manually reviewed.
It MUST NOT be used as a build contract candidate and MUST NOT be
used by deploy/release flows.

Valid proof statuses:

- `refused`
- `proposed`
- `build_proven`
- `runtime_proven`

`runtime_proven + evidence_only` is valid and is the default state
for generated-build artifacts.

### Candidate artifact

An artifact is **candidate-only** when it is eligible for human review
as a possible generated build contract, but still not admitted to
deploy/release. Candidate status means:

- AMOF may present it as a candidate generated build contract.
- AMOF may ask an operator to accept/decline it.
- AMOF MUST NOT use it as the source image contract for deployment.

Valid proof statuses:

- `runtime_proven` only.

Invalid:

- `proposed + candidate_only`
- `build_proven + candidate_only`
- `refused + candidate_only`

### Deploy-admitted artifact

An artifact is **deploy-admitted** when policy says it may serve as
the generated-build contract used by deployment/release flows. This
still does not mean production-ready. It means the generated artifact
is admitted as a build contract source.

Valid proof statuses:

- `runtime_proven` only.

Deploy-admitted requires stricter checks than candidate-only, including
operator confirmation and conflict resolution against the existing
build lane.

### Refused admission result

An admission policy result can be `refused` even when the artifact's
proof status is `runtime_proven`. Refusal says the artifact is good
evidence but not acceptable as a candidate/deploy contract under the
current policy.

## Candidate Criteria

To become `candidate_only`, a generated artifact MUST satisfy all of:

1. Artifact validates against `generated-build-contract.schema.json`.
2. `artifact.build_contract_kind == "generated"`.
3. `artifact.status == "runtime_proven"`.
4. `artifact.confidence == "accepted"`.
5. `artifact.runtime_family` is in the implemented first-wave family
   set (`python`, `node`, `go`) or a later explicitly implemented set.
6. `artifact.dockerfile_template.id` is present and the template id is
   one of the active generated-build templates.
7. `artifact.dockerfile_template.rendered_path` exists and points
   under `.amof/generated-builds/...` or another deterministic local
   generated-build path.
8. `artifact.image_outputs` contains at least one concrete image output
   whose values are not placeholders.
9. `artifact.build_proof.image_digest` is present and is a valid
   `sha256:<64 hex>` digest.
10. `artifact.runtime_proof.liveness_signal` is present.
11. Existing-build lane precedence has been evaluated and did not
    reject the generated lane (see below).
12. No risk flag is in the hard-block list.

Candidate does not require operator confirmation. It is still
read-only and non-deploy-admitted.

Candidate admission reasons SHOULD include:

- `runtime_proven`
- `template_rendered`
- `image_digest_recorded`
- `first_wave_runtime_family`
- `no_existing_build_contract_conflict`

## Deploy-Admitted Criteria

To become `deploy_admitted`, a generated artifact MUST satisfy all
candidate criteria plus all of:

1. Explicit operator confirmation exists and names the artifact digest.
2. The operator confirmation records the target ecosystem/service.
3. The artifact image output has a deploy-pullable image reference for
   the target substrate.
4. Existing-build precedence is resolved to one of:
   - no existing-build contract present; or
   - existing-build contract explicitly rejected/retired by policy and
     operator confirmation.
5. The generated Dockerfile path and artifact path are persisted in
   the local generated-build store index.
6. The generated artifact was produced from the current intended source
   repo/ref, or the operator explicitly accepted the source ref.
7. The artifact has no blocking risk flags.

Deploy-admitted admission reasons SHOULD include:

- all candidate reasons
- `operator_confirmed`
- `deploy_pull_reference_present`
- `source_ref_confirmed`
- `existing_build_precedence_resolved`

## What Runtime-Proven Still Does NOT Guarantee

`runtime_proven` only means:

- the image starts locally;
- the inferred entrypoint did not immediately crash;
- a bounded liveness signal was observed (`port_open`,
  `healthcheck_ok`, or `log_pattern_seen`).

It does NOT guarantee:

- production readiness;
- database/storage correctness;
- security posture;
- performance;
- Kubernetes compatibility;
- release readiness;
- deploy admission;
- rollback safety;
- chart/manifest correctness.

## Refusal Reasons

Admission policy MUST refuse when any of these are true:

- `artifact_status_below_runtime_proven`
- `artifact_schema_invalid`
- `build_contract_kind_not_generated`
- `confidence_not_accepted`
- `runtime_family_not_admission_enabled`
- `dockerfile_template_missing_or_unknown`
- `rendered_path_missing`
- `image_output_missing_or_placeholder`
- `build_digest_missing_or_invalid`
- `runtime_proof_missing`
- `runtime_liveness_signal_not_accepted`
- `existing_build_contract_present`
- `existing_build_contract_conflict_unresolved`
- `operator_confirmation_missing`
- `operator_confirmation_digest_mismatch`
- `deploy_pull_reference_missing`
- `source_ref_unconfirmed`
- `blocking_risk_flag_present`

Refusals MUST include `missing_prerequisites` and
`refusal_conditions` so operators see what is needed to advance.

## Existing-Build vs Generated-Build Precedence

Existing-build contracts have precedence by default.

If a trustworthy existing-build contract is present, generated-build
admission MUST refuse with:

```text
precedence_decision: existing_build_wins
refusal_conditions: ["existing_build_contract_present"]
```

This remains true even if a generated artifact exists and is
`runtime_proven`. The generated artifact stays evidence-only unless
the operator explicitly retires/rejects the existing build contract
under a separate policy.

### Operator requested generated lane anyway

If an operator explicitly requests the generated lane when an
existing-build contract is present, AMOF MUST surface the conflict:

- existing contract path/reference;
- generated artifact path/reference;
- why existing wins by default;
- what separate action is required to override or retire existing.

The result is still `refused` until that separate conflict-resolution
policy is satisfied.

## Machine-Readable Result

See `generated-build-admission-policy.schema.json`.

Required top-level fields:

- `policy_result_kind` — `generated_build_admission_policy_result`
- `artifact_ref`
- `artifact_proof_status`
- `admission_status` — `evidence_only` | `candidate_only` |
  `deploy_admitted` | `refused`
- `reasons`
- `missing_prerequisites`
- `refusal_conditions`
- `precedence_decision`
- `evidence_summary`
- `evaluated_at`

## Acceptance Checks

- A `runtime_proven` artifact with no existing build conflict, no
  blocking risks, concrete image output, digest, rendered path, and
  accepted confidence evaluates to `candidate_only`.
- A `runtime_proven` generated artifact in a repo with a trustworthy
  existing Dockerfile evaluates to `refused` with
  `precedence_decision: existing_build_wins`.
- A `runtime_proven` artifact satisfying candidate criteria plus
  operator confirmation, source ref confirmation, deploy-pullable image
  reference, and resolved existing-build precedence evaluates to
  `deploy_admitted`.

## Out Of Scope

- Implementing the policy evaluator.
- Backend/UI mutation endpoints.
- Deploy/release wiring.
- Cloud-dev.
- Generated-build execution from UI.
