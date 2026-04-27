# RunPod Heavy Lane Profile

Status: canonical
Date: 2026-04-27

## Scope

This contract defines the first AMOF-owned RunPod heavy inference lane.
It is opt-in, health-checked, and heavy-only. It is not a master lane and
does not replace the existing AMOF inference authority.

## Canonical Profile

Profile id:

```text
runner_code_heavy
```

Provider:

```text
runpod
```

Model:

```text
MiniMaxAI/MiniMax-M2.5
```

Allowed AMOF roles:

- `runner_code_heavy`
- `long_context_reviewer`

Forbidden roles:

- master/orchestrator authority
- default worker route
- summarizer

## Endpoint Contract

The lane consumes an OpenAI-compatible endpoint:

```text
RUNPOD_OPENAI_BASE_URL=https://api.runpod.ai/v2/<endpoint-id>/openai/v1
RUNPOD_API_KEY=<operator-managed secret>
```

Health check:

```http
GET ${RUNPOD_OPENAI_BASE_URL}/models
Authorization: Bearer ${RUNPOD_API_KEY}
```

The lane is usable only when:

- `RUNPOD_API_KEY` is present;
- `RUNPOD_OPENAI_BASE_URL` is present;
- `/models` returns HTTP 200;
- the configured model id is listed;
- the lane is selected explicitly by profile/role.

## Guardrails

- `allow_master: false`
- `allow_direct_git_write: false`
- `max_context_tokens: 32768`
- `hard_timeout_seconds: 7200`
- `max_cost_per_run_usd: 5.00`
- `idle_ttl_minutes: 120`
- no silent fallback for RunPod-scoped calls

## Substrate Truth

The existing reusable substrate includes:

- RunPod API key handling through `RUNPOD_API_KEY`;
- bounded pod lifecycle API under `/api/v1/runpod/pods`;
- AMOF-managed pod markers;
- TTL projection and explicit TTL enforcement;
- one reusable RunPod template:
  `amof-mvp-pytorch-cuda121` (`template_id: 4dnxg7h6lw`).

Current blocker:

- no OpenAI-compatible RunPod endpoint exists for the account;
- `RUNPOD_OPENAI_BASE_URL` is not configured.

## Verdict Rules

If the health endpoint reports missing `RUNPOD_OPENAI_BASE_URL` or no
RunPod endpoint, AMOF must not run planning or patch proofs. The correct
verdict is `replay_later` after a bounded OpenAI-compatible endpoint is
provisioned.

