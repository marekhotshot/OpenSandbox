# Generated Build Contract

Status: canonical
Date: 2026-04-26

## Source Of Truth

A *generated build contract* is the machine-readable AMOF artifact that
describes how a codebase **without** a trustworthy upstream build
instruction (Dockerfile, `skaffold.yaml`, compose file, etc.) should
be built. It is produced by AMOF detection + templating, not by a
human author of the target repo.

This contract is the dual of the **existing build contract**:

- `existing_build_contract` — the repo already ships a Dockerfile (or
  equivalent) we can validate and wire. AMOF treats the upstream as
  source of truth and only needs to record what was found.
- `generated_build_contract` — the repo does not ship anything we can
  trust today. AMOF infers the runtime, picks a template, generates
  the Dockerfile/build, and **must** advance the artifact through a
  proof ladder before it can claim the build is real.

Refusal-by-default is the rule. AMOF will not silently invent a build
for a repo it cannot honestly classify.

## Drift That Exists Today

- AMOF currently has no formal way to express "the build I am about
  to run is generated, not authored". Generated builds and existing
  builds get conflated in operator surfaces.
- There is no proof ladder: a build that has compiled into an image
  is treated the same as a build whose runtime has been observed
  healthy.
- There is no machine-readable detection record: when AMOF guesses a
  runtime family, the guess and its confidence are not persisted
  alongside the generated artifact.
- Mixed/unknown repos (multi-language monorepos, vendored polyglot
  trees, codebases with custom toolchains) currently get the same
  default treatment as clean single-runtime repos.

## Expected Behavior

### 1. Lane selection

When AMOF is asked to build a repo for the first time:

1. Look for an `existing_build_contract` (upstream Dockerfile,
   `skaffold.yaml`, `package.json#scripts.docker:*`, etc.).
2. If present and trustworthy → use the **existing** lane. Record
   what was found, validate it, wire it. Do not generate anything.
3. If absent or untrustworthy → enter the **generated** lane.

The two lanes never silently merge. The capability surface (UI,
release status, contract field) must always say which lane produced
the build.

### 2. Generated-lane refusal conditions

The generated lane MUST refuse with `kind: refused` when:

- No template in the active runtime taxonomy matches the repo with
  ≥ `accepted` confidence (see `generated-build-runtime-detector-matrix.md`).
- The repo contains hard signals for two or more runtime families
  whose templates would conflict (mixed-runtime monorepo without an
  explicit per-service mapping).
- The repo contains hard signals for a runtime family that is not in
  the implemented first-wave taxonomy (e.g. JVM/Maven, .NET, Rust)
  unless an explicit operator opt-in is provided.
- The codebase ships a Dockerfile that AMOF deliberately classified
  as untrustworthy. Refusing is safer than overwriting.
- Required inputs for the chosen template are missing (e.g. no
  `requirements.txt` or `pyproject.toml` for the Python template; no
  `package.json` for the Node template).

A refusal is itself a contract artifact. It records why the build was
not generated and what the operator can do to advance.

### 3. Generated-lane progression

Every generated build artifact carries an explicit `status` along the
proof ladder:

- `proposed` — detection succeeded, template selected, Dockerfile
  written. Not yet built. AMOF MUST NOT claim the contract is valid
  beyond "we generated it".
- `build_proven` — `docker build` against the generated Dockerfile
  exited 0 against the canonical context. AMOF MAY claim the image
  is buildable. AMOF MUST NOT claim the image is healthy at runtime.
- `runtime_proven` — the built image was actually started, the
  inferred entrypoint did not crash, and a minimal liveness signal
  (port open, healthcheck OK, log line emitted) was observed within
  the proof timeout. Only at this stage may AMOF claim the contract
  is fully real.

A generated build contract that is `proposed` is allowed to be
visible to the operator but MUST be visually distinct from `build_proven`
or `runtime_proven` artifacts. It MUST NOT be admitted by the
lifecycle dispatcher as a deploy source.

### 4. Required fields

See `generated-build-contract.schema.json` for the authoritative
shape. Every generated artifact MUST include:

- `build_contract_kind` — fixed string `generated`
- `runtime_family` — one of the families in the active taxonomy
- `confidence` — `low` | `medium` | `high` | `accepted` | `refused`
- `signals` — the detection evidence (file globs hit, package
  manifests parsed, scripts found)
- `dockerfile_template` — id of the template used and its version
- `image_outputs` — concrete image names that the build would
  produce (registry alias + tag plan)
- `inferred_port` — port the entrypoint is expected to expose
- `entrypoint` — final command emitted into the Dockerfile
- `risk_flags` — any caveats the operator must see (multi-language
  signals, custom toolchain heuristics, etc.)
- `status` — `proposed` | `build_proven` | `runtime_proven` |
  `refused`

### 5. Operator surface obligations

Any UI/API that surfaces a build coming from the generated lane MUST:

- Display the lane explicitly (`generated`, not just `build`)
- Display the proof status (`proposed`/`build_proven`/`runtime_proven`)
- Display the runtime family and confidence
- Surface refusal reasons when present, not just "no build available"

These obligations are independent of contract flip on any specific
ecosystem.

## Acceptance Checks

- For any ecosystem whose first-party build is produced by the
  generated lane, the recorded artifact must validate against
  `generated-build-contract.schema.json`.
- The generated artifact must have `status` ≥ `build_proven` before
  it is admitted by the lifecycle dispatcher as a deploy source.
- The generated artifact must have `status == runtime_proven` before
  any operator surface labels the build as healthy.
- Refusal artifacts must explain which detection signal failed or
  which family was unsupported. A bare `refused` is not acceptance.

## Related Artifacts

- `generated-build-contract.schema.json` — machine-readable schema.
- `generated-build-runtime-detector-matrix.md` — per-runtime-family
  detection signals and template assignments.
- `examples/generated-build-contract-python-fastapi.example.json`
- `examples/generated-build-contract-node-express.example.json`
- `examples/generated-build-contract-go-stdlib.example.json`

## Out Of Scope

- The existing-build lane. Existing-build contracts are validated
  and wired separately (UP8-13 ecosystem build contract +
  UP8-14..UP8-20 first-party PoC for `gmd`).
- Cluster-builder substrate hardening. The generated lane uses the
  same substrate primitives as existing builds; substrate work is
  tracked separately.
- Lifecycle dispatch wiring, chart integration, contract flip for
  any specific ecosystem.
- Cloud-dev, release/promote, deploy wiring, UI redesign.
