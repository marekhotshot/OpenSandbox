# Generated-Build Runtime Detector Matrix

Status: canonical
Date: 2026-04-26

## Source Of Truth

This document is the **canonical first-wave taxonomy and detection
matrix** for the generated-build lane. It defines:

- Which runtime families AMOF is allowed to claim it can generate a
  build for today.
- The hard and soft signals it uses to detect each family.
- The confidence scoring rules and refusal/ambiguity behavior.
- The Dockerfile template assigned to each family in the first wave.

It is the companion to `generated-build-contract.md` and
`generated-build-contract.schema.json`.

## First-Wave Runtime Families

Three families are in scope for the first implementation wave. They
are picked because each has a single dominant convention, a clean
distroless or `-slim` runtime base, and a small per-language template
surface.

| Family   | Status     | Why first wave                                            |
|----------|------------|-----------------------------------------------------------|
| `python` | first-wave | One dominant manifest (`pyproject.toml`/`requirements.txt`); `python:3.X-slim` runtime base; common `uvicorn`/`gunicorn`/`fastapi`/`flask` entrypoints |
| `node`   | first-wave | One dominant manifest (`package.json` + lockfile); `node:20-alpine` runtime base; well-known `start` script convention |
| `go`     | first-wave | One dominant manifest (`go.mod`); single-binary build; `gcr.io/distroless/static` runtime base; trivial `ENTRYPOINT` |
| `static` | first-wave | Reservoir for prebuilt-static-asset repos with no real runtime (used for refusal-with-suggestion paths today; promoted to nginx-static template later) |

### Deferred families

Explicitly **not** in the first wave. Asking AMOF to generate a build
for a repo that hard-signals one of these families MUST refuse with
`refusal_reason: "runtime_family_not_in_first_wave"` unless the
operator opts in:

| Family      | Why deferred                                                                                  |
|-------------|-----------------------------------------------------------------------------------------------|
| `dotnet`    | Multiple manifests (`.csproj`, `.sln`); SDK base footprint is large; nested context patterns. |
| `java`      | Two competing tool families (Maven, Gradle); JDK runtime split; warmup story varies.          |
| `rust`      | Slow builds; cargo workspace/sub-crate ambiguity; runtime base choice is non-trivial.         |
| `ruby`      | Bundler quirks; native gem dependencies; runtime base choice fragmented.                      |
| `php`       | Multiple webserver shapes; framework-specific entrypoints.                                    |
| `polyglot`  | Mixed-runtime monorepos. Refused entirely; per-service explicit map required.                 |
| `unknown`   | The family the detector lands on when no hard signal matches. Always refused.                 |

The deferred families are tracked here so a future wave does not
have to re-discover them.

## Detection Signals

### Hard signals (deterministic file presence)

A *hard signal* is a file (or a parsed manifest field) whose presence
proves the runtime family. Multiple matching hard signals push
confidence higher; conflicting hard signals across families push
confidence to `refused`.

| Family   | Hard signals                                                                                                         |
|----------|----------------------------------------------------------------------------------------------------------------------|
| `python` | `pyproject.toml`, `requirements.txt`, `setup.py`, `setup.cfg`, `Pipfile`, `poetry.lock`                              |
| `node`   | `package.json` (top-level), `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`                                       |
| `go`     | `go.mod`, `go.sum`                                                                                                   |
| `static` | `index.html` at repo root with no `package.json`/`go.mod`/`pyproject.toml`/`requirements.txt`                        |

Repos with hard signals from two or more families above are
*ambiguous* and trigger the polyglot refusal path unless an explicit
per-service mapping is supplied (see `generated-build-contract.md` §2).

### Soft signals (heuristic)

Used **only** to break ties or pick an entrypoint, never to override
hard signals.

| Family   | Soft signals                                                                                                                      |
|----------|-----------------------------------------------------------------------------------------------------------------------------------|
| `python` | `app.py`, `main.py`, `wsgi.py`, `asgi.py`; `[tool.poetry]` block; dependency hints `fastapi`/`flask`/`django`/`uvicorn`/`gunicorn` |
| `node`   | `package.json#scripts.start`, `package.json#main`; dependency hints `express`/`fastify`/`koa`/`next`                              |
| `go`     | `main.go` at repo root or `cmd/<name>/main.go`; `go.mod#module` name; `Makefile` `build` target                                   |
| `static` | `dist/`, `public/`, `static/` directories with web assets and no build manifests                                                  |

### Confidence scoring

Confidence is a discrete enum, not a float. Mapping rule:

