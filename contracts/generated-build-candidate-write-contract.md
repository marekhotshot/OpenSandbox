# Generated Build Candidate Write Contract

Status: canonical
Date: 2026-04-27

## Source Of Truth

The generated-build admission evaluator is read-only. It can return
`candidate_only`, but it does not persist candidate state.

This contract defines the **first write boundary** that may promote a
`runtime_proven` generated-build artifact from read-only evidence into
an explicit `candidate_only` record.

This is not deploy admission. It is not release admission. It does not
execute generated-build artifacts. It only records an operator-confirmed
candidate decision with an audit trail.

## Action Model

Action id:

```text
generated_build.promote_candidate.v1
```

Purpose:

```text
Persist a runtime_proven generated-build artifact as a candidate_only
generated build contract candidate for one ecosystem/service.
```

The action is allowed to write only:

- a candidate record under local generated-build candidate storage
- an audit receipt for the candidate promotion decision

The action MUST NOT write:

- deploy/release state
- chart values
- lifecycle build/deploy records
- generated Dockerfiles
- generated-build artifact proof status

## Preconditions

The write action MUST validate all of:

1. The referenced artifact exists in the local generated-build store.
2. The artifact validates against `generated-build-contract.schema.json`.
3. `artifact.build_contract_kind == "generated"`.
4. `artifact.status == "runtime_proven"`.
5. `artifact.confidence == "accepted"`.
6. `artifact.dockerfile_template.id` is known.
7. `artifact.dockerfile_template.rendered_path` is present.
8. `artifact.build_proof.image_digest` is present and matches the
   operator-confirmed digest.
9. `artifact.runtime_proof.liveness_signal` is present.
10. `artifact.image_outputs` contains a concrete image reference.
11. Admission preview evaluates to `candidate_only` for the same
    artifact/context.
12. Existing-build precedence is resolved as no conflict:
    `precedence_decision == "no_existing_build_contract"`.
13. Operator confirmation is present and names the target
    ecosystem/service.
14. Candidate storage has no active candidate for the same
    `(ecosystem, service)` unless the request explicitly supersedes it.

## Postconditions

On success:

- candidate status is persisted as `candidate_only`;
- candidate record references the artifact path and image digest;
- artifact proof status remains unchanged (`runtime_proven`);
- admission status is recorded separately from artifact proof status;
- audit receipt is written;
- no deploy/release admission is created.

On failure:

- no candidate record is written;
- no artifact is mutated;
- result status is `refused`;
- refusal conditions and missing prerequisites are returned.

## Operator Confirmation Requirements

The operator confirmation MUST include:

- `confirmed_by`
- `confirmed_at`
- `target_ecosystem`
- `target_service`
- `artifact_path`
- `confirmed_image_digest`
- `confirmed_runtime_family`
- `confirmed_template_id`
- `confirmed_source_repo`
- `confirmed_entrypoint`
- `acknowledgements`

Required acknowledgements:

- `runtime_proven_is_not_deploy_admission`
- `candidate_only_is_not_deploy_admitted`
- `existing_build_precedence_checked`
- `no_release_or_deploy_wiring_created`

The digest confirmation is a hard guard: if
`confirmed_image_digest != artifact.build_proof.image_digest`, the
action MUST refuse with `operator_confirmation_digest_mismatch`.

## Refusal Conditions

The action MUST refuse when any of these are true:

- `artifact_not_found`
- `artifact_schema_invalid`
- `artifact_status_below_runtime_proven`
- `build_contract_kind_not_generated`
- `confidence_not_accepted`
- `template_missing_or_unknown`
- `rendered_path_missing`
- `image_output_missing_or_placeholder`
- `build_digest_missing_or_invalid`
- `runtime_proof_missing`
- `existing_build_contract_present`
- `precedence_decision_not_candidate_safe`
- `operator_confirmation_missing`
- `operator_confirmation_digest_mismatch`
- `operator_confirmation_target_mismatch`
- `required_acknowledgement_missing`
- `active_candidate_exists_without_supersede`
- `candidate_store_write_failed`
- `audit_write_failed`

Every refusal MUST include `missing_prerequisites` and
`refusal_conditions`.

## Candidate Record

Candidate records are appendable/reversible local policy records. They
do not change the source artifact.

Minimal candidate record fields:

- `candidate_id`
- `status` — `candidate_only` | `superseded` | `reverted`
- `artifact_ref`
- `target_ecosystem`
- `target_service`
- `image_digest`
- `runtime_family`
- `template_id`
- `created_by`
- `created_at`
- `supersedes_candidate_id`
- `admission_policy_result`
- `audit_receipt_path`

## Audit Receipt

The audit receipt MUST record:

- action id
- request payload
- result payload
- artifact digest and path
- target ecosystem/service
- operator confirmation
- admission policy preview result
- previous candidate id if superseding
- timestamp

Receipts are evidence. They are not deploy instructions.

## Rollback And Supersession

Candidate promotion is reversible by writing a new candidate-state
record:

- `generated_build.revert_candidate.v1` marks a candidate as
  `reverted`.
- `generated_build.promote_candidate.v1` with `supersede_candidate_id`
  marks the previous candidate as `superseded` and creates a new
  `candidate_only` record.

Rollback/supersession MUST NOT delete the original artifact or the
original audit receipt.

Deploy-admitted records, when they exist in a later contract, MUST
reference a candidate id. Reverting a candidate that has downstream
deploy-admission records MUST refuse until those downstream records are
handled by their own policy.

## Acceptance Checks

- A runtime-proven Python artifact with matching digest/operator
  confirmation and no existing-build conflict returns
  `candidate_created`.
- The same artifact with mismatched confirmed digest returns `refused`
  with `operator_confirmation_digest_mismatch`.
- A runtime-proven artifact with existing-build conflict returns
  `refused` with `existing_build_contract_present`.
- A second candidate for the same ecosystem/service without
  `supersede_candidate_id` returns `refused`.

## Out Of Scope

- Implementing backend mutation.
- UI execution.
- Deploy/release wiring.
- Deploy-admitted write boundary.
- Cloud-dev.
- Runtime proof execution.
