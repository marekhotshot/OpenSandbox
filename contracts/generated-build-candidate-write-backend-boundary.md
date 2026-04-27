# Generated Build Candidate Write Backend Boundary

Status: canonical
Date: 2026-04-27

## Scope

This contract defines how the backend may expose
`generated_build.promote_candidate.v1` on top of the local generated-build
candidate store.

It is a backend mutation boundary only. It does not create deploy admission,
release admission, chart changes, lifecycle records, cloud-dev behavior, or UI
execution semantics.

## Action Model

Action id:

```text
generated_build.promote_candidate.v1
```

Backend command:

```http
POST /api/v1/control/generated-builds/candidates/promote
```

The public `/api/v1/generated-builds` surface remains read-only for generated
artifacts and admission previews. The candidate-write command belongs under the
control prefix because it mutates local candidate state and writes audit
evidence.

If the router is also mounted under a non-control prefix for legacy symmetry,
the mutation handler must still require step-up/control-grade authorization.

## Request Shape

The request body must validate against
`generated-build-candidate-write-request.schema.json`.

Required semantic fields:

- `action == "generated_build.promote_candidate.v1"`
- `artifact_ref.artifact_path`
- `artifact_ref.repo_path`
- `artifact_ref.service`
- `target_ecosystem`
- `target_service`
- `operator_confirmation`

Backend-safe optional fields:

- `supersede_candidate_id`
- `idempotency_key`

When `idempotency_key` is omitted, the backend must derive a deterministic key
from the normalized tuple:

```text
action
artifact_ref.artifact_path
artifact_ref.repo_path
artifact_ref.service
target_ecosystem
target_service
operator_confirmation.confirmed_image_digest
supersede_candidate_id
```

## Response Shape

The response body must validate against
`generated-build-candidate-write-result.schema.json`.

Domain outcomes:

- `candidate_created`
- `refused`

Policy refusals are command results, not transport failures. The backend should
return HTTP 200 for a well-formed request that is evaluated and refused by
policy, with `result: "refused"` and populated `refusal_conditions`.

Transport or framework errors are reserved for:

- malformed JSON
- schema-invalid request payload
- authentication or authorization failure
- unsupported action id
- unexpected server failure

## Auth Expectations

The mutation must require control-grade authorization, equivalent to the
backend's step-up-gated mutation actions.

The audit receipt must record both:

- authenticated backend principal
- operator confirmation principal from `operator_confirmation.confirmed_by`

If those principals differ, the backend may allow it only when the authenticated
principal is authorized to act for the confirmed operator; otherwise it must
refuse with `operator_confirmation_principal_mismatch`.

## Idempotency

The backend must persist enough idempotency metadata to make retries safe.

Rules:

- same `idempotency_key` plus same normalized request returns the original
  result with `replayed: true`;
- same `idempotency_key` plus different normalized request returns `refused`
  with `idempotency_key_conflict`;
- candidate creation must not produce duplicate candidate records on retry;
- audit receipt replay must reference the original receipt rather than writing
  a second success receipt.

## Backend Preconditions

The backend must validate all local-store preconditions from
`generated-build-candidate-write-contract.md`, plus backend-specific checks:

1. Request schema validates.
2. The action id is supported.
3. The request is authorized for the control mutation surface.
4. The artifact exists in local generated-build storage.
5. The artifact validates against `generated-build-contract.schema.json`.
6. The artifact proof status is exactly `runtime_proven`.
7. The artifact build contract kind is `generated`.
8. The artifact confidence is `accepted`.
9. Operator confirmation is present.
10. `operator_confirmation.confirmed_image_digest` matches
    `artifact.build_proof.image_digest`.
11. Admission preview for the same artifact and request context evaluates to
    `candidate_only`.
12. Existing-build precedence evaluates to no active conflict.
13. No active candidate exists for `(target_ecosystem, target_service)` unless
    `supersede_candidate_id` names the active candidate.
14. The idempotency key is either new or matches the original normalized
    request.

## Refusal Model

The backend must return `result: "refused"` for policy and command refusals,
including:

- `artifact_not_found`
- `artifact_schema_invalid`
- `artifact_status_below_runtime_proven`
- `build_contract_kind_not_generated`
- `confidence_not_accepted`
- `operator_confirmation_missing`
- `operator_confirmation_digest_mismatch`
- `operator_confirmation_principal_mismatch`
- `required_acknowledgement_missing`
- `existing_build_contract_present`
- `precedence_decision_not_candidate_safe`
- `active_candidate_exists_without_supersede`
- `supersede_candidate_mismatch`
- `idempotency_key_conflict`
- `candidate_store_write_failed`
- `audit_write_failed`

Every refused result must include:

- `reasons`
- `missing_prerequisites`
- `refusal_conditions`

## Postconditions

On `candidate_created`, the backend must write:

- candidate record
- active candidate pointer for `(target_ecosystem, target_service)`
- audit receipt
- idempotency replay record or equivalent persisted replay metadata

The backend must leave unchanged:

- original generated-build artifact
- artifact proof status
- admission preview result history
- deploy/release state

## Forbidden Writes

The backend mutation must never write:

- deploy state
- release state
- chart values
- lifecycle build records
- lifecycle deploy records
- generated Dockerfiles
- source repository contents
- generated-build artifact proof status
- deploy-admitted records

## API Placement

The implementation should keep read-only generated-build endpoints visibly
separate from candidate-write mutations:

- read-only artifact index: `GET /api/v1/generated-builds`
- read-only artifact detail: `GET /api/v1/generated-builds/artifact`
- read-only admission preview:
  `GET /api/v1/generated-builds/admission-preview`
- candidate mutation:
  `POST /api/v1/control/generated-builds/candidates/promote`

This keeps the operator mental model separate:

- artifact proof status describes build/runtime evidence;
- admission preview describes policy evaluation;
- candidate write state records an operator-confirmed local candidate decision.

## Acceptance Checks

The first backend implementation slice should prove:

- valid runtime-proven artifact with matching digest creates one candidate;
- retry with same idempotency key replays the same result without duplicate
  writes;
- same idempotency key with different digest refuses;
- existing-build conflict refuses;
- active candidate without supersession refuses;
- original artifact is byte-for-byte unchanged;
- no deploy/release/chart/lifecycle files are written.