| Conditions                                                                                       | Confidence  |
|--------------------------------------------------------------------------------------------------|-------------|
| ≥ 1 hard signal AND ≥ 1 matching soft signal AND no conflicting-family hard signal               | `accepted`  |
| ≥ 1 hard signal AND no conflicting-family hard signal                                            | `high`      |
| ≥ 2 soft signals AND no hard signal                                                              | `medium`    |
| Exactly 1 soft signal                                                                            | `low`       |
| Conflicting hard signals from two or more families OR no signals at all                          | `refused`   |

Only `accepted` clears the refusal threshold. `high`/`medium`/`low`
results are written into the artifact for operator review but the
generated lane MUST NOT advance past `proposed` for them. The bar
is intentionally strict: the cost of generating a wrong Dockerfile
is higher than the cost of refusing.

## Refusal Conditions

The matrix produces a `refused` outcome (and the contract carries
`status: "refused"` with a `refusal_reason`) when any of the
following hold:

- No hard signal matches any in-wave family AND fewer than 2 soft
  signals match. → `refusal_reason: "no_runtime_signal"`
- Hard signals match two or more in-wave families. →
  `refusal_reason: "polyglot_repo_no_per_service_map"`
- A hard signal matches a deferred family (e.g. `*.csproj`,
  `pom.xml`, `Cargo.toml`, `Gemfile`). →
  `refusal_reason: "runtime_family_not_in_first_wave"`
- The matched family lacks the required template inputs (e.g.
  `python` family selected but neither `pyproject.toml` nor
  `requirements.txt` is parseable). →
  `refusal_reason: "template_inputs_missing"`
- A trustworthy upstream Dockerfile is present (pre-empts the
  generated lane entirely; the existing-build lane wins). →
  `refusal_reason: "existing_build_contract_present"`

A refusal is itself a contract artifact. It MUST include enough
detail for the operator to advance:

```text
refusal_reason: polyglot_repo_no_per_service_map
risk_flags:
  - python_hard_signals: [pyproject.toml]
  - node_hard_signals:   [package.json, package-lock.json]
suggested_action:
  Provide an explicit per-service map (services[*].source_subpath)
  or split the repo so each service has one runtime family.
```

## First-Wave Template Assignments

| Family   | Template id                                | Runtime base                           | Notes                                                    |
|----------|--------------------------------------------|----------------------------------------|----------------------------------------------------------|
| `python` | `python-uvicorn-distroless-v1`             | `python:3.12-slim`                     | Multi-stage; uvicorn entrypoint; reads requirements.txt or pyproject.toml |
| `node`   | `node-express-distroless-v1`               | `node:20-alpine`                       | Multi-stage; honors `package.json#scripts.start`         |
| `go`     | `go-stdlib-distroless-v1`                  | `gcr.io/distroless/static`             | Multi-stage; `go build` on `./...` then static binary    |
| `static` | (no template in first wave; refusal lane)  | n/a                                    | First wave refuses with `suggested_action: serve_via_existing_nginx` |

Template specifics (assumptions, required inputs, known risks, proof
expectations) live in `generated-build-contract.md` §4 and in
`examples/`.

## Acceptance Checks

- A repo that only contains `pyproject.toml` + `app.py` (FastAPI
  hint) → `runtime_family: python`, `confidence: accepted`, template
  `python-uvicorn-distroless-v1`.
- A repo that only contains `package.json` (with a `start` script
  and `express` dep) + `index.js` → `runtime_family: node`,
  `confidence: accepted`, template `node-express-distroless-v1`.
- A repo that only contains `go.mod` + `main.go` → `runtime_family:
  go`, `confidence: accepted`, template `go-stdlib-distroless-v1`.
- A repo that contains both `package.json` and `pyproject.toml` →
  `status: refused`, `refusal_reason:
  "polyglot_repo_no_per_service_map"`.
- A repo that contains `Cargo.toml` and nothing else → `status:
  refused`, `refusal_reason: "runtime_family_not_in_first_wave"`.
- A repo that contains a Dockerfile already → the existing-build
  lane preempts. The generated lane records `status: refused`,
  `refusal_reason: "existing_build_contract_present"` so the audit
  trail is symmetric.

## Related Artifacts

- `generated-build-contract.md` — the contract this matrix supports.
- `generated-build-contract.schema.json` — schema validating the
  shape of artifacts that reference this matrix.
- `examples/` — concrete example artifacts for the three first-wave
  families plus a refusal example.

## Out Of Scope

- Implementing the detector. This document is design only.
- Implementing the templates. The template ids above are stable
  names for the first-wave plan; the actual files land in the
  implementation slice.
- Promoting any deferred family. Future waves may promote `dotnet`,
  `java`, `rust`, etc.; doing so requires a new entry in this
  matrix, a template, and an update to
  `generated-build-contract.schema.json` `runtime_family.enum`.
