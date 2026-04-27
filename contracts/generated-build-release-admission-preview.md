# Generated Build Release Admission Preview

Status: canonical
Date: 2026-04-27

## Scope

This contract defines a readonly release-admission preview for generated-build
candidate records.

It sits above local candidate state and below any future release/deploy write
boundary. It does not write release admission, deploy admission, chart values,
lifecycle records, artifacts, candidate records, or audit receipts.

## State Model

The preview result uses `release_admission_preview_status`, separate from all
existing state axes:

- artifact proof status — evidence about the generated artifact;
- admission preview status — generated-build artifact policy preview;
- candidate state — local operator-confirmed `candidate_only` record;
- release-admission preview status — readonly release policy preview;
- deploy/release truth — actual release/deploy system state.

Preview statuses:

- `release_candidate_only`: candidate exists and is coherent, but release
  admission prerequisites are not fully satisfied.
- `release_admitted_preview`: readonly policy says a later release-admission
  write could be requested for this candidate if a separate mutation boundary
  exists.
- `refused`: hard policy or safety conflict.
- `unavailable`: candidate/artifact evidence could not be loaded or parsed.

`release_admitted_preview` is not a release write. It is not deploy admission.
It is not deploy/release execution.

## Required Candidate State

The preview input must be a local generated-build candidate record with:

- `candidate_id`;
- `status == "candidate_only"`;
- `artifact_ref.artifact_path`;
- `artifact_ref.repo_path`;
- `artifact_ref.service`;
- `artifact_ref.image_digest`;
- `target_ecosystem`;
- `target_service`;
- `image_digest`;
- `admission_policy_result.admission_status == "candidate_only"`.

Superseded or reverted candidates must refuse.

## Required Artifact Evidence

The referenced artifact must still be loadable from local generated-build
storage and must satisfy:

- `build_contract_kind == "generated"`;
- `status == "runtime_proven"`;
- `confidence == "accepted"`;
- `build_proof.image_digest` matches the candidate digest;
- `runtime_proof.liveness_signal` is present;
- no blocking risk flag is present.

## Preview Context

Readonly preview context may include:

- `release_target`;
- `source_ref_confirmed`;
- `deploy_pull_reference_present`;
- `chart_contract_present`;
- `operator_preview_only_acknowledged`;
- `existing_release_candidate_present`.

Missing non-conflict context produces `release_candidate_only`, not a mutation.
Hard conflicts produce `refused`.

To preview `release_admitted_preview`, all must be true:

- `release_target` is present;
- source ref is confirmed;
- deploy-pull reference is present;
- chart contract has been reviewed/present;
- operator acknowledges preview-only semantics;
- no existing release candidate conflict is present.

## Refusal Conditions

Hard refusals include:

- `candidate_status_not_candidate_only`;
- `candidate_artifact_digest_mismatch`;
- `artifact_status_below_runtime_proven`;
- `candidate_admission_not_candidate_only`;
- `build_contract_kind_not_generated`;
- `confidence_not_accepted`;
- `runtime_proof_missing`;
- `blocking_risk_flag_present`;
- `existing_release_candidate_present`;
- `release_or_deploy_mutation_requested`.

Unavailable conditions include:

- `candidate_not_found`;
- `artifact_not_found`;
- `candidate_record_invalid`;
- `artifact_record_invalid`.

Missing prerequisites include:

- `release_target`;
- `source_ref_confirmation`;
- `deploy_pull_reference_confirmation`;
- `chart_contract_review`;
- `operator_preview_only_acknowledgement`.

## Forbidden Assumptions

The preview must never assume:

- candidate state is release truth;
- `release_admitted_preview` is an actual release admission;
- an image digest can be deployed without a later mutation boundary;
- chart/lifecycle/release records are updated;
- rollback is available.

## Backend Placement

Readonly endpoint:

```http
GET /api/v1/generated-builds/candidates/{candidate_id}/release-admission-preview
```

It must not require the control prefix and must not expose a mutation route.

## Acceptance Checks

- A coherent `candidate_only` record with missing release context returns
  `release_candidate_only`.
- The same candidate with all readonly context supplied returns
  `release_admitted_preview`.
- Existing release candidate conflict returns `refused`.
- Superseded/reverted candidate returns `refused`.
- Candidate/artifact digest mismatch returns `refused`.
- The preview writes no files.

