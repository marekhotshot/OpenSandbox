# Generated Build Candidate Promotion Operator UI

Status: canonical
Date: 2026-04-27

## Scope

This contract defines the local-only operator UI boundary for promoting a
runtime-proven generated-build artifact to `candidate_only` state.

The UI may call only the existing local backend mutation:

```http
POST /api/v1/control/generated-builds/candidates/promote
```

It must not create deploy admission, release admission, chart changes,
lifecycle records, cloud-dev state, or non-local storage.

## Placement

The action belongs on the generated-build artifact detail surface, after the
read-only admission preview and before raw artifact JSON.

The action acts on exactly one stored artifact:

- artifact proof status from the stored artifact;
- admission preview status from read-only policy evaluation;
- candidate state from local candidate records.

These states must stay visually distinct. A candidate promotion never changes
the artifact proof status and never implies deploy/release truth.

## Visibility And Disabled Rules

The action is visible when an artifact is selected.

It is enabled only when:

- `artifact.build_contract_kind == "generated"`;
- `artifact.status == "runtime_proven"`;
- `artifact.confidence == "accepted"`;
- `artifact.build_proof.image_digest` is present;
- `artifact.runtime_proof.liveness_signal` is present;
- admission preview status is `candidate_only`;
- target ecosystem and target service are supplied;
- all required acknowledgements are checked.

It is disabled with explicit reasons when:

- artifact proof status is below `runtime_proven`;
- admission preview is refused or unavailable;
- digest/runtime/template/source/entrypoint evidence is missing;
- target ecosystem/service is missing;
- required acknowledgements are not checked.

## Confirmation Contents

The confirmation dialog must show system-derived evidence:

- artifact proof status;
- admission preview status;
- artifact digest;
- runtime family;
- template id;
- source repo/ref when available;
- entrypoint;
- service;
- rendered template path when available.

The operator must provide or confirm:

- target ecosystem;
- target service;
- `confirmed_by`;
- all required acknowledgements.

Required acknowledgement text:

- Runtime-proven evidence is not deploy admission.
- Candidate-only state is not deploy-admitted.
- Existing-build precedence has been checked.
- No release or deploy wiring is created by this action.

## Result Handling

On `candidate_created`, the UI must:

- show `candidate_only`;
- show the candidate id;
- show whether the result was replayed;
- refresh readonly candidate inspection.

On `refused`, the UI must:

- show exact `refusal_conditions`;
- show `missing_prerequisites`;
- not claim a candidate was created;
- refresh readonly candidate inspection without fabricating state.

On idempotent replay, the UI must say the result was replayed and must not
present it as a second candidate creation.

## Forbidden UI Actions

This surface must not show or trigger these actions:

- Deploy;
- Promote to release;
- Release;
- Rollback;
- chart update;
- lifecycle deploy.

Safety copy must include:

```text
Candidate promotion is not deploy admission.
Candidate promotion is not release admission.
```

